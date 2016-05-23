#!/usr/bin/env python
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
import sqlite3
import argparse
import datetime
from collections import OrderedDict

import pyfits

# The schema to use for each table: 'name':'type'
schema = OrderedDict()
schema['path'] = 'text'
schema['ccdNum'] = 'int'
schema['version'] = 'int'
schema['expTime'] = 'float'
schema['filter'] = 'text'
schema['label'] = 'text'
schema['validStart'] = 'text'
schema['validEnd'] = 'text'
schema['registered'] = 'text'
schema['extension'] = 'int'

# Key to image types
imageTypes = {2: 'dark',
              4: 'flat',
              3: 'bias',
              6: 'fringe',
#              5: 'mask',
              }

# Key to filter names
filterNames = {0: 'NONE',
               1: 'u',
               2: 'g',
               3: 'r',
               4: 'i',
               5: 'z',
               6: 'i2',
               # Ignoring narrow-bands for now
               }

def fixString(s):
    """Work around apparent pyfits bug: it's not terminating strings at the NULL"""
    c = s.find('\0')
    return s if c == -1 else s[:c]


def parseDetrendDatabase(tableName, create=False):
    if os.path.exists("calibRegistry.sqlite3") and args.create:
        os.unlink("calibRegistry.sqlite3")
        create = True
    conn = sqlite3.connect("calibRegistry.sqlite3")

    # Create tables
    if create:
        for imageType in imageTypes.values():
            createCmd = "CREATE TABLE " + imageType + " (id INTEGER PRIMARY KEY AUTOINCREMENT, " + \
                ", ".join([" ".join(kv) for kv in schema.items()]) + \
                ")"
            print createCmd
            conn.execute(createCmd)
        conn.commit()

    # Parse FITS table into sqlite
    convertUnixTime = lambda time: datetime.datetime.fromtimestamp(time).isoformat()
    fits = pyfits.open(tableName)
    table = fits[1].data
    for row in table:
        validStart = convertUnixTime(row['START_TIME'])
        validEnd = convertUnixTime(row['STOP_TIME'])
        registered = convertUnixTime(row['REG_TIME'])
        expTime = float(row['EXPTIME'])
        imageType = row['IMAGETYP']
        filtNum = row['FILTER']
        ccdNum = int(row['CCDNUM'])
        version = int(row['VERSION'])
        label = fixString(row['LABEL'])
        path = fixString(row['PATH'])

        if imageType not in imageTypes or filtNum not in filterNames:
            continue
        imageType = imageTypes[imageType]
        filterName = filterNames[filtNum]

        # Remove multiple versions, since our own software doesn't yet handle selection
        # among multiple versions
        cur = conn.cursor()
        cmd = "DELETE FROM " + imageType + \
            " WHERE FILTER = ? AND validStart = ? AND validEnd = ? AND version <= ?"
        values = [filterName, validStart, validEnd, version]
        cur.execute(cmd, values)

        for i in range(36):
            cmd = "INSERT OR IGNORE INTO " + imageType + " VALUES (NULL, " + ",".join("?" * len(schema)) + ")"
            values = [path, ccdNum, version, expTime, filterName, label, validStart, validEnd,
                      registered, i+1]
            conn.execute(cmd, values)
    fits.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse the CFHT Elixir detrend database to create " + \
                                         "a calibration registry")
    parser.add_argument("table", nargs=1, help="FITS table to parse")
    parser.add_argument("--create", action="store_true", help="Create new registry?")
    args = parser.parse_args()

    parseDetrendDatabase(args.table[0], args.create)
