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

place = 'new-mexico_sandoval'
matches = dl.places.find(place)
if not matches: st()
aoi = matches[0]
location = dl.places.shape(place)
# fire_coords1 = [-106.33291249604501, 35.772363328866696]
fire_coords1 = [-106.4479236, 35.8457509]

def get_feature_collection(const_id, aoi):
  rand_date = datetime.date(2010 + randint(1, 7), 7, 1 + randint(1, 28)) # Los Conchas
  # rand_date = datetime.date(2013, 6, 4 + randint(1, 14))

  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=15)).strftime('%Y-%m-%d')
  print([rand_start, rand_end])

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
  
  filename = "./images/%s/jemez_fire/%s_%s.png" % (aoi['name'], rand_start, mu_sec)
  savefig(filename, dpi=500, facecolor='k')
  time.sleep(2)
  if os.stat(filename).st_size < 1*10**6: os.remove(filename)

def get_images():
  # make sure we have features. WILL STAY IN LOOP FOREVER.
  satellite = 'L8' #'L8SR'
  feature_collection, rand_start = get_feature_collection(satellite, aoi) 
  while not feature_collection['features']:
    feature_collection, rand_start = get_feature_collection(satellite, aoi)

  pr = pointed_region(fire_coords1, place, 5, 5000)
  tiles = pr.possible_regions()

  print(len(tiles))

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
    plt.figure(figsize=[7,7], facecolor='k')
    plt.axis('off')
    plt.imshow(arr)
    save_image(aoi, tile, rand_start)

for i in range(5): get_images()
plt.show()