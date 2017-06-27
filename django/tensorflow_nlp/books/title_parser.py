import nltk


sentence = 'Dang dude! That was the last burrito in the house.'
tokens = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)
entities.draw()