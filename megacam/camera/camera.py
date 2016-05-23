#!!!!This file is auto generated.----Do not edit!!!!
#!!!!Edit input file and regenerate with $OBS_CFHT_DIR/bin/genCameraRepository.py
import lsst.afw.cameraGeom.cameraConfig
assert type(config)==lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (type(config).__module__, type(config).__name__)
# Plate scale of the camera in arcsec/mm
config.plateScale=13.7

# Name of native coordinate system
config.transformDict.nativeSys='FocalPlane'

config.transformDict.transforms={}
config.transformDict.transforms['Pupil']=lsst.afw.geom.transformConfig.TransformConfig()
config.transformDict.transforms['Pupil'].transform['multi'].transformDict=None
# x, y translation vector
config.transformDict.transforms['Pupil'].transform['affine'].translation=[0.0, 0.0]

# 2x2 linear matrix in the usual numpy order;
#             to rotate a vector by theta use: cos(theta), sin(theta), -sin(theta), cos(theta)
config.transformDict.transforms['Pupil'].transform['affine'].linear=[1.0, 0.0, 0.0, 1.0]

# Coefficients for the radial polynomial; coeff[0] must be 0
config.transformDict.transforms['Pupil'].transform['radial'].coeffs=None

import lsst.afw.geom.xyTransformFactory
config.transformDict.transforms['Pupil'].transform['inverted'].transform.retarget(target=lsst.afw.geom.xyTransformFactory.makeRadialXYTransform, ConfigClass=lsst.afw.geom.xyTransformFactory.RadialXYTransformConfig)
# Coefficients for the radial polynomial; coeff[0] must be 0
config.transformDict.transforms['Pupil'].transform['inverted'].transform.coeffs=[0.0, 14805.4, 13619.3, 426637.0]

config.transformDict.transforms['Pupil'].transform.name='inverted'
config.detectorList={}
config.detectorList[0]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[0].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[0].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[0].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[0].bbox_x0=0

# Name of detector slot
config.detectorList[0].name='ccd00'

# Pixel size in the x dimension in mm
config.detectorList[0].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[0].transformDict.nativeSys=None

config.detectorList[0].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[0].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[0].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[0].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_x=-114.399

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[0].offset_y=99.46125

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[0].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[0].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[0].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[0].serial='834175'

# pitch (rotation about y) of the detector in degrees
config.detectorList[0].pitchDeg=0.0

# ID of detector slot
config.detectorList[0].id=0

config.detectorList[1]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[1].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[1].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[1].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[1].bbox_x0=0

# Name of detector slot
config.detectorList[1].name='ccd01'

# Pixel size in the x dimension in mm
config.detectorList[1].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[1].transformDict.nativeSys=None

config.detectorList[1].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[1].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[1].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[1].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_x=-85.806

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[1].offset_y=99.47475

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[1].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[1].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[1].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[1].serial='835234'

# pitch (rotation about y) of the detector in degrees
config.detectorList[1].pitchDeg=0.0

# ID of detector slot
config.detectorList[1].id=1

config.detectorList[2]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[2].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[2].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[2].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[2].bbox_x0=0

# Name of detector slot
config.detectorList[2].name='ccd02'

# Pixel size in the x dimension in mm
config.detectorList[2].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[2].transformDict.nativeSys=None

config.detectorList[2].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[2].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[2].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[2].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_x=-57.24

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[2].offset_y=99.48825

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[2].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[2].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[2].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[2].serial='8352153'

# pitch (rotation about y) of the detector in degrees
config.detectorList[2].pitchDeg=0.0

# ID of detector slot
config.detectorList[2].id=2

config.detectorList[3]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[3].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[3].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[3].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[3].bbox_x0=0

# Name of detector slot
config.detectorList[3].name='ccd03'

# Pixel size in the x dimension in mm
config.detectorList[3].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[3].transformDict.nativeSys=None

config.detectorList[3].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[3].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[3].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[3].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_x=-28.6875

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[3].offset_y=99.50175

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[3].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[3].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[3].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[3].serial='8261144'

# pitch (rotation about y) of the detector in degrees
config.detectorList[3].pitchDeg=0.0

