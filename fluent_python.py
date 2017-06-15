import collections
from random import choice

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

# def key_shuffle(deck)