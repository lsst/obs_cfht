#
# LSST Data Management System
# Copyright 2008-2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import os
import numbers
import unittest

from lsst.utils import getPackageDir
import lsst.utils.tests
import lsst.pipe.tasks.photoCal as photoCal


class ColortermOverrideTestCase(unittest.TestCase):

    """Test that colorterms specific to CFHT override correctly"""

    def setUp(self):
        colortermsFile = os.path.join(getPackageDir("obs_cfht"), "config", "colorterms.py")
        self.photoCalConf = photoCal.PhotoCalConfig()
        self.photoCalConf.colorterms.load(colortermsFile)

    def testColorterms(self):
        """Test that the colorterm libraries are formatted correctly"""
        refFilters = ["u", "g", "r", "i", "z"]
        cfhtPhysicalFilters = ["u.MP9301", "g.MP9401", "r.MP9601", "i.MP9701", "z.MP9801"]
        for filter in cfhtPhysicalFilters:
            ct = self.photoCalConf.colorterms.getColorterm(filter, photoCatName="e2v")  # exact match
            self.assertIn(ct.primary, refFilters)
            self.assertIn(ct.secondary, refFilters)
            self.assertIsInstance(ct.c0, numbers.Number)
            self.assertIsInstance(ct.c1, numbers.Number)
            self.assertIsInstance(ct.c2, numbers.Number)


def setup_module(module):
    lsst.utils.tests.init()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
