from lsst.obs.cfht.ingest import MegacamParseTask
root.parse.retarget(MegacamParseTask)
root.parse.hdu = 1 # PHU
root.parse.translation = {'runId': 'RUNID',
                          'object': 'OBJECT',
                          'visit': 'EXPNUM',
                          'date': 'DATE-OBS',
                          'expTime': 'EXPTIME',
                          }
root.parse.translators = {'taiObs': 'translate_taiObs',
                          'ccd': 'translate_ccd',
                          'filter': 'translate_filter',
                          'defects': 'translate_defects',
                          }
root.parse.extnames = ["ccd%02d" % ccd for ccd in range(36)]
root.register.columns = {'runId':     'text',
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
root.register.unique = ['visit', 'ccd']
root.register.visit = ['visit', 'state', 'taiObs', 'date', 'filter']
