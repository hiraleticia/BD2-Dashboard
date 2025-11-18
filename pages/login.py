import streamlit as st
import os
from db import init_connection, run_query

# 1. Função para carregar o CSS
def load_css(file_name):
    """Lê um arquivo CSS e o injeta no Streamlit usando st.markdown."""
    try:
        # Tenta construir o caminho para o arquivo CSS
        # Garante que o caminho seja relativo ao local onde o script está rodando
        css_path = os.path.join("styles", file_name) 
        
        with open(css_path, "r") as f:
            css = f.read()
            # Usa st.markdown para injetar o CSS dentro de uma tag <style>
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error(f"Erro: Arquivo CSS não encontrado em '{css_path}'")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o CSS: {e}")

# Configuração da página (Garante que a barra lateral esteja escondida NO LOGIN)
st.set_page_config(
    page_title="Login - Spotify Dashboard",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed" # ESSENCIAL: Garante que o sidebar não apareça
)

# --- Configuração Inicial de Session State (Importante para evitar KeyErrors) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Se o usuário JÁ estiver logado, redireciona de volta para a Home Page (spotify.py)
if st.session_state.logged_in:
    st.switch_page("app.py") 

# Função de login (chama ao clicar no botão)
def do_login():
    """Lida com a lógica de login e redireciona para a Home Page."""

    username_input = st.session_state.input_username.strip()

    if username_input == "":
        st.error("Por favor, digite seu nome de usuário.")
        return

    # 1. PREPARA A QUERY PARA VALIDAR O USUÁRIO
    query = """
        SELECT id, nome_de_usuario 
        FROM Conta 
        WHERE nome_de_usuario = %s;
    """

    # 2. EXECUTA A QUERY
    # Passamos o nome de usuário como uma tupla (parâmetro)
    try:
        df_user = run_query(query, (username_input,))
    except Exception as e:
        st.error(f"Erro ao verificar usuário")
        return

    # 3. VERIFICA O RESULTADO
    if df_user.empty:
        # Usuário NÃO encontrado
        st.error("Usuário não encontrado. Verifique o nome de usuário.")
        st.session_state.logged_in = False
    else:
        # Usuário ENCONTRADO
        # Armazena as informações do usuário na sessão
        st.session_state.username = df_user.iloc[0]['nome_de_usuario']
        st.session_state.user_id = int(df_user.iloc[0]['id'])
        st.session_state.logged_in = True

        # 4. Redireciona para a página principal
        st.switch_page("app.py")

# CSS personalizado (Mantenha o CSS do seu login.py aqui)
st.markdown("""
<style>
    /* ... (Coloque o CSS do login.py aqui) ... */
    .stApp > header {
        display: none; /* Esconde o cabeçalho padrão do Streamlit */
    }
    /* E o mais importante: Esconde o sidebar no login */
    [data-testid="stSidebar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)


# Layout do Formulário de Login (igual ao que eu fiz antes)
st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1]) 

with col2:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<span class='logo-icon'>🎵</span>", unsafe_allow_html=True)
    st.markdown("<h1 class='form-title'>Spotify Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='form-subtitle'>Entre para ver sua análise e dados gerais.</p>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.text_input(
            "Nome de Usuário:",
            key="input_username", 
            placeholder="Seu nome de usuário ou artista",
            label_visibility="visible"
        )
        
        st.form_submit_button("Entrar", on_click=do_login, type="primary")

    st.info("O login é apenas pelo nome de usuário para fins do projeto.")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)