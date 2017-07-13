from cleaning_data import *
from pdb import set_trace as st
import pci_neural_net as nn
from random import randint

TRUE_LCCN_QUERY = "select ROWID from url where url='%s'"
WORDS, LCCN_WS = get_titles_and_prefixes()

mynet = nn.librarynet('nn.db')

def fresh_start():
  mynet.droptables()
  mynet.maketables()
  mynet.insertdata(WORDS, 'word')
  mynet.insertdata(LCCN_WS, 'url')

def setup_random_training(): # get prefixes too.
  pairs = title_prefix_pairs()
  rand_index = randint(0, len(pairs)-1)
  return(pairs[rand_index])

def get_ids(table_name): # move to sqlite_extended.
  query = "select ROWID from %s" % table_name
  resp, ids = mynet.qqs(query), []
  for row in resp: ids.append(row[0])
  return(ids)

def title_ids(title_words):
  query, word_ids = "select ROWID from word where word='%s'", []

  for word in title_words:
    word_id = mynet.qq(query % word)[0]
    word_ids.append(word_id)
  return(word_ids)

def get_best_guess(mynet, title_ids): # put this in pci_neural_net
  prefix_ids = get_ids('url')
  result = mynet.getresult(title_ids, prefix_ids)
  url_index = result.index(max(result)) + 1 # max index
  prefix = mynet.qq('select url from url where ROWID=%d' % url_index)[0]
  return(prefix)

def training_test(mynet):
  list2 = get_ids('url')

  for i in range(10): # test 10 different input titles.
    title_words, lccn = setup_random_training()

    # SELECTED TEXT
    print("\n\ntitle: %s, lccn: %s\n" % (title_words, lccn))

    list1 = title_ids(title_words)
    true_lccn = mynet.qq(TRUE_LCCN_QUERY % lccn)[0] - 1

    # generates hiddennode if one is not present.
    mynet.generatehiddennode(list1, list2)

    print(f"Before Training: {mynet.getresult(list1, list2)}\n")

    for i in range(3):
      mynet.trainquery(list1, list2, true_lccn)
      result = []
      for val in mynet.getresult(list1, list2): result.append(round(val, 3))
      print(f"After Training: {result}")

    print("Best LCCN PREFIX Guess: %s" % get_best_guess(mynet, list1))


# fresh_start()
training_test(mynet)
# mynet.showtablesrows()
# st()
