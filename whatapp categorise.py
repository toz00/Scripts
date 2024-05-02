# Charger le modèle entraîné
# Assurez-vous que le modèle est sauvegardé après l'entraînement, par exemple, en utilisant model.save("nom_du_modele")
# Assurez-vous que le chemin du modèle est correct
loaded_model = tf.keras.models.load_model("Whatappmodele")

# Fonction pour prédire l'auteur d'un message
def predict_author(message):
    # Prétraiter le message
    message_seq = tokenizer.texts_to_sequences([message])
    message_pad = pad_sequences(message_seq, maxlen=max_len, padding='post')
    # Prédire l'auteur
    prediction = loaded_model.predict(message_pad)
    # Récupérer le nom de l'auteur à partir de la prédiction
    author = "Alice" if prediction[0] > 0.5 else "Bob"
    return author

# Exemple d'utilisation de la fonction predict_author pour classifier de nouveaux messages
new_message = "J'ai vu un chaton mignon dans la rue."
predicted_author = predict_author(new_message)
print("L'auteur du message est :", predicted_author)