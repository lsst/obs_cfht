"""
CFHT-specific overrides for RunIsrTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

obsConfigDir = os.path.join(getPackageDir("obs_cfht"), "config")

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(obsConfigDir, "isr.py"))
