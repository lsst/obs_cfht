import lsst.afw.image as afwImage
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
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
        #Validate Input
        if self.config.doBias and bias is None:
            raise RuntimeError("Must supply a bias exposure if config.doBias True")
        if self.config.doDark and dark is None:
            raise RuntimeError("Must supply a dark exposure if config.doDark True")
        if self.config.doFlat and flat is None:
            raise RuntimeError("Must supply a flat exposure if config.doFlat True")
        if self.config.doFringe and fringes is None:
            raise RuntimeError("Must supply fringe list or exposure if config.doFringe True")

        defects = [] if defects is None else defects

        ccd = ccdExposure.getDetector()
        ccdExposure = self.convertIntToFloat(ccdExposure)
        metadata = ccdExposure.getMetadata()
        
        # Detect saturation
        # Saturation values recorded in the fits hader is not reliable, try to estimate it from the pixel vales
        # Find the peak location in the high end part the pixel values' histogram and set the saturation level at 
        # safe * (peak location) where safe is a configurable parameter (typically 0.95)
        image = ccdExposure.getMaskedImage().getImage()
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
                amp.setReadNoise(metadata.get("RDNOISEA"))
            elif amp.getName() == "B":
                amp.setGain(metadata.get("GAINB"))
                amp.setReadNoise(metadata.get("RDNOISEB"))
            else :
                raise ValueError("Unexpected amplifier name : %s"%(amp.getName()))
            
            self.saturationDetection(ccdExposure, amp)
            self.overscanCorrection(ccdExposure, amp)
        
        if self.config.doAssembleCcd:
            ccdExposure = self.assembleCcd.assembleCcd(ccdExposure)

        if self.config.doBias:
            self.biasCorrection(ccdExposure, bias)

        if self.config.doDark:
            self.darkCorrection(ccdExposure, dark)
        
        for amp in ccd:
            ampExposure = ccdExposure.Factory(ccdExposure, amp.getBBox(), afwImage.PARENT)
            self.updateVariance(ampExposure, amp)

        if self.config.doFringe and not self.config.fringeAfterFlat:
            self.fringe.removeFringe(ccdExposure, fringes)

        if self.config.doFlat:
            self.flatCorrection(ccdExposure, flat)

        self.maskAndInterpDefect(ccdExposure, defects)

        self.saturationInterpolation(ccdExposure)

        self.maskAndInterpNan(ccdExposure)

        if self.config.doFringe and self.config.fringeAfterFlat:
            self.fringe.removeFringe(ccdExposure, fringes)
        
        ccdExposure.getCalib().setFluxMag0(self.config.fluxMag0T1 * ccdExposure.getCalib().getExptime())

        return pipeBase.Struct(
            exposure = ccdExposure,
        )