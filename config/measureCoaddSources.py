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
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

"""CFHT / Megacam-specific overrides for MeasureMergedCoaddSourcesTask"""

import os.path
from lsst.utils import getPackageDir

config.measurement.load(os.path.join(getPackageDir("obs_cfht"), "config", "apertures.py"))
config.measurement.load(os.path.join(getPackageDir("obs_cfht"), "config", "kron.py"))
config.measurement.load(os.path.join(getPackageDir("obs_cfht"), "config", "convolvedFluxes.py"))
config.measurement.load(os.path.join(getPackageDir("obs_cfht"), "config", "hsm.py"))
config.load(os.path.join(getPackageDir("obs_cfht"), "config", "cmodel.py"))

config.match.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"
#config.match.refObjLoader.load(os.path.join(getPackageDir("obs_cfht"), "config", "filterMap.py"))
config.match.refObjLoader.filterMap = {
    'u': 'g',
    'g': 'g',
    'r': 'r',
    'i': 'i',
    'i2': 'i',
    'z': 'z',
    'y': 'y',
}


config.doWriteMatchesDenormalized = True

#
# This isn't good!  There appears to be no way to configure the base_PixelFlags measurement
# algorithm based on a configuration parameter; see DM-4159 for a discussion.  The name
# BRIGHT_MASK must match assembleCoaddConfig.brightObjectMaskName
#
config.measurement.plugins["base_PixelFlags"].masksFpCenter.append("BRIGHT_OBJECT")
config.measurement.plugins["base_PixelFlags"].masksFpAnywhere.append("BRIGHT_OBJECT")

config.measurement.plugins.names |= ["base_InputCount"]
