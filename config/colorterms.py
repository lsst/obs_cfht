"""Set color terms for MegaCam"""

from lsst.pipe.tasks.colorterms import Colorterm, ColortermDict

# 2018-09-04: Michael Wood-Vasey:
# The color terms should translate between the photometric reference catalog
# and the system transmission of MegaCam.
# I've added a set of color terms here for the PS1 reference catalog
# assuming that the PS1 catalog is on the AB system.
config.data = {
    "ps1*": ColortermDict(
        data={
            "u.MP9301": Colorterm(primary="u", secondary="g", c0=0.0, c1=-0.241),
            "g.MP9401": Colorterm(primary="g", secondary="r", c0=0.0, c1=-0.153),
            "r.MP9601": Colorterm(primary="r", secondary="g", c0=0.0, c1=0.024),
            "i.MP9701": Colorterm(primary="i", secondary="r", c0=0.0, c1=0.085),
            "z.MP9801": Colorterm(primary="z", secondary="i", c0=0.0, c1=-0.074),
        }
    ),
    "e2v": ColortermDict(
        data={
            "u.MP9301": Colorterm(primary="u", secondary="g", c0=0.0, c1=-0.241),
            "g.MP9401": Colorterm(primary="g", secondary="r", c0=0.0, c1=-0.153),
            "r.MP9601": Colorterm(primary="r", secondary="g", c0=0.0, c1=0.024),
            "i.MP9701": Colorterm(primary="i", secondary="r", c0=0.0, c1=0.085),
            "z.MP9801": Colorterm(primary="z", secondary="i", c0=0.0, c1=-0.074),
        }
    ),
}
