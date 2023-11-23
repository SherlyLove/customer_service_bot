import json
import numpy as np
import tensorflow as tf
import pickle


from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import SGD


from sklearn.preprocessing import LabelEncoder


# Load json file and extract required data
with open('intents/intents-bitext-01.json') as file:
    data = json.load(file)
    
training_sentences = []
training_labels = []
labels = []
responses = []


for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses.append(intent['responses'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
        
num_classes = len(labels)

# Convert target labels into a model understandable form
lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels = lbl_encoder.transform(training_labels)


# vectorize text data corpus
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>" # out of vocabulary token

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)  # make all training text sequences into the same size


# Define Neural Network Architecture for proposed model
model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

optimizer = SGD(lr=0.01)
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

model.summary()


# Model training
epochs = 500
history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)


# Save trained model
model.save("models/csb-model-1")

# Save fitted tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
# save the fitted label encoder
with open('label_encoder.pickle', 'wb') as enc_file:
    pickle.dump(lbl_encoder, enc_file, protocol=pickle.HIGHEST_PROTOCOL)
    
print("Model created and saved successfully")