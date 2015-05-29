"""Set color terms for MegaCam"""

from lsst.pipe.tasks.colorterms import Colorterm, ColortermDictConfig

root.library = {
    "e2v": ColortermDictConfig(dict={
        "u": Colorterm(primary="u", secondary="g", c0=0.0, c1=-0.241),
        "g": Colorterm(primary="g", secondary="r", c0=0.0, c1=-0.153),
        "r": Colorterm(primary="r", secondary="g", c0=0.0, c1= 0.024),
        "i": Colorterm(primary="i", secondary="r", c0=0.0, c1= 0.085),
        "z": Colorterm(primary="z", secondary="i", c0=0.0, c1=-0.074),
    }),
}
