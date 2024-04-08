import psycopg2
import pandas as pd
import numpy as np

# Connexion à la base de données PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="nom_de_la_base",
    user="nom_utilisateur",
    password="mot_de_passe"
)

# Création d'un curseur
cursor = conn.cursor()

# Nom de la table à charger
table_name = "nom_de_la_table"

# Requête pour récupérer les données
query = f"SELECT * FROM {table_name}"
cursor.execute(query)
data = cursor.fetchall()

# Récupération des noms de colonnes
cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
column_names = [desc[0] for desc in cursor.description]

# Création d'un DataFrame Pandas
df = pd.DataFrame(data, columns=column_names)

# Parcours des colonnes et normalisation des colonnes de type float entre 0 et 1
for col in df.columns:
    if df[col].dtype == 'float64':
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Affichage du DataFrame normalisé
print(df)

# Fermeture de la connexion
cursor.close()
conn.close()