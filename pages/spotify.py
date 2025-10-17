import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Dashboard Análise do Spotify",
    # page_icon="../images/logo_spotify.svg",
    layout="wide"
)

# # Inicializar session_state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = "Usuário"

# CSS personalizado
st.markdown("""
<style>
    /* Cabeçalho */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: #191414;
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Título principal */
    .main-title {
        text-align: center;
        color: #1DB954;
        font-size: 2.5rem;
        margin: 1rem 0;
    }
    
    .image-label {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    
    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1DB954;
        color: white;
    }
    
    /* Barra de pesquisa */
    .search-container {
        margin: 2rem 0;
    }
    
    /* Conteúdo */
    .content-box {
        background-color: #f9f9f9;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho com informações de login
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(f"<h4 style='color: #1DB954;'>👤 Logado como: {st.session_state.username}</h4>", unsafe_allow_html=True)
with col2:
    st.button("🚪 Sair", type="secondary")
        

# Título e logo
st.markdown("<h1 class='main-title'>Dashboard para análise Spotify</h1>", unsafe_allow_html=True)

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