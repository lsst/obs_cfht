#!/usr/bin/env python

import os
import math

import lsst.daf.base as dafBase
import lsst.pex.logging as pexLog
import lsst.pex.exceptions as pexExceptions
import lsst.pex.config as pexConfig
import lsst.afw.geom as afwGeom
import lsst.afw.table as afwTable
import lsst.afw.image as afwImage
import lsst.meas.algorithms.utils as maUtils

import lsst.meas.astrom as measAstrom
from lsst.meas.astrom.config import MeasAstromConfig, AstrometryNetDataConfig

import lsst.afw.display.ds9 as ds9

#from .config import MeasAstromConfig, AstrometryNetDataConfig
#import sip as astromSip

import numpy as np # for isfinite()

class CfhtAstrometry(measAstrom.Astrometry) :

    def _solve(self, sources, wcs, imageSize, pixelScale, radecCenter,
               searchRadius, parity, filterName=None, xy0=None):
        solver = self._getSolver()

        x0,y0 = 0,0
        if xy0 is not None:
            x0,y0 = xy0

        # select sources with valid x,y, flux
        xybb = afwGeom.Box2D()
        # Make sure that we are not using cosmic rays as valid sources
        badStarPixelFlags = ["flags.pixel.cr.center"]
        goodsources = afwTable.SourceCatalog(sources.table)
        badkeys = [goodsources.getSchema().find(name).key for name in badStarPixelFlags]
        
        for s in sources:
            if np.isfinite(s.getX()) and np.isfinite(s.getY()) and np.isfinite(s.getPsfFlux()) and self._isGoodSource(s, badkeys) :
                goodsources.append(s)
                xybb.include(afwGeom.Point2D(s.getX() - x0, s.getY() - y0))
            
        print "*** CfhtAstrometry - Number of selected sources for astrometry : ", len(goodsources)
    
        if len(goodsources) < len(sources):
            self.log.logdebug('Keeping %i of %i sources with finite X,Y positions and PSF flux' %
                              (len(goodsources), len(sources)))
        self._debug(('Feeding sources in range x=[%.1f, %.1f], y=[%.1f, %.1f] ' +
                     '(after subtracting x0,y0 = %.1f,%.1f) to Astrometry.net') %
                    (xybb.getMinX(), xybb.getMaxX(), xybb.getMinY(), xybb.getMaxY(), x0, y0))
        # setStars sorts them by PSF flux.
        solver.setStars(goodsources, x0, y0)
        solver.setMaxStars(self.config.maxStars)
        solver.setImageSize(*imageSize)
        solver.setMatchThreshold(self.config.matchThreshold)
        raDecRadius = None
        if radecCenter is not None:
            raDecRadius = (radecCenter.getLongitude().asDegrees(),
                        radecCenter.getLatitude().asDegrees(),
                        searchRadius.asDegrees())
            solver.setRaDecRadius(*raDecRadius)
            self.log.logdebug('Searching for match around RA,Dec = (%g, %g) with radius %g deg' %
                              raDecRadius)

        if pixelScale is not None:
            dscale = self.config.pixelScaleUncertainty
            scale = pixelScale.asArcseconds()
            lo = scale / dscale
            hi = scale * dscale
            solver.setPixelScaleRange(lo, hi)
            self.log.logdebug('Searching for matches with pixel scale = %g +- %g %% -> range [%g, %g] arcsec/pix' %
                              (scale, 100.*(dscale-1.), lo, hi))

        if parity is not None:
            solver.setParity(parity)
            self.log.logdebug('Searching for match with parity = ' + str(parity))

        # Find and load index files within RA,Dec range and scale range.
        if raDecRadius is not None:
            multiInds = self._getMIndexesWithinRange(*raDecRadius)
        else:
            multiInds = self.multiInds
        qlo,qhi = solver.getQuadSizeLow(), solver.getQuadSizeHigh()
        ntotal = sum([len(mi) for mi in self.multiInds])

        toload_multiInds = set()
        toload_inds = []
        for mi in multiInds:
            for i in range(len(mi)):
                ind = mi[i]
                if not ind.overlapsScaleRange(qlo, qhi):
                    continue
                toload_multiInds.add(mi)
                toload_inds.append(ind)

        with CfhtAstrometry._LoadedMIndexes(toload_multiInds):
            solver.addIndices(toload_inds)
            self.memusage('Index files loaded: ')

            cpulimit = self.config.maxCpuTime
            solver.run(cpulimit)

            self.memusage('Solving finished: ')

        self.memusage('Index files unloaded: ')

        if solver.didSolve():
            self.log.logdebug('Solved!')
            wcs = solver.getWcs()
            self.log.logdebug('WCS: %s' % wcs.getFitsMetadata().toString())

            if x0 != 0 or y0 != 0:
                wcs.shiftReferencePixel(x0, y0)
                self.log.logdebug('After shifting reference pixel by x0,y0 = (%i,%i), WCS is: %s' %
                                  (x0, y0, wcs.getFitsMetadata().toString()))

        else:
            self.log.warn('Did not get an astrometric solution from Astrometry.net')
            wcs = None
            # Gather debugging info...

            # -are there any reference stars in the proposed search area?
            if radecCenter is not None:
                ra = radecCenter.getLongitude()
                dec = radecCenter.getLatitude()
                refs = self.getReferenceSources(ra, dec, searchRadius, filterName)
                self.log.info('Searching around RA,Dec = (%g,%g) with radius %g deg yields %i reference-catalog sources' %
                              (ra.asDegrees(), dec.asDegrees(), searchRadius.asDegrees(), len(refs)))

        qa = solver.getSolveStats()
        print qa.toString()
        self.log.logdebug('qa: %s' % qa.toString())
        return wcs, qa

        
    def _isGoodSource(self, candsource, keys):
        for k in keys:
            if candsource.get(k):
                return False
        return True
        
    def _getImageParams(self, wcs, exposure, filterName=None, imageSize=None,
                        x0=None, y0=None):
        if exposure is not None:
            ex0,ey0 = exposure.getX0(), exposure.getY0()
            if x0 is None:
                x0 = ex0
            if y0 is None:
                y0 = ey0
            self._debug('Got exposure x0,y0 = %i,%i' % (ex0,ey0))
            if filterName is None:
                filterName = exposure.getFilter().getName()
                self._debug('Setting filterName = "%s" from exposure metadata' % str(filterName))
#               Temporary fix to deal with i2 filter instead of i
                if filterName == "i2" :
                    filterName = "i"
                    print "filterName set to i, instead of i2"
            if imageSize is None:
                imageSize = (exposure.getWidth(), exposure.getHeight())
                self._debug('Setting image size = (%i, %i) from exposure metadata' % (imageSize))
        if x0 is None:
            x0 = 0
        if y0 is None:
            y0 = 0
        return filterName, imageSize, x0, y0
