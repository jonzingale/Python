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

# Mostly, this code is for finding fiery
# parts on the earth. Forest fires, volcanos
# and industrial processes. The code relies
# on there being a 'place' and some geocoords. 
# Then the inside_outside module gets close.

place = 'pennsylvania_allegheny'
matches = dl.places.find(place)
if not matches: st()
aoi = matches[0]
location = dl.places.shape(place)
# geocoords = [-19.6264763, 63.6266683] # Eyjafjallajökull
geocoords = [-79.9877977, 40.4278674] # Pgh

def get_avail_bands(const_id='L8SR'):
   pprint(dl.raster.get_bands_by_constellation(const_id))

def get_feature_collection(const_id, aoi):
  # eruption at Eyjafjallajökull, L7
  # rand_date = datetime.date(2010, randint(4,5), 10 + randint(0,10))

  # ANYTIME
  rand_date = datetime.date(2014 + randint(0,2), randint(1,12), randint(1,29))

  # Eyjafjallajökull hotspots L8, L8SR
  # rand_date = datetime.date(2013, 7, 19)
  
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

  # Check that directory exists. If not, make it.
  dir_name = "./images/%s" % aoi['name']
  dir_cond = os.path.isdir(dir_name)
  if not dir_cond: os.mkdir(dir_name)

  filename = "./images/%s/%s_%s.png" % (aoi['name'], rand_start, mu_sec)
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
        # bands=['nir','red', 'green', 'bai'], #, Modis09
        # scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],

        bands=['swir2','swir1','red','bai'], # L7, L8SR, L8 : cirrus[0,4000]
        scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],
        data_type='Byte',# Float32' 'Float64' 'Byte' 'UInt16'
        resolution=5,
        cutline=tile['geometry'],
    )
    plt.figure(figsize=[7,7], facecolor='k') # does not affect save.
    plt.axis('off')
    plt.imshow(arr)
    save_image(aoi, tile, rand_start)

for i in range(5): get_images()
plt.show()