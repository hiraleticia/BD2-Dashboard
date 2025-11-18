import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy
import warnings

@st.cache_resource
def init_connection():
    load_dotenv()
    try:
        # Constrói a URL de conexão
        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        # Cria o engine com pool_pre_ping para evitar conexões perdidas
        return sqlalchemy.create_engine(db_url, pool_pre_ping=True)
    except Exception as e:
        st.error(f"Erro na conexão com SQLAlchemy: {e}")
        return None

@st.cache_data(ttl=3600)
def run_query(query, params=None):
    conn = None
    try:
        # Pega o engine cacheado
        engine = init_connection()
        conn = engine.raw_connection()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            df = pd.read_sql(query, conn, params=params)

        return df
    except Exception as e:
        st.error(f"Erro na query: {e}")
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()