#
# LSST Data Management System
# Copyright 2016 LSST Corporation.
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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from lsst.afw.coord import Coord, IcrsCoord, Observatory, Weather
from lsst.daf.butlerUtils import MakeRawVisitInfo

__all__ = ["MakeMegacamRawVisitInfo"]


class MakeMegacamRawVisitInfo(MakeRawVisitInfo):

    """Make a VisitInfo from the FITS header of a raw Megacam image
    """

    def setArgDict(self, md, argDict):
        """Set an argument dict for makeVisitInfo and pop associated metadata

        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet
        @param[in,out] argdict  a dict of arguments
        """
        MakeRawVisitInfo.setArgDict(self, md, argDict)
        argDict["darkTime"] = self.popFloat(md, "DARKTIME")
        argDict["boresightAzAlt"] = Coord(
            self.popAngle(md, "TELAZ"),
            self.popAngle(md, "TELALT"),
        )
        argDict["boresightRaDec"] = IcrsCoord(
            self.popAngle(md, "RA_DEG",),
            self.popAngle(md, "DEC_DEG"),
        )
        argDict["boresightAirmass"] = self.popFloat(md, "AIRMASS")
        argDict["observatory"] = Observatory(
            self.popAngle(md, "LONGITUD"),
            self.popAngle(md, "LATITUDE"),
            4204,  # from Wikipedia
        )
        argDict["weather"] = Weather(
            self.popFloat(md, "TEMPERAT"),
            self.popFloat(md, "PRESSURE")*100.0,  # 100 Pascal per millibar
            self.popFloat(md, "RELHUMID"),
        )

    def getDateAvg(self, md, exposureTime):
        """Return date at the middle of the exposure

        @param[in,out] md  FITS metadata; changed in place
        @param[in] exposureTime  exposure time in sec
        """
        dateObs = self.popMjdDate(md, "MJD-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)
