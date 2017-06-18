import descarteslabs as dl
from pprint import pprint
from pdb import set_trace
import os

# Find potential matches
matches = dl.places.find('new-mexico_taos')
pprint(matches)
# The first one looks good to me, so lets make that our area of interest.
aoi = matches[0]

# This area of interest just gives us some basic properties such as bounding boxes.
# To access a GeoJSON Geometry object of that place, we call the `Places.shape` method, in this case
# accessing a low-resolution version of this particular shape.
shape = dl.places.shape(aoi['slug'], geom='low')

# If you'd like, load up some libraries like matplotlib, shapley, and cartopy,
# and use them to plot Taos county.
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import shapely.geometry
import cartopy

bbox = shape['bbox']

# Lets load up the Albers Equal Area projection.
lonlat_crs = cartopy.crs.PlateCarree()
albers = cartopy.crs.AlbersEqualArea(central_latitude=36.0, central_longitude=-105)

fig = plt.figure(figsize=(4, 8))
ax = plt.subplot(projection=albers) # Specify projection of the map here
shp = shapely.geometry.shape(shape['geometry'])

# When adding a geometry in latlon coordinates, specify the latlon projection
ax.add_geometries([shp], lonlat_crs)

# You can set extents in latlon, as long as you specify the projection with `crs`
# ax.set_extent((bbox[0], bbox[2], bbox[1], bbox[3]), crs=lonlat_crs) # SEGFAULT
ax.gridlines(crs=lonlat_crs)
plt.show()

