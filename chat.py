import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import random
import pickle

import colorama
from colorama import Fore, Style, Back
colorama.init()

with open("intents/intents-bitext-01.json") as file:
    data = json.load(file)
    
    
# Main chat function
def chat(msg):
    # Load trained model
    model = keras.models.load_model('models/csb-model-1')
    
    
    # load tokenizer object
    with open("tokenizer.pickle", 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    # Load label encoder object
    with open("label_encoder.pickle", "rb") as enc:
        lbl_encoder = pickle.load(enc)
        
    # parameters
    max_len = 20
    
    
    # Get response
    result = model.predict(keras.preprocessing.sequence.pad_sequences(
        tokenizer.texts_to_sequences([msg]), truncating='post', maxlen=max_len
    ))
    tag = lbl_encoder.inverse_transform([np.argmax(result)])
    
    for i in data['intents']:
        if i['tag'] == tag:
            response = np.random.choice(i['responses'])
    
    return response