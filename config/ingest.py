from lsst.obs.cfht.ingest import MegacamParseTask

config.parse.retarget(MegacamParseTask)
config.parse.hdu = 1 # PHU
config.parse.translation = {'runId': 'RUNID',
                          'object': 'OBJECT',
                          'visit': 'EXPNUM',
                          'date': 'DATE-OBS',
                          'expTime': 'EXPTIME',
                          }
config.parse.translators = {'taiObs': 'translate_taiObs',
                          'ccd': 'translate_ccd',
                          'filter': 'translate_filter',
                          'defects': 'translate_defects',
                          }
config.parse.extnames = ["ccd%02d" % ccd for ccd in range(36)]
config.register.columns = {'runId':     'text',
                         'object':    'text',
                         'visit':     'int',
                         'ccd':       'int',
                         'extension': 'int',
                         'state':     'text',
                         'filter':    'text',
                         'date':      'text',
                         'taiObs':    'text',
                         'expTime':   'double',
                         'defects':   'text',
                         }
config.register.unique = ['visit', 'ccd']
config.register.visit = ['visit', 'state', 'taiObs', 'date', 'filter']
