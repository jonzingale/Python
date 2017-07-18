from IPython.display import display, Image
from descarteslabs.services import Places
from descarteslabs.services import Metadata
from mpl_toolkits.axes_grid1 import make_axes_locatable
from copy import deepcopy
from skimage import measure
from skimage.morphology import dilation
from skimage.morphology import disk
from pprint import pprint
from pylab import *
import descarteslabs as dl
import matplotlib.pyplot as plt
import numpy as np

from pdb import set_trace as st
from random import *
import datetime

# MODIS9 : Moderate Resolution Imaging Spectroradiometer
# L7, L8 : LandSat Satellite
# S2A: Sentinel 2A

# Find potential AOI matches
# matches = dl.places.find('ireland')
matches = dl.places.find('new-mexico_taos')
# matches = dl.places.find('oregon_multnomah')
# matches = dl.places.find('new-mexico_santa-fe')
# matches = dl.places.find('ohio_cuyahoga')
# matches = dl.places.find('texas_travis')
if not matches: st()

# The first one looks good, so let's make that our area of interest.
aoi = matches[0]
shape = dl.places.shape(aoi['slug'], geom='low')

def get_bands():
  bands = [them['const_id'] for them in dl.metadata.sources()]
  return(bands)

def get_feature_collection(const_id, aoi):
  rand_date = datetime.date(2016, randint(1,12), randint(1,28))
  rand_start = rand_date.strftime('%Y-%m-%d')
  rand_end = (rand_date + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

  feature_collection = dl.metadata.search(const_id=const_id,
                                          start_time=rand_start,
                                          end_time=rand_end,
                                          limit=10, place=aoi['slug'])
  return(feature_collection)

def view_bands_and_ranges(const_id):
  avail_bands = dl.raster.get_bands_by_constellation(const_id).keys()
  ranges = appropriate_ranges(avail_bands, const_id)
  paired = zip(avail_bands, ranges)
  return(list(paired))

def appropriate_ranges(band_names, const_id):
  band_data = dl.raster.get_bands_by_constellation(const_id)
  ranges, physical_ranges = [], []

  for band in band_names:
    if band in band_data.keys():
      ranges.append(band_data[band]['valid_range'])
      physical_ranges.append(band_data[band]['physical_range'])
    else: ranges.append(None)
  return([ranges, physical_ranges])

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
  return([bands_list[:4], feature_collection, const_id])

def get_raster(bands, const_id, feature_collection):
  # Collect the id's for each feature
  ids = [f['id'] for f in feature_collection['features']]
  scales, physical_ranges = appropriate_ranges(bands, const_id)

  # Rasterize the features.
  arr, meta = dl.raster.ndarray(
      ids,
      bands=bands,
      scales=physical_ranges,
      data_type='Byte',# Float32' 'Float64' 'Byte'
      resolution=60, # 60m
      cutline=shape['geometry'],
  )
  plt.figure(figsize=[7,7], facecolor='k')
  plt.axis('off')
  plt.imshow(arr)

import os
import time
def save_image(aoi, const_id, somebands):
  mu_sec = datetime.datetime.time(datetime.datetime.now()).microsecond
  place_name = aoi['name'] # make sure Directory exists.

  feature_name = ('_').join([const_id] + sorted(somebands))
  pprint(feature_name)

  filename = "./images/%s/%s%s.png" % (place_name, feature_name, mu_sec)
  savefig(filename, dpi=300, facecolor='k')
  time.sleep(3)
  if os.stat(filename).st_size < 4*10**5: os.remove(filename)

def print_available_bands(const_id='L8'):
  somebands, feature_collection, const_id = get_randomized_bands(const_id) 
  get_raster(somebands, const_id, feature_collection)
  save_image(aoi, const_id, somebands)

for i in range(1): print_available_bands()
plt.show()
