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
                     band="u",
                     lambdaEff=374, lambdaMin=336, lambdaMax=412),
    FilterDefinition(physical_filter="u.MP9302",
                     band="u",
                     afw_name="u2",
                     lambdaEff=354, lambdaMin=310, lambdaMax=397),
    FilterDefinition(physical_filter="u.MP9303",
                     band="u",
                     afw_name="u3",
                     lambdaEff=395, lambdaMin=390, lambdaMax=400),
    FilterDefinition(physical_filter="g.MP9401",
                     band="g",
                     lambdaEff=487, lambdaMin=414, lambdaMax=560),
    FilterDefinition(physical_filter="g.MP9402",
                     band="g",
                     afw_name="g2",
                     lambdaEff=472, lambdaMin=396, lambdaMax=548),
    FilterDefinition(physical_filter="g.MP9501",
                     band="g",
                     afw_name="g3",
                     lambdaEff=501, lambdaMin=495, lambdaMax=506),
    FilterDefinition(physical_filter="g.MP9502",
                     band="g",
                     afw_name="g4",
                     lambdaEff=511, lambdaMin=506, lambdaMax=516),
    FilterDefinition(physical_filter="r.MP9601",
                     band="r",
                     lambdaEff=628, lambdaMin=567, lambdaMax=689),
    FilterDefinition(physical_filter="r.MP9602",
                     band="r",
                     afw_name="r2",
                     lambdaEff=640, lambdaMin=566, lambdaMax=714),
    FilterDefinition(physical_filter="r.MP9603",
                     band="r",
                     afw_name="r3",
                     lambdaEff=659, lambdaMin=654, lambdaMax=664),
    FilterDefinition(physical_filter="r.MP9604",
                     band="r",
                     afw_name="r4",
                     lambdaEff=672, lambdaMin=666, lambdaMax=677),
    FilterDefinition(physical_filter="r.MP9605",
                     band="r",
                     afw_name="r5",
                     lambdaEff=611, lambdaMin=400, lambdaMax=821),
    FilterDefinition(physical_filter="i.MP9701",
                     band="i",
                     lambdaEff=778, lambdaMin=702, lambdaMax=853,),
    FilterDefinition(physical_filter="i.MP9702",
                     band="i",
                     afw_name="i2",
                     lambdaEff=764, lambdaMin=684, lambdaMax=845),
    FilterDefinition(physical_filter="i.MP9703",
                     band="i",
                     afw_name="i3",
                     lambdaEff=776, lambdaMin=696, lambdaMax=857,),
    FilterDefinition(physical_filter="z.MP9801",
                     band="z",
                     lambdaEff=1170, lambdaMin=827, lambdaMax=1514),
    FilterDefinition(physical_filter="z.MP9901",
                     band="z",
                     afw_name="z2",
                     lambdaEff=926, lambdaMin=849, lambdaMax=1002),
)
