import os
from keras.datasets import imdb
import numpy as np
import keras
from nltk import word_tokenize
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.preprocessing import sequence

config = tf.ConfigProto()
config.gpu_options.allow_growth = False
set_session(tf.Session(config=config))

model = keras.models.load_model(os.path.join(os.getcwd(), "model.h5"))
model._make_predict_function()

reverse_word_index = dict([(value, key) for (key, value) in word_to_id.items()])

def predict(data):
    return model.predict(pred)
