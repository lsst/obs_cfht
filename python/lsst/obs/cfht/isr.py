from lsst.ip.isr import IsrTask
import lsst.ip.isr.isr as isr

class MegacamIsrTask(IsrTask):
    def convertIntToFloat(self, exp):
        """No need to convert"""
        return exp

    def biasCorrection(self, exposure, dataRef):
        bias = dataRef.get("bias")
        bias = self.assembleCcd.assembleCcd(bias)
        isr.biasCorrection(exposure.getMaskedImage(), bias.getMaskedImage())

    def darkCorrection(self, exposure, dataRef):
        """Apply dark correction in place
    
        @param[in,out]  exposure        exposure to process
        @param[in]      dataRef         data reference at same level as exposure
        """
        dark = dataRef.get("dark")
        dark = self.assembleCcd.assembleCcd(dark)
        isr.darkCorrection(
            maskedImage = exposure.getMaskedImage(),
            darkMaskedImage = dark.getMaskedImage(),
            expScale = exposure.getCalib().getExptime(),
            darkScale = dark.getCalib().getExptime(),
        )

    def flatCorrection(self, exposure, dataRef):
        flat = dataRef.get("flat")
        flat = self.assembleCcd.assembleCcd(flat)
        isr.flatCorrection(
            maskedImage = exposure.getMaskedImage(),
            flatMaskedImage = flat.getMaskedImage(),
            scalingType = self.config.flatScalingType,
            userScale = self.config.flatUserScale,
        )
