#!/usr/bin/env python

# This file is part of obs_cfht.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import re
import sys

import lsst.afw.cameraGeom.utils as cameraGeomUtils
import lsst.afw.display as afwDisplay
from lsst.obs.cfht import MegaPrime


def checkStr(strVal, level):
    """Check if a string is a valid identifier

    Parameters
    ----------
    strVal : `str`
       String containing the identifier.
    level : `str`
       Level of the identifier: "amp", "ccd", or "raft".

    Returns
    -------
    result : `bool`
       `True` if valid.

    Raises
    ------
    ValueError
       Raised if an unknown ``level`` is provided or an unknown ``strVal`` is
       given for the given ``level``.
    """
    if level == 'amp':
        matchStr = '^ccd[0-9][0-9] [aAbB]$'
        if not re.match(matchStr, strVal):
            raise ValueError(("Specify both ccd name (e.g. ccd21) and amp name (either A or B) "
                              "surrounded by quotes, e.g \"ccd21 A\": %s"%(strVal)))
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
    parser.add_argument('--showAmp', help='Display an amplifier segment.  May have multiple arguments. '
                                          'Format like \"ccd_name amp_name\" e.g. '
                                          '\"ccd00 A\"', type=str, nargs='+')
    parser.add_argument('--showCcd', help='Display a CCD from the mosaic.  May have multiple arguments. '
                                          'Format like ccd_name e.g. \"ccd16\"', type=str,
                                          nargs='+')
    parser.add_argument('--showRaft',
                        help='Display a Raft from the mosaic.  May have multiple arguments. '
                             'Format like raft_name e.g. \"North\"', type=str, nargs='+')
    parser.add_argument('--showCamera', help='Display the camera mosaic.', action='store_true')
    parser.add_argument('--cameraBinSize', type=int, default=20,
                        help='Size of binning when displaying the full camera mosaic')
    parser.add_argument('--plotFocalPlane', action='store_true',
                        help='Plot the focalplane in an interactive matplotlib window')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    instrument = MegaPrime()
    camera = instrument.getCamera()
    frame = 0
    disp = afwDisplay.Display(frame=frame)
    if args.showAmp:
        for ampStr in args.showAmp:
            if checkStr(ampStr, 'amp'):
                ccd, amp = ampStr.split()
                detector = camera[ccd]
                amplifier = detector[amp]
                cameraGeomUtils.showAmp(amplifier, display=disp)
                frame += 1
                disp = afwDisplay.Display(frame=frame)

    if args.showCcd:
        for ccdStr in args.showCcd:
            if checkStr(ccdStr, 'ccd'):
                detector = camera[ccdStr]
                cameraGeomUtils.showCcd(detector, display=disp)
                frame += 1
                disp = afwDisplay.Display(frame=frame)

    raftMap = {'north': ['ccd%02d'%val for val in range(18)],
               'south': ['ccd%02d'%val for val in range(18, 36)]}
    if args.showRaft:
        for raftStr in args.showRaft:
            if checkStr(raftStr, 'raft'):
                detectorNameList = []
                for detector in camera:
                    detName = detector.getName()
                    if detName in raftMap[raftStr.lower()]:
                        detectorNameList.append(detName)
                cameraGeomUtils.showCamera(camera, detectorNameList=detectorNameList, display=disp, binSize=4)
                frame += 1
                disp = afwDisplay.Display(frame=frame)

    if args.showCamera:
        cameraGeomUtils.showCamera(camera, display=disp, binSize=args.cameraBinSize)

    if args.plotFocalPlane:
        cameraGeomUtils.plotFocalPlane(camera, 2., 2.)
