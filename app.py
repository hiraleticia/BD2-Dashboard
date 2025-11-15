import streamlit as st
import sqlalchemy
import psycopg2
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from db import run_query

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

# ------ TAB ARTISTA ------
def get_top3_musicas_art(id_do_artista):
    # Top 3 músicas mais ouvidas de um artista
    query = '''
    SELECT 
        musica.nome,
        escutamusica.numero_reproducoes    
    FROM musica
        JOIN escutamusica ON musica.id_da_musica = escutamusica.id_da_musica
        JOIN album ON musica.id_album = album.id_album
        JOIN conteudo ON album.id_album = conteudo.id
        WHERE conteudo.id_do_artista = %s
            ORDER BY escutamusica.numero_reproducoes DESC
            LIMIT 3; '''
    return run_query(query, (id_do_artista,))


def get_art_mais_seguidores():
    query = '''
    SELECT Conta.nome, COUNT(Seguir.id_do_usuario) AS total_seguidores
    FROM Seguir 
        JOIN Conta ON Seguir.id_da_conta = Conta.id
        JOIN Artista ON Artista.id_do_artista = Conta.id
        GROUP BY Conta.nome
        ORDER BY total_seguidores DESC
        LIMIT 1;'''
    return run_query(query)


def get_album_mais_salvo_do_artista(id_do_artista):
    # Query para o album mais salvo de um artista específico
    query = """
    SELECT
        C_ALBUM.nome AS Nome_do_Album,
        COUNT(SA.id_album) AS Total_de_Vezes_Salvo
    FROM
        SalvaAlbum SA 
    JOIN
        Album ALB ON SA.id_album = ALB.id_album
    JOIN
        Conteudo C_ALBUM ON ALB.id_album = C_ALBUM.id 
    WHERE
        C_ALBUM.id_do_artista = %s  -- Parâmetro para o ID do artista
    GROUP BY
        C_ALBUM.nome
    ORDER BY
        Total_de_Vezes_Salvo DESC
    LIMIT 1;"""

    return run_query(query, (id_do_artista,))


# ------ TAB GERAL ------
def get_top_5_musicas_geral():
    # 5 musicas mais ouvidas no spotify
    query = """
    SELECT
        M.nome AS Nome_da_Musica,
        C.nome AS Nome_do_Album,
        SUM(EM.numero_reproducoes) AS Total_de_Reproducoes
    FROM
        EscutaMusica EM
    JOIN
        Musica M ON EM.id_da_musica = M.id_da_musica
    JOIN
        Album A ON M.id_album = A.id_album
    JOIN
        Conteudo C ON A.id_album = C.id
    GROUP BY
        M.id_da_musica, M.nome, C.nome
    ORDER BY
        Total_de_Reproducoes DESC
    LIMIT 5;"""

    return run_query(query)


def get_top_10_albuns_com_mais_faixas():
    # Busca o ranking de top 10 álbuns com mais músicas
    query = """
        SELECT a.nome, COUNT(m.id_da_musica) AS total_de_musicas
        FROM Musica AS m
            JOIN Album AS a ON m.id_album = a.id_album
            GROUP BY a.nome
                ORDER BY total_de_musicas DESC
                LIMIT 10;"""

    return run_query(query)


def get_top5_albuns_salvos():
    # Top 5 albuns mais seguidos
    query = '''
    SELECT Conteudo.nome, COUNT(SalvaAlbum.id_da_conta) AS total_salvos
    FROM SalvaAlbum 
        JOIN Album ON SalvaAlbum.id_album = Album.id_album
        JOIN Conteudo ON Album.id_album = Conteudo.id
        GROUP BY Conteudo.nome
            ORDER BY total_salvos DESC
            LIMIT 5;'''
    return run_query(query)


def get_top5_podcast_seguidos():
    # Top 5 podcasts mais seguidos
    query = '''
    SELECT Conteudo.nome, COUNT(SeguePodcast.id_da_conta) AS total_seguidores
    FROM SeguePodcast
        JOIN Podcast ON SeguePodcast.id_podcast = Podcast.id_podcast
        JOIN Conteudo ON Podcast.id_podcast = Conteudo.id
        GROUP BY Conteudo.nome
            ORDER BY total_seguidores DESC
            LIMIT 5;'''

    return run_query(query)


def get_art_5album():
    # Nomes dos artistas que possuem mais de 5 albuns publicados
    query = """
    SELECT Conta.nome FROM Conta, Artista, Conteudo, Album
    WHERE Conta.id = Artista.id_do_artista
        AND Artista.id_do_artista = Conteudo.id_do_artista
        AND Conteudo.id = Album.id_album
        GROUP BY Conta.nome
        	HAVING COUNT(Album.id_album) > 5;"""

    return run_query(query)


