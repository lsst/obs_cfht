#
# LSST Data Management System
# Copyright 2008-2017 AURA/LSST.
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
import unittest
import lsst.utils.tests

from lsst.pipe.tasks.makeSkyMap import MakeSkyMapConfig
from lsst.pipe.tasks.multiBand import MergeDetectionsConfig
from lsst.pipe.tasks.multiBand import MergeMeasurementsConfig
from lsst.pipe.tasks.processCcd import ProcessCcdConfig
from lsst.utils import getPackageDir


class ConfigOverrideTestCase(lsst.utils.tests.TestCase):
    """Test that config overrides apply without error."""
    CONFIG_DIR = os.path.join(getPackageDir("obs_cfht"), "config")

    def testOverrides(self):
        # Other config overrides at time of writing:
        #
        # colorterms.py: Tested implicitly in processCcd.py
        # singleFrameDriver.py: Requires pipe_drivers, which is not a
        # dependency of this package.
        for configClass, overrideFilename in {
            MakeSkyMapConfig: "makeSkyMap.py",
            MergeDetectionsConfig: "mergeCoaddDetections.py",
            MergeMeasurementsConfig: "mergeCoaddMeasurements.py",
            ProcessCcdConfig: "processCcd.py"
        }.items():
            config = configClass()
            try:
                config.load(os.path.join(self.CONFIG_DIR, overrideFilename))
            except AttributeError as e:
                # A failure to load configuration is a test failure, not an
                # error, so we convert the exception appropriately.
                self.fail(e)


def setup_module(module):
    lsst.utils.tests.init()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
