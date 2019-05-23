from cleaning_data import *
from pdb import set_trace as st
import pci_neural_net as nn
from random import randint

mynet = nn.librarynet('nn.db')

TRUE_LCCN_QUERY = "select ROWID from url where url='%s'"
WORDS, LCCN_WS = get_titles_and_prefixes()
PREFIX_IDS = mynet.get_ids('url')

def fresh_start():
  mynet.droptables()
  mynet.maketables()
  mynet.insertdata(WORDS, 'word')
  mynet.insertdata(LCCN_WS, 'url')

def setup_random_training(): # get prefixes too.
  pairs = title_prefix_pairs()
  rand_index = randint(0, len(pairs)-1)
  return(pairs[rand_index])

def title_ids(title_words):
  query, word_ids = "select ROWID from word where word='%s'", []

  for word in title_words:
    word_id = mynet.qq(query % word)[0]
    word_ids.append(word_id)
  return(word_ids)

# TODO: Getting title_ids needs to be abstracted.
# I don't want to rely on hand cleaning titles
# which are input and finding their IDS manually.
def get_best_guess(mynet, title_ids): # put this in pci_neural_net
  result = mynet.getresult(title_ids, PREFIX_IDS)
  url_index = result.index(max(result)) + 1 # max index
  prefix = mynet.qq('select url from url where ROWID=%d' % url_index)[0]
  return(prefix)

def guessing_test(mynet):
  for i in range(10): # test n different input titles.
    title_words, lccn = setup_random_training()

    list1 = title_ids(title_words)
    true_lccn = mynet.qq(TRUE_LCCN_QUERY % lccn)[0] - 1

    # generates hiddennode if one is not present.
    # mynet.generatehiddennode(list1, PREFIX_IDS)

    # GUESSING CODE:
    print("\ntitle: %s, lccn: %s" % ((' ').join(title_words), lccn)) # SELECTED TEXT
    print("Best LCCN PREFIX Guess: %s" % get_best_guess(mynet, list1))

def training_test(mynet):
  for i in range(10): # test n different input titles.
    title_words, lccn = setup_random_training()

    list1 = title_ids(title_words)
    true_lccn = mynet.qq(TRUE_LCCN_QUERY % lccn)[0] - 1

    # generates hiddennode if one is not present.
    mynet.generatehiddennode(list1, PREFIX_IDS)

    # TRAINING CODE:
    print(f"Before Training: {mynet.getresult(list1, PREFIX_IDS)}\n")
    for i in range(3):
      mynet.trainquery(list1, PREFIX_IDS, true_lccn)
      result = []
      for val in mynet.getresult(list1, PREFIX_IDS): result.append(round(val, 3))
      print("After Training: %s" % result)

# fresh_start()
# training_test(mynet)
guessing_test(mynet)
# mynet.showtablesrows()
# st()
