import psycopg2
import numpy as np

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="nom_de_la_base_de_donnees",
    user="nom_utilisateur",
    password="mot_de_passe"
)

# Création d'un curseur
cur = conn.cursor()

# Requête SQL pour récupérer les données
cur.execute("SELECT * FROM nom_de_la_table")

# Récupération des données
data = cur.fetchall()

# Fermeture de la connexion
conn.close()

# Normalisation des colonnes de type float entre 0 et 1
for i in range(len(data[0])):
    if isinstance(data[0][i], float):
        column_data = [row[i] for row in data]
        min_value = min(column_data)
        max_value = max(column_data)
        data = [[row[j] if j != i else (row[j] - min_value) / (max_value - min_value) for j in range(len(row))] for row in data]

# Création d'un générateur qui renvoie les données par groupe de 50 lignes
def data_generator():
    for i in range(0, len(data), 50):
        yield data[i:i+50]

# Utilisation du générateur
for batch in data_generator():
    print(batch)