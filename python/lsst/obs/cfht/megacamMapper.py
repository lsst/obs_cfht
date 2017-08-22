from builtins import map
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

import pyfits

import lsst.afw.geom as afwGeom
import lsst.afw.image as afwImage
import lsst.afw.image.utils as afwImageUtils

from lsst.daf.persistence import Policy
from lsst.obs.base import CameraMapper, exposureFromImage
import lsst.pex.policy as pexPolicy
from .makeMegacamRawVisitInfo import MakeMegacamRawVisitInfo

# Solely to get boost serialization registrations for Measurement subclasses
import lsst.meas.algorithms  # flake8: noqa


class MegacamMapper(CameraMapper):
    packageName = "obs_cfht"

    MakeRawVisitInfoClass = MakeMegacamRawVisitInfo

    def __init__(self, **kwargs):
        policyFile = Policy.defaultPolicyFile("obs_cfht", "MegacamMapper.yaml", "policy")
        policy = Policy(policyFile)
        super(MegacamMapper, self).__init__(policy, os.path.dirname(policyFile), **kwargs)

        # The "ccd" provided by the user is translated through the registry into an extension name for the "raw"
        # template.  The template therefore doesn't include "ccd", so we need to ensure it's explicitly included
        # so the ArgumentParser can recognise and accept it.

        self.exposures['raw'].keyDict['ccd'] = int

        afwImageUtils.resetFilters()
        afwImageUtils.defineFilter('u', lambdaEff=374, alias="u.MP9301")
        afwImageUtils.defineFilter('u2', lambdaEff=354, alias="u.MP9302")
        afwImageUtils.defineFilter('g', lambdaEff=487, alias="g.MP9401")
        afwImageUtils.defineFilter('g2', lambdaEff=472, alias="g.MP9402")
        afwImageUtils.defineFilter('r', lambdaEff=628, alias="r.MP9601")
        afwImageUtils.defineFilter('r2', lambdaEff=640, alias="r.MP9602")
        afwImageUtils.defineFilter('i', lambdaEff=778, alias="i.MP9701")
        afwImageUtils.defineFilter('i2', lambdaEff=764, alias="i.MP9702")
        afwImageUtils.defineFilter('i3', lambdaEff=776, alias="i.MP9703")
        afwImageUtils.defineFilter('z', lambdaEff=1170, alias="z.MP9801")
        afwImageUtils.defineFilter('z2', lambdaEff=926, alias="z.MP9901")

        # define filters?
        self.filterIdMap = dict(u=0, g=1, r=2, i=3, z=4, i2=5, u2=6, g2=7, r2=8, i3=9, z2=10)

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
        for name in ("raw", "calexp", "postISRCCD", "src", "icSrc", "icMatch"):
            self.mappings[name].keyDict.update(keys)

    def bypass_defects(self, datasetType, pythonType, butlerLocation, dataId):
        """Return a defect based on the butler location returned by map_defects

        @param[in] butlerLocation: a ButlerLocation with locationList = path to defects FITS file
        @param[in] dataId: the usual data ID; "ccd" must be set

        Note: the name "bypass_XXX" means the butler makes no attempt to convert the ButlerLocation
        into an object, which is what we want for now, since that conversion is a bit tricky.
        """
        (ccdKey, ccdSerial) = self._getCcdKeyVal(dataId)
        defectsFitsPath = butlerLocation.locationList[0]
        with pyfits.open(defectsFitsPath) as hduList:
            for hdu in hduList[1:]:
                if str(hdu.header["SERIAL"]) != ccdSerial:
                    continue

                defectList = []
                for data in hdu.data:
                    bbox = afwGeom.Box2I(
                        afwGeom.Point2I(int(data['x0']), int(data['y0'])),
                        afwGeom.Extent2I(int(data['width']), int(data['height'])),
                    )
                    defectList.append(afwImage.DefectBase(bbox))
                return defectList

        raise RuntimeError("No defects for ccdSerial %s in %s" % (ccdSerial, defectsFitsPath))

    def _defectLookup(self, dataId):
        """Find the defects for a given CCD.
        @param dataId (dict) Dataset identifier
        @return (string) path to the defects file or None if not available"""

        if self.registry is None:
            raise RuntimeError("No registry for defect lookup")

        rows = self.registry.executeQuery(
            ("defects",),
            ("raw",),
            [("visit", "?"), ("ccd", "?")], None, (dataId['visit'], dataId['ccd']),
        )
        if len(rows) == 0:
            return None

        if len(rows) == 1:
            return os.path.join(self.defectPath, rows[0][0])
        else:
            raise RuntimeError("Querying for defects (%s) returns %d files: %s" %
                               (dataId['id'], len(rows), ", ".join([_[0] for _ in rows])))

    def _getCcdKeyVal(self, dataId):
        ccdName = self._extractDetectorName(dataId)
        return ("ccdSerial", self.camera[ccdName].getSerial())

    def _extractDetectorName(self, dataId):
        return "ccd%02d" % dataId['ccd']

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        pathId = self._transformId(dataId)
        visit = int(pathId['visit'])
        ccd = int(pathId['ccd'])
        return visit * 36 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve identifier for CCD"""
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        """Hook to retrieve number of bits in identifier for CCD"""
        return 32

    def _computeCoaddExposureId(self, dataId, singleFilter):
        """Compute the 64-bit (long) identifier for a coadd.

        @param dataId (dict)       Data identifier with tract and patch.
        @param singleFilter (bool) True means the desired ID is for a single-
                                   filter coadd, in which case dataId
                                   must contain filter.
        """
        tract = int(dataId['tract'])
        if tract < 0 or tract >= 128:
            raise RuntimeError('tract not in range [0,128)')
        patchX, patchY = list(map(int, dataId['patch'].split(',')))
        for p in (patchX, patchY):
            if p < 0 or p >= 2**13:
                raise RuntimeError('patch component not in range [0, 8192)')
        id = (tract * 2**13 + patchX) * 2**13 + patchY
        if singleFilter:
            return id * 8 + self.filterIdMap[dataId['filter']]
        return id

    def bypass_CoaddExposureId_bits(self, datasetType, pythonType, location, dataId):
        return 1 + 7 + 13*2 + 3

    def bypass_CoaddExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, True)

    bypass_deepCoaddId = bypass_CoaddExposureId

    bypass_deepCoaddId_bits = bypass_CoaddExposureId_bits

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, False)

    bypass_deepMergedCoaddId_bits = bypass_CoaddExposureId_bits

    def _computeStackExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a Stack exposure.

        @param dataId (dict) Data identifier with stack, patch, filter
        """
        nPatches = 1000000
        return (int(dataId["stack"]) * nPatches + int(dataId["patch"]))

    def _standardizeDetrend(self, detrend, image, dataId, filter=False):
        """Hack up detrend images to remove troublesome keyword"""
        md = image.getMetadata()
        removeKeyword(md, 'RADECSYS')  # Irrelevant, and use of "GAPPT" breaks wcslib
        md.set('TELAZ', 0)       # Irrelevant, -9999 value breaks VisitInfo, and absence generates a warning
        md.set('TELALT', 0)      # Irrelevant, -9999 value breaks VisitInfo, and absence generates a warning
        exp = exposureFromImage(image, logger=self.log)
        return self._standardizeExposure(self.calibrations[detrend], exp, dataId, filter=filter,
                                         trimmed=False)

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
