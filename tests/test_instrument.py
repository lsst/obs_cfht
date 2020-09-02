# This file is part of daf_butler.
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

"""Tests of the HyperSuprimeCam instrument class.
"""

import unittest

import lsst.utils.tests
import lsst.obs.cfht
from lsst.obs.base.instrument_tests import InstrumentTests, InstrumentTestData


class TestMegaCam(InstrumentTests, lsst.utils.tests.TestCase):
    def setUp(self):
        physical_filters = {
            "u.MP9301",
            "u.MP9302",
            "u.MP9303",
            "g.MP9401",
            "g.MP9402",
            "g.MP9501",
            "g.MP9502",
            "r.MP9601",
            "r.MP9602",
            "r.MP9603",
            "r.MP9604",
            "r.MP9605",
            "i.MP9701",
            "i.MP9702",
            "i.MP9703",
            "z.MP9801",
            "z.MP9901",
        }
        self.data = InstrumentTestData(name="MegaPrime",
                                       nDetectors=36,
                                       firstDetectorName="ccd00",
                                       physical_filters=physical_filters)

        self.instrument = lsst.obs.cfht.MegaPrime()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == '__main__':
    lsst.utils.tests.init()
    unittest.main()
