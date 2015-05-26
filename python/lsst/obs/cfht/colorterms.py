from lsst.pipe.tasks.colorterms import Colorterm

colortermsData = dict(
    # e2v chips
    # Retrieved from: http://www3.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/community/CFHTLS-SG/docs/extra/filters.html
    # on 4/1/2014
    e2v = dict(
        u = Colorterm("u", "g", 0., -0.241),
        g = Colorterm("g", "r", 0., -0.153),
        r = Colorterm("r", "g", 0., 0.024),
        i = Colorterm("i", "r", 0., 0.085),
        z = Colorterm("z", "i", 0., -0.074),
        ),
    )
