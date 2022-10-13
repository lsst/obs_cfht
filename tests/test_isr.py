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
#
import os
import unittest

import lsst.afw.image as afwImage
import lsst.utils.tests

from lsst.obs.cfht import MegaPrime
from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask


testDataPackage = "testdata_cfht"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except LookupError:
    testDataDirectory = None


@unittest.skipIf(testDataDirectory is None, "Skipping tests as testdata_cfht is not setup")
class CfhtIsrTestCase(lsst.utils.tests.TestCase):
    """Test for the CFHT IsrTask wrapper."""

    def setUp(self):
        # We'll need a detector, so get the first one.
        self.camera = MegaPrime().getCamera()
        detector = self.camera[0]

        # Get the override.
        self.configPath = os.path.join(lsst.utils.getPackageDir("obs_cfht"), "config",
                                       "isr.py")
        # Read the image data.
        imageLocation = os.path.join(testDataDirectory, "DATA/raw/08BL05/w2.+2+2/2008-11-01/i2",
                                     "1038843o.fits.fz")
        self.exposure = self.imageHandler(imageLocation, detector)

    @staticmethod
    def imageHandler(location, detector=None):
        """Quick method to handle image reading.

        Parameters
        ----------
        location : `str`
            FITS file location.
        detector : `lsst.afw.cameraGeom.Detector`, optional
            Detector to attach to the exposure.

        Returns
        -------
        exp : `lsst.afw.image.Exposure`
            Fully constructed exposure.
        """
        if detector:
            hdu = detector.getId() + 1
        else:
            hdu = 1

        reader = afwImage.ExposureFitsReader(location)
        imReader = afwImage.ImageFitsReader(location, hdu=hdu)

        exp = afwImage.makeExposure(afwImage.makeMaskedImage(imReader.read()))
        exp.setMetadata(reader.readMetadata())
        exp.setInfo(reader.readExposureInfo())

        if detector:
            exp.setDetector(detector)

        return exp

    def test_processing(self):
        # Process image and confirm it doesn't fail.

        config = CfhtIsrTask.ConfigClass()

        # Manually fix config.
        config.doDark = False
        config.doDefect = False
        config.doFlat = False
        config.doBias = False
        config.doFringe = False
        config.fringeAfterFlat = False
        config.doWrite = False
        config.fringe.filters = ["i.MP9701", "i.MP9702", "z.MP9801"]
        config.fringe.pedestal = True
        config.fringe.small = 1
        config.fringe.large = 50
        config.doAssembleIsrExposures = True
        config.doSuspect = False
        config.fluxMag0T1 = {"i.MP9702": 100.0}

        task = CfhtIsrTask(config=config)
        results = task.run(self.exposure, camera=self.camera)
        md = results.exposure.getMetadata()
        amplifiers = list(results.exposure.getDetector().getAmplifiers())

        # Check that saturation level are set correctly.
        self.assertEqual(md['SATURATE'], 65535)

        # Check that the gain and read noise match what is in the
        # GAINA and GAINB/RDNOISEA RDNOISEB fields.
        self.assertEqual(md['GAINA'], amplifiers[0].getGain())
        self.assertEqual(md['GAINB'], amplifiers[1].getGain())
        self.assertEqual(md['RDNOISEA'], amplifiers[0].getReadNoise())
        self.assertEqual(md['RDNOISEB'], amplifiers[1].getReadNoise())


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
