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
import sqlite as sqlite3
import sys

if os.path.exists("calibRegistry.sqlite3"):
    os.unlink("calibRegistry.sqlite3")
conn = sqlite3.connect("calibRegistry.sqlite3")

cmd = "create table %s (id integer primary key autoincrement"
cmd += ", path text, derivedRunId text, runId text, version int"
cmd += ", validStart text, validEnd text"

for t in ("bias", "dark", "flat", "fringe"):
    createCmd = cmd % (t,)
    if t == "dark":
        createCmd += ", expTime int"
    elif t in ("flat", "fringe"):
        createCmd += ", filter text"
    conn.execute(createCmd + ")")

conn.commit()

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

f = file(sys.argv[1])
for line in f:
    if line.startswith('#'):
        continue
    words = line.split()
    if len(words) == 0:
        continue
    elif len(words) != 9:
        print "Warning: Unrecognized line:"
        print line
        continue
    path, usedDC3a, runId, start, stop, filter, detrend, version, ccds = \
            line.split()

    if detrend == "mask":
        continue
    assert detrend in ("bias", "dark", "flat", "fringe")

    y, m, d = start.split("-")
    m = months.index(m) + 1
    start = "%s-%02d-%s" % (y, m, d)

    y, m, d = stop.split("-")
    m = months.index(m) + 1
    stop = "%s-%02d-%s" % (y, m, d)

    cmd = "INSERT INTO %s VALUES (NULL, ?, ?, ?, ?, ?, ?" % (detrend,)
    if detrend in ("dark", "flat", "fringe"):
        cmd += ", ?)"
    else:
        cmd += ")"

    if detrend == "dark":
        expTime = path.split(".")[2]

    derivedRunId = path.split(".")[0]

    values = [path, derivedRunId, runId, version, start, stop]
    if detrend == "dark":
        values.append(expTime)
    elif detrend in ("flat", "fringe"):
        values.append(filter)
    conn.execute(cmd, values)

    # print line
    conn.commit()

conn.close()
