import os.path

from lsst.utils import getPackageDir

cfhtConfigDir = os.path.join(getPackageDir("obs_cfht"), "config")
config.calibrate.photoCal.colorterms.load(os.path.join(cfhtConfigDir, 'colorterms.py'))

from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask
config.isr.retarget(CfhtIsrTask)

config.isr.doBias = False
config.isr.doDark = False
config.isr.doFlat = False
config.isr.doFringe = False
config.isr.fringeAfterFlat = False
config.isr.doWrite = False
config.isr.fringe.filters = ['i', 'i2', 'z']
config.isr.fringe.pedestal = True
config.isr.fringe.small = 1
config.isr.fringe.large = 50
config.isr.doAssembleIsrExposures = True

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
