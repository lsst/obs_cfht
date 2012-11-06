from lsst.obs.cfht.isr import MegacamIsrTask
root.isr.retarget(MegacamIsrTask)

root.isr.doBias = True
root.isr.doDark = False
root.isr.doFlat = True
root.isr.doWrite = False
#root.isr.setGainAssembledCcd = False
root.isr.assembleCcd.doRenorm = False
root.isr.assembleCcd.setGain = False

root.calibrate.repair.cosmicray.nCrPixelMax = 1000000
