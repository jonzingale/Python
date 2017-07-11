from math import tanh
from sqlite3 import dbapi2 as sqlite
from pdb import set_trace as st
import pandas as pd
import time

GETSTRENGTH_QUERY = 'select strength from %s where fromid=%d and toid=%d'
SETSTRENGTH_QUERY = 'select rowid from %s where fromid=%d and toid=%d'
INSSTRENGTH_QUERY = 'insert into %s (fromid, toid, strength) values (%d,%d,%f)'
UPDATE_STRENGTH_QUERY = 'update %s set strength=%f where rowid=%d'
GETHIDDEN_QUERY = "select rowid from hiddennode where create_key='%s'"
CREATEHIDDEN_QUERY = "insert into hiddennode (create_key) values ('%s')"
GETWORDHIDDEN_QUERY = 'select toid from wordhidden where fromid=%d'
GETURLHIDDEN_QUERY = 'select fromid from hiddenurl where toid=%d'

TABLES = ['word','wordhidden', 'hiddennode', 'hiddenurl','url']
# ROWID

def dtanh(y): return(1.0-y*y)

# WORD -WORDHIDDEN-> HIDDENNODE -HIDDENURL-> URL
class searchnet:
  def __init__(self, dbname):
    self.con = sqlite.connect(dbname)
    self.cur = self.con.cursor()

    # .headers on
    # .mode column

  def q(self, query):
    resp = self.con.execute(query).fetchall()
    return(resp)

  def __del__(self):
    self.con.close()

  def droptables(self):
    for table in TABLES:
      self.con.execute(f"drop table {table}")

  def inserturls(self, ary): # insert words into database
    # verify that words are unique. If so stuff'em in the database.
    url_rows = self.con.execute('select * from url').fetchall()

    current_urls = []
    for url in url_rows: current_urls.append(url[0])

    for url in ary:
      if url not in current_urls:
        self.con.execute("insert into url values('%s')" % url)
        # test that url is in database.
        query = "select word from word where word='%s'" % word
        stored_row = self.con.execute(query).fetchone()
        current_urls.append(stored_row[0])

    text = "Total urls: %s" % current_urls
    print(text)

  def insertwords(self, ary): # insert words into database
    # verify that words are unique. If so stuff'em in the database.
    word_rows = self.con.execute('select * from word').fetchall()

    current_words = []
    for word in word_rows: current_words.append(word[0])

    for word in ary:
      if word not in current_words:
        self.con.execute("insert into word values('%s')" % word)
        # test that word is in database.
        query = "select word from word where word='%s'" % word
        stored_row = self.con.execute(query).fetchone()
        current_words.append(stored_row[0])

    text = "Total Words: %s" % current_words
    print(text)

  def showtablerows(self):
    for table in TABLES:
      rows = self.con.execute(f"select * from {table}")
      print(f"{table}")
      for row in rows: print(row)
      print('\n')

  def maketables(self):
    self.con.execute('create table word(word)')
    self.con.execute('create table wordhidden(fromid,toid,strength)')
    self.con.execute('create table hiddennode(create_key)')
    self.con.execute('create table hiddenurl(fromid,toid,strength)')
    self.con.execute('create table url(url)')
    self.con.commit()

  def getstrength(self, fromid, toid, layer):
    if layer == 0: table = 'wordhidden'
    else: table = 'hiddenurl'
    res = self.con.execute(GETSTRENGTH_QUERY % (table, fromid, toid)).fetchone()
    if res == None:
      if layer == 0: return(-0.2)
      if layer == 1: return(0)
    return(res[0])

  def setstrength(self,fromid,toid,layer,strength):
    if layer == 0: table='wordhidden'
    else: table = 'hiddenurl'
    res = self.con.execute(SETSTRENGTH_QUERY % (table, fromid, toid)).fetchone()
    if res == None:
      self.con.execute(INSSTRENGTH_QUERY % (table, fromid, toid, strength))
    else:
      rowid = res[0]
      self.con.execute(UPDATE_STRENGTH_QUERY % (table, strength, rowid))

  def generatehiddennode(self, wordids, urls):
    print(wordids)

    if len(wordids) > 3: return(None) # SHORT KEYS?
    # Check if a node already exists for this set of words.
    createkey = '_'.join(sorted([str(wi) for wi in wordids]))
    res = self.con.execute(GETHIDDEN_QUERY % createkey).fetchone()

    # If node does not already exist.
    if res == None:
      st()
      cur = self.con.execute(CREATEHIDDEN_QUERY % createkey)
      hiddenid = cur.lastrowid
      
      # Set default weights
      for wordid in wordids:
        self.setstrength(wordid, hiddenid, 0, 1.0/len(wordids))
      for urlid in urls:
        self.setstrength(hiddenid, urlid, 1, 0.1)
      self.con.commit()

  # FeedForward
  def getallhiddenids(self, wordids, urlids):
    l1={}
    for wordid in wordids:
      cur = self.con.execute(GETWORDHIDDEN_QUERY % wordid)
      for row in cur: l1[row[0]] = 1
    for urlid in urlids:
      cur=self.con.execute(GETURLHIDDEN_QUERY % urlid)
    return(list(l1.keys()))

  def setupnetwork(self, wordids, urlids):
    #value lists
    self.wordids = wordids
    self.hiddenids = self.getallhiddenids(wordids, urlids)
    self.urlids = urlids

    # node outputs
    self.ai = [1.0] * len(self.wordids)
    self.ah = [1.0] * len(self.hiddenids)
    self.ao = [1.0] * len(self.urlids)

    # create weights matrix
    self.wi = [[self.getstrength(wordid, hiddenid, 0) for hiddenid in self.hiddenids] for wordid in self.wordids]
    self.wo = [[self.getstrength(hiddenid, urlid, 1) for urlid in self.urlids] for hiddenid in self.hiddenids]

  def feedforward(self):
    # the only inputs are the query words
    for i in range(len(self.wordids)): self.ai[i] = 1.0

    # hidden activations
    for j in range(len(self.hiddenids)):
      sum = 0.0
      for i in range(len(self.wordids)):
        sum += (self.ai[i] * self.wi[i][j])
      self.ah[j] = tanh(sum)

    # output activations
    for k in range(len(self.urlids)):
      sum = 0.0
      for j in range(len(self.hiddenids)):
        sum += (self.ah[j] * self.wo[j][k])
      self.ao[k] = tanh(sum)

    return self.ao[:]

  # SETUP TEST FOR FEEDFORWARD 
  def getresult(self, wordids, urlids):
    self.setupnetwork(wordids, urlids)
    return(self.feedforward())

  # BackPropagation
  def backPropagate(self, targets, N=0.5):
    # calculate errors for output
    output_deltas = [0.0] * len(self.urlids)
    for k in range(len(self.urlids)):
      error = targets[k] - self.ao[k]
      output_deltas[k] = dtanh(self.ao[k]) * error

    # calculate errors for hidden layer
    hidden_deltas = [0.0] * len(self.hiddenids)
    for j in range(len(self.hiddenids)):
      error = 0.0
      for k in range(len(self.urlids)):
        error += (output_deltas[k] * self.wo[j][k])
      hidden_deltas[j] = dtanh(self.ah[j]) * error

    # update output weights
    for j in range(len(self.hiddenids)):
      for k in range(len(self.urlids)):
        change = output_deltas[k] * self.ah[j]
        self.wo[j][k] += (N * change)

    # update input weights
    for i in range(len(self.wordids)):
      for j in range(len(self.hiddenids)):
        change = hidden_deltas[j] * self.ai[i]
        self.wi[i][j] += (N * change)

  # TRAINING
  def trainquery(self, wordids, urlids, selectedurl):
    # generate a hidden node if necessary
    self.generatehiddennode(wordids, urlids)
    self.setupnetwork(wordids, urlids)
    self.feedforward()

    targets = [0.0] * len(urlids)
    targets[urlids.index(selectedurl)] = 1.0
    self.backPropagate(targets)
    self.updatedatabase()

  def updatedatabase(self):
    # set them to database values
    for i in range(len(self.wordids)):
      for j in range(len(self.hiddenids)):
        self.setstrength(self.wordids[i], self.hiddenids[j], 0, self.wi[i][j])
    for j in range(len(self.hiddenids)):
      for k in range(len(self.urlids)):
        self.setstrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])
    self.con.commit()
