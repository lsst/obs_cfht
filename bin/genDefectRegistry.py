import os
import re
import sqlite3
import sys

if os.path.exists("defectRegistry.sqlite3"):
    os.unlink("defectRegistry.sqlite3")
conn = sqlite3.connect("defectRegistry.sqlite3")

cmd = "create table defect (id integer primary key autoincrement"
cmd += ", path text, version int"
cmd += ", validStart text, validEnd text)"
conn.execute(cmd)
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

    cmd = "INSERT INTO defect VALUES (NULL, ?, ?, ?, ?)"
    pathwords = path.split(".")
    if pathwords[0] == "static":
        path = ".".join(pathwords[:5]) + ".paf"
    else:
        path = ".".join(pathwords[:5]) + ".n.paf"
    conn.execute(cmd, (path, version, start, stop))
    conn.commit()

conn.close()
