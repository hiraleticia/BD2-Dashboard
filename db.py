import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

@st.cache_resource
def init_connection():
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return None

@st.cache_data(ttl=3600)
def run_query(query, params=None):
    """Executa query e retorna DataFrame"""
    try:
        # Pega a conexão cacheada
        conn = init_connection()
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Erro na query: {e}")
        return pd.DataFrame()