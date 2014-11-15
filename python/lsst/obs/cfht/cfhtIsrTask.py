import lsst.afw.image as afwImage
import lsst.meas.algorithms as measAlg
import lsst.afw.cameraGeom as cameraGeom
import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.ip.isr as ipIsr

class CfhtIsrTask(ipIsr.IsrTask) :
    def run(self, sensorRef):
        """Perform instrument signature removal on an exposure
        
        Steps include:
        - Detect saturation, apply overscan correction, bias, dark and flat
        - Perform CCD assembly
        - Interpolate over defects, saturated pixels and all NaNs
        - Persist the ISR-corrected exposure as "postISRCCD" if config.doWrite is True

        @param sensorRef daf.persistence.butlerSubset.ButlerDataRef of the data to be processed
        @return a pipeBase.Struct with fields:
        - exposure: the exposure after application of ISR
        """
        self.log.log(self.log.INFO, "Performing ISR on sensor %s" % (sensorRef.dataId))
        ccdExposure = sensorRef.get('raw')
        ccd = ccdExposure.getDetector()
        
        ccdNum = sensorRef.dataId['ccd']
    
        ccdExposure = self.convertIntToFloat(ccdExposure)
        metadata = ccdExposure.getMetadata()
        
        flag = 1
        for amp in ccd:
            amp.setSaturation(metadata.get("SATURATE"))
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
        
        ccdExposure = self.assembleCcd.assembleCcd(ccdExposure)
        ccd = ccdExposure.getDetector()

        if self.config.doBias:
            self.biasCorrection(ccdExposure, sensorRef)
        
        if self.config.doDark:
            self.darkCorrection(ccdExposure, sensorRef)
        
        for amp in ccd:
            ampExposure = ccdExposure.Factory(ccdExposure, amp.getBBox(), afwImage.PARENT)
            self.updateVariance(ampExposure, amp)

        if self.config.doFringe and not self.config.fringeAfterFlat:
            self.fringe.run(ccdExposure, sensorRef,
                            assembler=self.assembleCcd if self.config.doAssembleDetrends else None)
        
        if self.config.doFlat:
            self.flatCorrection(ccdExposure, sensorRef)

        defects = sensorRef.get('defects')
        self.maskAndInterpDefect(ccdExposure, defects)
        
        self.saturationInterpolation(ccdExposure)
        
        self.maskAndInterpNan(ccdExposure)

        if self.config.doFringe and self.config.fringeAfterFlat:
            self.fringe.run(ccdExposure, sensorRef,
                            assembler=self.assembleCcd if self.config.doAssembleDetrends else None)
        
        ccdExposure.getCalib().setFluxMag0(self.config.fluxMag0T1 * ccdExposure.getCalib().getExptime())

        if self.config.doWrite:
            sensorRef.put(ccdExposure, "postISRCCD")
        
        self.display("postISRCCD", ccdExposure)

        return pipeBase.Struct(
            exposure = ccdExposure,
        )
