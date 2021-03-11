"""
CFHT-specific overrides for IsrTask
"""
config.doBias = False
config.doDark = False
config.doFlat = False
config.doFringe = False
config.fringeAfterFlat = False
config.doWrite = False
config.fringe.filters = ["i.MP9701", "i.MP9702", "z.MP9801"]
config.fringe.pedestal = True
config.fringe.small = 1
config.fringe.large = 50
config.doAssembleIsrExposures = True
config.doSuspect = False
