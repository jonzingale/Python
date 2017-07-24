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

place = 'washington_snohomish'
location = dl.places.shape(place)
tiles = dl.raster.dltiles_from_shape(20, 2048, 16, location)
regions = tiles['features']

coords = [] # get coords for all regions.
for region in regions: # remove last coord
  coords.append(region['geometry']['coordinates'][0][0:-1])

# counter_clockwise_segment.
def orth(x, y): return(array([-y, x]))

# vectorize three coords: c1 --> c2 --> c3
def oriented_arrows(c1, c2, c3): return(c2 - c1, c3 - c2)

# positive when in the region. 
def is_inside(pt, e1, e2):
  cond = pt.dot(orth(*e1)) > 0 and pt.dot(orth(*e2)) > 0
  return(cond)

# Test 1
def test1():
  # is able to determine inside or outside for random coords and pts.
  rando = randint(1, len(coords)) - 1
  p, q, r, *ss = [array(vect) for vect in coords[rando]]
  vv, ww = oriented_arrows(p, q, r)
  pt_between = array((p+r)/2)

  inside = is_inside(pt_between, vv, ww) == True
  outside = is_inside(vv, pt_between, ww) == False
  print([inside, outside])

test1()

# Test 2
russ = array([47.8496568,-121.9752158])

def euclidean_dist(pt, qt): return(pdist([pt, qt]))

def flatten(lst):
  flat_list = []
  for elem in lst: flat_list += elem 
  return(flat_list)

def closest_vertex(pt):
  f_coords = flatten(coords)
  pairs = [(cc, euclidean_dist(russ, cc)) for cc in f_coords]
  return(min(pairs)[0])

def possible_same_vertices(vert):
  f_coords = flatten(coords)
  # for cc in f_coords: print(euclidean_dist(vert, cc))  
  close = [cc for cc in f_coords if euclidean_dist(vert, cc) < 0.5]
  return(close)

def find_relevant_verts(vert):
  cc = next(coord for coord in coords if vert in coord)

  v_dex = cc.index(vert)
  verts = [cc[v_dex - i - 1 % len(cc)] for i in range(3)]
  return([array(vert) for vert in verts])

def get_region_from_coords(coords):
  for region in regions:
    r_coords = region['geometry']['coordinates'][0]
    if coords in r_coords: return(region)

def test2():
  # Calculates correct region from vertex closest to russ's house.
  best_vertex = closest_vertex(russ)
  possible_verts = possible_same_vertices(best_vertex)

  for p_vert in possible_verts:
    verts = find_relevant_verts(p_vert)
    vv, ww = oriented_arrows(*verts)
    if is_inside(russ, vv, ww):
      region = get_region_from_coords(list(verts[0]))
      print("\n%s\n" % region)

test2()