import os.path
from lsst.utils import getPackageDir

if hasattr(config.astrometryRefObjLoader, "ref_dataset_name"):
    config.astrometryRefObjLoader.ref_dataset_name = 'pan-starrs'
if hasattr(config.photometryRefObjLoader, "ref_dataset_name"):
    config.photometryRefObjLoader.ref_dataset_name = 'sdss'
# existing PS1 refcat does not have coordinate errors
config.astrometryReferenceErr = 10

#filterMapFile = os.path.join(getPackageDir("obs_cfht"), "config", "filterMap.py")

config.astrometryRefObjLoader.filterMap = {
    'u': 'g',
    'g': 'g',
    'r': 'r',
    'i': 'i',
    'i2': 'i',
    'z': 'z',
    'y': 'y',
}
config.photometryRefObjLoader.filterMap = {
    'u': 'U',
    'g': 'G',
    'r': 'R',
    'i': 'I',
    'i2': 'I',
    'z': 'Z',
    'y': 'Z',
}

config.astrometryVisitOrder = 7
