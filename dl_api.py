import descarteslabs as dl
from pprint import pprint
from pdb import set_trace
import matplotlib
import matplotlib.pyplot as plt
import shapely.geometry
import cartopy
import itertools
import json
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
ax.set_extent((bbox[0], bbox[2], bbox[1], bbox[3]), crs=lonlat_crs)
ax.gridlines(crs=lonlat_crs)

# What imagery is available?
sources = dl.metadata.sources()
groups = {}
for group, items in itertools.groupby(sources, key=lambda v: v['const_id']):
    groups[group] = list(items)
pprint(groups)

feature_collection = dl.metadata.search(const_id='L8', start_time='2017-03-12',
                                        end_time='2017-03-20', limit=10, place=aoi['slug'])
# As the variable name implies, this returns a FeatureCollection GeoJSON dictionary.
# Its 'features' are the available scenes.
print(len(feature_collection['features']))
# The 'id' associated with each feature is a unique identifier into our imagery database.
# In this case there are two L8 scenes from adjoining WRS rows.
print([f['id'] for f in feature_collection['features']])

# Let's plot the footprints of the scenes:
lonlat_crs = cartopy.crs.PlateCarree()
albers = cartopy.crs.AlbersEqualArea(central_latitude=36.0, central_longitude=-105)

fig = plt.figure(figsize=(6, 8))
ax = plt.subplot(projection=albers) # Specify projection of the map here

ax.add_geometries([shapely.geometry.shape(shape['geometry'])],
                   lonlat_crs)

# Get the geometry from each feature
shapes = [shapely.geometry.shape(f['geometry']) for
          f in feature_collection['features']]

ax.add_geometries(shapes, lonlat_crs, alpha=0.3, color='green')

# Get a bounding box of the combined scenes
union = shapely.geometry.MultiPolygon(polygons=shapes)
bbox = union.bounds
ax.set_extent((bbox[0], bbox[2], bbox[1], bbox[3]), crs=lonlat_crs)
ax.gridlines(crs=lonlat_crs)

plt.show()
