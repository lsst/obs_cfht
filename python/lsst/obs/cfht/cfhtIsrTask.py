import lsst.pex.config as pexConfig
from lsst.ip.isr import IsrTask
import numpy as np

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
    
    def run(self, ccdExposure, bias=None, dark=None,  flat=None, defects=None, fringes=None):
        """Perform instrument signature removal on an exposure
        
        Steps include:
        - Detect saturation, apply overscan correction, bias, dark and flat
        - Perform CCD assembly
        - Interpolate over defects, saturated pixels and all NaNs
        - Persist the ISR-corrected exposure as "postISRCCD" if config.doWrite is True

        @param[in] ccdExposure  -- lsst.afw.image.exposure of detector data
        @param[in] bias -- exposure of bias frame
        @param[in] dark -- exposure of dark frame
        @param[in] flat -- exposure of flatfield
        @param[in] defects -- list of detects
        @param[in] fringes -- exposure of fringe frame or list of fringe exposure

        @return a pipeBase.Struct with fields:
        - exposure: the exposure after application of ISR
        """
        ccd = ccdExposure.getDetector()
        floatExposure = self.convertIntToFloat(ccdExposure)
        metadata = floatExposure.getMetadata()
        
        # Detect saturation
        # Saturation values recorded in the fits hader is not reliable, try to estimate it from the pixel vales
        # Find the peak location in the high end part the pixel values' histogram and set the saturation level at 
        # safe * (peak location) where safe is a configurable parameter (typically 0.95)
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
                gain = metadata.get("GAINA")
                amp.setGain(gain)
                # We have to devide the noise which is in the fits header by the gain as the 
                # stack is expecting the noise in ADU
                amp.setReadNoise(metadata.get("RDNOISEA")/gain)
            elif amp.getName() == "B":
                gain = metadata.get("GAINB")
                amp.setGain(gain)
                amp.setReadNoise(metadata.get("RDNOISEB")/gain)
            else :
                raise ValueError("Unexpected amplifier name : %s"%(amp.getName()))

        return IsrTask.run(self, 
            ccdExposure = ccdExposure,
            bias = bias,
            dark = dark,
            flat = flat,
            defects = defects,
            fringes = fringes,
        )