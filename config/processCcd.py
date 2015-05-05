import os
root.load(os.path.join(os.environ['OBS_CFHT_DIR'], 'config', 'colorterms.py'))

from lsst.obs.cfht.cfhtCalibrate import CfhtCalibrateTask
root.calibrate.retarget(CfhtCalibrateTask)

from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask
root.isr.retarget(CfhtIsrTask)

root.isr.doBias = False
root.isr.doDark = False
root.isr.doFlat = False
root.isr.doFringe = False
root.isr.fringeAfterFlat = False
root.isr.doWrite = False
root.isr.setGainAssembledCcd = True
root.isr.assembleCcd.doRenorm = False
root.isr.assembleCcd.setGain = False
root.isr.fringe.filters = ['i', 'i2', 'z']
root.isr.fringe.pedestal = True
root.isr.fringe.small = 1
root.isr.fringe.large = 50
root.isr.doAssembleIsrExposures = True

root.calibrate.repair.doCosmicRay=True
root.calibrate.repair.cosmicray.cond3_fac=2.5
root.calibrate.repair.cosmicray.cond3_fac2=0.4
root.calibrate.repair.cosmicray.niteration=3
root.calibrate.repair.cosmicray.nCrPixelMax=100000
root.calibrate.repair.cosmicray.minSigma=6.0
root.calibrate.repair.cosmicray.min_DN=150.0

root.calibrate.initialPsf.fwhm=1.0

root.calibrate.measurePsf.starSelector.name = "objectSize"

try :
    root.calibrate.astrometry.refObjLoader.filterMap = { 'i2': 'i',
                                                   }
except :
    root.calibrate.astrometry.solver.filterMap = { 'i2': 'i',
                                                   }
                                                   

