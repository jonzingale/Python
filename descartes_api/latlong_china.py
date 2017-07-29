from pprint import pprint
import descarteslabs as dl
import matplotlib.pyplot as plt
from pdb import set_trace as st
from random import *
from pylab import *
import datetime
import time
import os

import json

from inside_outside import pointed_region

# The aoi place code as this is no longer necessary.
# Instead, this code uses long and lat directly and
# then derives the features via the geometry.
# tile = dl.raster.dltile_from_latlon(31.9706798, 119.9484696, 30, 2048, 16)
# geometry = json.dumps(tile['geometry'])

# Geocords in correct orientation
# name, *geocoords = ['Mongolia', 50.2916455,93.5796776]
# name, *geocoords = ['hawaii', 19.44276, -155.23398]
# name, *geocoords = ['gaungzhou', 23.1309874, 113.2631488]
# name, *geocoords = ['changzhou', 31.6152322, 120.2098807]
# name, *geocoords = ['singapore', 1.3220315, 103.9310956]
# name, *geocoords = ['Brazil', -23.7329092, -46.4427626]
# name, *geocoords = ['norway',62.1008792,5.7588653]
# name, *geocoords = ['russia',65.8995174,44.1387822]
# name, *geocoords = ['Budapest',47.4811282,18.9902215]
# name, *geocoords = ['Budapest',47.6900869,19.076262] # szentendrei
name, *geocoords = ['Budapest',46.955091,17.8995783]  # lake belaton, hotel annabella
# name, *geocoords = ['russia',68.172482,53.8014399]
# name, *geocoords = ['japan',36.7975629,138.7505393] # labyrinth festival
# name, *geocoords = ['iceland',65.6713177,-16.8587428] # Hverarönd boiling mud
# name, *geocoords = ['Finland',60.2067757,25.0429881] # helsinki
# name, *geocoords = ['Amazon', -2.2473374, -55.1659967]

def get_avail_bands(const_id='L8SR'):
   pprint(dl.raster.get_bands_by_constellation(const_id))

def get_feature_collection(const_id, tile):
  # rand_date = datetime.date(2014 + randint(0,2), randint(6,8), randint(1,29))
  rand_date = datetime.date(2014,8,13)

  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
  print(rand_start)

  geometry = json.dumps(tile['geometry'])

  feature_collection = dl.metadata.search(
    const_id=const_id, start_time=rand_start, end_time=rand_end,
    limit=10, geom=geometry)

  return(feature_collection, rand_start)

def save_image(tile, rand_start, size=4096, resolution=0):
  # mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond

  # Check that directory exists. If not, make it.
  dir_name = "./images/%s" % name
  dir_cond = os.path.isdir(dir_name)
  if not dir_cond: os.mkdir(dir_name)

  filename = "./images/%s/%s_%s.png" % (name, rand_start, resolution)
  savefig(filename, dpi=500, facecolor='k')
  time.sleep(2)
  if os.stat(filename).st_size < 1*10**6: os.remove(filename)

def get_images():
  resolution = 10
  size = 2**12 # max so far?
  tile = dl.raster.dltile_from_latlon(*geocoords, resolution, size, 16)
  tiles = [tile]

  # make sure we have features.
  feature_collection, rand_start = get_feature_collection('L8SR', tile)
  while not feature_collection['features']:
    feature_collection, rand_start = get_feature_collection('L8SR', tile)

  for tile in tiles:
    ids = [f['id'] for f in feature_collection['features']]

    arr, meta = dl.raster.ndarray(
        ids,
        bands=['swir2', 'swir1', 'red', 'bai'], #nir
        scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],
        data_type='Byte',
        resolution=resolution,
        cutline=tile['geometry'],
    )
    plt.figure(figsize=[7,7], facecolor='k')
    plt.axis('off')
    plt.imshow(arr)
    save_image(tile, rand_start, size, resolution)

for i in range(13): get_images()
# plt.show()