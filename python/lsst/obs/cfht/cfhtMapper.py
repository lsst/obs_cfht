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

import os
import re
from lsst.daf.persistence import Mapper, ButlerLocation, LogicalLocation
import lsst.daf.butlerUtils as butlerUtils
import lsst.daf.base as dafBase
import lsst.afw.image as afwImage
import lsst.afw.cameraGeom as afwCameraGeom
import lsst.afw.cameraGeom.utils as cameraGeomUtils
import lsst.afw.image.utils as imageUtils
import lsst.pex.logging as pexLog
import lsst.pex.policy as pexPolicy

from lsst.obs.camera import CameraMapper

class CfhtMapper(CameraMapper):
    def __init__(self, policy=None, root=".", registry=None, calibRoot=None):
        CameraMapper.__init__(self, policy=policy, root=root, registry=registry, calibRoot=calibRoot)

        self.filterMap = {
            "u.MP9301": "u",
            "g.MP9401": "g",
            "r.MP9601": "r",
            "i.MP9701": "i",
            "i.MP9702": "i2",
            "z.MP9801": "z"
        }

        # Note that i2 is mapped to the same slot for DC3b as LSST y
        # since CFHT does not have a y band.
        self.filterIdMap = {
                'u': 0, 'g': 1, 'r': 2, 'i': 3, 'z': 4, 'y': 5, 'i2': 5}

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
