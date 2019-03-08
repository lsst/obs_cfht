# Set up aperture photometry
# 'config' should be a SourceMeasurementConfig

config.plugins.names |= ["base_CircularApertureFlux"]
config.plugins["base_CircularApertureFlux"].radii = [3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]

# Use a large aperture to be independent of seeing in calibration
config.plugins["base_CircularApertureFlux"].maxSincRadius = 12.0
