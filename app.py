import streamlit as st
import sqlalchemy
import psycopg2
import pandas as pd
import plotly.express as px
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

conn = init_connection()


@st.cache_data(ttl=3600)
def run_query(query, params=None):
    """Executa query e retorna DataFrame"""
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Erro na query: {e}")
        return pd.DataFrame()


def get_pokemon_data():
    """Nomes dos artistas que possuem mais de 5 albuns publicados"""
    query = """
    SELECT Conta.nome FROM Conta, Artista, Conteudo, Album
    WHERE Conta.id = Artista.id_do_artista
        AND Artista.id_do_artista = Conteudo.id_do_artista
        AND Conteudo.id = Album.id_album
        GROUP BY Conta.nome
        	HAVING COUNT(Album.id_album) > 5;""" 
    
    return run_query(query)

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
    
    df_artistas = get_pokemon_data()

    # Verifica se o DataFrame não está vazio antes de tentar exibir
    if not df_artistas.empty:
        st.subheader("Artistas com mais de 5 Álbuns")
        # Opção 1: Exibir como uma tabela interativa (recomendado para DataFrames)
        st.dataframe(df_artistas) 
        
        # Opção 2: Exibir como uma tabela estática
        # st.table(df_artistas) 
        
        # Opção 3: Exibir o conteúdo (Streamlit decide o melhor formato)
        # st.write(df_artistas) 
    else:
        st.warning("Nenhum artista encontrado com mais de 5 álbuns ou ocorreu um erro na query.")

   

    # Placeholder para gráficos

    col1, col2 = st.columns(2)

    with col1:

        st.info("🎵 Total de músicas: 1.234")

        st.info("👥 Total de artistas: 456")

    with col2:

        st.info("📀 Total de álbuns: 789")

        st.info("⏱️ Tempo total: 45h 23min")

   

    # Conteúdo placeholder

    with st.expander("Ver mais detalhes"):

        for i in range(5):

            st.write(f"Informação detalhada {i+1}")

   

    st.markdown("</div>", unsafe_allow_html=True)



# TAB 2: Análise de Artistas

with tab2:

    st.markdown("<div class='content-box'>", unsafe_allow_html=True)

   

    # Barra de pesquisa

    st.markdown("<div class='search-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:

        artista_pesquisa = st.text_input(

            "🔍 Pesquisar artista",

            placeholder="Pesquise por um artista",

            label_visibility="collapsed"

        )

    with col2:

        pesquisar_btn = st.button("🔍 Pesquisar", type="primary")

    st.markdown("</div>", unsafe_allow_html=True)

   

    # Título dinâmico

    if artista_pesquisa and pesquisar_btn:

        st.header(f"🎤 Análise do artista: {artista_pesquisa}")

        st.success(f"Mostrando resultados para: {artista_pesquisa}")

       

        # Placeholder para dados do artista

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric("Total de músicas", "42")

        with col2:

            st.metric("Popularidade", "85/100")

        with col3:

            st.metric("Gênero principal", "Pop")

       

        # Mais informações

        with st.expander("Ver análise completa"):

            for i in range(5):

                st.write(f"Detalhe da análise {i+1}")

    else:

        st.header("🎤 Análise dos Artistas")

        st.info("👆 Use a barra de pesquisa acima para buscar um artista")

        st.subheader("Aqui ficarão os gráficos da Análise dos Artistas")

       

        # Conteúdo placeholder

        for i in range(5):

            st.write(f"Informação {i+1}")

   

    st.markdown("</div>", unsafe_allow_html=True)



# TAB 3: Análise do Usuário

with tab3:

    st.markdown("<div class='content-box'>", unsafe_allow_html=True)

    st.header(f"👤 Análise de {st.session_state.username}")

    st.subheader("Aqui ficarão os gráficos da Análise do Usuário")

   

    # Métricas do usuário

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric("Músicas ouvidas", "523")

    with col2:

        st.metric("Horas ouvindo", "128h")

    with col3:

        st.metric("Artistas favoritos", "34")

    with col4:

        st.metric("Gênero preferido", "Rock")

   

    # Mais detalhes

    st.markdown("---")

    st.subheader("📈 Histórico de audição")

   

    # Conteúdo placeholder

    with st.expander("Ver estatísticas detalhadas"):

        for i in range(5):

            st.write(f"Estatística {i+1}")

   

    st.markdown("</div>", unsafe_allow_html=True)



# Rodapé

st.markdown("---")

st.markdown(

    "<p style='text-align: center; color: #888;'>Dashboard Spotify Analytics © 2025</p>",

    unsafe_allow_html=True

)