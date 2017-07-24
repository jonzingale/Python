import descarteslabs as dl

from pprint import pprint
import matplotlib.pyplot as plt
import shapely.geometry
import cartopy
import json
import numpy as np


ctown = dl.places.shape('ohio_cuyahoga')
tiles = dl.raster.dltiles_from_shape(30.0, 2048, 16, ctown)
# pprint(tiles['features'][0])

lonlat_crs = cartopy.crs.PlateCarree()
albers = cartopy.crs.AlbersEqualArea(central_latitude=41.3, central_longitude=-82)
fig = plt.figure(figsize=(6, 8))
ax = plt.subplot(projection=albers) # Specify projection of the map here
ax.add_geometries([shapely.geometry.shape(ctown['geometry'])], lonlat_crs)

# Get the geometry from each feature
shapes = [shapely.geometry.shape(f['geometry']) for f in tiles['features']]
ax.add_geometries(shapes, lonlat_crs, alpha=0.3, color='green')

# Get a bounding box of the combined scenes
union = shapely.geometry.MultiPolygon(polygons=shapes)
bbox = union.bounds
ax.set_extent((bbox[0], bbox[2], bbox[1], bbox[3]), crs=lonlat_crs)
ax.gridlines(crs=lonlat_crs)
plt.show()