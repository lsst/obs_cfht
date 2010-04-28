import os
import re
import sqlite3
from lsst.daf.persistence import Mapper, ButlerLocation, LogicalLocation
import lsst.daf.butlerUtils as butlerUtils
import lsst.afw.image as afwImage
import lsst.afw.cameraGeom as afwCameraGeom
import lsst.afw.cameraGeom.utils as cameraGeomUtils
import lsst.afw.image.utils as imageUtils
import lsst.pex.policy as pexPolicy

class CfhtMapper(Mapper):
    def __init__(self, policy=None, root=".", registry=None, calibRoot=None):
        Mapper.__init__(self)

        self.policy = policy
        if self.policy is None:
            self.policy = pexPolicy.Policy()
        defaultFile = pexPolicy.DefaultPolicyFile("obs_cfht",
                "CfhtMapperDictionary.paf", "policy")
        defaultPolicy = pexPolicy.Policy.createPolicy(defaultFile,
                defaultFile.getRepositoryPath())
        self.policy.mergeDefaults(defaultPolicy)

        self.root = root
        if self.policy.exists('root'):
            self.root = self.policy.getString('root')
        self.calibRoot = calibRoot
        if self.policy.exists('calibRoot'):
            self.calibRoot = self.policy.getString('calibRoot')
        if self.calibRoot is None:
            self.calibRoot = self.root

        # Do any location map substitutions
        self.root = LogicalLocation(self.root).locString()
        self.calibRoot = LogicalLocation(self.calibRoot).locString()

        registryPath = registry
        if registryPath is None and self.policy.exists('registryPath'):
            registryPath = self.policy.getString('registryPath')
            if not os.path.exists(registryPath):
                registryPath = None
        if registryPath is None:
            registryPath = os.path.join(self.root, "registry.sqlite3")
            if not os.path.exists(registryPath):
                registryPath = None
        if registryPath is None:
            registryPath = "registry.sqlite3"
            if not os.path.exists(registryPath):
                registryPath = None
        if registryPath is not None:
            self.registry = butlerUtils.Registry.create(registryPath)

        # self.keys = self.registry.getFields()
        self.keys = ["field", "visit", "ccd", "amp", "filter"]

        self.filterMap = {
            "u.MP9301": "u",
            "g.MP9401": "g",
            "r.MP9601": "r",
            "i.MP9701": "i",
            "i.MP9702": "i2",
            "z.MP9801": "z"
         }

        calibRegistryPath = None
        if self.policy.exists('calibRegistryPath'):
            calibRegistryPath = self.policy.getString('calibRegistryPath')
            if not os.path.exists(calibRegistryPath):
                calibRegistryPath = None
        if calibRegistryPath is None:
            calibRegistryPath = os.path.join(self.calibRoot,
                    "calibRegistry.sqlite3")
            if not os.path.exists(calibRegistryPath):
                calibRegistryPath = None
        if calibRegistryPath is None:
            calibRegistryPath = "calibRegistry.sqlite3"
            if not os.path.exists(calibRegistryPath):
                calibRegistryPath = None
        if calibRegistryPath is not None:
            self.calibRegistry = butlerUtils.Registry.create(calibRegistryPath)
            # for k in self.calibRegistry.getFields():
            #     if k not in self.keys:
            #         self.keys.append(k)
        self.keys.append(["filter", "expTime"])

        for datasetType in ["raw", "bias", "flat", "fringe",
            "postISR", "postISRCCD", "visitim", "psf", "calexp", "src", "obj"]:
            # dark
            key = datasetType + "Template"
            if self.policy.exists(key):
                setattr(self, key, self.policy.getString(key))

        self.cameraPolicyLocation = os.path.join(
                defaultFile.getRepositoryPath(),
                self.policy.getString('cameraDescription'))
        cameraPolicy = cameraGeomUtils.getGeomPolicy(self.cameraPolicyLocation)
        self.camera = cameraGeomUtils.makeCamera(cameraPolicy)

        filterPolicy = pexPolicy.Policy.createPolicy(
                os.path.join(defaultFile.getRepositoryPath(),
                    self.policy.getString('filterDescription')))
        imageUtils.defineFiltersFromPolicy(filterPolicy, reset=True)


    def getKeys(self):
        return self.keys

