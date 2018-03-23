#
# LSST Data Management System
# Copyright 2012-2017 LSST Corporation.
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

from __future__ import absolute_import, division, print_function
from builtins import range
import math
import os
import sys

import unittest
import warnings
from lsst.utils import getPackageDir
import lsst.utils.tests
import lsst.daf.persistence as dafPersist
import lsst.afw.cameraGeom.utils as cameraGeomUtils
import lsst.pex.exceptions as pexExcept
from lsst.daf.base import DateTime
from lsst.afw.image import RotType
from lsst.afw.geom import degrees, SpherePoint

try:
    type(display)
except NameError:
    display = False

frame = 0


class GetRawTestCase(lsst.utils.tests.TestCase):

    """Testing butler raw image retrieval"""

    def setUp(self):
        datadir = self.getTestDataDir()
        self.repoPath = os.path.join(datadir, "DATA")
        self.calibPath = os.path.join(datadir, "CALIB")
        self.butler = dafPersist.Butler(root=self.repoPath,
                                        calibRoot=self.calibPath)
        self.size = (2112, 4644)
        self.dataId = {'visit': 1038843}
        self.filter = "i2"
        self.exposureTime = 615.037
        self.darkTime = 615.0
        dateObs = DateTime(54771.6066250, DateTime.MJD, DateTime.UTC)
        self.dateAvg = DateTime(dateObs.nsecs(DateTime.TAI) + int(0.5e9*self.exposureTime), DateTime.TAI)
        self.boresightRaDec = SpherePoint(135.409417, -2.400000, degrees)
        self.boresightAzAlt = SpherePoint(122.34, 52.02, degrees)
        self.boresightAirmass = 1.269
        self.rotType = RotType.UNKNOWN
        self.obs_longitude = -155.468876*degrees
        self.obs_latitude = 19.825252*degrees
        self.obs_elevation = 4204
        self.weath_airTemperature = 0.90
        self.weath_airPressure = 617.65*100  # 100 Pascal/millibar
        self.weath_humidity = 39.77
        # NOTE: if we deal with DM-8053 and get UT1 implemented, ERA will change slightly.
        lst = 104.16591666666666*degrees
        self.era = lst - self.obs_longitude

    def tearDown(self):
        del self.butler

    def assertExposure(self, exp, ccd, checkFilter=True):
        print("dataId: ", self.dataId)
        print("ccd: ", ccd)
        print("width: ", exp.getWidth())
        print("height: ", exp.getHeight())
        print("detector name: ", exp.getDetector().getName())
        print("filter name: ", exp.getFilter().getFilterProperty().getName())

        self.assertEqual(exp.getWidth(), self.size[0])
        self.assertEqual(exp.getHeight(), self.size[1])
        self.assertEqual(exp.getDetector().getName(), "ccd%02d" % ccd)
        if checkFilter:
            self.assertEqual(exp.getFilter().getFilterProperty().getName(), self.filter)

        if display and ccd % 18 == 0:
            global frame
            frame += 1
            ccd = exp.getDetector()
            for amp in ccd:
                amp = amp
                print(ccd.getId(), amp.getId(), amp.getDataSec().toString(),
                      amp.getBiasSec().toString(), amp.getElectronicParams().getGain())
            cameraGeomUtils.showCcd(ccd, ccdImage=exp, frame=frame)

    def getTestDataDir(self):
        try:
            datadir = getPackageDir("testdata_cfht")
        except pexExcept.NotFoundError as e:
            warnings.warn(e.args[0])
            raise unittest.SkipTest("Skipping test as testdata_cfht is not setup")
        return datadir

    def testRaw(self):
        """Test retrieval of raw image"""
        if display:
            global frame
            frame += 1
            cameraGeomUtils.showCamera(self.butler.mapper.camera, frame=frame)

        for ccd in range(36):
            raw = self.butler.get("raw", self.dataId, ccd=ccd, immediate=True)

            self.assertExposure(raw, ccd)

            visitInfo = raw.getInfo().getVisitInfo()
            self.assertAlmostEqual(visitInfo.getDate().get(), self.dateAvg.get())
            self.assertEqual(visitInfo.getEra(), self.era)
            self.assertAlmostEqual(visitInfo.getExposureTime(), self.exposureTime)
            self.assertAlmostEqual(visitInfo.getDarkTime(), self.darkTime)
            self.assertSpherePointsAlmostEqual(visitInfo.getBoresightRaDec(), self.boresightRaDec)
            self.assertSpherePointsAlmostEqual(visitInfo.getBoresightAzAlt(), self.boresightAzAlt)
            self.assertAlmostEqual(visitInfo.getBoresightAirmass(), self.boresightAirmass)
            self.assertTrue(math.isnan(visitInfo.getBoresightRotAngle()))
            self.assertEqual(visitInfo.getRotType(), self.rotType)
            observatory = visitInfo.getObservatory()
            self.assertAnglesAlmostEqual(observatory.getLongitude(), self.obs_longitude)
            self.assertAnglesAlmostEqual(observatory.getLatitude(), self.obs_latitude)
            self.assertAlmostEqual(observatory.getElevation(), self.obs_elevation)
            weather = visitInfo.getWeather()
            self.assertAlmostEqual(weather.getAirTemperature(), self.weath_airTemperature)
            self.assertAlmostEqual(weather.getAirPressure(), self.weath_airPressure)
            self.assertAlmostEqual(weather.getHumidity(), self.weath_humidity)

    def getDetrend(self, detrend):
        """Test retrieval of detrend image"""
        for ccd in range(36):
            flat = self.butler.get(detrend, self.dataId, ccd=ccd, immediate=True)

            self.assertExposure(flat, ccd, checkFilter=False)

    def testFlat(self):
        self.getDetrend("flat")

    def testBias(self):
        self.getDetrend("bias")

    def testFringe(self):
        self.getDetrend("fringe")

    def testPackageName(self):
        name = dafPersist.Butler.getMapperClass(root=self.repoPath).packageName
        self.assertEqual(name, "obs_cfht")


def setup_module(module):
    lsst.utils.tests.init()


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    if "--display" in sys.argv:
        display = True
    lsst.utils.tests.init()
    unittest.main()
