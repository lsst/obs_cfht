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

import re

from lsst.pipe.tasks.ingest import ParseTask

filters = {'u.MP9301': 'u',
           'g.MP9401': 'g',
           'r.MP9601': 'r',
           'i.MP9701': 'i',
           'i.MP9702': 'i2',
           'z.MP9801': 'z',
           }

class MegacamParseTask(ParseTask):
    def translate_ccd(self, md):
        try:
            extname = self.getExtensionName(md)
            return int(extname[3:]) # chop off "ccd"
        except:
            # Dummy value, intended for PHU (need something to get filename)
            return 99

    def translate_filter(self, md):
        filtName = md.get("FILTER").strip()
        if filtName not in filters:
            return "UNKNOWN"
        return filters[filtName]

    def translate_taiObs(self, md):
        # Field name is "taiObs" but we're giving it UTC; shouldn't matter so long as we're consistent
        (yr, month, day) = (md.get("DATE-OBS").strip()).split("-")
        (hr, min, sec) = (md.get("UTC-OBS").strip()).split(":")
        (sec1, sec2) = sec.split('.')
        return "%04d-%02d-%02dT%02d:%02d:%02d.%02d"%(int(yr), int(month), int(day),
                                                     int(hr), int(min), int(sec1), int(sec2))
    def translate_defects(self, md):
        maskName = md.get("IMRED_MK").strip()
        maskName, ccd = maskName.split(".fits")
        filter = md.get("FILTER").strip().split('.')[0]
        if filter == "i" or filter == "i2" or filter == "z" :
            maskName = maskName+"_enlarged"
        maskFile = maskName+".nn/"+ccd[1:6]+".fits"
        return maskFile
        
    def getInfo(self, filename):
        phuInfo, infoList = super(MegacamParseTask, self).getInfo(filename)
        match = re.search(r"\d+(?P<state>o|p)\.fits.*", filename)
        if not match:
            raise RuntimeError("Unable to parse filename: %s" % filename)
        phuInfo['state'] = match.group('state')
        phuInfo['extension'] = 0
        for num, info in enumerate(infoList):
            info['state'] = match.group('state')
            info['extension'] = num + 1
        return phuInfo, infoList
