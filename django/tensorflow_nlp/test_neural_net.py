import pci_neural_net as nn
from pdb import set_trace as st

WORDS = ["categories", "for", "the", "working", "mathematician", "programming", "collective", "intelligence", "building", "smart", "web", "20", "applications", "elementary", "categories", "elementary", "toposes", "conceptual", "mathematics", "first", "introduction", "to", "thermal", "physics", "methods", "in", "number", "theory", "an", "of", "numbers", "by", "ivan", "niven", "and", "herbert", "zuckerman", "differential", "equations", "dynamical", "systems", "an", "chaos", "gauge", "fields", "knots", "gravity", "finite", "markov", "chains", "john", "kemeny", "laurie", "snell", "de", "la", "grammatologie", "english", "vintage", "murakami", "introduction", "probability", "its", "russian", "algebraic", "geometry", "statistical", "learning", "sets"]
LCCN_WS = ["T", "QA", "QC", "P", "PL", "Q"]

mynet = nn.searchnet('nn.db')

# unless things work.
mynet.droptables()
mynet.maketables()

mynet.insertwords(WORDS)
mynet.inserturls(LCCN_WS)

def get_ids(word_array, table_name):
  query = "select ROWID from %s" % table_name
  resp, ids = mynet.q(query), []

  for row in resp: ids.append(row[0])
  return(ids)

def test(mynet):
  all_words = get_ids(WORDS, 'word')
  list1 = all_words[5:13] # from single title
  list2 = get_ids(LCCN_WS, 'url')

  # generates hiddennode if one is not present.
  mynet.generatehiddennode(list1, list2)

  correct_url = list2[0] # T

  print(f"Before Training: {mynet.getresult(list1, list2)}")
  for i in range(20):
    mynet.trainquery(list1, list2, correct_url)
    result = []
    for val in mynet.getresult(list1, list2): result.append(round(val, 4))
    print(f"After Training: {result}")

def run_test(mynet):
  # mynet.showtablerows()
  test(mynet)

run_test(mynet)
