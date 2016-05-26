"""!Generate camera data for CFHT MegaCam

WARNING: this code is deprecated because it generates incorrect overscan;
see DM-5524 which fixed the problem by editing the generated amp info catalogs directly.

Example:

    python bin/genCameraRepository.py megacam/Full_Megacam_geom.paf megacam/camera

If `megacam/camera` already exists the move it first, or add `--clobber`
"""
import argparse
import eups
import os
import copy
import shutil

import lsst.pex.policy as pexPolicy
import lsst.afw.table as afwTable
import lsst.afw.geom as afwGeom
from lsst.afw.cameraGeom import SCIENCE, FOCAL_PLANE, PUPIL, CameraConfig, DetectorConfig,\
                                makeCameraFromCatalogs, NullLinearityType
from lsst.obs.cfht import MegacamMapper

PIXELSIZE = 0.0135 #mm/pix
def makeCameraFromPolicy(filename, writeRepo=False, outputDir=None, doClobber=False, ccdToUse=None,
    shortNameMethod=lambda x: x):
    """
    Make a Camera from a paf file
    @param filename: name of policy file to read
    @param writeRepo: write out repository files?
    @param outputDir: output directory to write files into
    @param doClobber: clobber any files existing in the repository?
    @param ccdToUse: Type of ccd to use, otherwise use ccd specified in the paf
    @param shortNameMethod: Method to compactify ccd names into names easily used in paths
    @return Camera object
    """
    #This is all fragile as the CameraGeomDictionary.paf will go away.
    policyFile = pexPolicy.DefaultPolicyFile("afw", "CameraGeomDictionary.paf", "policy")
    defPolicy = pexPolicy.Policy.createPolicy(policyFile, policyFile.getRepositoryPath(), True)

    polFile = pexPolicy.DefaultPolicyFile("obs_cfht", filename)
    geomPolicy = pexPolicy.Policy.createPolicy(polFile)
    geomPolicy.mergeDefaults(defPolicy.getDictionary())
    ampParams = makeAmpParams(geomPolicy)
    ccdParams = makeCcdParams(geomPolicy, ampParams)
    ccdInfoDict = parseCcds(geomPolicy, ccdParams, ccdToUse)
    camConfig = parseCamera(geomPolicy)
    camConfig.detectorList = dict([(i, ccdInfo) for i, ccdInfo in enumerate(ccdInfoDict['ccdInfo'])])
    if writeRepo:
        if outputDir is None:
            raise ValueError("Need output directory for writting")
        def makeDir(dirPath, doClobber=False):
            """Make a directory; if it exists then clobber or fail, depending on doClobber

            @param[in] dirPath: path of directory to create
            @param[in] doClobber: what to do if dirPath already exists:
                if True and dirPath is a dir, then delete it and recreate it, else raise an exception
            @throw RuntimeError if dirPath exists and doClobber False
            """
            if os.path.exists(dirPath):
                if doClobber and os.path.isdir(dirPath):
                    print "Clobbering directory %r" % (dirPath,)
                    shutil.rmtree(dirPath)
                else:
                    raise RuntimeError("Directory %r exists" % (dirPath,))
            print "Creating directory %r" % (dirPath,)
            os.makedirs(dirPath)

        # write data products
        makeDir(dirPath=outputDir, doClobber=doClobber)

        camConfigPath = os.path.join(outputDir, "camera.py")
        with open(camConfigPath, 'w') as outfile:
            outfile.write(
                "#!!!!This file is auto generated.----Do not edit!!!!\n"+\
                "#!!!!Edit input file and regenerate with $OBS_CFHT_DIR/bin/genCameraRepository.py\n")
            camConfig.saveToStream(outfile)

        for detectorName, ampTable in ccdInfoDict['ampInfo'].iteritems():
            shortDetectorName = shortNameMethod(detectorName)
            ampInfoPath = os.path.join(outputDir, shortDetectorName + ".fits")
            ampTable.writeFits(ampInfoPath)

    return makeCameraFromCatalogs(camConfig, ccdInfoDict['ampInfo'])

