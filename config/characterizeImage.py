# characterize image task config for CFHT single frame measurement

config.refObjLoader.filterMap = {'i2': 'i'}
config.refObjLoader.ref_dataset_name = "ps1_pv3_3pi_20170110"

config.repair.doCosmicRay = True
config.repair.cosmicray.cond3_fac = 2.5
config.repair.cosmicray.cond3_fac2 = 0.4
config.repair.cosmicray.niteration = 3
config.repair.cosmicray.nCrPixelMax = 100000
config.repair.cosmicray.minSigma = 6.0
config.repair.cosmicray.min_DN = 150.0
