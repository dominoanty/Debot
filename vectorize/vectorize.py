import gensim
import os

import params

BLANK_VECTOR = [0 for i in range(200)]

# model = gensim.models.KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), 'glove.twitter.27B.200d.w2v.txt'),unicode_errors='ignore', binary=False)
model = gensim.models.KeyedVectors.load(os.path.join(os.path.dirname(__file__), 'twitter.w2v'), mmap='r')

def vectorize_filter(token_list):
    vector_form = []
    for token in token_list:
        if token in model:
            vector_form.append(model[token])
    vector_form = vector_form[:min(len(vector_form), params.VEC_PADDING)]
    lenv = len(vector_form)
    for i in range(lenv, params.VEC_PADDING):
        vector_form.append(BLANK_VECTOR)
    return vector_form
