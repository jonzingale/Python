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
  rand_date = datetime.date(2016, randint(6,8), randint(1,28)) # june - august
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

  feature_collection = dl.metadata.search(const_id=const_id,
                                          start_time=rand_start,
                                          end_time=rand_end,
                                          limit=10, place=aoi['slug'])
  return(feature_collection)

def save_image(aoi):
  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond

  filename = "./images/%s/%s.png" % (aoi, mu_sec)
  savefig(filename, dpi=300, facecolor='k')
  time.sleep(2)
  if os.stat(filename).st_size < 2*10**6: os.remove(filename)

# Find potential AOI matches
aoi = 'hungary'
matches = dl.places.find(aoi)
iceland = dl.places.shape(aoi)

# resolution, tilesize, pad
tiles = dl.raster.dltiles_from_shape(60.0, 2048, 16, iceland)
# iceland_tiles = [38, 31, 23, 18, 17, 16, 12, 10, 3, 2]
# tile = tiles['features'][38]

feature_collection = get_feature_collection('L8', matches[0])

for tile in tiles['features'][:10]:
  ids = [f['id'] for f in feature_collection['features']]

  arr, meta = dl.raster.ndarray(
      ids,
      bands=['red','green','blue','alpha'],
      scales=[[0,4000],[0,4000],[0,4000],None],
      data_type='Byte',# Float32' 'Float64' 'Byte'
      resolution=60,
      cutline=tile['geometry'],
  )
  plt.figure(figsize=[7,7], facecolor='k')
  plt.axis('off')
  plt.imshow(arr)
  save_image(aoi)
plt.show()