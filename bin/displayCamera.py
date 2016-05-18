#!/usr/bin/env python
import argparse
import re
import sys

import lsst.obs.cfht as obs_cfht
import lsst.afw.cameraGeom.utils as cameraGeomUtils
from lsst.afw.cameraGeom import Camera

def checkStr(strVal, level):
    """Check if a string is a valid identifier
    @param[in] strVal: String containing the identifier
    @param[in] level: level of identifier: amp, ccd, raft
    return True if valid
    """
    if level == 'amp':
        matchStr = '^ccd[0-9][0-9] [aAbB]$'
        if not re.match(matchStr, strVal):
            raise ValueError("Specify ccd name and amp name (either A or B): %s"%(strVal))
    elif level == 'ccd':
        matchStr = '^ccd[0-9][0-9]$'
        if not re.match(matchStr, strVal):
            raise ValueError("Specify the ccd name: e.g. ccd21: %s"%(strVal))
    elif level == 'raft':
        if not strVal.lower() in ('north', 'south'):
            raise ValueError("Specify the raft name as 'north' or 'south': %s"%(strVal))
    else:
        raise ValueError("level must be one of: ('amp', 'ccd', 'raft')")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Display the MegaCam camera')
    parser.add_argument('--showAmp', help='Show an amplifier segment in ds9  May have multiple arguments. '\
                                          'Format like ccd_name amp_name e.g. '\
                                          '\"ccd00 A\"', type=str, nargs='+')
    parser.add_argument('--showCcd', help='Show a CCD from the mosaic in ds9.  May have multiple arguments. '\
                                          'Format like ccd_name e.g. \"ccd16\"', type=str,
                                          nargs='+')
    parser.add_argument('--showRaft', help='Show a Raft from the mosaic in ds9.  May have multiple arguments. '\
                                           'Format like raft_name e.g. \"North\"', type=str, nargs='+')
    parser.add_argument('--showCamera', help='Show the camera mosaic in ds9.', action='store_true')
    parser.add_argument('--cameraBinSize', type= int, default=20,
                        help='Size of binning when displaying the full camera mosaic')
    parser.add_argument('--plotFocalPlane', action='store_true',
                        help='Plot the focalplane in an interactive matplotlib window')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    mapper = obs_cfht.MegacamMapper()
    camera = mapper.camera
    frame = 0
    ampMap = {'a':'0,0', 'b':'1,0'}
    if args.showAmp:
        for ampStr in args.showAmp:
            if checkStr(ampStr, 'amp'):
                ccd, amp = ampStr.split()
                detector = camera[ccd]
                amplifier = detector[ampMap[amp.lower()]]
                cameraGeomUtils.showAmp(amplifier, frame=frame)
                frame += 1

    if args.showCcd:
        for ccdStr in args.showCcd:
            if checkStr(ccdStr, 'ccd'):
                detector = camera[ccdStr]
                cameraGeomUtils.showCcd(detector, frame=frame)
                frame += 1

    raftMap = {'north':['ccd%02d'%val for val in range(18)],
               'south':['ccd%02d'%val for val in range(18, 36)]}
    if args.showRaft:
        for raftStr in args.showRaft:
            if checkStr(raftStr, 'raft'):
                detectorList = []
                for detector in camera:
                    detName = detector.getName()
                    if detName in raftMap[raftStr.lower()]:
                        detectorList.append(detector)
                tmpCamera = Camera(raftStr, detectorList, camera._transformMap)
                cameraGeomUtils.showCamera(tmpCamera, frame=frame, binSize=1)
                frame += 1

    if args.showCamera:
        cameraGeomUtils.showCamera(camera, frame=frame, binSize=args.cameraBinSize)

    if args.plotFocalPlane:
        cameraGeomUtils.plotFocalPlane(camera, 2., 2.)
