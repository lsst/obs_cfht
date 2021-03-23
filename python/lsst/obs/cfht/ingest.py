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

__all__ = ["MegacamParseTask", "MegaPrimeRawIngestTask"]

import re

from lsst.daf.butler import ButlerURI, Formatter
import lsst.obs.base
from lsst.obs.base.ingest import RawFileData
from astro_metadata_translator import fix_header

from lsst.pipe.tasks.ingest import ParseTask
import lsst.pex.exceptions

filters = {'u.MP9301': 'u',
           'u.MP9302': 'u2',
           'g.MP9401': 'g',
           'g.MP9402': 'g2',
           'r.MP9601': 'r',
           'r.MP9602': 'r2',
           'i.MP9701': 'i',
           'i.MP9702': 'i2',
           'i.MP9703': 'i3',
           'z.MP9801': 'z',
           'z.MP9901': 'z2',
           }


class MegaPrimeRawIngestTask(lsst.obs.base.RawIngestTask):
    """Task for ingesting raw MegaPrime multi-extension FITS data into Gen3.
    """
    def extractMetadata(self, filename: ButlerURI) -> RawFileData:
        datasets = []

        try:
            with filename.as_local() as local_file:
                fitsData = lsst.afw.fits.Fits(local_file.ospath, "r")

                # NOTE: The primary header (HDU=0) does not contain detector
                # data.
                for i in range(1, fitsData.countHdus()):
                    fitsData.setHdu(i)
                    header = fitsData.readMetadata()
                    if not header["EXTNAME"].startswith("ccd"):
                        continue
                    fix_header(header)
                    datasets.append(self._calculate_dataset_info(header, filename))
        except Exception as e:
            self.log.debug("Problem extracting metadata from %s: %s", filename, e)
            # Indicate to the caller that we failed to read.
            # Do not try to ingest partial contents of file.
            datasets = []
            formatterClass = Formatter
            instrument = None
            self._on_metadata_failure(filename, e)
            if self.config.failFast:
                raise RuntimeError(f"Problem extracting metadata for file {filename}") from e
        else:
            # The data model currently assumes that whilst multiple datasets
            # can be associated with a single file, they must all share the
            # same formatter.
            instrument, formatterClass = self._determine_instrument_formatter(datasets[0].dataId, filename)
            if instrument is None:
                datasets = []

        self.log.info(f"Found images for {len(datasets)} detectors in {filename}")
        return RawFileData(datasets=datasets, filename=filename,
                           FormatterClass=formatterClass,
                           instrument=instrument)


class MegacamParseTask(ParseTask):

    def translate_ccd(self, md):
        try:
            extname = self.getExtensionName(md)
            return int(extname[3:])  # chop off "ccd"
        except LookupError:
            # Dummy value, intended for PHU (need something to get filename)
            return 99

    def translate_filter(self, md):
        filtName = md.getScalar("FILTER").strip()
        if filtName not in filters:
            return "UNKNOWN"
        return filters[filtName]

    def translate_taiObs(self, md):
        # Field name is "taiObs" but we're giving it UTC; shouldn't matter so
        # long as we're consistent
        (yr, month, day) = (md.getScalar("DATE-OBS").strip()).split("-")
        (hr, min, sec) = (md.getScalar("UTC-OBS").strip()).split(":")
        (sec1, sec2) = sec.split('.')
        return "%04d-%02d-%02dT%02d:%02d:%02d.%02d"%(int(yr), int(month), int(day),
                                                     int(hr), int(min), int(sec1), int(sec2))

    def translate_defects(self, md):
        maskName = md.getScalar("IMRED_MK").strip()
        maskName, ccd = maskName.split(".fits")
        filter = md.getScalar("FILTER").strip().split('.')[0]
        if filter in ["i", "i2", "i3", "z", "z2"]:
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

    def getExtensionName(self, md):
        """Get the name of an extension.

        Parameters
        ----------
        md : `PropertySet`
            Metadata to get the name from.

        Returns
        -------
        name : `str` or None
            Name of the extension if it exists.  None otherwise.
        """
        # We have to overwrite this method because some (mostly recent) Megacam
        # images have a different header where the keword "EXTNAME" appears one
        # time instead of two. In the later case ext is a tuple while in the
        # other case it is a single value
        try:
            # This returns a tuple
            ext = md.getScalar("EXTNAME")
            # Most of the time the EXTNAME keyword appears 2 times in the
            # header (1st time to specify that the image is compressed) but
            # sometimes it appears only once even if the image is compressed
            if type(ext) == tuple or type(ext) == list:
                return ext[1]
            else:
                return ext
        except lsst.pex.exceptions.Exception:
            return None
