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

import glob
import os
import re
import sqlite3
import sys

if os.path.exists("defectRegistry.sqlite3"):
    os.unlink("defectRegistry.sqlite3")
conn = sqlite3.connect("defectRegistry.sqlite3")

cmd = "create table defect (id integer primary key autoincrement"
cmd += ", maskname text, path text, version int, ccdSerial int"
cmd += ", validStart text, validEnd text)"
conn.execute(cmd)
conn.commit()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

f = file(sys.argv[1])
root = sys.argv[2]
for line in f:
    if line.startswith('#'):
        continue
    words = line.split()
    if len(words) == 0:
        continue
    elif len(words) != 8:
        print "Warning: Unrecognized line:"
        print line
        continue
    path, runId, start, stop, filter, detrend, version, ccds = \
            line.split()

    if detrend != "mask":
        continue

    y, m, d = start.split("-")
    m = months.index(m) + 1
    start = "%s-%02d-%s" % (y, m, d)

    y, m, d = stop.split("-")
    m = months.index(m) + 1
    stop = "%s-%02d-%s" % (y, m, d)

    cmd = "INSERT INTO defect VALUES (NULL, ?, ?, ?, ?, ?, ?)"
    pathwords = path.split(".")
    if pathwords[0] == "static":
        path = ".".join(pathwords[:5])
    else:
        path = ".".join(pathwords[:5]) + ".n"

    for f in glob.glob(os.path.join(root, path, "defects*.fits")):
        m = re.search(r'defects(\d+)\.fits', f)
        if not m:
            print >>sys.stderr, "Unrecognized file: %s" % (f,)
            continue
        print f
        conn.execute(cmd, (".".join(pathwords[:5]), f, version, int(m.group(1)), start, stop))

    conn.commit()

conn.close()
