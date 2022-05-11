# characterize image task config for CFHT single frame measurement

# These cosmic ray defaults work for validation_data_cfht (which is post-ISR
# data, thus not actually raw); it may not be correct for all CFHT data.
config.requireCrForPsf = False
config.repair.cosmicray.nCrPixelMax = 100000
config.repair.cosmicray.min_DN = 3000
