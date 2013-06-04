#
# LSST Data Management System
# Copyright 2012 LSST Corporation.
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
import pwd

import lsst.daf.base as dafBase
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.daf.butlerUtils import CameraMapper, exposureFromImage
import lsst.pex.policy as pexPolicy

class MegacamMapper(CameraMapper):
    def __init__(self, outputRoot=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_cfht", "MegacamMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)
        super(MegacamMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

        # The "ccd" provided by the user is translated through the registry into an extension name for the "raw"
        # template.  The template therefore doesn't include "ccd", so we need to ensure it's explicitly included
        # so the ArgumentParser can recognise and accept it.
        for mapping in self.exposures.values():
            if 'visit' in mapping.keyDict:
                mapping.keyDict['ccd'] = int

        afwImageUtils.defineFilter('u', lambdaEff=350, alias="u.MP9301")
        afwImageUtils.defineFilter('g', lambdaEff=450, alias="g.MP9401")
        afwImageUtils.defineFilter('r', lambdaEff=600, alias="r.MP9601")
        afwImageUtils.defineFilter('i', lambdaEff=750, alias="i.MP9701")
        afwImageUtils.defineFilter('i2', lambdaEff=750, alias="i.MP9702")
        afwImageUtils.defineFilter('z', lambdaEff=900, alias="z.MP9801")

        # Ensure each dataset type of interest knows about the full range of keys available from the registry
        keys = {'runId': str,
                'object': str,
                'visit': int,
                'ccd': int,
                'extension': int,
                'state': str,
                'filter': str,
                'date': str,
                'taiObs': str,
                'expTime': float,
                }
        for name in ("raw", "calexp", "postISRCCD", "src"):
            self.mappings[name].keyDict.update(keys)

    def _extractDetectorName(self, dataId):
        return "ccd%02d" % dataId['ccd']

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        pathId = self._transformId(dataId)
        visit = long(pathId['visit'])
        ccd = long(pathId['ccd'])
        return visit * 36 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve identifier for CCD"""
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve number of bits in identifier for CCD"""
        return 32

    def _computeStackExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a Stack exposure.

        @param dataId (dict) Data identifier with stack, patch, filter
        """
        nPatches = 1000000
        return (long(dataId["stack"]) * nPatches + long(dataId["patch"]))

    def bypass_stackExposureId(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve identifier for stack/coadd"""
        return self._computeStackExposureId(dataId)

    def bypass_stackExposureId_bits(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve number of bits in identifier for stack/coadd"""
        return 32 # not really, but this leaves plenty of space for sources

    def _standardizeDetrend(self, detrend, image, dataId, filter=False):
        """Hack up detrend images to remove troublesome keyword"""
        md = image.getMetadata()
        removeKeyword(md, 'RADECSYS') # Irrelevant, and use of "GAPPT" breaks wcslib
        exp = exposureFromImage(image)
        return self._standardizeExposure(self.calibrations[detrend], exp, dataId, filter=filter, trimmed=False)

    def std_bias(self, image, dataId):
        return self._standardizeDetrend("bias", image, dataId, filter=False)

    def std_dark(self, image, dataId):
        return self._standardizeDetrend("dark", image, dataId, filter=False)

    def std_flat(self, image, dataId):
        return self._standardizeDetrend("flat", image, dataId, filter=True)

    def std_fringe(self, image, dataId):
        return self._standardizeDetrend("fringe", image, dataId, filter=True)


def removeKeyword(md, key):
    """Remove a keyword from a header without raising an exception if it doesn't exist"""
    if md.exists(key):
        md.remove(key)