def parseCamera(policy):
    """
    Make a CameraConfig from a policy
    @param policy: Policy object to parse
    @return CameraConfig parsed from the policy
    """
    camPolicy = policy.get('Camera')
    camConfig = CameraConfig()
    camConfig.name = camPolicy.get('name')
    # Using pixel scale 0.185 arcsec/pixel from:
    # http://arxiv.org/pdf/0908.3808v1.pdf
    camConfig.plateScale = 13.70 #arcsec/mm

    # Radial distortion correction polynomial coeff.
    conv_1 = 14805.4
    conv_2 = 13619.3
    conv_3 = 426637.0

    tConfig = afwGeom.TransformConfig()
    tConfig.transform.name = 'inverted'
    radialClass = afwGeom.xyTransformRegistry['radial']
    tConfig.transform.active.transform.retarget(radialClass)

    coeffs = [0., conv_1, conv_2, conv_3]
    tConfig.transform.active.transform.coeffs = coeffs

    tmc = afwGeom.TransformMapConfig()
    tmc.nativeSys = FOCAL_PLANE.getSysName()
    tmc.transforms = {PUPIL.getSysName():tConfig}
    camConfig.transformDict = tmc
    return camConfig

def makeAmpParams(policy):
    """
    Construct Amp level information from the Policy
    @param policy: Policy object to parse
    @return a dictionary of dictionaries of amp parameters keyed by amp type and param name
    """
    retParams = {}
    for amp in policy.getArray('Amp'):
        retParams[amp.get('ptype')] = {}
        retParams[amp.get('ptype')]['datasec'] = amp.getArray('datasec')
        retParams[amp.get('ptype')]['biassec'] = amp.getArray('biassec')
        retParams[amp.get('ptype')]['ewidth'] = amp.get('ewidth')
        retParams[amp.get('ptype')]['eheight'] = amp.get('eheight')
    return retParams

def makeCcdParams(policy, ampParms):
    """
    Construct CCD level information from the Policy
    @param policy: Policy to parse
    @param ampParms: Dictionary of dictionaries of amp parameters returned by makeAmpParams
    @return a dictionary of dictionaries of CCD parameters keyed by CCD type and param name
    """
    retParams = {}
    for ccd in policy.getArray('Ccd'):
        ptype = ccd.get('ptype')
        tdict = {}
        #The policy file has units of pixels, but to get to
        #pupil coords we need to work in units of mm
        tdict['pixelSize'] = PIXELSIZE
        tdict['offsetUnit'] = 'mm'
        tdict['ampArr'] = []
        xsize = 0
        ysize = 0
        for amp in ccd.getArray('Amp'):
            # on disk the data are all in the same orientation
            ampType = amp.get('ptype')
            parms = copy.copy(ampParms[ampType])
            xsize += parms['datasec'][2] - parms['datasec'][0] + 1
            #I think the megacam chips only have a single row of amps
            ysize = parms['datasec'][3] - parms['datasec'][1] + 1
            parms['id'] = amp.get('serial')
            parms['flipX'] = amp.get('flipLR')
            #As far as I know there is no bilateral symmetry in megacam
            parms['flipY'] = False
            tdict['ampArr'].append(parms)
        tdict['xsize'] = xsize
        tdict['ysize'] = ysize
        retParams[ptype] = tdict
    return retParams

def makeEparams(policy):
    """
    Construct electronic parameters for each amp in the mosaic.
    @param policy: Policy object to parse
    @return dictionary of arrays of dictionaries of electronic parameters keyed by CCD name and parameter name
    """
    rafts = policy.getArray('Electronic.Raft')
    if len(rafts) > 1:
        raise ValueError("These cameras should only have one raft")
    eparms = {}
    for ccd in rafts[0].getArray('Ccd'):
        eparms[ccd.get('name')] = []
        for amp in ccd.getArray('Amp'):
            eparm = {}
            eparm['index'] = amp.getArray('index')
            eparm['gain'] = amp.get('gain')
            eparm['readNoise'] = amp.get('readNoise')
            eparm['saturation'] = amp.get('saturationLevel')
            eparms[ccd.get('name')].append(eparm)
    return eparms