# ID of detector slot
config.detectorList[3].id=3

config.detectorList[4]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[4].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[4].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[4].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[4].bbox_x0=0

# Name of detector slot
config.detectorList[4].name='ccd04'

# Pixel size in the x dimension in mm
config.detectorList[4].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[4].transformDict.nativeSys=None

config.detectorList[4].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[4].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[4].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[4].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_x=-0.054

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[4].offset_y=99.50175

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[4].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[4].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[4].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[4].serial='8341174'

# pitch (rotation about y) of the detector in degrees
config.detectorList[4].pitchDeg=0.0

# ID of detector slot
config.detectorList[4].id=4

config.detectorList[5]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[5].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[5].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[5].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[5].bbox_x0=0

# Name of detector slot
config.detectorList[5].name='ccd05'

# Pixel size in the x dimension in mm
config.detectorList[5].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[5].transformDict.nativeSys=None

config.detectorList[5].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[5].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[5].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[5].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_x=28.431

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[5].offset_y=99.48825

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[5].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[5].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[5].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[5].serial='8351205'

# pitch (rotation about y) of the detector in degrees
config.detectorList[5].pitchDeg=0.0

# ID of detector slot
config.detectorList[5].id=5

config.detectorList[6]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[6].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[6].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[6].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[6].bbox_x0=0

# Name of detector slot
config.detectorList[6].name='ccd06'

# Pixel size in the x dimension in mm
config.detectorList[6].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[6].transformDict.nativeSys=None

config.detectorList[6].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[6].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[6].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[6].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_x=57.078

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[6].offset_y=99.46125

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[6].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[6].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[6].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[6].serial='8351133'

# pitch (rotation about y) of the detector in degrees
config.detectorList[6].pitchDeg=0.0

# ID of detector slot
config.detectorList[6].id=6

config.detectorList[7]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[7].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[7].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[7].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[7].bbox_x0=0

# Name of detector slot
config.detectorList[7].name='ccd07'

# Pixel size in the x dimension in mm
config.detectorList[7].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[7].transformDict.nativeSys=None

config.detectorList[7].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[7].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[7].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[7].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_x=85.6575

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[7].offset_y=99.43425

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[7].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[7].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[7].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[7].serial='835163'

# pitch (rotation about y) of the detector in degrees
config.detectorList[7].pitchDeg=0.0

# ID of detector slot
config.detectorList[7].id=7

config.detectorList[8]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[8].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[8].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[8].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[8].bbox_x0=0

# Name of detector slot
config.detectorList[8].name='ccd08'

# Pixel size in the x dimension in mm
config.detectorList[8].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[8].transformDict.nativeSys=None

config.detectorList[8].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[8].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[8].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[8].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[8].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[8].offset_x=114.2505

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[8].offset_y=99.44775

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[8].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[8].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[8].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[8].serial='8261133'

# pitch (rotation about y) of the detector in degrees
config.detectorList[8].pitchDeg=0.0

# ID of detector slot
config.detectorList[8].id=8

config.detectorList[9]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[9].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[9].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[9].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[9].bbox_x0=0

# Name of detector slot
config.detectorList[9].name='ccd09'

# Pixel size in the x dimension in mm
config.detectorList[9].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[9].transformDict.nativeSys=None

config.detectorList[9].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[9].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[9].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[9].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[9].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[9].offset_x=-114.3855

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[9].offset_y=31.51575

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[9].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[9].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[9].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[9].serial='917213'

# pitch (rotation about y) of the detector in degrees
config.detectorList[9].pitchDeg=0.0

# ID of detector slot
config.detectorList[9].id=9

config.detectorList[10]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[10].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[10].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[10].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[10].bbox_x0=0

# Name of detector slot
config.detectorList[10].name='ccd10'

# Pixel size in the x dimension in mm
config.detectorList[10].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[10].transformDict.nativeSys=None

config.detectorList[10].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[10].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[10].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[10].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[10].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[10].offset_x=-85.7925

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[10].offset_y=31.50225

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[10].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[10].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[10].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[10].serial='835244'

# pitch (rotation about y) of the detector in degrees
config.detectorList[10].pitchDeg=0.0

# ID of detector slot
config.detectorList[10].id=10

