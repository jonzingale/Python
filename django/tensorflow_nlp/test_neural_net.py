import pci_neural_net as nn
from pdb import set_trace as st

mynet = nn.searchnet('nn.db')
mynet.droptables()
mynet.maketables()
cur = mynet.con.cursor()

# query('select rowid from wordhidden')
def query(qstring):
  cur.execute(qstring)
  resp = cur.fetchall()
  print(resp)

def test():
  wWorld, wRiver, wBank, wGanges = 101, 102, 103, 104
  uWorldBank, uRiver, uEarth = 201, 202, 203
  list1 = [wWorld, wGanges]
  list2 = [uWorldBank, uRiver, uEarth]
  mynet = nn.searchnet('nn.db')

  print(f"Before Training: {mynet.getresult(list1, list2)}")
  mynet.trainquery(list1, list2, uRiver)
  print(f"After Training: {mynet.getresult(list1, list2)}")

def run_test():
  test()
  mynet.showtablerows()


run_test()

st()