def addAmp(ampCatalog, amp, eparams):
    """ Add an amplifier to an AmpInfoCatalog

    @param ampCatalog: An instance of an AmpInfoCatalog object to fill with amp properties
    @param amp: Dictionary of amp geometric properties
    @param eparams: Dictionary of amp electronic properties for this amp
    """
    record = ampCatalog.addNew()

    xtot = amp['ewidth']
    ytot = amp['eheight']

    allPixels = afwGeom.Box2I(afwGeom.Point2I(0, 0), afwGeom.Extent2I(xtot, ytot))
    biassl = amp['biassec']
    biasSec = afwGeom.Box2I(afwGeom.Point2I(biassl[0], biassl[1]), afwGeom.Point2I(biassl[2], biassl[3]))
    datasl = amp['datasec']
    dataSec = afwGeom.Box2I(afwGeom.Point2I(datasl[0], datasl[1]), afwGeom.Point2I(datasl[2], datasl[3]))

    extended = dataSec.getMin().getX()
    voverscan = ytot - dataSec.getMaxY()
    pscan = dataSec.getMin().getY()

    if not voverscan:
        voscanSec = afwGeom.Box2I(afwGeom.Point2I(extended, dataSec.getMax().getY()),
                                  afwGeom.Extent2I(dataSec.getDimensions().getX(), 0))
    else:
        voscanSec = afwGeom.Box2I(afwGeom.Point2I(extended, dataSec.getMax().getY()+1),
                                  afwGeom.Extent2I(dataSec.getDimensions().getX(), voverscan))
    pscanSec = afwGeom.Box2I(afwGeom.Point2I(extended, 0),
                             afwGeom.Extent2I(dataSec.getDimensions().getX(), pscan))

    if amp['flipX']:
        #No need to flip bbox or allPixels since they
        #are at the origin and span the full pixel grid
        biasSec.flipLR(xtot)
        dataSec.flipLR(xtot)
        voscanSec.flipLR(xtot)
        pscanSec.flipLR(xtot)

    bbox = afwGeom.BoxI(afwGeom.PointI(0, 0), dataSec.getDimensions())
    bbox.shift(afwGeom.Extent2I(dataSec.getDimensions().getX()*eparams['index'][0], 0))

    shiftp = afwGeom.Extent2I(xtot*eparams['index'][0], 0)
    allPixels.shift(shiftp)
    biasSec.shift(shiftp)
    dataSec.shift(shiftp)
    voscanSec.shift(shiftp)
    pscanSec.shift(shiftp)

    record.setBBox(bbox)
    record.setRawXYOffset(afwGeom.ExtentI(0,0))
    #Set amplifier names according to the CFHT convention (A, B)
    if eparams['index'][0] == 0 and eparams['index'][1] == 0 :
        record.setName("A")
    elif eparams['index'][0] == 1 and eparams['index'][1] == 0 :
        record.setName("B")
    else :
        raise ValueError("Unexpected index parameter %i, %i"%(eparams['index'][0], eparams['index'][1]))
    record.setReadoutCorner(afwTable.LR if amp['flipX'] else afwTable.LL)
    record.setGain(eparams['gain'])
    record.setReadNoise(eparams['readNoise'])
    record.setSaturation(eparams['saturation'])
    record.setSuspectLevel(float("nan"))  # SUSPECT level unknown
    #The files do not have any linearity information
    record.setLinearityType(NullLinearityType)
    record.setLinearityCoeffs([1.,])
    record.setHasRawInfo(True)
    record.setRawFlipX(False)
    record.setRawFlipY(False)
    record.setRawBBox(allPixels)
    record.setRawDataBBox(dataSec)
    record.setRawHorizontalOverscanBBox(biasSec)
    record.setRawVerticalOverscanBBox(voscanSec)
    record.setRawPrescanBBox(pscanSec)