###############################################################################
#
# Utility functions
#
###############################################################################

    def _needField(self, dataId):
        if dataId.has_key('field'):
            return dataId
        actualId = dict(dataId)
        rows = self.registry.executeQuery(("field",), ("raw",),
                {'visit': "?"}, None, (dataId['visit'],))
        assert len(rows) == 1
        actualId['field'] = str(rows[0][0])
        return actualId

    def _needFilter(self, dataId):
        if dataId.has_key('filter'):
            return dataId
        actualId = dict(dataId)
        rows = self.registry.executeQuery(("filter",), ("raw",),
                {'visit': "?"}, None, (dataId['visit'],))
        assert len(rows) == 1
        actualId['filter'] = str(rows[0][0])
        return actualId

    def _mapActualToPath(self, actualId):
        pathId = dict(actualId)
        return pathId

    def _extractDetectorName(self, dataId):
        return "CFHT %(ccd)d" % dataId

    def _extractAmpId(self, dataId):
        return (self._extractDetectorName(dataId),
                int(dataId['amp']), 0)

    def _setAmpDetector(self, item, dataId):
        ampId = self._extractAmpId(dataId)
        detector = cameraGeomUtils.findAmp(
                self.camera, afwCameraGeom.Id(ampId[0]), ampId[1], ampId[2])
        item.setDetector(detector)

    def _setCcdDetector(self, item, dataId):
        ccdId = self._extractDetectorName(dataId)
        detector = cameraGeomUtils.findCcd(
                self.camera, afwCameraGeom.Id(ccdId))
        item.setDetector(detector)

    def _setFilter(self, item, dataId):
        md = item.getMetadata()
        filterName = None
        if md.exists("FILTER"):
            filterName = item.getMetadata().get("FILTER").strip()
            if self.filterMap.has_key(filterName):
                filterName = self.filterMap[filterName]
        if filterName is None:
            rows = self.registry.executeQuery(("filter",), ("raw",),
                    {'visit': "?"}, None, (dataId['visit'],))
            assert len(rows) == 1
            filterName = str(rows[0][0])
        filter = afwImage.Filter(filterName)
        item.setFilter(filter)

    def _setWcs(self, item):
        md = item.getMetadata()
        item.setWcs(afwImage.makeWcs(md))
        wcsMetadata = exposure.getWcs().getFitsMetadata()
        for kw in wcsMetadata.paramNames():
            md.remove(kw)

    def _standardizeExposure(self, item, dataId, isAmp=False):
        stripFits(item.getMetadata())
        if isAmp:
            self._setAmpDetector(item, dataId)
        else:
            self._setCcdDetector(item, dataId)
        self._setFilter(item, dataId)
        return item

    def _standardizeCalib(self, item, dataId, filterNeeded):
        stripFits(item.getMetadata())
        self._setAmpDetector(item, dataId)
        if filterNeeded:
            self._setFilter(item, dataId)
        return item

    def _calibLookup(self, datasetType, dataId):
        result = dict(dataId)
        rows = self.registry.executeQuery(("taiObs","filter"), ("raw",),
                {"visit": "?"}, None, (dataId['visit'],))
        assert len(rows) == 1
        taiObs, filter = rows[0]

        if datasetType in ("flat", "fringe"):
            rows = self.calibRegistry.executeQuery(("derivedRunId",),
                    (datasetType,), {"filter": "?"},
                    ("DATE(?)", "DATE(validStart)", "DATE(validEnd)"),
                    (filter, taiObs))
        else:
            rows = self.calibRegistry.executeQuery(("derivedRunId",),
                    (datasetType,), None,
                    ("DATE(?)", "DATE(validStart)", "DATE(validEnd)"),
                    (taiObs,))
        if len(rows) == 0:
            result['run'] = "***NONEXISTENT***"
        else:
            assert len(rows) == 1
            result['run'] = str(rows[0][0])
        return result

###############################################################################

    def map_camera(self, dataId):
        return ButlerLocation(
                "lsst.afw.cameraGeom.Camera", "Camera",
                "PafStorage", self.cameraPolicyLocation, dataId)

    def std_camera(self, item, dataId):
        pol = cameraGeomUtils.getGeomPolicy(item)
        return cameraGeomUtils.makeCamera(pol)

