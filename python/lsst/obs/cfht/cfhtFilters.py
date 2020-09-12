# This file is part of obs_cfht.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ("MEGAPRIME_FILTER_DEFINITIONS",)

from lsst.obs.base import FilterDefinition, FilterDefinitionCollection

# Filter specification comes from
# https://www.cfht.hawaii.edu/Instruments/Filters/megaprimenew.html

# With current afwFilter singleton we can not define abstract filters
# properly since we are only allowed one u alias.
MEGAPRIME_FILTER_DEFINITIONS = FilterDefinitionCollection(
    FilterDefinition(physical_filter="u.MP9301",
                     abstract_filter="u",
                     lambdaEff=374, lambdaMin=336, lambdaMax=412),
    FilterDefinition(physical_filter="u.MP9302",
                     abstract_filter="u2",
                     alias={"u2"},
                     lambdaEff=354, lambdaMin=310, lambdaMax=397),
    FilterDefinition(physical_filter="u.MP9303",
                     abstract_filter="u3",
                     lambdaEff=395, lambdaMin=390, lambdaMax=400),
    FilterDefinition(physical_filter="g.MP9401",
                     abstract_filter="g",
                     lambdaEff=487, lambdaMin=414, lambdaMax=560),
    FilterDefinition(physical_filter="g.MP9402",
                     abstract_filter="g2",
                     alias={"g2"},
                     lambdaEff=472, lambdaMin=396, lambdaMax=548),
    FilterDefinition(physical_filter="g.MP9501",
                     abstract_filter="g3",
                     lambdaEff=501, lambdaMin=495, lambdaMax=506),
    FilterDefinition(physical_filter="g.MP9502",
                     abstract_filter="g4",
                     lambdaEff=511, lambdaMin=506, lambdaMax=516),
    FilterDefinition(physical_filter="r.MP9601",
                     abstract_filter="r",
                     lambdaEff=628, lambdaMin=567, lambdaMax=689),
    FilterDefinition(physical_filter="r.MP9602",
                     abstract_filter="r2",
                     alias={"r2"},
                     lambdaEff=640, lambdaMin=566, lambdaMax=714),
    FilterDefinition(physical_filter="r.MP9603",
                     abstract_filter="r3",
                     lambdaEff=659, lambdaMin=654, lambdaMax=664),
    FilterDefinition(physical_filter="r.MP9604",
                     abstract_filter="r4",
                     lambdaEff=672, lambdaMin=666, lambdaMax=677),
    FilterDefinition(physical_filter="r.MP9605",
                     abstract_filter="r5",
                     lambdaEff=611, lambdaMin=400, lambdaMax=821),
    FilterDefinition(physical_filter="i.MP9701",
                     abstract_filter="i",
                     lambdaEff=778, lambdaMin=702, lambdaMax=853,),
    FilterDefinition(physical_filter="i.MP9702",
                     abstract_filter="i2",
                     alias={"i2"},
                     lambdaEff=764, lambdaMin=684, lambdaMax=845),
    FilterDefinition(physical_filter="i.MP9703",
                     abstract_filter="i3",
                     alias={"i3"},
                     lambdaEff=776, lambdaMin=696, lambdaMax=857,),
    FilterDefinition(physical_filter="z.MP9801",
                     abstract_filter="z",
                     lambdaEff=1170, lambdaMin=827, lambdaMax=1514),
    FilterDefinition(physical_filter="z.MP9901",
                     abstract_filter="z2",
                     alias={"z2"},
                     lambdaEff=926, lambdaMin=849, lambdaMax=1002),
)
