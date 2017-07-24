# inside_outside calculates for a given geocoord
# and a collection of tiles, which tile the geocoord
# belongs to. Some assumptions are made:
# 1) Each tile region is convex.
# 2) Coords given counter-clockwise from bottom left.

import descarteslabs as dl
from scipy.spatial.distance import pdist
from numpy import *
# Ack: tile geocoords do not match precisely.
# one would figure that if a given vertex is the endpoint
# for a bounding line of one tile it must be the an endpoint
# for the same bounding line on another tile. This observation
# can not be relied upon.

class inside_outside:
  def __init__(self, point, a_pt, b_pt, c_pt): # *coords?
    endpoints = [array(pt) for pt in [a_pt, b_pt, c_pt]]
    self._oriented_arrows(point, *endpoints)
    self.inside = self.is_inside(point)

  # vectorize three coords: c1 --> c2 --> c3
  def _oriented_arrows(self, pt, c1, c2, c3):
    self.ba = c2 - c1
    self.cb = c3 - c2
    self.pt = array(pt) - c2
    self.mid = (self.cb + self.ba)/2

  # counter_clockwise_segment.
  def orth(self, x, y): return(array([-y, x]))

  def l_dot(self, point):
    return(point.dot(self.orth(*self.ba)) > 0)

  def r_dot(self, point):
    return(point.dot(self.orth(*self.cb)) > 0)

  def acute(self, point):
    return(self.l_dot(point) or self.r_dot(point))

  # positive when in the region.
  def is_inside(self, point):
    pt = self.pt
    dots = self.l_dot(pt) and self.r_dot(pt)
    return(dots == self.acute(pt))

class pointed_region(inside_outside):
  def __init__(self, point, place, res=20, tilesize=2048):
    location = dl.places.shape(place)
    tiles = dl.raster.dltiles_from_shape(res, tilesize, 16, location)
    self.regions = tiles['features']
    self.point = point
    self.coords = self.all_coords()
    self.closest_vertices = self.closest_vertices(point)

  def all_coords(self):
    coords = [] # get coords for all regions.
    for region in self.regions: # remove wrap-around coord
      coords.append(region['geometry']['coordinates'][0][0:-1])
    return(coords)

  def _flatten(self, lst):
    flat_list = []
    for elem in lst: flat_list += elem 
    return(flat_list)

  def closest_vertices(self, pt):
    f_coords = self._flatten(self.coords)
    f_coords.sort(key=lambda x: pdist([array(pt), x]))
    return(f_coords[:8]) # closest 8

  def _find_relevant_verts(self, vert):
    cc = next(coord for coord in self.coords if vert in coord)

    v_dex = cc.index(vert)
    verts = [cc[(v_dex - (i - 1)) % len(cc)] for i in range(3)]
    return(verts)

  def _get_region_from_coords(self, coords):
    for region in self.regions:
      r_coords = region['geometry']['coordinates'][0]
      if coords in r_coords: return(region)

  def possible_regions(self):
    possible_verts = self.closest_vertices
    possible_regions = []

    for p_vert in possible_verts:
      verts = self._find_relevant_verts(p_vert)
      io = inside_outside(self.point, *verts)

      if io.inside:
        region = self._get_region_from_coords(list(verts[1])) # middle vertex
        possible_regions.append(region)

    return(possible_regions)
