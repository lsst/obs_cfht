root.calibrate.repair.cosmicray.nCrPixelMax = 1000000
root.calibrate.repair.doCosmicRay=True
root.calibrate.repair.cosmicray.cond3_fac=2.5
root.calibrate.repair.cosmicray.cond3_fac2=0.4
root.calibrate.repair.cosmicray.niteration=3
root.calibrate.repair.cosmicray.nCrPixelMax=100000
root.calibrate.repair.cosmicray.minSigma=6.0
root.calibrate.repair.cosmicray.min_DN=150.0

#root.calibrate.astrometry.forceKnownWcs=True
#root.calibrate.astrometry.solver.catalogMatchDist=10.0
root.calibrate.astrometry.solver.sipOrder=4
root.calibrate.astrometry.solver.calculateSip=True
root.calibrate.astrometry.solver.useWcsPixelScale=True
#root.calibrate.astrometry.solver.matchThreshold=15.0

root.calibrate.initialPsf.fwhm=1.0
root.calibrate.photocal.magLimit=24.0

#root.calibrate.measurePsf.starSelector.name='secondMoment'
root.calibrate.measurePsf.starSelector.name = "objectSize"
root.calibrate.measurePsf.starSelector['objectSize'].widthMax=10.0
root.calibrate.measurePsf.starSelector['objectSize'].widthMin=0.0
root.calibrate.measurePsf.starSelector['objectSize'].fluxMin=12500.0
#root.calibrate.measurePsf.starSelector.name = "sizeMagnitude"
#root.calibrate.measurePsf.starSelector["objectSize"].sourceFluxField = "initial.flux.psf"

# Select and configure psfex PSF solver
#import lsst.meas.extensions.psfex.psfexPsfDeterminer
#root.calibrate.measurePsf.psfDeterminer["psfex"].spatialOrder = 2
#root.calibrate.measurePsf.psfDeterminer.name = "psfex"

#from lsst.obs.cfht.cfhtMeasurement import CfhtSourceMeasurementTask
#root.calibrate.initialMeasurement.retarget(CfhtSourceMeasurementTask)
##root.calibrate.measurement.retarget(CfhtSourceMeasurementTask)

from lsst.obs.cfht.astrometry import CfhtAstrometryTask
root.calibrate.astrometry.retarget(CfhtAstrometryTask)

#from lsst.obs.cfht.cfhtMeasurePsf import CfhtMeasurePsfTask
#root.calibrate.measurePsf.retarget(CfhtMeasurePsfTask)

#from lsst.obs.cfht.cfhtIsrTask import CfhtIsrTask
#root.isr.retarget(CfhtIsrTask)

from lsst.obs.cfht.cfhtCalibrate import CfhtCalibrateTask
root.calibrate.retarget(CfhtCalibrateTask)
