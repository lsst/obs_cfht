#!/usr/bin/env python

import numpy
#from lsst.pex.exceptions import LsstCppException, LengthError
import lsst.pex.config as pexConfig
import lsst.daf.base as dafBase
import lsst.pipe.base as pipeBase
import lsst.meas.astrom as measAstrom
import lsst.pipe.tasks.astrometry as ptAstrometry
from lsst.meas.astrom.sip import makeCreateWcsWithSip

from lsst.obs.cfht.cfhtastrom import CfhtAstrometry

class CfhtAstrometryTask(ptAstrometry.AstrometryTask):

    @pipeBase.timeMethod
    def astrometry(self, exposure, sources, bbox=None):
        """Solve astrometry to produce WCS

        @param exposure Exposure to process
        @param sources Sources
        @param bbox Bounding box, or None to use exposure
        @return Struct(matches: star matches, matchMeta: match metadata)
        """
        if not self.config.forceKnownWcs:
            self.log.info("Solving astrometry")

        if bbox is None:
            bbox = exposure.getBBox(afwImage.PARENT)

        if not self.astrometer:
            self.astrometer = CfhtAstrometry(self.config.solver, log=self.log)

        kwargs = dict(x0=bbox.getMinX(), y0=bbox.getMinY(), imageSize=bbox.getDimensions())

        if self.config.forceKnownWcs:
            self.log.info("Forcing the input exposure's WCS")
            if self.config.solver.calculateSip:
                self.log.warn("'forceKnownWcs' and 'solver.calculateSip' options are both set." +
                              " Will try to compute a TAN-SIP WCS starting from the input WCS.")
            astrom = self.astrometer.useKnownWcs(sources, exposure=exposure, **kwargs)
        else:
            astrom = self.astrometer.determineWcs(sources, exposure, **kwargs)

        if astrom is None or astrom.getWcs() is None:
            raise RuntimeError("Unable to solve astrometry")

        matches = astrom.getMatches()
        matchMeta = astrom.getMatchMetadata()
        if matches is None or len(matches) == 0:
            raise RuntimeError("No astrometric matches")
        self.log.info("%d astrometric matches" %  (len(matches)))

        if not self.config.forceKnownWcs:
            # Note that this is the Wcs for the provided positions, which may be distorted
            exposure.setWcs(astrom.getWcs())

        self.display('astrometry', exposure=exposure, sources=sources, matches=matches)

        return pipeBase.Struct(matches=matches, matchMeta=matchMeta)
