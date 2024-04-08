import pandas as pd
from sqlalchemy import create_engine
import os
import logging

# Configuration
input_file = 'data/raw_data.csv'
output_file = 'data/processed_data.parquet'
db_connection_string = 'postgresql://username:password@host:port/database'

# Set up logging
logging.basicConfig(filename='data_pipeline.log', level=logging.INFO)

def extract_data():
    """
    Extrait les données brutes depuis un fichier CSV.
    """
    try:
        df = pd.read_csv(input_file)
        logging.info(f"Données extraites depuis {input_file}")
        return df
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction des données : {e}")
        raise

def transform_data(df):
    """
    Transforme les données brutes.
    """
    try:
        # Effectuer des transformations sur les données
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = df['amount'].astype(float)
        logging.info("Données transformées")
        return df
    except Exception as e:
        logging.error(f"Erreur lors de la transformation des données : {e}")
        raise

def load_data(df):
    """
    Charge les données transformées dans une base de données PostgreSQL.
    """
    try:
        engine = create_engine(db_connection_string)
        df.to_parquet(output_file)
        logging.info(f"Données chargées dans {output_file}")
        df.to_sql('processed_data', engine, if_exists='replace', index=False)
        logging.info("Données chargées dans la base de données")
    except Exception as e:
        logging.error(f"Erreur lors du chargement des données : {e}")
        raise

def main():
    """
    Exécute le pipeline de données.
    """
    try:
        raw_data = extract_data()
        transformed_data = transform_data(raw_data)
        load_data(transformed_data)
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution du pipeline : {e}")

if __name__ == "__main__":
    main()