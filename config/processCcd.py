"""
CFHT-specific overrides for processCcdTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

from lsst.meas.astrom import MatchOptimisticBTask

cfhtConfigDir = os.path.join(getPackageDir("obs_cfht"), "config")
config.calibrate.photoCal.colorterms.load(os.path.join(cfhtConfigDir, 'colorterms.py'))

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(cfhtConfigDir, "isr.py"))

config.calibrate.photoCal.colorterms.load(os.path.join(cfhtConfigDir, 'colorterms.py'))

config.charImage.repair.doCosmicRay = True
config.charImage.repair.cosmicray.cond3_fac = 2.5
config.charImage.repair.cosmicray.cond3_fac2 = 0.4
config.charImage.repair.cosmicray.niteration = 3
config.charImage.repair.cosmicray.nCrPixelMax = 100000
config.charImage.repair.cosmicray.minSigma = 6.0
config.charImage.repair.cosmicray.min_DN = 150.0

# Astrometry
for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader,
                     ):
    refObjLoader.filterMap = {'i2': 'i'}
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

config.calibrate.astrometry.wcsFitter.order = 3
if isinstance(config.calibrate.astrometry.matcher, MatchOptimisticBTask):
    config.calibrate.astrometry.matcher.maxMatchDistArcSec = 5
    config.calibrate.astrometry.sourceSelector['matcher'].excludePixelFlags = False

config.calibrate.photoCal.applyColorTerms = True
config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

# this was the default prior to DM-11521.  New default is 2000.
config.calibrate.deblend.maxFootprintSize=0

# Better astrometry matching
config.calibrate.astrometry.matcher.numBrightStars = 150
