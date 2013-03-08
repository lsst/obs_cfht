root.isr.doBias = True
root.isr.doDark = False
root.isr.doFlat = True
root.isr.doFringe = True
root.isr.fringeAfterFlat = True
root.isr.doWrite = False
root.isr.setGainAssembledCcd = True
root.isr.assembleCcd.doRenorm = False
root.isr.assembleCcd.setGain = False
root.isr.fringe.filters = ['i', 'i2', 'z']
root.isr.fringe.pedestal = True
root.isr.fringe.small = 1
root.isr.fringe.large = 50
root.isr.doAssembleDetrends = True

root.calibrate.repair.cosmicray.nCrPixelMax = 100000
