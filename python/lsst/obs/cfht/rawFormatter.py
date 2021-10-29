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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import lsst.afw.image
import lsst.afw.fits
from lsst.obs.base import FitsRawFormatterBase
from astro_metadata_translator import MegaPrimeTranslator, fix_header
import logging

from .cfhtFilters import MEGAPRIME_FILTER_DEFINITIONS
from ._instrument import MegaPrime

__all__ = ("MegaPrimeRawFormatter",)

log = logging.getLogger(__name__)


class MegaPrimeRawFormatter(FitsRawFormatterBase):
    """Gen3 Butler formatter for MegaPrime raw data.

    MegaPrime uses multi-extension FITS files.
    """

    translatorClass = MegaPrimeTranslator
    filterDefinitions = MEGAPRIME_FILTER_DEFINITIONS

    def getDetector(self, id):
        return MegaPrime().getCamera()[id]

    def _toExtName(self, detectorId):
        """Return the extension name associated with the given detector.

        Parameters
        ----------
        detectorId : `int`
            The detector ID to search for.

        Returns
        -------
        name : `str`
            The name of the extension associated with this detector.
        """
        return f"ccd{detectorId:02d}"

    def _scanHdus(self, filename, detectorId):
        """Scan through a file for the HDU containing data from one detector.

        Parameters
        ----------
        filename : `str`
            The file to search through.
        detectorId : `int`
            The detector id to search for.

        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata: `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.

        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        fitsData = lsst.afw.fits.Fits(filename, 'r')
        # NOTE: The primary header (HDU=0) does not contain detector data.
        extname = self._toExtName(detectorId)
        for i in range(1, fitsData.countHdus()):
            fitsData.setHdu(i)
            metadata = fitsData.readMetadata()
            if metadata.get("EXTNAME") == extname:
                log.debug("Found detector %s in extension %s", detectorId, i)
                return i, metadata
        else:
            raise ValueError(f"Did not find detectorId={detectorId} in any HDU of {filename}.")

    def _determineHDU(self, detectorId):
        """Determine the correct HDU number for a given detector id.

        Parameters
        ----------
        detectorId : `int`
            The detector id to search for.

        Returns
        -------
        index : `int`
            The index of the HDU with the requested data.
        metadata : `lsst.daf.base.PropertyList`
            The metadata read from the header for that detector id.

        Raises
        ------
        ValueError
            Raised if detectorId is not found in any of the file HDUs
        """
        filename = self.fileDescriptor.location.path
        # We start by assuming that ccdN is HDU N+1
        index = detectorId + 1
        metadata = lsst.afw.fits.readMetadata(filename, index)

        # There may be two EXTNAME headers but the second one is the one
        # we want (the first indicates compression).
        if metadata.get("EXTNAME") == self._toExtName(detectorId):
            return index, metadata

        log.info("Did not find detector=%s at expected HDU=%s in %s: scanning through all HDUs.",
                 detectorId, index, filename)
        return self._scanHdus(filename, detectorId)

    def readMetadata(self):
        # Headers are duplicated so no need to merge with primary
        index, metadata = self._determineHDU(self.dataId["detector"])
        fix_header(metadata)
        return metadata

    def readImage(self):
        index, metadata = self._determineHDU(self.dataId["detector"])
        reader = lsst.afw.image.ImageFitsReader(self.fileDescriptor.location.path, hdu=index)
        return reader.read()