###############################################################################

    def map_raw(self, dataId):
        pathId = self._needField(self._needFilter(dataId))
        path = os.path.join(self.root, self.rawTemplate % pathId)
        return ButlerLocation(
                "lsst.afw.image.DecoratedImageU", "DecoratedImageU",
                "FitsStorage", path, dataId)

    def query_raw(self, key, format, dataId):

        return self.registry.getCollection(key, format, dataId)

    def std_raw(self, item, dataId):
        exposure = afwImage.makeExposure(
                afwImage.makeMaskedImage(item.getImage()))
        md = item.getMetadata()
        exposure.setMetadata(md)
        exposure.setWcs(afwImage.makeWcs(md))
        wcsMetadata = exposure.getWcs().getFitsMetadata()
        for kw in wcsMetadata.paramNames():
            md.remove(kw)
        return self._standardizeExposure(exposure, dataId, True)

###############################################################################

    def map_bias(self, dataId):
        dataId = self._calibLookup("bias", dataId)
        path = os.path.join(self.calibRoot, self.biasTemplate % dataId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def query_bias(self, key, format, dataId):
        return self.calibRegistry.queryMetadata("bias", key, format, dataId)

    def std_bias(self, item, dataId):
        return self._standardizeCalib(item, dataId, False)

###############################################################################

#     def map_dark(self, dataId):
#         dataId = self._calibLookup("dark", dataId)
#         pathId = self._mapActualToPath(self._mapIdToActual(dataId))
#         path = os.path.join(self.calibRoot, self.darkTemplate % pathId)
#         return ButlerLocation(
#                 "lsst.afw.image.ExposureF", "ExposureF",
#                 "FitsStorage", path, dataId)
# 
#     def query_dark(self, key, format, dataId):
#         return self.calibRegistry.queryMetadata("dark", key, format, dataId)
# 
#     def std_dark(self, item, dataId):
#         return self._standardizeCalib(item, dataId, False)

###############################################################################

    def map_flat(self, dataId):
        dataId = self._needFilter(dataId)
        dataId = self._calibLookup("flat", dataId)
        path = os.path.join(self.calibRoot, self.flatTemplate % dataId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def query_flat(self, key, format, dataId):
        return self.calibRegistry.queryMetadata("flat", key, format, dataId)

    def std_flat(self, item, dataId):
        return self._standardizeCalib(item, dataId, True)

###############################################################################

    def map_fringe(self, dataId):
        dataId = self._needFilter(dataId)
        dataId = self._calibLookup("fringe", dataId)
        path = os.path.join(self.calibRoot, self.fringeTemplate % dataId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def query_fringe(self, key, format, dataId):
        return self.calibRegistry.queryMetadata("fringe", key, format, dataId)

    def std_fringe(self, item, dataId):
        return self._standardizeCalib(item, dataId, True)

###############################################################################

    def map_postISR(self, dataId):
        pathId = self._needFilter(dataId)
        path = os.path.join(self.root, self.postISRTemplate % pathId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def std_postISR(self, item, dataId):
        return self._standardizeExposure(item, dataId, True)

###############################################################################

    def map_postISRCCD(self, dataId):
        pathId = self._needFilter(dataId)
        path = os.path.join(self.root, self.postISRCCDTemplate % pathId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def std_postISRCCD(self, item, dataId):
        return self._standardizeExposure(item, dataId)

###############################################################################

    def map_visitim(self, dataId):
        pathId = self._needFilter(dataId)
        path = os.path.join(self.root, self.visitimTemplate % pathId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def std_visitim(self, item, dataId):
        return self._standardizeExposure(item, dataId)

###############################################################################

    def map_psf(self, dataId):
        pathId = self._needFilter(dataId)
        path = os.path.join(self.root, self.psfTemplate % pathId)
        return ButlerLocation(
                "lsst.meas.algorithms.PSF", "PSF",
                "BoostStorage", path, dataId)

###############################################################################

    def map_calexp(self, dataId):
        pathId = self._needFilter(dataId)
        path = os.path.join(self.root, self.calexpTemplate % pathId)
        return ButlerLocation(
                "lsst.afw.image.ExposureF", "ExposureF",
                "FitsStorage", path, dataId)

    def std_calexp(self, item, dataId):
        return self._standardizeExposure(item, dataId)

###############################################################################

def stripFits(propertySet):
    for kw in ("SIMPLE", "BITPIX", "EXTEND", "NAXIS", "NAXIS1", "NAXIS2",
            "BSCALE", "BZERO"):
        if propertySet.exists(kw):
            propertySet.remove(kw)
