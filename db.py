import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sqlalchemy
from sqlalchemy import text

@st.cache_resource
def init_connection():
    load_dotenv()
    try:
        db_url = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        # pool_pre_ping=True ajuda a evitar conexões perdidas (broken pipe)
        return sqlalchemy.create_engine(db_url, pool_pre_ping=True)
    except Exception as e:
        st.error(f"Erro na conexão com SQLAlchemy: {e}")
        return None

@st.cache_data(ttl=3600)
def run_query(query, params=None):
    try:
        # Pega o engine cacheado
        engine = init_connection()
        with engine.connect() as conn:
            # Se houver parâmetros, usamos o método seguro do SQLAlchemy
            if params:
                # pd.read_sql aceita parâmetros como dict ou tuple/list dependendo do driver,
                # mas passar diretamente para o pandas via conexão SQLAlchemy é o mais seguro.
                df = pd.read_sql(text(query), conn, params=params)
            else:
                df = pd.read_sql(text(query), conn)
        return df
    except Exception as e:
        st.error(f"Erro na query: {e}")
        return pd.DataFrame()