# Let's start with importing all the toolboxes we
# will need for both analysis and vizualization.
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
import numpy as np
import matplotlib.pyplot as plt

from pdb import set_trace as st

# First let's define the AOI as the county in which the Soberanes fire occurred

# Find potential AOI matches
# matches = dl.places.find('california_monterey') # silverton fire? ~7/1/2017
matches = dl.places.find('new-mexico_taos')
pprint(matches)
# The first one looks good, so let's make that our area of interest.
aoi = matches[0]
shape = dl.places.shape(aoi['slug'], geom='low')

# Check for imagery before the start date of July 22nd

feature_collection = dl.metadata.search(const_id='L8', start_time='2016-07-22', end_time='2016-07-31',
                                        limit=10, place=aoi['slug'])
# As the variable name implies, this returns a FeatureCollection GeoJSON dictionary.
# Its 'features' are the available scenes.

print(len(feature_collection['features']))
# The 'id' associated with each feature is a unique identifier into our imagery database.
# In this case there are 4 L8 scenes from adjoining WRS rows.
print([f['id'] for f in feature_collection['features']])

# Now check for imagery in late October, i.e., towards the end of the fire
feature_collection = dl.metadata.search(const_id='L8', start_time='2016-10-15', end_time='2016-10-31',
                                        limit=10, place=aoi['slug'])

print(len(feature_collection['features']))
print([f['id'] for f in feature_collection['features']])

def print_available_bands():
  # Let's print out all the available bands we have for Landsat 8
  L8_bands = dl.raster.get_bands_by_constellation("L8").keys()
  print(L8_bands)
  # Even though the 'bai' listed here stands for Burn Area Index, we need a normalized version of this index
  # We get the NBR (normalized burn ratio) by using the swir2 and nir bands

  # Collect the id's for each feature
  ids = [f['id'] for f in feature_collection['features']]
  # Rasterize the features.
  #  * Select red, green, blue, alpha
  #  * Scale the incoming data with range [0, 10000] down to [0, 4000] (40% TOAR)
  #  * Choose an output type of "Byte" (uint8)
  #  * Choose 60m resolution
  #  * Apply a cutline of Taos county
  arr, meta = dl.raster.ndarray(
      ids,
      bands=['red', 'green', 'blue', 'alpha'],
      scales=[[0,2048], [0, 2048], [0, 2048], None],
      data_type='Byte',
      resolution=60,
      cutline=shape['geometry'],
  )

  # Note: A value of 1 in the alpha channel signifies where there is valid data.
  # We use this throughout the majority of our imagery as a standard way of specifying
  # valid or nodata regions. This is particularly helpful if a value of 0 in a particular
  # band has meaning, rather than specifying a lack of data.

  # We'll use matplotlib to make a quick plot of the image.
  plt.figure(figsize=[10,10])
  plt.axis('off')
  plt.imshow(arr)
  plt.show()

# Let's choose a different band combination to look at the fire scar
# Rasterize the features.
#  * Select swir2, nir, aerosol, alpha
#  * Scale the incoming data with range [0, 10000] down to [0, 4000] (40% TOAR)
#  * Choose an output type of "Byte" (uint8)
#  * Choose 60m resolution for quicker vizualiation
#  * Apply a cutline of Taos county
def choose_different_band_combination(timewindow):
  feature_collection = dl.metadata.search(const_id='L8',
                                          start_time=timewindow[0],
                                          end_time=timewindow[1],
                                          limit=10, place=aoi['slug'])
  # Collect the id's for each feature
  ids = [f['id'] for f in feature_collection['features']]

  arr, meta = dl.raster.ndarray(
      ids,
      bands=['swir2', 'nir', 'aerosol', 'alpha'],
      scales=[[0,4000], [0, 4000], [0, 4000], None],
      data_type='Byte',
      resolution=60,
      cutline=shape['geometry'],
  )
  # We'll use matplotlib to make a quick plot of the image.
  plt.figure(figsize=[8,8])
  plt.axis('off')
  plt.imshow(arr)
  plt.show()

# Now let's track activity in this AOI over 4 time windows
# and look at the 4 false color images.
def track_activity_over_four_windows():
  times=[['2017-03-24','2017-03-30'], ['2017-03-09','2017-03-16'],
         ['2017-03-17','2017-03-24'], ['2017-03-01','2017-03-08']]

  axes = [[0,0],[0,1],[1,0],[1,1]]
  fig, ax = plt.subplots(2,2,figsize=[5,4], dpi=300) # size of raster.
  ax=ax.flatten()
  for iax in ax.reshape(-1):
      iax.get_xaxis().set_ticks([])
      iax.get_yaxis().set_ticks([])

  for i, timewindow in enumerate(times):
      feature_collection = dl.metadata.search(const_id='L8', start_time=timewindow[0], end_time=timewindow[1],
                                          limit=10, place=aoi['slug'])
      ids = [f['id'] for f in feature_collection['features']]
      arr, meta = dl.raster.ndarray(
          ids,
          bands=['swir2', 'nir', 'aerosol', 'alpha'],
          scales=[[0,4000], [0, 4000], [0, 4000], None],
          data_type='Byte',
          resolution=60,
          cutline=shape['geometry'],
      )
      #ax[axes[i][0], axes[i][1]].imshow(arr)
      ax[i].imshow(arr)
      ax[i].set_xlabel('%s' %timewindow[1] , fontsize=8)

  fig.suptitle('Jemez Fire Progress', size=8)
  fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.025, wspace=0.025, hspace=0.025)
  plt.show()


timewindow = ['2017-04-01','2017-04-21'] # 4/21/2017 last real date.
choose_different_band_combination(timewindow)
