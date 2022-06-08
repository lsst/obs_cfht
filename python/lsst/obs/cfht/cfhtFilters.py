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
                     band="u"),
    FilterDefinition(physical_filter="u.MP9302",
                     band="u",
                     afw_name="u2"),
    FilterDefinition(physical_filter="u.MP9303",
                     band="u",
                     afw_name="u3"),
    FilterDefinition(physical_filter="g.MP9401",
                     band="g"),
    FilterDefinition(physical_filter="g.MP9402",
                     band="g",
                     afw_name="g2"),
    FilterDefinition(physical_filter="g.MP9501",
                     band="g",
                     afw_name="g3"),
    FilterDefinition(physical_filter="g.MP9502",
                     band="g",
                     afw_name="g4"),
    FilterDefinition(physical_filter="r.MP9601",
                     band="r"),
    FilterDefinition(physical_filter="r.MP9602",
                     band="r",
                     afw_name="r2"),
    FilterDefinition(physical_filter="r.MP9603",
                     band="r",
                     afw_name="r3"),
    FilterDefinition(physical_filter="r.MP9604",
                     band="r",
                     afw_name="r4"),
    FilterDefinition(physical_filter="r.MP9605",
                     band="r",
                     afw_name="r5"),
    FilterDefinition(physical_filter="i.MP9701",
                     band="i"),
    FilterDefinition(physical_filter="i.MP9702",
                     band="i",
                     afw_name="i2"),
    FilterDefinition(physical_filter="i.MP9703",
                     band="i",
                     afw_name="i3"),
    FilterDefinition(physical_filter="z.MP9801",
                     band="z"),
    FilterDefinition(physical_filter="z.MP9901",
                     band="z",
                     afw_name="z2"),
)
