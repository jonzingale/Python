from pdb import set_trace as st
from itertools import *
import csv
import re

# cleaning library data for neural net.

FILENAME = './books_book_view.csv'
BLACKLIST_WORDS = ['of', 'the', 'to', 'and', ':', 'in', 'a', 'de', 'la', 'an',
                   'its']

# TODO: uncouple get_titles_and_prefixes from title_prefix_pairs.

def title_prefix_pairs(): # words generally for database
  title_words, lccn_prefix, pairs = [], [], []

  with open(FILENAME, newline='') as csvfile:
    book_csv = csv.reader(csvfile, delimiter=',')
    next(book_csv, None) # skip header

    for row in book_csv:
      # title cleaning
      title = re.sub(',', '', row[1])
      words = title.lower().split()
      words = takewhile(lambda x: x!='[by]' and x!='by', words)

      clean_title = []
      for word in words:
        if word not in BLACKLIST_WORDS:
          clean_title.append(word)

      for word in words:
        ww = re.sub('\W+', '', word).lower()
        if len(ww) > 2: title_words.append(ww)

      # prefix cleaning
      mt = re.match('^\D+',row[3])
      if mt : lccn_prefix.append(mt[0])
      pairs.append((clean_title, mt[0]))
  return(pairs)

def get_titles_and_prefixes(): # cleaned titles as titles
  title_words, lccn_prefix = [], []
  pairs = title_prefix_pairs()

  for (title, lccn) in pairs:
    title_words += title
    lccn_prefix.append(lccn)

  # uniquify
  title_words = list(set(title_words))
  lccn_prefix = list(set(lccn_prefix))

  return([title_words, lccn_prefix])

# FOR TESTING:
# words, prefixes = get_titles_and_prefixes()
# print("title words:\n%s\n\nprefixes:\n%s" % (words, prefixes))
