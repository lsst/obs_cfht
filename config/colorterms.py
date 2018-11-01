"""Set color terms for MegaCam"""

from lsst.pipe.tasks.colorterms import Colorterm, ColortermDict

# 2018-09-04: Michael Wood-Vasey:
# The color terms should translate between the photometric reference catalog
# and the system transmission of MegaCam.
# I've added a set of color terms here for the PS1 reference catalog
# assuming that the PS1 catalog is on the AB system.
config.data = {
    "ps1*": ColortermDict(data={
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
