import os.path

from lsst.utils import getPackageDir

config.processCcd.load(os.path.join(getPackageDir("obs_cfht"), "config", "processCcd.py"))
config.ccdKey = 'ccd'
