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

"""Unit tests for Gen3 CFHT raw data ingest.
"""

import unittest
import os
import lsst.utils.tests

from lsst.daf.butler import Butler, DataCoordinate
from lsst.obs.base.ingest_tests import IngestTestBase

testDataPackage = "testdata_cfht"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, f"{testDataPackage} must be set up")
class MegaPrimeIngestTestCase(IngestTestBase, lsst.utils.tests.TestCase):

    curatedCalibrationDatasetTypes = ()
    ingestDir = os.path.dirname(__file__)
    instrumentClassName = "lsst.obs.cfht.MegaPrime"
    rawIngestTask = "lsst.obs.cfht.MegaPrimeRawIngestTask"
    filterLabel = lsst.afw.image.FilterLabel(physical="i.MP9702", band="i2")

    @property
    def file(self):
        return os.path.join(testDataDirectory, "DATA/raw/08BL05/w2.+2+2/2008-11-01/i2/1038843o.fits.fz")

    dataIds = [dict(instrument="MegaPrime", exposure=1038843, detector=i) for i in range(36)]

    @property
    def visits(self):
        butler = Butler(self.root, collections=[self.outputRun])
        return {
            DataCoordinate.standardize(
                instrument="MegaPrime",
                visit=1038843,
                universe=butler.registry.dimensions
            ): [
                DataCoordinate.standardize(
                    instrument="MegaPrime",
                    exposure=1038843,
                    universe=butler.registry.dimensions
                )
            ]
        }

    def checkRepo(self, files=None):
        # We ignore `files` because there's only one raw file in
        # testdata_subaru, and we know it's a science frame.
        # If we ever add more, this test will need to change.
        butler = Butler(self.root, collections=[self.outputRun])
        expanded = butler.registry.expandDataId(self.dataIds[0])
        self.assertEqual(expanded.records["exposure"].observation_type, "science")


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
