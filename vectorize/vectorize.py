import gensim
import os
# model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'glove.twitter.27B.200d.w2v.txt'),unicode_errors='ignore', binary=False)
model = gensim.models.KeyedVectors.load(os.path.join(os.path.dirname(__file__), 'twitter.w2v'), mmap='r')
