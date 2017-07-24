# inside_outside calculates for a given geocoord
# and a collection of tiles, which tile the geocoord
# belongs to. Some assumptions are made:
# 1) Each tile region is convex.
# 2) Coords given by the api are pre-ordered along the perimeter.

import descarteslabs as dl
from scipy.spatial.distance import pdist
from pdb import set_trace as st
from random import randint
from numpy import *
# Ack: tile geocoords do not match precisely.
# one would figure that if a given vertex is the endpoint
# for a bounding line of one tile it must be the an endpoint
# for the same bounding line on another tile. This observation
# can not be relied upon.

class inside_outside:
  def __init__(self, point, a_pt, b_pt, c_pt):
    endpoints = [array(pt) for pt in [a_pt, b_pt, c_pt]]
    vv, ww = self._oriented_arrows(*endpoints)
    self.inside = self.is_inside(array(point), vv, ww)

  # counter_clockwise_segment.
  def _orth(self, x, y): return(array([-y, x]))

  # vectorize three coords: c1 --> c2 --> c3
  def _oriented_arrows(self, c1, c2, c3): return(c2 - c1, c3 - c2)

  # positive when in the region. 
  def is_inside(self, pt, e1, e2):
    cond = pt.dot(self._orth(*e1)) > 0 and pt.dot(self._orth(*e2)) > 0
    return(cond)

class pointed_region(inside_outside):
  def __init__(self, point, place):
    location = dl.places.shape(place)
    tiles = dl.raster.dltiles_from_shape(20, 2048, 16, location)
    self.regions = tiles['features']

    self.point = point
    self.coords = self.all_coords()
    self.closest_vertex = self.closest_vertex(point)

  def all_coords(self):
    coords = [] # get coords for all regions.
    for region in self.regions: # remove wrap-around coord
      coords.append(region['geometry']['coordinates'][0][0:-1])
    return(coords)

  # euclidean distance
  def _dist(self, pt, qt): return(pdist([pt, qt]))

  def _flatten(self, lst):
    flat_list = []
    for elem in lst: flat_list += elem 
    return(flat_list)

  def closest_vertex(self, pt):
    f_coords = self._flatten(self.coords)
    pairs = [(cc, self._dist(array(pt), cc)) for cc in f_coords]
    return(min(pairs)[0])

  def _possible_same_vertices(self):
    f_coords = self._flatten(self.coords)
    vert = self.closest_vertex
    close = [cc for cc in f_coords if self._dist(vert, cc) < 0.5]
    return(close)

  def _find_relevant_verts(self, vert):
    cc = next(coord for coord in self.coords if vert in coord)

    v_dex = cc.index(vert)
    verts = [cc[v_dex - i - 1 % len(cc)] for i in range(3)]
    return(verts)

  def _get_region_from_coords(self, coords):
    for region in self.regions:
      r_coords = region['geometry']['coordinates'][0]
      if coords in r_coords: return(region)

  def possible_regions(self):
    possible_verts = self._possible_same_vertices()

    for p_vert in possible_verts:
      verts = self._find_relevant_verts(p_vert)
      io = inside_outside(self.point, *verts)

      if io.inside:
        region = self._get_region_from_coords(list(verts[0]))
        return(region)