def get_art_mais_mus_publi():
    # Artista com o maior número de músicas publicadas
    query = '''
    SELECT MIN(Conta.nome) FROM Artista, Conta, Conteudo, Album, Musica
    WHERE Artista.id_do_artista = Conta.id
        AND Conteudo.id_do_artista = Artista.id_do_artista
        AND Album.id_album = Conteudo.id
        AND Musica.id_album = Album.id_album
        GROUP BY Conta.nome
            HAVING COUNT(Musica.id_da_musica) = (
            SELECT MAX(total) FROM (
                SELECT COUNT(Musica.id_da_musica) AS total
                    FROM Artista, Conta, Conteudo, Album, Musica
                        WHERE Artista.id_do_artista = Conta.id
                            AND Conteudo.id_do_artista = Artista.id_do_artista
                            AND Album.id_album = Conteudo.id
                            AND Musica.id_album = Album.id_album
                            GROUP BY Conta.nome
    )
    );'''
    return run_query(query)


# ------ TAB USUÁRIO -------
def get_top1_musica_ouvida(user_id):
    # A música mais ouvida do usuário
    query = '''
    SELECT Musica.nome, EscutaMusica.numero_reproducoes 
    FROM EscutaMusica
        JOIN Musica ON EscutaMusica.id_da_musica = Musica.id_da_musica
        WHERE EscutaMusica.id_da_conta = %s
        ORDER BY EscutaMusica.numero_reproducoes DESC
        LIMIT 1;'''
    return run_query(query, (user_id,))


def get_top1_episodio_ouvido():
    query = '''
    SELECT Episodio.nome, EscutaEpisodio.numero_reproducoes
    FROM EscutaEpisodio
        JOIN Episodio ON EscutaEpisodio.id_episodio = Episodio.id_episodio
        WHERE EscutaEpisodio.id_da_conta = :id_usuauio_logado
        ORDER BY EscutaEpisodio.numero_reproducoes DESC
        LIMIT 1;'''
    return run_query(query)


def get_top1_art_ouvido(user_id):
    # Artista mais ouvido pelo usuário
    query = '''
    WITH ReproducoesMusica AS ( 
    -- Calcula o total de reproduções de músicas por Artista para o usuário
    SELECT Conteudo.id_do_artista, 
    SUM(EscutaMusica.numero_reproducoes) AS total_reproducoes 
        FROM EscutaMusica 
        JOIN Musica ON EscutaMusica.id_da_musica = Musica.id_da_musica
        JOIN Album ON Musica.id_album = Album.id_album 
        JOIN Conteudo ON Album.id_album = Conteudo.id 
        WHERE EscutaMusica.id_da_conta = %s
        GROUP BY Conteudo.id_do_artista 
    ),
    ReproducoesEpisodio AS ( 
    -- Calcula o total de reproduções de episódios por Artista para o usuário
    SELECT Conteudo.id_do_artista, 
    SUM(EscutaEpisodio.numero_reproducoes) AS total_reproducoes
        FROM EscutaEpisodio 
        JOIN Episodio ON EscutaEpisodio.id_episodio = Episodio.id_episodio 
        JOIN Podcast ON Episodio.id_podcast = Podcast.id_podcast 
        JOIN Conteudo ON Podcast.id_podcast = Conteudo.id 
        WHERE EscutaEpisodio.id_da_conta = %s 
            GROUP BY Conteudo.id_do_artista 
    )
    -- Une os resultados e busca o artista com a maior contagem
    SELECT Conta.nome, 
    SUM(TabelaTemp.total_reproducoes) AS reproducoes_totais
        FROM ( 
            SELECT id_do_artista, total_reproducoes FROM ReproducoesMusica
            UNION ALL 
            SELECT id_do_artista, total_reproducoes FROM ReproducoesEpisodio 
        ) AS TabelaTemp
            JOIN Artista ON TabelaTemp.id_do_artista = Artista.id_do_artista 
            JOIN Conta ON Artista.id_do_artista = Conta.id
            GROUP BY Conta.nome
            ORDER BY reproducoes_totais DESC 
            LIMIT 1;'''
    return run_query(query, (user_id, user_id))


def get_genero_album_ouvido(user_id):
    # Gênero de album mais ouvido pelo usuário
    query = '''
    SELECT Conteudo.genero, 
    SUM(EscutaMusica.numero_reproducoes) AS reproducoes_totais
        FROM EscutaMusica 
        JOIN Musica ON EscutaMusica.id_da_musica = Musica.id_da_musica
        JOIN Album ON Musica.id_album = Album.id_album
        JOIN Conteudo ON Album.id_album = Conteudo.ID
            WHERE EscutaMusica.id_da_conta = %s
            GROUP BY Conteudo.genero
            ORDER BY reproducoes_totais DESC
            LIMIT 1;'''
    return run_query(query, (user_id,))