config.detectorList[11]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[11].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[11].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[11].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[11].bbox_x0=0

# Name of detector slot
config.detectorList[11].name='ccd11'

# Pixel size in the x dimension in mm
config.detectorList[11].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[11].transformDict.nativeSys=None

config.detectorList[11].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[11].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[11].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[11].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[11].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[11].offset_x=-57.24

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[11].offset_y=31.48875

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[11].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[11].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[11].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[11].serial='8352155'

# pitch (rotation about y) of the detector in degrees
config.detectorList[11].pitchDeg=0.0

# ID of detector slot
config.detectorList[11].id=11

config.detectorList[12]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[12].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[12].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[12].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[12].bbox_x0=0

# Name of detector slot
config.detectorList[12].name='ccd12'

# Pixel size in the x dimension in mm
config.detectorList[12].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[12].transformDict.nativeSys=None

config.detectorList[12].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[12].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[12].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[12].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[12].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[12].offset_x=-28.6605

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[12].offset_y=31.52925

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[12].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[12].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[12].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[12].serial='8351204'

# pitch (rotation about y) of the detector in degrees
config.detectorList[12].pitchDeg=0.0

# ID of detector slot
config.detectorList[12].id=12

config.detectorList[13]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[13].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[13].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[13].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[13].bbox_x0=0

# Name of detector slot
config.detectorList[13].name='ccd13'

# Pixel size in the x dimension in mm
config.detectorList[13].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[13].transformDict.nativeSys=None

config.detectorList[13].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[13].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[13].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[13].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[13].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[13].offset_x=-0.081

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[13].offset_y=31.54275

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[13].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[13].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[13].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[13].serial='8351173'

# pitch (rotation about y) of the detector in degrees
config.detectorList[13].pitchDeg=0.0

# ID of detector slot
config.detectorList[13].id=13

config.detectorList[14]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[14].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[14].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[14].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[14].bbox_x0=0

# Name of detector slot
config.detectorList[14].name='ccd14'

# Pixel size in the x dimension in mm
config.detectorList[14].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[14].transformDict.nativeSys=None

config.detectorList[14].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[14].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[14].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[14].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[14].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[14].offset_x=28.4985

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[14].offset_y=31.48875

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[14].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[14].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[14].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[14].serial='8434135'

# pitch (rotation about y) of the detector in degrees
config.detectorList[14].pitchDeg=0.0

# ID of detector slot
config.detectorList[14].id=14

config.detectorList[15]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[15].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[15].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[15].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[15].bbox_x0=0

# Name of detector slot
config.detectorList[15].name='ccd15'

# Pixel size in the x dimension in mm
config.detectorList[15].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[15].transformDict.nativeSys=None

config.detectorList[15].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[15].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[15].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[15].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[15].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[15].offset_x=57.0915

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[15].offset_y=31.48875

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[15].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[15].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[15].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[15].serial='8341173'

# pitch (rotation about y) of the detector in degrees
config.detectorList[15].pitchDeg=0.0

# ID of detector slot
config.detectorList[15].id=15

config.detectorList[16]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[16].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[16].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[16].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[16].bbox_x0=0

# Name of detector slot
config.detectorList[16].name='ccd16'

# Pixel size in the x dimension in mm
config.detectorList[16].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[16].transformDict.nativeSys=None

config.detectorList[16].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[16].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[16].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[16].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[16].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[16].offset_x=85.644

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[16].offset_y=31.54275

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[16].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[16].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[16].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[16].serial='8351114'

# pitch (rotation about y) of the detector in degrees
config.detectorList[16].pitchDeg=0.0

# ID of detector slot
config.detectorList[16].id=16

config.detectorList[17]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[17].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[17].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[17].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[17].bbox_x0=0

# Name of detector slot
config.detectorList[17].name='ccd17'

# Pixel size in the x dimension in mm
config.detectorList[17].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[17].transformDict.nativeSys=None

config.detectorList[17].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[17].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[17].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[17].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[17].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[17].offset_x=114.2505

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[17].offset_y=31.39425

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[17].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[17].yawDeg=180.0

# roll (rotation about x) of the detector in degrees
config.detectorList[17].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[17].serial='7432193'

