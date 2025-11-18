import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy

@st.cache_resource
def init_connection():
    load_dotenv()
    try:
        # 1. Construir a string de conexão (URI) para o SQLAlchemy
        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

        # 2. Criar um engine do SQLAlchemy
        engine = sqlalchemy.create_engine(db_url)
        return engine  # Retorna o engine

    except Exception as e:
        st.error(f"Erro na conexão com SQLAlchemy: {e}")
        return None

@st.cache_data(ttl=3600)
def run_query(query, params=None):
    try:
        # Pega o engine cacheado
        engine = init_connection()

        # 3. pd.read_sql funciona nativamente com o engine do SQLAlchemy
        # Isso elimina o UserWarning
        df = pd.read_sql(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Erro na query: {e}")
        return pd.DataFrame()