def get_genero_podcast_ouvido(user_id):
    # Gênero de podcast mais ouvido pelo usuário
    query = '''
    SELECT Conteudo.genero, 
    SUM(EscutaEpisodio.numero_reproducoes) AS reproducoes_totais
        FROM EscutaEpisodio
            JOIN Episodio ON EscutaEpisodio.id_episodio = Episodio.id_episodio
        JOIN Podcast ON Episodio.id_podcast = Podcast.id_podcast
        JOIN Conteudo ON Podcast.id_podcast = Conteudo.id
            WHERE EscutaEpisodio.id_da_conta = %s
            GROUP BY Conteudo.genero
            ORDER BY reproducoes_totais DESC
            LIMIT 1;'''
    return run_query(query, (user_id,))


def get_total_musicas_usuario(user_id):
    query = """
        SELECT COUNT(*) as total_musicas
        FROM escutamusica
            WHERE id_da_conta = %s;"""
    return run_query(query, (user_id,))

def get_top5_musicas_ouvidas(user_id):
    query = '''
    SELECT musica.nome,
        escutamusica.numero_reproducoes
    FROM musica
        JOIN escutamusica ON musica.id_da_musica = escutamusica.id_da_musica
        WHERE escutamusica.id_da_conta = %s
        GROUP BY musica.id_da_musica, musica.nome, escutamusica.numero_reproducoes
        ORDER BY escutamusica.numero_reproducoes DESC
        LIMIT 5;
    SELECT musica.nome,
        escutamusica.numero_reproducoes
    FROM musica
        JOIN escutamusica ON musica.id_da_musica = escutamusica.id_da_musica
        WHERE escutamusica.id_da_conta = %s
        GROUP BY musica.id_da_musica, musica.nome, escutamusica.numero_reproducoes
        ORDER BY escutamusica.numero_reproducoes DESC
        LIMIT 5;'''
    return run_query(query, (user_id,))

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

    st.header("🎤 Análise dos Artistas")

    # --- 1. DESTAQUES GERAIS DA CATEGORIA ---
    st.subheader("Destaques da Categoria")
    df_mais_seguidores = get_art_mais_seguidores()
    if not df_mais_seguidores.empty:
        artista_nome = df_mais_seguidores.iloc[0]['nome']
        seguidores = df_mais_seguidores.iloc[0]['total_seguidores']
        st.metric(label="Artista com Mais Seguidores",
                  value=artista_nome,
                  delta=f"{seguidores} seguidores")
    else:
        st.info("Não foi possível carregar o artista com mais seguidores.")

    st.markdown("---")

    # --------- 1) Dropdown de artista ---------
    st.subheader("Selecione um artista para análise")

    query_artistas = """
        SELECT a.id_do_artista, c.nome
        FROM Artista a
        JOIN Conta c ON a.id_do_artista = c.id
        ORDER BY c.nome;
    """
    df_artistas = run_query(query_artistas)

    artista_escolhido = st.selectbox(
        "Digite para filtrar artistas:",
        df_artistas["nome"].tolist()
    )

    id_artista = int(df_artistas[df_artistas["nome"] == artista_escolhido]["id_do_artista"].iloc[0])

    st.success(f"Artista selecionado: {artista_escolhido}")

    col_metric_1, col_metric_2 = st.columns(2)

    # Métrica: Top 3 Músicas
    # Métrica: Top 3 Músicas
    with col_metric_1:
        st.markdown("<h5>Top 3 Músicas Mais Ouvidas</h5>", unsafe_allow_html=True)
        df_top3_musicas = get_top3_musicas_art(id_artista)  # Usando a função corrigida

        if not df_top3_musicas.empty:
            # 1. Criar uma string formatada para a lista
            lista_musicas_formatada = ""

            # 2. Iterar sobre o DataFrame para construir a lista
            # Usamos .reset_index() para garantir a numeração 1, 2, 3
            for index, row in df_top3_musicas.reset_index().iterrows():
                # Formata o texto de "reprodução"
                plays_text = "reprodução" if row['numero_reproducoes'] == 1 else "reproduções"

                # Adiciona à string, ex: "1. Nome da Música (10 reproduções)"
                lista_musicas_formatada += f"{index + 1}. **{row['nome']}** ({row['numero_reproducoes']} {plays_text})\n"

            # 3. Exibir a lista com st.markdown
            st.markdown(lista_musicas_formatada)

        else:
            st.info("Este artista não possui músicas em ranking.")

    # Métrica: Álbum Mais Salvo
    with col_metric_2:
        st.markdown("<h5>Álbum Mais Salvo</h5>", unsafe_allow_html=True)
        df_album_salvo = get_album_mais_salvo_do_artista(id_artista)
        if not df_album_salvo.empty:
            album_nome = df_album_salvo.iloc[0]['nome_do_album']
            salvos = df_album_salvo.iloc[0]['total_de_vezes_salvo']
            st.metric(label="Álbum Destaque",
                      value=album_nome,
                      delta=f"{salvos} salvos")
        else:
            st.info("Este artista não possui álbuns salvos.")

    st.markdown("---")

    # --------- 2) Dropdown dependente de álbum ---------
    st.subheader("Selecione um álbum deste artista")

    query_albuns = """
        SELECT al.id_album, ct.nome AS nome_album
        FROM Album al
        JOIN Conteudo ct ON al.id_album = ct.id
        WHERE ct.id_do_artista = %s
        ORDER BY nome_album;
    """

    df_albuns = run_query(query_albuns, params=(id_artista,))

    if df_albuns.empty:
        st.warning("Este artista não possui álbuns cadastrados.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        album_escolhido = st.selectbox(
            "Álbuns disponíveis:",
            df_albuns["nome_album"].tolist()
        )
        id_album = int(df_albuns[df_albuns["nome_album"] == album_escolhido]["id_album"].iloc[0])

        st.info(f"Álbum selecionado: {album_escolhido}")

        st.subheader(f"Discografia de {artista_escolhido}")

        # 1. Query para contar músicas por álbum
        query_contagem_musicas = """
                    SELECT
                        ct.nome AS nome_album,
                        COUNT(m.id_da_musica) AS total_musicas
                    FROM Musica m
                    JOIN Album al ON m.id_album = al.id_album
                    JOIN Conteudo ct ON al.id_album = ct.id
                    WHERE ct.id_do_artista = %s
                    GROUP BY ct.nome
                    ORDER BY total_musicas DESC;
                """

        # 2. Executa a query
        df_contagem = run_query(query_contagem_musicas, params=(id_artista,))

        # 3. Verifica se há dados e plota o gráfico
        if not df_contagem.empty:
            fig_bar = px.bar(
                df_contagem,
                x="nome_album",
                y="total_musicas",
                title="Contagem de Músicas por Álbum",
                labels={'nome_album': 'Álbum', 'total_musicas': 'Nº de Músicas'},
                text='total_musicas'  # Mostra o número no topo da barra
            )

            # 4. Aplica o estilo escuro e formatação
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
                plot_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
                title_font_color='#FFFFFF',  # Título branco
                font_color='#FFFFFF',  # Eixos e legendas brancos
                xaxis={'categoryorder': 'total descending'}  # Ordena as barras
            )

            fig_bar.update_traces(
                textposition='outside',  # Posição do texto (fora da barra)
                marker_color='#1ED760'  # Cor das barras (verde Spotify)
            )

            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Este artista não possui músicas cadastradas em álbuns.")

        # Adiciona um separador visual
        st.markdown("---")

        # --------- 3) Gráfico de pizza: músicas mais ouvidas ---------
        st.subheader("Músicas escutadas do álbum selecionado")

        query_musicas = """
            SELECT m.nome AS musica,
                   COUNT(em.id_da_conta) AS reproducoes
            FROM Musica m
            LEFT JOIN EscutaMusica em
                   ON m.id_da_musica = em.id_da_musica
            WHERE m.id_album = %s
            GROUP BY m.nome
            ORDER BY reproducoes DESC;
        """

        df_musicas = run_query(query_musicas, params=(id_album,))

        if df_musicas.empty:
            st.warning("Nenhuma reprodução registrada para este álbum.")
        else:
            fig = px.pie(
                df_musicas,
                names="musica",
                values="reproducoes",
                title=f"Músicas mais escutadas — {album_escolhido}"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Fundo principal transparente
                plot_bgcolor='rgba(0,0,0,0)',  # Fundo da área do gráfico transparente
                font_color='#FFFFFF',  # Cor da fonte (título e legenda)
                legend_font_color = '#FFFFFF',
                title_font_color = '#FFFFFF'
            )
            st.plotly_chart(fig)




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

    df_total_musicas = get_total_musicas_usuario(user_id_logado)
    total_musicas = df_total_musicas.iloc[0]['total_musicas'] if not df_total_musicas.empty else 0
    with col1:
        st.metric("Total de Músicas Ouvidas", total_musicas)

    with col2:

        st.metric("Horas ouvindo", "128h")

    # Métrica 3: Artista Favorito
    df_art_fav = get_top1_art_ouvido(user_id_logado)
    artista_fav = df_art_fav.iloc[0]['nome'] if not df_art_fav.empty else "N/A"
    with col3:
        st.metric("Artistas favoritos", artista_fav)

    # Métrica 2: Gênero de Álbum Favorito
    df_gen_album = get_genero_album_ouvido(user_id_logado)
    genero_album_pref = df_gen_album.iloc[0]['genero'] if not df_gen_album.empty else "N/A"
    with col4:
        st.metric("Gênero Preferido", genero_album_pref)

   

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