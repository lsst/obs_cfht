import numpy as np

import lsst.pex.config as pexConfig
from lsst.ip.isr import IsrTask

class CfhtIsrTaskConfig(IsrTask.ConfigClass) :
    safe = pexConfig.Field(
        dtype = float,
        doc = "Safety margin for CFHT sensors gain determination",
        default = 0.95,
    )
    
    def setDefaults(self):
        IsrTask.ConfigClass.setDefaults(self)

class CfhtIsrTask(IsrTask) :
    ConfigClass = CfhtIsrTaskConfig
    
    def run(self, ccdExposure, bias=None, linearizer=None, dark=None, flat=None, defects=None,
            fringes=None, bfKernel=None):
        """Perform instrument signature removal on an exposure
        
        Steps include:
        - Detect saturation, apply overscan correction, bias, dark and flat
        - Perform CCD assembly
        - Interpolate over defects, saturated pixels and all NaNs
        - Persist the ISR-corrected exposure as "postISRCCD" if config.doWrite is True

        @param[in] ccdExposure  -- lsst.afw.image.exposure of detector data
        @param[in] bias -- exposure of bias frame
        @param[in] linearizer -- linearizing functor; a subclass of lsst.ip.isr.LinearizeBase
        @param[in] dark -- exposure of dark frame
        @param[in] flat -- exposure of flatfield
        @param[in] defects -- list of detects
        @param[in] fringes -- exposure of fringe frame or list of fringe exposure
        @param[in] bfKernel - kernel used for brighter-fatter correction; currently unsupported

        @return a pipeBase.Struct with fields:
        - exposure: the exposure after application of ISR
        """
        if bfKernel is not None:
            raise ValueError("CFHT ISR does not currently support brighter-fatter correction.")

        ccd = ccdExposure.getDetector()
        floatExposure = self.convertIntToFloat(ccdExposure)
        metadata = floatExposure.getMetadata()
        
        # Detect saturation
        # Saturation values recorded in the fits hader is not reliable, try to estimate it from
        # the pixel vales
        # Find the peak location in the high end part the pixel values' histogram and set the saturation
        # level at safe * (peak location) where safe is a configurable parameter (typically 0.95)
        image = floatExposure.getMaskedImage().getImage()
        imageArray = image.getArray()
        maxValue = np.max(imageArray)
        if maxValue > 60000.0 :
            hist, bin_edges = np.histogram(imageArray.ravel(),bins=100,range=(60000.0,maxValue+1.0))
            saturate = int(self.config.safe*bin_edges[np.argmax(hist)])
        else :
            saturate = metadata.get("SATURATE")
        self.log.info("Saturation set to %d" % saturate)
        
        for amp in ccd:
            amp.setSaturation(saturate)
            if amp.getName() == "A":
                amp.setGain(metadata.get("GAINA"))
                rdnA = metadata.get("RDNOISEA")
                # Check if the noise value is making sense for this amp. If not, replace with value
                # stored in RDNOISE slot. This change is necessary to process some old CFHT images
                # (visit : 7xxxxx) where RDNOISEA/B = 65535
                if rdnA > 60000.0 :
                    rdnA = metadata.get("RDNOISE")
                amp.setReadNoise(rdnA)
            elif amp.getName() == "B":
                amp.setGain(metadata.get("GAINB"))
                rdnB = metadata.get("RDNOISEB")
                # Check if the noise value is making sense for this amp. If not, replace with value
                # stored in RDNOISE slot. This change is necessary to process some old CFHT images
                # (visit : 7xxxxx) where RDNOISEA/B = 65535
                if rdnB > 60000.0 :
                    rdnB = metadata.get("RDNOISE")
                amp.setReadNoise(rdnB)
            else :
                raise ValueError("Unexpected amplifier name : %s"%(amp.getName()))

        return IsrTask.run(self,
            ccdExposure = ccdExposure,
            bias = bias,
            linearizer = linearizer,
            dark = dark,
            flat = flat,
            defects = defects,
            fringes = fringes,
        )
