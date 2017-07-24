from pprint import pprint
import descarteslabs as dl
import matplotlib.pyplot as plt
from pdb import set_trace as st
from random import *
from pylab import *
import datetime
import time
import os

def get_feature_collection(const_id, aoi):
  rand_date = datetime.date(2016, randint(8,9), randint(1,28)) # May - August
  # rand_date = datetime.date(2016, 3, 10)
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
  print(rand_start)

  feature_collection = dl.metadata.search(const_id=const_id,
                                          start_time=rand_start,
                                          end_time=rand_end,
                                          limit=10, place=aoi['slug'])
  return(feature_collection)

def save_image(aoi):
  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond

  # Check that directory exists. If not, make it.
  dir_name = "./images/%s" % aoi['name']
  dir_cond = os.path.isdir(dir_name)
  if not dir_cond: os.mkdir(dir_name)

  filename = "./images/%s/%s.png" % (aoi['name'], mu_sec)
  savefig(filename, dpi=300, facecolor='k')
  time.sleep(3)
  if os.stat(filename).st_size < 1*10**6: os.remove(filename)

# Find potential AOI matches
# place = 'new-mexico_santa-fe'
# place = 'cuba'
place = 'washington_snohomish'
matches = dl.places.find(place)
if not matches: st()
aoi = matches[0]
location = dl.places.shape(place)

# resolution, tilesize, pad
tiles = dl.raster.dltiles_from_shape(5, 4000, 16, location) # 2048

# make sure we have features.
feature_collection = get_feature_collection('L8SR', aoi)
while not feature_collection['features']:
  feature_collection = get_feature_collection('L8SR', aoi)

shuffle(tiles['features'])

# russ = (47.8496568,-121.9752158)
pprint(len(tiles['features']))
for tile in tiles['features'][:10]:

  ids = [f['id'] for f in feature_collection['features']]
  # st()
# ('L8SR', ['red', 'green', 'blue', 'cloud', 'bright',
# 'qa_snow', 'qa_water', 'qa_cirrus', 'qa_cloud', 'nir',
# 'swir1', 'swir2', 'aerosol', 'cirrus', 'thermal', 'sr_cirrus',
# 'sr_cloud', 'sr_adjacent_cloud', 'sr_cloud_shadow', 'sr_water',
# 'aerosol_level', 'ipflags_enum', 'alpha', 'evi', 'visual_cloud_mask',
# 'rsqrt', 'ndwi2', 'ndwi1', 'ndvi', 'ndwi', 'bai']), 
  arr, meta = dl.raster.ndarray(
      ids,
      # keep frequencies low to high?
      bands=['swir2','swir1','red','bai'],
      scales=[[0,4000],[0,4000],[0,4000],[0, 65535]],
      data_type='Byte',# Float32' 'Float64' 'Byte'
      resolution=5,
      cutline=tile['geometry'],
  )
  plt.figure(figsize=[7,7], facecolor='k')
  plt.axis('off')
  plt.imshow(arr)
  save_image(aoi)
plt.show()