"""
CFHT-specific overrides for processCcdTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

obsConfigDir = os.path.join(getPackageDir("obs_cfht"), "config")

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(obsConfigDir, "isr.py"))

config.calibrate.photoCal.colorterms.load(os.path.join(obsConfigDir, 'colorterms.py'))

config.charImage.repair.doCosmicRay = True
config.charImage.repair.cosmicray.cond3_fac = 2.5
config.charImage.repair.cosmicray.cond3_fac2 = 0.4
config.charImage.repair.cosmicray.niteration = 3
config.charImage.repair.cosmicray.nCrPixelMax = 100000
config.charImage.repair.cosmicray.minSigma = 6.0
config.charImage.repair.cosmicray.min_DN = 150.0

# Configuration for AstrometryTask, the default. If the user retargets to
# ANetAstrometryTask, they must update the astrometry.solver.filterMap config
# manually; doing it here is impossible because these overrides are applied
# before any user overrides where retargeting could occur.
for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader):
    refObjLoader.filterMap = {'i2': 'i'}
config.calibrate.astrometry.wcsFitter.order = 3
config.calibrate.astrometry.matcher.maxMatchDistArcSec = 5

config.calibrate.photoCal.applyColorTerms = True
config.calibrate.photoCal.photoCatName = "e2v"
# this was the default prior to DM-11521.  New default is 2000.
config.calibrate.deblend.maxFootprintSize=0
