#!/usr/bin/env python

import unittest
import lsst.utils.tests as utilsTests

import lsst.daf.persistence as dafPersist
from lsst.obs.cfht import CfhtMapper

class GetBiasTestCase(unittest.TestCase):
    """Testing butler bias image retrieval"""

    def setUp(self):
        self.bf = dafPersist.ButlerFactory(mapper=CfhtMapper(
            root="./tests/data",calibRoot="./tests/data/calib"))
        self.butler = self.bf.create()

    def tearDown(self):
        del self.butler
        del self.bf

    def testBias(self):
        """Test retrieval of bias image"""
        raw = self.butler.get("bias", visit=788033, snap=0, ccd=23, amp=0)
        self.assertEqual(raw.getWidth(), 1056)
        self.assertEqual(raw.getHeight(), 4644)
        self.assertEqual(raw.getDetector().getId().getName(), "ID0")
        self.assertEqual(raw.getDetector().getParent().getId().getName(),
                "CFHT 23")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def suite():
    """Returns a suite containing all the test cases in this module."""

    utilsTests.init()

    suites = []
    suites += unittest.makeSuite(GetBiasTestCase)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

def run(shouldExit = False):
    """Run the tests"""
    utilsTests.run(suite(), shouldExit)

if __name__ == "__main__":
    run(True)