# pitch (rotation about y) of the detector in degrees
config.detectorList[17].pitchDeg=0.0

# ID of detector slot
config.detectorList[17].id=17

config.detectorList[18]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[18].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[18].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[18].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[18].bbox_x0=0

# Name of detector slot
config.detectorList[18].name='ccd18'

# Pixel size in the x dimension in mm
config.detectorList[18].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[18].transformDict.nativeSys=None

config.detectorList[18].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[18].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[18].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[18].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[18].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[18].offset_x=-114.3855

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[18].offset_y=-31.47525

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[18].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[18].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[18].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[18].serial='917243'

# pitch (rotation about y) of the detector in degrees
config.detectorList[18].pitchDeg=0.0

# ID of detector slot
config.detectorList[18].id=18

config.detectorList[19]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[19].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[19].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[19].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[19].bbox_x0=0

# Name of detector slot
config.detectorList[19].name='ccd19'

# Pixel size in the x dimension in mm
config.detectorList[19].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[19].transformDict.nativeSys=None

config.detectorList[19].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[19].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[19].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[19].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[19].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[19].offset_x=-85.806

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[19].offset_y=-31.44825

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[19].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[19].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[19].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[19].serial='8341165'

# pitch (rotation about y) of the detector in degrees
config.detectorList[19].pitchDeg=0.0

# ID of detector slot
config.detectorList[19].id=19

config.detectorList[20]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[20].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[20].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[20].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[20].bbox_x0=0

# Name of detector slot
config.detectorList[20].name='ccd20'

# Pixel size in the x dimension in mm
config.detectorList[20].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[20].transformDict.nativeSys=None

config.detectorList[20].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[20].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[20].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[20].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[20].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[20].offset_x=-57.24

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[20].offset_y=-31.46175

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[20].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[20].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[20].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[20].serial='8352134'

# pitch (rotation about y) of the detector in degrees
config.detectorList[20].pitchDeg=0.0

# ID of detector slot
config.detectorList[20].id=20

config.detectorList[21]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[21].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[21].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[21].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[21].bbox_x0=0

# Name of detector slot
config.detectorList[21].name='ccd21'

# Pixel size in the x dimension in mm
config.detectorList[21].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[21].transformDict.nativeSys=None

config.detectorList[21].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[21].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[21].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[21].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[21].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[21].offset_x=-28.647

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[21].offset_y=-31.44825

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[21].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[21].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[21].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[21].serial='8374175'

# pitch (rotation about y) of the detector in degrees
config.detectorList[21].pitchDeg=0.0

# ID of detector slot
config.detectorList[21].id=21

config.detectorList[22]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[22].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[22].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[22].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[22].bbox_x0=0

# Name of detector slot
config.detectorList[22].name='ccd22'

# Pixel size in the x dimension in mm
config.detectorList[22].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[22].transformDict.nativeSys=None

config.detectorList[22].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[22].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[22].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[22].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[22].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[22].offset_x=-0.081

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[22].offset_y=-31.46175

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[22].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[22].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[22].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[22].serial='8351115'

# pitch (rotation about y) of the detector in degrees
config.detectorList[22].pitchDeg=0.0

# ID of detector slot
config.detectorList[22].id=22

config.detectorList[23]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[23].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[23].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[23].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[23].bbox_x0=0

# Name of detector slot
config.detectorList[23].name='ccd23'

# Pixel size in the x dimension in mm
config.detectorList[23].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[23].transformDict.nativeSys=None

config.detectorList[23].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[23].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[23].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[23].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[23].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[23].offset_x=28.566

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[23].offset_y=-31.42125

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[23].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[23].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[23].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[23].serial='835164'

# pitch (rotation about y) of the detector in degrees
config.detectorList[23].pitchDeg=0.0

# ID of detector slot
config.detectorList[23].id=23

config.detectorList[24]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[24].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[24].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[24].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[24].bbox_x0=0

# Name of detector slot
config.detectorList[24].name='ccd24'

# Pixel size in the x dimension in mm
config.detectorList[24].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[24].transformDict.nativeSys=None

