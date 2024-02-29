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

"""Butler instrument description for the CFHT MegaCam camera.
"""

__all__ = ("MegaPrime",)

import os
from functools import lru_cache

from astro_metadata_translator import MegaPrimeTranslator
from lsst.afw.cameraGeom import makeCameraFromPath, CameraConfig
from lsst.obs.base import Instrument, VisitSystem
from .cfhtFilters import MEGAPRIME_FILTER_DEFINITIONS

from lsst.utils.introspection import get_full_type_name
from lsst.utils import getPackageDir


class MegaPrime(Instrument):
    filterDefinitions = MEGAPRIME_FILTER_DEFINITIONS
    policyName = "megacam"
    obsDataPackage = None
    translatorClass = MegaPrimeTranslator

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        packageDir = getPackageDir("obs_cfht")
        self.configPaths = [os.path.join(packageDir, "config")]

    @classmethod
    def getName(cls):
        return "MegaPrime"

    def getCamera(self):
        path = os.path.join(getPackageDir("obs_cfht"), self.policyName, "camera")
        return self._getCameraFromPath(path)

    @staticmethod
    @lru_cache()
    def _getCameraFromPath(path):
        """Return the camera geometry given solely the path to the location
        of that definition."""
        config = CameraConfig()
        config.load(os.path.join(path, "camera.py"))
        return makeCameraFromPath(
            cameraConfig=config,
            ampInfoPath=path,
            shortNameFunc=lambda name: name.replace(" ", "_"),
        )

    def register(self, registry, update=False):
        camera = self.getCamera()
        obsMax = 2**31
        with registry.transaction():
            registry.syncDimensionData(
                "instrument",
                {
                    "name": self.getName(), "detector_max": 36, "visit_max": obsMax, "exposure_max": obsMax,
                    "class_name": get_full_type_name(self),
                    # Some schemas support default visit_system
                    "visit_system": VisitSystem.ONE_TO_ONE.value,
                },
                update=update
            )

            for detector in camera:
                registry.syncDimensionData(
                    "detector",
                    {
                        "instrument": self.getName(),
                        "id": detector.getId(),
                        "full_name": detector.getName(),
                        "name_in_raft": detector.getName(),
                        "raft": None,  # MegaPrime does not have rafts
                        "purpose": str(detector.getType()).split(".")[-1],
                    },
                    update=update
                )

            self._registerFilters(registry, update=update)

    def getRawFormatter(self, dataId):
        # local import to prevent circular dependency
        from .rawFormatter import MegaPrimeRawFormatter
        return MegaPrimeRawFormatter
