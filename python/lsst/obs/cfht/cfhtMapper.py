# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
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

import re

import lsst.daf.base as dafBase
import lsst.afw.image as afwImage
import lsst.afw.coord as afwCoord
import lsst.afw.geom as afwGeom
import lsst.pex.policy as pexPolicy

from lsst.daf.butlerUtils import CameraMapper

class CfhtMapper(CameraMapper):
    def __init__(self, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_cfht", "CfhtMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)
        super(CfhtMapper, self).__init__(policy, policyFile.getRepositoryPath(), **kwargs)

    def _transformId(self, dataId):
        actualId = dataId.copy()
        if actualId.has_key("ccdName"):
            m = re.search(r'CFHT (\d+)', actualId['ccdName'])
            actualId['ccd'] = int(m.group(1))
        if actualId.has_key("ampName"):
            m = re.search(r'ID(\d+)', actualId['ampName'])
            actualId['amp'] = int(m.group(1))
        return actualId

    def _extractDetectorName(self, dataId):
        return "CFHT %(ccd)d" % dataId

    def _extractAmpId(self, dataId):
        return (self._extractDetectorName(dataId),
                int(dataId['amp']), 0)


    def _computeAmpExposureId(self, dataId):
        #visit, snap, raft, sensor, channel):
        """Compute the 64-bit (long) identifier for an amp exposure.

        @param dataId (dict) Data identifier with visit, snap, raft, sensor, channel
        """
        dataId = self._transformId(dataId)
        return (dataId['visit'] << 7) + (dataId['ccd'] << 1) + dataId['amp']

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, raft, sensor
        """
        dataId = self._transformId(dataId)
        return (dataId['visit'] << 6) + dataId['ccd']


    def add_sdqaAmp(self, dataId):
        ampExposureId = self._calculateAmpExposureId(dataId)
        return {"ampExposureId": ampExposureId, "sdqaRatingScope": "AMP"}

    def add_sdqaCcd(self, dataId):
        ccdExposureId = self._calculateCcdExposureId(dataId)
        return {"ccdExposureId": ccdExposureId, "sdqaRatingScope": "CCD"}
    
    def _addSources(self, dataId):
        """Generic 'add' function to add ampExposureId and filterId"""
        # Note that sources are identified by what is called an ampExposureId,
        # but in this case all we have is a CCD.
        ampExposureId = self._computeCcdExposureId(dataId)
        filterId = self.filterIdMap[pathId['filter']]
        return {"ampExposureId": ampExposureId, "filterId": filterId}

    def _addSkytile(self, dataId):
        """Generic 'add' function to add skyTileId"""
        return {"skyTileId": dataId['skyTile']}

for dsType in ("icSrc", "src"):
    setattr(CfhtMapper, "add_" + dsType, CfhtMapper._addSources)
for dsType in ("source", "badSource", "invalidSource", "object", "badObject"):
    setattr(CfhtMapper, "add_" + dsType, CfhtMapper._addSkytile)
