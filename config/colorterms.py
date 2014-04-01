"""Set color terms for MegaCam"""

from lsst.meas.photocal.colorterms import Colorterm
from lsst.obs.cfht.colorterms import colortermsData
Colorterm.setColorterms(colortermsData)
Colorterm.setActiveDevice("e2v")
