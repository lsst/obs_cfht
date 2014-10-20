import lsst.pipe.tasks.astrometry as ptAstrometry
from lsst.obs.cfht.cfhtastrom import CfhtAstrometry

class CfhtAstrometryTask(ptAstrometry.AstrometryTask):

    def __init__(self, schema, **kwargs):

        ptAstrometry.AstrometryTask.__init__(self, schema, **kwargs)

        self.astrometer = CfhtAstrometry(self.config.solver, log=self.log)
