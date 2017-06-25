from pprint import pprint as pp
from pdb import set_trace as st
import os
import re

blacklist = '''\.|HEAD|COMMIT|update.sample|\w+\-(commit|rebase
                 |push|apply|post)|master|index|config'''

def contents_of_crude():
  ff = []
  for root, dir, files in os.walk('./../'):
    for file in files:
      if len(file) < 38 and not re.match(blacklist, file):
        ff.append(file)

  ff.sort()
  pp(ff)

os.system('clear')

contents_of_crude()