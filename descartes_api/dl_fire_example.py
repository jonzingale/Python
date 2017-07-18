from IPython.display import display, Image
from descarteslabs.services import Places
from descarteslabs.services import Metadata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from copy import deepcopy
from skimage import measure
from skimage.morphology import dilation #, erosion, opening, closing, white_tophat
from skimage.morphology import disk
from pprint import pprint
from pylab import *
import descarteslabs as dl
import matplotlib.pyplot as plt
import numpy as np

from pdb import set_trace as st
from random import *
import datetime

# Find potential AOI matches
# matches = dl.places.find('new-mexico_taos')
# matches = dl.places.find('ohio_cuyahoga')
matches = dl.places.find('texas_travis')
# pprint(matches)

# The first one looks good, so let's make that our area of interest.
aoi = matches[0]
shape = dl.places.shape(aoi['slug'], geom='low')

def get_bands():
  bands = [them['const_id'] for them in dl.metadata.sources()]
  return(bands)

def get_feature_collection(const_id, aoi):
  # searches for imagery
  rand_date = datetime.date(2012 + randint(0,4), randint(1,12), randint(1,28))
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

  feature_collection = dl.metadata.search(const_id=const_id,
                                          start_time=rand_start,
                                          end_time=rand_end,
                                          limit=40, place=aoi['slug'])
  return(feature_collection)

def appropriate_ranges(band_names, const_id):
  ranges, band_data = [], dl.raster.get_bands_by_constellation(const_id)

  for band in band_names:
    if band in band_data.keys():
      ranges.append(band_data[band]['valid_range'])
    else: ranges.append(None)#[0,1]) # default
  return(ranges)

def get_randomized_bands(const_id):
  len_bands_list, features = 0, []

  while len_bands_list < 4 or not features:
    bands = get_bands()
    rando = randint(0, len(bands)-1)
    const_id = bands[rando]
    feature_collection = get_feature_collection(const_id, aoi)
    features = feature_collection['features']
    avail_bands = dl.raster.get_bands_by_constellation(const_id).keys()
    len_bands_list = len(avail_bands)
  bands_list = list(avail_bands)
  shuffle(bands_list)
  return([bands_list[:4], feature_collection])

def print_available_bands(const_id='modis09'):
  somebands, feature_collection = get_randomized_bands(const_id) 
  scale_ranges = appropriate_ranges(somebands, const_id)

  # Collect the id's for each feature
  ids = [f['id'] for f in feature_collection['features']] # ARBITRARILY LIMIT

  # Rasterize the features.
  arr, meta = dl.raster.ndarray(
      ids,
      bands=somebands,
      scales=scale_ranges,
      data_type='Byte', # Choose an output type of "Byte" (uint8)
      resolution=60, # Choose 60m resolution
      cutline=shape['geometry'], # Apply a cutline of Taos county
  )

  plt.figure(figsize=[10,10], facecolor='k')
  plt.axis('off')
  plt.imshow(arr)
  pprint(somebands)
  # pprint(meta['bands'])

  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond
  place_name = aoi['name'] # make sure Directory exists.

  savefig("./images/%s/random_%s%s" % (place_name, place_name, mu_sec),
          dpi=300, facecolor='k')#, transparent=True)
          # orientation='portrait', papertype=None, format=None,
          # transparent=False, bbox_inches=None, pad_inches=0.1,
          # frameon=None, edgecolor='w')

for i in range(25): print_available_bands()
plt.show()