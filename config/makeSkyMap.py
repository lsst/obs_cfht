# Updated version following hsc example

print "*** in obs_cfht/config/makeSkyMap.py"

root.skyMap = "discrete"

# Configuration for HealpixSkyMap
root.skyMap["healpix"].log2NSide = 5
root.skyMap["healpix"].pixelScale = 0.18
root.skyMap["healpix"].patchBorder = 333 # Pixels
root.skyMap["healpix"].tractOverlap = 2.0/60 # Degrees
root.skyMap["healpix"].projection = "TAN"

# Configuration for DiscreteSkyMap
# 0: ACTJ0022M0036
# 1: M31
root.skyMap["discrete"].raList = [213, 216]
root.skyMap["discrete"].decList = [51, 54]
root.skyMap["discrete"].radiusList = [0.5, 0.5]
root.skyMap["discrete"].pixelScale = 0.185
