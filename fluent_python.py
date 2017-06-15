from random import choice, getrandbits
import collections
import math

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
  ranks = [str(n) for n in range(2, 11)] + list('JQKA')
  suits = 'spades diamonds clubs hearts'.split()

  def __init__(self):
    self._cards = [Card(rank, suit) for suit in self.suits
    for rank in self.ranks]

  def __len__(self):
    return len(self._cards)

  # this method extends [i] to a deck,
  # also iterable now 'for card in deck'. 
  def __getitem__(self, position):
    return self._cards[position]


beer_card = Card('7', 'diamonds')

deck = FrenchDeck()
grab_one = choice(deck)

slice_eq = list(range(0,101,10)) == list(range(0,101,1))[::10]

def rev_deck(deck):
  for c in reversed(deck): print(c)

# Shuffling #
def key_shuffle(deck):
  size = len(deck)
  zipped = list(zip(rands(size), deck))
  zipped.sort()
  it = zip(*zipped)
  return list(it)[1]

def rands(n):
  ary = []
  logn = math.log(n**3,2)
  for i in range(n):
    ary.append(getrandbits(math.floor(logn)))
  return ary

print(key_shuffle(deck))








