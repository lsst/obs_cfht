import glob
import os
import re
import sqlite3
import sys
import lsst.daf.base as dafBase
import lsst.afw.image as afwImage

if os.path.exists("registry.sqlite3"):
    os.unlink("registry.sqlite3")
conn = sqlite3.connect("registry.sqlite3")

cmd = "create table raw (id integer primary key autoincrement"
cmd += ", field text, visit int, filter text, ccd int, amp int"
cmd += ", taiObs text, expTime double)"
conn.execute(cmd)
conn.commit()

root = sys.argv[1]
for fits in glob.glob(os.path.join(root,
    "[DW][0-4]", "raw", "v*-f*", "s00", "c*-a[01].fits*")):
    print fits
    m = re.search(r'([DW][0-4])/raw/v(\d+)-f(\w)/s00/c(\d+)-a([01])\.fits',
            fits)
    if not m:
        print >>sys.stderr, "Warning: Unrecognized file:", fits
        continue

    field, visit, filter, ccd, amp = m.groups()

    md = afwImage.readMetadata(fits)
    expTime = md.get("EXPTIME")
    mjdObs = md.get("MJD-OBS")
    taiObs = dafBase.DateTime(mjdObs, dafBase.DateTime.MJD,
            dafBase.DateTime.UTC).toString()[:-1]
    conn.execute("INSERT INTO raw VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
        (field, visit, filter, ccd, amp, taiObs, expTime))

conn.commit()
conn.close()
