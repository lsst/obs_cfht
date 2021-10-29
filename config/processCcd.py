"""
CFHT-specific overrides for processCcdTask
"""
import os.path

from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

configDir = os.path.dirname(__file__)

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(cfhtConfigDir, "isr.py"))


characterizeImage = os.path.join(configDir, "characterizeImage.py")
config.characterizeImage.load(characterizeImage)

calibrate = os.path.join(configDir, "calibrate.py")
config.calibrate.load(calibrate)
