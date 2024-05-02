import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# Charger les données à partir de la base de données


connection_string = 'mysql://user:password@localhost/database_name'
data = pd.read_sql_query("SELECT * FROM chats", connection_string)



# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(data['message'], data['author'], test_size=0.2, random_state=42)

# Prétraitement des données texte
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

# Conversion des textes en séquences d'entiers
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Ajout de rembourrage pour que toutes les séquences aient la même longueur
max_len = 20
X_train_pad = pad_sequences(X_train_seq, maxlen=max_len, padding='post')
X_test_pad = pad_sequences(X_test_seq, maxlen=max_len, padding='post')

# Création du modèle
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=64, input_length=max_len),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compilation du modèle
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entraînement du modèle
model.fit(X_train_pad, y_train, epochs=10, batch_size=16, validation_data=(X_test_pad, y_test))
