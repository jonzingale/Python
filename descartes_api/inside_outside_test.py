# inside_outside_test.py
from inside_outside import *

coords1 = [[-123.00429591625054, 48.07359441877019], [-122.44584023727208, 48.07225822450253], [-122.44178049578387, 48.44650658572517]]
pop_region = {'geometry': {'type': 'Polygon', 'coordinates': [[[-81.95750474969289, 41.36681009919029], [-81.71647572302413, 41.368563228576214], [-81.71847704288182, 41.55014052658925], [-81.96017911189826, 41.54837623898916], [-81.95750474969289, 41.36681009919029]]]}, 'type': 'Feature', 'properties': {'cs_code': 'EPSG:32617', 'pad': 16, 'zone': 17, 'key': '4000:16:5.0:17:-4:229', 'tilesize': 4000, 'resolution': 5.0, 'ti': -4, 'outputBounds': [419920.0, 4579920.0, 440080.0, 4600080.0], 'tj': 229}}
               
lakewood = [-81.95750474969289, 41.36681009919029]
pop = [-81.8183898, 41.4907088]

def test1():
  # is able to determine inside or outside for random coords and pts.
  aa, bb, cc = [array(pt) for pt in coords1]
  pt_between = list(array((aa+cc)/2))

  good_case = inside_outside(pt_between, aa, bb, cc).inside == True
  bad_case = inside_outside(aa, pt_between, bb, cc).inside == False
  print([good_case, bad_case])

def test2():
  # Calculates correct region from vertex closest to Russ.
  pr = pointed_region(pop, 'ohio_cuyahoga', 5, 4000)
  regions = pr.possible_regions()
  print(pop_region in regions)

test1()
test2()