config.detectorList[24].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[24].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[24].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[24].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[24].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[24].offset_x=57.078

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[24].offset_y=-31.43475

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[24].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[24].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[24].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[24].serial='8351185'

# pitch (rotation about y) of the detector in degrees
config.detectorList[24].pitchDeg=0.0

# ID of detector slot
config.detectorList[24].id=24

config.detectorList[25]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[25].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[25].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[25].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[25].bbox_x0=0

# Name of detector slot
config.detectorList[25].name='ccd25'

# Pixel size in the x dimension in mm
config.detectorList[25].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[25].transformDict.nativeSys=None

config.detectorList[25].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[25].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[25].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[25].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[25].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[25].offset_x=85.671

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[25].offset_y=-31.38075

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[25].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[25].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[25].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[25].serial='8352185'

# pitch (rotation about y) of the detector in degrees
config.detectorList[25].pitchDeg=0.0

# ID of detector slot
config.detectorList[25].id=25

config.detectorList[26]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[26].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[26].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[26].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[26].bbox_x0=0

# Name of detector slot
config.detectorList[26].name='ccd26'

# Pixel size in the x dimension in mm
config.detectorList[26].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[26].transformDict.nativeSys=None

config.detectorList[26].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[26].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[26].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[26].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[26].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[26].offset_x=114.1965

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[26].offset_y=-31.47525

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[26].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[26].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[26].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[26].serial='835173'

# pitch (rotation about y) of the detector in degrees
config.detectorList[26].pitchDeg=0.0

# ID of detector slot
config.detectorList[26].id=26

config.detectorList[27]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[27].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[27].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[27].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[27].bbox_x0=0

# Name of detector slot
config.detectorList[27].name='ccd27'

# Pixel size in the x dimension in mm
config.detectorList[27].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[27].transformDict.nativeSys=None

config.detectorList[27].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[27].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[27].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[27].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[27].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[27].offset_x=-114.291

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[27].offset_y=-99.50175

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[27].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[27].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[27].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[27].serial='8261165'

# pitch (rotation about y) of the detector in degrees
config.detectorList[27].pitchDeg=0.0

# ID of detector slot
config.detectorList[27].id=27

config.detectorList[28]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[28].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[28].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[28].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[28].bbox_x0=0

# Name of detector slot
config.detectorList[28].name='ccd28'

# Pixel size in the x dimension in mm
config.detectorList[28].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[28].transformDict.nativeSys=None

config.detectorList[28].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[28].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[28].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[28].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[28].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[28].offset_x=-85.8195

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[28].offset_y=-99.35325

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[28].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[28].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[28].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[28].serial='743233'

# pitch (rotation about y) of the detector in degrees
config.detectorList[28].pitchDeg=0.0

# ID of detector slot
config.detectorList[28].id=28

config.detectorList[29]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[29].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[29].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[29].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[29].bbox_x0=0

# Name of detector slot
config.detectorList[29].name='ccd29'

# Pixel size in the x dimension in mm
config.detectorList[29].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[29].transformDict.nativeSys=None

config.detectorList[29].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[29].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[29].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[29].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[29].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[29].offset_x=-57.213

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[29].offset_y=-99.36675

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[29].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[29].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[29].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[29].serial='8351164'

# pitch (rotation about y) of the detector in degrees
config.detectorList[29].pitchDeg=0.0

# ID of detector slot
config.detectorList[29].id=29

config.detectorList[30]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[30].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[30].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[30].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[30].bbox_x0=0

# Name of detector slot
config.detectorList[30].name='ccd30'

# Pixel size in the x dimension in mm
config.detectorList[30].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[30].transformDict.nativeSys=None

config.detectorList[30].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[30].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[30].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[30].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[30].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[30].offset_x=-28.6065

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[30].offset_y=-99.43425

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[30].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[30].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[30].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[30].serial='8261195'

# pitch (rotation about y) of the detector in degrees
config.detectorList[30].pitchDeg=0.0

# ID of detector slot
config.detectorList[30].id=30

config.detectorList[31]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[31].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[31].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[31].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[31].bbox_x0=0

# Name of detector slot
config.detectorList[31].name='ccd31'

# Pixel size in the x dimension in mm
config.detectorList[31].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[31].transformDict.nativeSys=None

