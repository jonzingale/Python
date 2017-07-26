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

geocoords = [119.9484696, 31.9706798] # china steel
name = 'china'

def get_avail_bands(const_id='L8SR'):
   pprint(dl.raster.get_bands_by_constellation(const_id))

def get_feature_collection(const_id, tile):
  rand_date = datetime.date(2014 + randint(0,2), randint(1,12), randint(1,29))
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
  print(rand_start)

  geometry = json.dumps(tile['geometry'])

  feature_collection = dl.metadata.search(
    const_id=const_id, start_time=rand_start, end_time=rand_end,
    limit=10, geom=geometry)

  return(feature_collection, rand_start)

def save_image(tile, rand_start):
  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond

  # Check that directory exists. If not, make it.
  dir_name = "./images/%s" % name
  dir_cond = os.path.isdir(dir_name)
  if not dir_cond: os.mkdir(dir_name)

  filename = "./images/%s/%s_%s.png" % (name, rand_start, mu_sec)
  savefig(filename, dpi=500, facecolor='k')
  time.sleep(2)
  if os.stat(filename).st_size < 1*10**6: os.remove(filename)

def get_images():
  tile = dl.raster.dltile_from_latlon(*geocoords,30,2048,16)
  tiles = [tile]

  # make sure we have features.
  feature_collection, rand_start = get_feature_collection('L8SR', tile)
  while not feature_collection['features']:
    feature_collection, rand_start = get_feature_collection('L8SR', tile)

  for tile in tiles:
    ids = [f['id'] for f in feature_collection['features']]

    arr, meta = dl.raster.ndarray(
        ids,
        bands=['swir2', 'swir1', 'red', 'bai'],
        scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],
        data_type='Byte',
        resolution=5,
        cutline=tile['geometry'],
    )
    plt.figure(figsize=[7,7], facecolor='k')
    plt.axis('off')
    plt.imshow(arr)
    save_image(tile, rand_start)

for i in range(15): get_images()
plt.show()