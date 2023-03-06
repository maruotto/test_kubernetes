from keras.datasets import imdb
import numpy as np
import keras
from nltk import word_tokenize
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.preprocessing import sequence
import nltk

config = tf.ConfigProto()
config.gpu_options.allow_growth = False
set_session(tf.Session(config=config))

model = keras.models.load_model("")
model._make_predict_function()

reverse_word_index = dict([(value, key) for (key, value) in word_to_id.items()])

def decode_back_sentence(decoded):
    decoded_review = ' '.join([reverse_word_index[i] for i in decoded])
    return decoded_review

def predict(sentence):

    encoded = encode_sentence(sentence)

    pred = np.array([encoded])
    pred = vectorize_sequences(pred)
    a = model.predict(pred)
    return str(a[0][0])

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

def encode_sentence(sentence):
    test=[1]
    for word in word_tokenize(sentence):
        word_id = word_to_id.get(word, word_to_id["<UNK>"])
        if word_id > 9999:
            word_id = word_to_id["<UNK>"]
        test.append(word_id)
    return test