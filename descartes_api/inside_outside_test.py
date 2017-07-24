# inside_outside_test.py
from inside_outside import *

coords1 = [[-123.00429591625054, 48.07359441877019], [-122.44584023727208, 48.07225822450253], [-122.44178049578387, 48.44650658572517]]
russ_region = {'geometry': {'type': 'Polygon', 'coordinates': [[[-123.00429591625054, 48.07359441877019], [-122.44584023727208, 48.07225822450253], [-122.44178049578387, 48.44650658572517], [-123.00432738986194, 48.447860347804706], [-123.00429591625054, 48.07359441877019]]]}, 'type': 'Feature', 'properties': {'cs_code': 'EPSG:32610', 'pad': 16, 'zone': 10, 'key': '2048:16:20.0:10:0:130', 'tilesize': 2048, 'resolution': 20.0, 'ti': 0, 'outputBounds': [499680.0, 5324480.0, 541280.0, 5366080.0], 'tj': 130}}

def test1():
  # is able to determine inside or outside for random coords and pts.
  aa, bb, cc = [array(pt) for pt in coords1]
  pt_between = list(array((aa+cc)/2))

  good_case = inside_outside(pt_between, aa, bb, cc).inside == True
  bad_case = inside_outside(aa, pt_between, bb, cc).inside == False
  print([good_case, bad_case])

def test2():
  # Calculates correct region from vertex closest to Russ.
  russ = [47.8496568, -121.9752158]
  pr = pointed_region(russ, 'washington_snohomish')
  region = pr.possible_regions()
  print(region == russ_region )

test1()
test2()