def parseCcds(policy, ccdParams, ccdToUse=None):
    """
    Make DetectorConfigs for each CCD in the mosaic
    @param policy: Poicy object to parse
    @param ccdParams: CCD level parameters returned by makeCcdParams
    @param ccdToUse: Type of CCD to use to construct the config, use Policy value if None
    @return a dictionary containing a list of DetectorConfigs and a dictionary of AmpInfoTable objects
    keyed on CCD name
    """
    specialChipMap = {}
    eParams = makeEparams(policy)
    ampInfoDict ={}
    ccdInfoList = []
    rafts = policy.getArray('Raft')
    if len(rafts) > 1:
        raise ValueError("Expecting only one raft")
    for ccd in rafts[0].getArray('Ccd'):
        detConfig = DetectorConfig()
        schema = afwTable.AmpInfoTable.makeMinimalSchema()
        ampCatalog = afwTable.AmpInfoCatalog(schema)
        if ccdToUse is not None:
            ccdParam = ccdParams[ccdToUse]
        else:
            ccdParam = ccdParams[ccd.get('ptype')]
        detConfig.name = ccd.get('name')
        detConfig.serial = str(ccd.get('serial'))
        detConfig.id = int(ccd.get('name')[-2:])
        offset = ccd.getArray('offset')
        if ccdParam['offsetUnit'] == 'pixels':
            offset[0] *= ccdParam['pixelSize']
            offset[1] *= ccdParam['pixelSize']
        detConfig.offset_x = offset[0]
        detConfig.offset_y = offset[1]
        if detConfig.name in specialChipMap:
            detConfig.detectorType = specialChipMap[detConfig.name]
        else:
            detConfig.detectorType = SCIENCE
        detConfig.pixelSize_x = ccdParam['pixelSize']
        detConfig.pixelSize_y = ccdParam['pixelSize']
        detConfig.refpos_x = (ccdParam['xsize'] - 1)/2.
        detConfig.refpos_y = (ccdParam['ysize'] - 1)/2.
        detConfig.bbox_x0 = 0
        detConfig.bbox_y0 = 0
        detConfig.bbox_x1 = ccdParam['xsize'] - 1
        detConfig.bbox_y1 = ccdParam['ysize'] - 1
        detConfig.rollDeg = 0.
        detConfig.pitchDeg = 0.
        detConfig.yawDeg = 90.*ccd.get('nQuarter') + ccd.getArray('orientation')[2]
        for amp in ccdParam['ampArr']:
            eparms = None
            for ep in eParams[ccd.get('name')]:
                if amp['id'] == ep['index'][0]:
                    eparms = ep
            if eparms is None:
                raise ValueError("Could not find electronic params.")
            addAmp(ampCatalog, amp, eparms)
        ampInfoDict[ccd.get('name')] = ampCatalog
        ccdInfoList.append(detConfig)
    return {"ccdInfo":ccdInfoList, "ampInfo":ampInfoDict}

if __name__ == "__main__":
    print "WARNING: this code generates incorrect vertical overscan; see DM-5524"
    baseDir = eups.productDir("obs_cfht")

    parser = argparse.ArgumentParser()
    parser.add_argument("LayoutPolicy", help="Policy file to parse for camera information")
    parser.add_argument("OutputDir", help="Location for the persisted camerea")
    parser.add_argument("--clobber", action="store_true", dest="clobber", default=False,
        help="remove and re-create the output directory if it exists")
    args = parser.parse_args()

    camera = makeCameraFromPolicy(args.LayoutPolicy, writeRepo=True, outputDir=args.OutputDir,
        ccdToUse='bottom', doClobber=args.clobber, shortNameMethod=MegacamMapper.getShortCcdName)
