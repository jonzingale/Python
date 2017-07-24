from pprint import pprint
import descarteslabs as dl
import matplotlib.pyplot as plt
from pdb import set_trace as st
from random import *
from pylab import *
import datetime
import time
import os

from inside_outside import pointed_region

# Find potential AOI matches
place = 'iceland'
matches = dl.places.find(place)
if not matches: st()
aoi = matches[0]
location = dl.places.shape(place)
geocoords = [-19.6271567, 63.6045345]

def get_feature_collection(const_id, aoi):
  rand_date = datetime.date(2016, randint(1,12), randint(1,28))
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
  print(rand_start)

  feature_collection = dl.metadata.search(const_id=const_id,
                                          start_time=rand_start,
                                          end_time=rand_end,
                                          limit=10, place=aoi['slug'])
  return(feature_collection, rand_start)

def save_image(aoi, tile, rand_start):
  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond
  filename = "./images/%s/volcano/%s_%s.png" % (aoi['name'], rand_start, mu_sec)
  savefig(filename, dpi=500, facecolor='k')
  time.sleep(2)
  if os.stat(filename).st_size < 1*10**6: os.remove(filename)

def get_images():
  # make sure we have features.
  feature_collection, rand_start = get_feature_collection('L8SR', aoi)
  while not feature_collection['features']:
    feature_collection, rand_start = get_feature_collection('L8SR', aoi)


  # resolution, tilesize, pad
  # tiles = dl.raster.dltiles_from_shape(5, 4000, 16, location) # 2048

  pr = pointed_region(geocoords, place, 5, 4000)
  tiles = pr.possible_regions()

  for tile in tiles:
    ids = [f['id'] for f in feature_collection['features']]

    arr, meta = dl.raster.ndarray(
        ids,
        bands=['swir2','swir1','red','bai'],
        scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],
        data_type='Byte',# Float32' 'Float64' 'Byte'
        resolution=5,
        cutline=tile['geometry'],
    )
    plt.figure(figsize=[7,7], facecolor='k') # does not affect save.
    plt.axis('off')
    plt.imshow(arr)
    save_image(aoi, tile, rand_start)

for i in range(15): get_images()
plt.show()