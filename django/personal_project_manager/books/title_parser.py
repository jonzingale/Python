from pdb import set_trace as st
from nltk.tree import Tree
import nltk

ss = 'The red tree is staring out of the foggy window.'

tokens = nltk.word_tokenize(ss)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
# entities.draw()

print(tagged)
