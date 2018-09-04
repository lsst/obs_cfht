"""Set color terms for MegaCam"""

from lsst.pipe.tasks.colorterms import Colorterm, ColortermDict

config.data = {
    "ps1_pv3_3pi_20170110": ColortermDict(data={
        "u": Colorterm(primary="u", secondary="g", c0=0.0, c1=-0.241),
        "g": Colorterm(primary="g", secondary="r", c0=0.0, c1=-0.153),
        "r": Colorterm(primary="r", secondary="g", c0=0.0, c1=0.024),
        "i": Colorterm(primary="i", secondary="r", c0=0.0, c1=0.085),
        "z": Colorterm(primary="z", secondary="i", c0=0.0, c1=-0.074),
    }),
    "e2v": ColortermDict(data={
        "u": Colorterm(primary="u", secondary="g", c0=0.0, c1=-0.241),
        "g": Colorterm(primary="g", secondary="r", c0=0.0, c1=-0.153),
        "r": Colorterm(primary="r", secondary="g", c0=0.0, c1=0.024),
        "i": Colorterm(primary="i", secondary="r", c0=0.0, c1=0.085),
        "z": Colorterm(primary="z", secondary="i", c0=0.0, c1=-0.074),
    }),
}
