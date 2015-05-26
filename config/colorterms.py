"""Set color terms for MegaCam"""

from lsst.pipe.tasks.colorterms import Colorterm
from lsst.obs.cfht.colorterms import colortermsData
Colorterm.setColorterms(colortermsData)
Colorterm.setActiveDevice("e2v")
