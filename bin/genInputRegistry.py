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

import glob
import os
import re
import sqlite as sqlite3
import sys
import lsst.daf.base as dafBase
import lsst.afw.image as afwImage
import lsst.skypix as skypix

if os.path.exists("registry.sqlite3"):
    os.unlink("registry.sqlite3")
conn = sqlite3.connect("registry.sqlite3")

cmd = "create table raw (id integer primary key autoincrement"
cmd += ", field text, visit int, filter text, ccd int, amp int"
cmd += ", taiObs text, expTime double, unique(visit, ccd, amp))"
conn.execute(cmd)
cmd = "create table raw_skyTile (id integer, skyTile integer"
cmd += ", unique(id, skyTile), foreign key(id) references raw(id))"
conn.execute(cmd)
conn.execute("""create table raw_visit (visit int, field text, filter text,
        taiObs text, expTime double, unique(visit))""")
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

    for row in conn.execute("SELECT last_insert_rowid()"):
        id = row[0]
        break

    wcs = afwImage.makeWcs(md)
    poly = skypix.imageToPolygon(wcs, md.get("NAXIS1"), md.get("NAXIS2"),
            padRad=0.000075) # about 15 arcsec
    qsp = skypix.createQuadSpherePixelization()
    pix = qsp.intersect(poly)
    for skyTileId in pix:
        conn.execute("INSERT INTO raw_skyTile VALUES(?, ?)",
                (id, skyTileId))

conn.commit()
conn.execute("""insert into raw_visit
        select distinct visit, field, filter, taiObs, expTime from raw""")
conn.close()
