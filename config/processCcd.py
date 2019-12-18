"""
CFHT-specific overrides for processCcdTask
"""
import os.path

from lsst.utils import getPackageDir
from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask

from lsst.meas.astrom import MatchOptimisticBConfig

ObsConfigDir = os.path.join(getPackageDir("obs_cfht"), "config")

#### Future
#bgFile = os.path.join(ObsConfigDir, "background.py")

config.calibrate.photoCal.colorterms.load(os.path.join(ObsConfigDir, 'colorterms.py'))

config.isr.retarget(CfhtIsrTask)
config.isr.load(os.path.join(ObsConfigDir, "isr.py"))

config.calibrate.photoCal.colorterms.load(os.path.join(ObsConfigDir, 'colorterms.py'))

config.charImage.repair.doCosmicRay = True
config.charImage.repair.cosmicray.cond3_fac = 2.5
config.charImage.repair.cosmicray.cond3_fac2 = 0.4
config.charImage.repair.cosmicray.niteration = 3
config.charImage.repair.cosmicray.nCrPixelMax = 100000
config.charImage.repair.cosmicray.minSigma = 6.0
config.charImage.repair.cosmicray.min_DN = 150.0

# PSF determination
config.charImage.measurePsf.reserve.fraction = 0.2
config.charImage.measurePsf.starSelector["objectSize"].sourceFluxField = 'base_PsfFlux_instFlux'
try:
    import lsst.meas.extensions.psfex.psfexPsfDeterminer
    config.charImage.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
    config.charImage.measurePsf.psfDeterminer["psfex"].psfexBasis = 'PIXEL_AUTO'
    config.charImage.measurePsf.psfDeterminer["psfex"].samplingSize = 0.5
    config.charImage.measurePsf.psfDeterminer["psfex"].kernelSize = 81
    config.charImage.measurePsf.psfDeterminer.name = "psfex"
except ImportError as e:
    print("WARNING: Unable to use psfex: %s" % e)
    config.charImage.measurePsf.psfDeterminer.name = "pca"

# Astrometry
for refObjLoader in (config.calibrate.astromRefObjLoader,
                     config.calibrate.photoRefObjLoader,
                     config.charImage.refObjLoader,
                     ):
    refObjLoader.filterMap = {'i2': 'i'}
    refObjLoader.filterMap = {'r2': 'r'}
    refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

config.calibrate.astrometry.wcsFitter.order = 3
if isinstance(config.calibrate.astrometry.matcher, MatchOptimisticBConfig):
    config.calibrate.astrometry.matcher.maxMatchDistArcSec = 5

config.calibrate.photoCal.applyColorTerms = True
config.calibrate.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

# Needed to be compatible with gen2 reference catalogs
config.calibrate.connections.astromRefCat = "ps1_pv3_3pi_20170110"
config.calibrate.connections.photoRefCat = "ps1_pv3_3pi_20170110"

# this was the default prior to DM-11521.  New default is 2000.
config.calibrate.deblend.maxFootprintSize=0

# Better astrometry matching
config.calibrate.astrometry.matcher.numBrightStars = 150

# Demand astrometry and photoCal succeed
config.calibrate.requireAstrometry = True
config.calibrate.requirePhotoCal = True

config.calibrate.doWriteMatchesDenormalized = True

# Detection
config.charImage.detection.isotropicGrow = True
config.calibrate.detection.isotropicGrow = True

# Activate calibration of measurements: required for aperture corrections
config.charImage.load(os.path.join(ObsConfigDir, "cmodel.py"))
config.charImage.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.charImage.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.charImage.measurement.load(os.path.join(ObsConfigDir, "convolvedFluxes.py"))
config.charImage.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))
if "ext_shapeHSM_HsmShapeRegauss" in config.charImage.measurement.plugins:
    # no deblending has been done
    config.charImage.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = ""

config.calibrate.measurement.load(os.path.join(ObsConfigDir, "apertures.py"))
config.calibrate.measurement.load(os.path.join(ObsConfigDir, "kron.py"))
config.calibrate.measurement.load(os.path.join(ObsConfigDir, "hsm.py"))

# Deblender
config.charImage.deblend.maskLimits["NO_DATA"] = 0.25 # Ignore sources that are in the vignetted region
config.charImage.deblend.maxFootprintArea = 10000
config.calibrate.deblend.maxFootprintSize=0
config.calibrate.deblend.maskLimits["NO_DATA"] = 0.25 # Ignore sources that are in the vignetted region
config.calibrate.deblend.maxFootprintArea = 10000

config.charImage.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.calibrate.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.charImage.measurement.plugins["base_Jacobian"].pixelScale = 0.185
config.calibrate.measurement.plugins["base_Jacobian"].pixelScale = 0.185

# Convolved fluxes can fail for small target seeing if the observation seeing is larger
if "ext_convolved_ConvolvedFlux" in config.charImage.measurement.plugins:
    names = config.charImage.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames()
    config.charImage.measureApCorr.allowFailure += names
