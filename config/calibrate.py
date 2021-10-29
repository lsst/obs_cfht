import os.path

from lsst.meas.astrom import MatchOptimisticBTask

configDir = os.path.dirname(__file__)

config.photoCal.colorterms.load(os.path.join(configDir, 'colorterms.py'))

config.astromRefObjLoader.filterMap = {'i2': 'i'}
config.astromRefObjLoader.ref_dataset_name = "gaia_dr2_20200414"
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
