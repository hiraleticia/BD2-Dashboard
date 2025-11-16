import streamlit as st
import altair as alt
import sqlalchemy
import psycopg2
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from db import run_query
import plot_querys as pq

# ----------------------------------------
# 1. Função para carregar o CSS
# ----------------------------------------
def load_css(file_name):
    """Lê um arquivo CSS e o injeta no Streamlit usando st.markdown."""
    try:
        # Tenta construir o caminho para o arquivo CSS
        # Garante que o caminho seja relativo ao local onde o script está rodando
        css_path = os.path.join("assets/styles", file_name) 
        
        with open(css_path, "r") as f:
            css = f.read()
            # Usa st.markdown para injetar o CSS dentro de uma tag <style>
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error(f"Erro: Arquivo CSS não encontrado em '{css_path}'")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o CSS: {e}")

# ----------------------------------------
# 2. Funções e Verificação de Login
# ----------------------------------------

# Configuração da página (Colapsa a barra lateral no início, a menos que o conteúdo force a aparecer)
st.set_page_config(
    page_title="Dashboard Análise do Spotify",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed" # Tenta colapsar o sidebar
)

# Inicializar/Garantir session_state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = "Usuário Convidado"

# >>> Lógica Principal de Autenticação <<<
# Se o usuário NÃO estiver logado, redireciona para a página de login e interrompe a execução
if not st.session_state.logged_in:
    # Redireciona para o login que está na pasta pages
    st.switch_page("pages/login.py") 
    # st.stop() é opcional aqui, switch_page já faz o trabalho de encerrar o script atual.

# Função de Logout (só é exibida se estiver logado)
def do_logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("pages/login.py") # Redireciona de volta ao login

# ----------------------------------------
# 3. Carregamento do CSS
# ----------------------------------------
load_css("app.css") # <-- Carrega o arquivo .css da página

# ----------------------------------------
# 3. Layout do Dashboard (SÓ EXECUTA SE ESTIVER LOGADO)
# ----------------------------------------

# Cabeçalho com informações de login
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"<h4 style='color: #1ED760;'>👤 Logado como: {st.session_state.username}</h4>", unsafe_allow_html=True)
    with col2:
        # Conecta o botão de sair à função do_logout
        st.button("🚪 Sair", type="secondary", on_click=do_logout)
        
# Título e logo
st.markdown("<h1 class='main-title'>Dashboard para análise Spotify</h1>", unsafe_allow_html=True)

# ... (Restante do seu layout do dashboard (Tabs, métricas, etc.)
# ... (NÃO PRECISA MUDAR O RESTO DO CÓDIGO DO spotify.py)
# ...
col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    # st.image("images\logo_spotify.svg", width=200)

    st.markdown("<p class='image-label'>Um dashboard sobre uma aplicação análoga ao Spotify</p>", unsafe_allow_html=True)



# Sistema de Tabs

tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "🎤 Análise Artistas", "👤 Análise do Usuário"])



# TAB 1: Visão Geral

with tab1:

    st.markdown("<div class='content-box'>", unsafe_allow_html=True)

    st.header("📊 Visão Geral")

    st.subheader("Aqui ficarão os gráficos da Visão Geral")

    # Placeholder para gráficos

    col1, col2 = st.columns(2)

    with col1:

        st.info("🎵 Total de músicas: 1.234")
        st.info("👥 Total de artistas: 456")

        st.subheader("TOP 5 músicas mais reproduzidas: 🎧")

        pq.plot_top5_musicas_geral()

    with col2:

        st.info("📀 Total de álbuns: 789")
        st.info("⏱️ Total de podcasts: 45h 23min")

   

    # Conteúdo placeholder

    with st.expander("Ver mais detalhes"):
        for i in range(5):
            st.write(f"Informação detalhada {i+1}")

    st.markdown("</div>", unsafe_allow_html=True)


# TAB 2: Análise de Artistas

with tab2:
    st.header("🎤 Análise dos Artistas")
    pq.plot_info_artista()


# TAB 3: Análise do Usuário

with tab3:
    # Pegue o ID do usuário da sessão
    user_id_logado = st.session_state.user_id
    username_logado = st.session_state.username

    st.markdown("<div class='content-box'>", unsafe_allow_html=True)
    st.header(f"👤 Análise de {st.session_state.username}")  # Nome vindo do login
    st.subheader("Suas estatísticas pessoais")

    # Métricas do usuário

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pq.plot_total_musicas(user_id_logado)

    with col2:
        pq.plot_tempo_total_escutado(user_id_logado)

    with col3:
        pq.plot_genero_musica_preferido(user_id_logado)
        pq.plot_artista_favorito(user_id_logado)

    with col4:
        pq.plot_musica_favorita(user_id_logado)

    # Mais detalhes

    st.markdown("---")

    st.subheader("📈 Análise de estatísticas")

    # Conteúdo placeholder

    with st.expander("Ver estatísticas detalhadas"):
        pq.plot_top5_musicas_usuario(user_id_logado)

        # st.markdown("---")
   

    st.markdown("</div>", unsafe_allow_html=True)



# Rodapé

st.markdown("---")

st.markdown(

    "<p style='text-align: center; color: #888;'>Dashboard Spotify Analytics © 2025</p>",

    unsafe_allow_html=True

)