config.detectorList[31].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[31].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[31].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[31].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[31].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[31].offset_x=-0.054

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[31].offset_y=-99.40725

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[31].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[31].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[31].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[31].serial='835183'

# pitch (rotation about y) of the detector in degrees
config.detectorList[31].pitchDeg=0.0

# ID of detector slot
config.detectorList[31].id=31

config.detectorList[32]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[32].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[32].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[32].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[32].bbox_x0=0

# Name of detector slot
config.detectorList[32].name='ccd32'

# Pixel size in the x dimension in mm
config.detectorList[32].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[32].transformDict.nativeSys=None

config.detectorList[32].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[32].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[32].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[32].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[32].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[32].offset_x=28.5255

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[32].offset_y=-99.42075

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[32].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[32].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[32].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[32].serial='8352104'

# pitch (rotation about y) of the detector in degrees
config.detectorList[32].pitchDeg=0.0

# ID of detector slot
config.detectorList[32].id=32

config.detectorList[33]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[33].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[33].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[33].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[33].bbox_x0=0

# Name of detector slot
config.detectorList[33].name='ccd33'

# Pixel size in the x dimension in mm
config.detectorList[33].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[33].transformDict.nativeSys=None

config.detectorList[33].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[33].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[33].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[33].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[33].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[33].offset_x=57.1185

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[33].offset_y=-99.36675

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[33].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[33].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[33].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[33].serial='8352154'

# pitch (rotation about y) of the detector in degrees
config.detectorList[33].pitchDeg=0.0

# ID of detector slot
config.detectorList[33].id=33

config.detectorList[34]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[34].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[34].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[34].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[34].bbox_x0=0

# Name of detector slot
config.detectorList[34].name='ccd34'

# Pixel size in the x dimension in mm
config.detectorList[34].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[34].transformDict.nativeSys=None

config.detectorList[34].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[34].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[34].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[34].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[34].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[34].offset_x=85.6845

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[34].offset_y=-99.38025

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[34].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[34].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[34].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[34].serial='826173'

# pitch (rotation about y) of the detector in degrees
config.detectorList[34].pitchDeg=0.0

# ID of detector slot
config.detectorList[34].id=34

config.detectorList[35]=lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
# y0 of pixel bounding box
config.detectorList[35].bbox_y0=0

# y1 of pixel bounding box
config.detectorList[35].bbox_y1=4611

# x1 of pixel bounding box
config.detectorList[35].bbox_x1=2047

# x0 of pixel bounding box
config.detectorList[35].bbox_x0=0

# Name of detector slot
config.detectorList[35].name='ccd35'

# Pixel size in the x dimension in mm
config.detectorList[35].pixelSize_x=0.0135

# Name of native coordinate system
config.detectorList[35].transformDict.nativeSys=None

config.detectorList[35].transformDict.transforms=None
# x position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[35].refpos_x=1023.5

# y position of the reference point in the detector in pixels in transposed coordinates.
config.detectorList[35].refpos_y=2305.5

# Pixel size in the y dimension in mm
config.detectorList[35].pixelSize_y=0.0135

# Detector type: SCIENCE=0, FOCUS=1, GUIDER=2, WAVEFRONT=3
config.detectorList[35].detectorType=0

# x offset from the origin of the camera in mm in the transposed system.
config.detectorList[35].offset_x=114.1695

# y offset from the origin of the camera in mm in the transposed system.
config.detectorList[35].offset_y=-99.51525

# Transpose the pixel grid before orienting in focal plane?
config.detectorList[35].transposeDetector=None

# yaw (rotation about z) of the detector in degrees. This includes any necessary rotation to go from detector coordinates to camera coordinates after optional transposition.
config.detectorList[35].yawDeg=0.0

# roll (rotation about x) of the detector in degrees
config.detectorList[35].rollDeg=0.0

# Serial string associated with this specific detector
config.detectorList[35].serial='8261143'

# pitch (rotation about y) of the detector in degrees
config.detectorList[35].pitchDeg=0.0

# ID of detector slot
config.detectorList[35].id=35

# Coefficients for radial distortion
config.radialCoeffs=None

# Name of this camera
config.name='CFHT MegaCam'

