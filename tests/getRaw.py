#!/usr/bin/env python

import unittest
import lsst.utils.tests as utilsTests

import lsst.daf.persistence as dafPersist
from lsst.obs.cfht import CfhtMapper

class GetRawTestCase(unittest.TestCase):
    """Testing butler raw image retrieval"""

    def setUp(self):
        self.bf = dafPersist.ButlerFactory(mapper=CfhtMapper(
            root="./tests/data",calibRoot="./tests/data/calib"))
        self.butler = self.bf.create()

    def tearDown(self):
        del self.butler
        del self.bf

    def testRaw(self):
        """Test retrieval of raw image"""
        raw = self.butler.get("raw", visit=788033, ccd=23, amp=0)
        self.assertEqual(raw.getWidth(), 1056)
        self.assertEqual(raw.getHeight(), 4644)
        self.assertEqual(raw.getFilter().getFilterProperty().getName(), "i")
        self.assertEqual(raw.getDetector().getId().getName(), "ID0")
        self.assertEqual(raw.getDetector().getParent().getId().getName(),
                "CFHT 23")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def suite():
    """Returns a suite containing all the test cases in this module."""

    utilsTests.init()

    suites = []
    suites += unittest.makeSuite(GetRawTestCase)
    suites += unittest.makeSuite(utilsTests.MemoryTestCase)
    return unittest.TestSuite(suites)

def run(shouldExit = False):
    """Run the tests"""
    utilsTests.run(suite(), shouldExit)

if __name__ == "__main__":
    run(True)
