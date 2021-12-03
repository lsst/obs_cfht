"""
CFHT-specific overrides for processCcdTask
"""
import os.path

from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

configDir = os.path.dirname(__file__)

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(configDir, "isr.py"))


characterizeImage = os.path.join(configDir, "characterizeImage.py")
config.charImage.load(characterizeImage)

calibrate = os.path.join(configDir, "calibrate.py")
config.calibrate.load(calibrate)
