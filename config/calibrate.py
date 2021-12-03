import os.path

from lsst.meas.astrom import MatchOptimisticBTask

configDir = os.path.dirname(__file__)

config.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))

config.astromRefObjLoader.ref_dataset_name = "gaia_dr2_20200414"
# TODO DM-27843: workaround for gen3 not supporting anyFilterMapsToThis
config.astromRefObjLoader.filterMap = {'g': 'phot_g_mean',
                                       'r': 'phot_g_mean',
                                       'i': 'phot_g_mean',
                                       'z': 'phot_g_mean',
                                       'y': 'phot_g_mean'}

config.photoRefObjLoader.filterMap = {'i2': 'i'}
config.photoRefObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

config.connections.astromRefCat = "gaia_dr2_20200414"
config.connections.photoRefCat = "ps1_pv3_3pi_20170110"

config.astrometry.wcsFitter.order = 3
if isinstance(config.astrometry.matcher, MatchOptimisticBTask):
    config.astrometry.matcher.maxMatchDistArcSec = 5
    config.astrometry.sourceSelector['matcher'].excludePixelFlags = False

config.photoCal.applyColorTerms = True
config.photoCal.photoCatName = "ps1_pv3_3pi_20170110"

# this was the default prior to DM-11521.  New default is 2000.
config.deblend.maxFootprintSize=0

# Better astrometry matching
config.astrometry.matcher.numBrightStars = 150

# ====================================
# TODO DM-31063: below are things taken from obs_subaru that should be moved
# into a generic pipeline config once gen2 is gone.
config.measurement.plugins.names |= ["base_CircularApertureFlux"]
config.measurement.plugins["base_CircularApertureFlux"].radii = [3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]
# Use a large aperture to be independent of seeing in calibration
config.measurement.plugins["base_CircularApertureFlux"].maxSincRadius = 12.0

import lsst.meas.extensions.photometryKron
config.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]

from lsst.utils import getPackageDir
config.measurement.load(os.path.join(getPackageDir("meas_extensions_shapeHSM"), "config", "enable.py"))
config.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = "deblend_nChild"
# Enable debiased moments
config.measurement.plugins.names |= ["ext_shapeHSM_HsmPsfMomentsDebiased"]


config.measurement.plugins.names |= ["base_Jacobian", "base_FPPosition"]
config.measurement.plugins["base_Jacobian"].pixelScale = 0.187 
