from pdb import set_trace as st
import csv
import re

# cleaning library data for neural net.

# verify that this path works as it should.
FILENAME = '~/Desktop/books_book_view.csv'

def get_titles_and_prefixes():
  title_words, lccn_prefix = [], []
  with open(FILENAME, newline='') as csvfile:
    book_csv = csv.reader(csvfile, delimiter=',')
    next(book_csv, None) # skip header
    for row in book_csv:
      # title cleaning
      words = row[1].split()
      for word in words:
        ww = re.sub('\W+', '', word).lower()
        if len(ww) > 2: title_words.append(ww)

      # prefix cleaning
      mt = re.match('^\D+',row[3])
      if mt : lccn_prefix.append(mt[0])

  # uniquify
  title_words = list(set(title_words))
  lccn_prefix = list(set(lccn_prefix))

  return([title_words, lccn_prefix])


resp = get_titles_and_prefixes()
print("title words:\n%s\n\nprefixes:\n%s" % (resp[0], resp[1]))
