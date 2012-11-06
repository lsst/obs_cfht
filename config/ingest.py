from lsst.obs.cfht.ingest import MegacamParseTask
root.parse.retarget(MegacamParseTask)
root.parse.hdu = 1 # PHU
root.parse.translation = {'runId': 'RUNID',
                          'object': 'OBJECT',
                          'exp': 'EXPNUM',
                          'date': 'DATE-OBS',
                          'expTime': 'EXPTIME',
                          'filter': 'FILTER',
                          }
root.parse.translators = {'taiObs': 'translate_taiObs',
                          'ccd': 'translate_ccd',
                          }
root.parse.extnames = ["ccd%02d" % ccd for ccd in range(36)]
root.register.columns = {'runId':    'text',
                         'object':   'text',
                         'exp':      'int',
                         'ccd':      'int',
                         'state':    'text',
                         'filter':   'text',
                         'date':     'text',
                         'taiObs':   'text',
                         'expTime':  'double',
                         }
root.register.unique = ['exp', 'ccd', 'state']
root.register.visit = ['exp', 'state', 'date', 'filter']
