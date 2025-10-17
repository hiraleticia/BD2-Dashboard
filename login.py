import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Login - Spotify Dashboard",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# CSS personalizado com cores do seu design
st.markdown("""
<style>
    /* Remove padding padrão */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Fundo gradient */
    .stApp {
        background: linear-gradient(to bottom, #0D1B2A 0%, #08121E 100%);
    }
    
    /* Container principal de login */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .login-container {
        background-color: #1B263B;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
        max-width: 768px;
        width: 100%;
        overflow: hidden;
    }
    
    /* Título */
    .form-title {
        color: #E0E1DD;
        font-size: 30px;
        text-align: center;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .form-subtitle {
        color: #BFC0C2;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Logo */
    .logo-container {
        text-align: center;
        font-size: 4rem;
        margin: 20px 0;
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #0D1B2A !important;
        border: 1px solid #415A77 !important;
        border-radius: 6px !important;
        color: #E0E1DD !important;
        padding: 12px !important;
    }
    
    .stTextInput > label {
        color: #BFC0C2 !important;
        font-size: 14px !important;
    }
    
    /* Botão de login */
    .stButton > button {
        width: 60%;
        background-color: #1ED760 !important;
        color: #0D1B2A !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 10px !important;
        margin: 10px auto !important;
        display: block !important;
    }
    
    .stButton > button:hover {
        background-color: #39FF7E !important;
        border: 1px solid #fff !important;
    }
    
    /* Link */
    .forgot-password {
        text-align: center;
        margin-top: 15px;
    }
    
    .forgot-password a {
        color: #1ED760;
        text-decoration: none;
        font-size: 14px;
    }
    
    .forgot-password a:hover {
        text-decoration: underline;
    }
    
    /* Mensagem lateral */
    .side-message {
        background-color: #1ED760;
        color: #0D1B2A;
        padding: 40px;
        text-align: center;
        border-radius: 0 12px 12px 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 480px;
    }
    
    .msg-dash {
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .msg {
        font-size: 20px;
        font-weight: 500;
    }
    
    /* Info box */
    .stAlert {
        background-color: rgba(30, 215, 96, 0.1) !important;
        border: 1px solid #1ED760 !important;
        color: #E0E1DD !important;
    }
</style>
""", unsafe_allow_html=True)



# Usuário está logado - Redireciona para dashboard
# (Substitui: window.location.href = '../../index.html')

st.markdown(f"""
<div style='text-align: center; padding: 50px;'>
    <h2 style='color: #1ED760;'>Entre na sua conta:</h2>
    <p style='color: #BFC0C2; font-size: 18px;'>Redirecionando para o dashboard...</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎵 Login", use_container_width=True):
        # Se você tem múltiplas páginas, use:
        st.switch_page("pages/spotify.py")
        st.info("Clique para ir ao dashboard (configure as páginas)")
    

# Auto-redirect após 2 segundos (opcional)
st.markdown("""
<script>
    setTimeout(function() {
        // window.location.href = 'dashboard.html';
    }, 2000);
</script>
""", unsafe_allow_html=True)