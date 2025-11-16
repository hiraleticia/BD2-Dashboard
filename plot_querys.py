import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import queries as q
from db import run_query

#--------------------------------------------
#--------------------GERAL-------------------
#--------------------------------------------
def plot_top5_musicas_geral():
    try:
        df_top_musicas = q.get_top5_musicas_geral()
    except Exception as e:
        st.error(f"Erro ao buscar os dados do banco de dados: {e}")
        df_top_musicas = pd.DataFrame()

    if not df_top_musicas.empty:

        # 2. Criar o Gráfico de Barras com Altair
        chart = alt.Chart(df_top_musicas).mark_bar().encode(
            # Eixo X
            x=alt.X('total_de_reproducoes',
                    title='Total de Reproduções',
                    axis=alt.Axis(format=',')
                    ),
            # Eixo Y
            y=alt.Y('nome_da_musica',
                    title='Música',
                    sort='-x'
                    ),
            # Cor
            color=alt.Color('nome_do_album',
                            title='Álbum',
                            legend=alt.Legend(orient="bottom")
                            ),
            # Tooltip
            tooltip=[
                alt.Tooltip('nome_da_musica', title='Música'),
                alt.Tooltip('nome_do_album', title='Álbum'),
                alt.Tooltip('total_de_reproducoes', title='Reproduções', format=',')
            ]
        ).properties(
            height=350,
            background='transparent'  # <-- ADICIONADO: Fundo principal transparente
        ).interactive()

        # --- INÍCIO DAS CONFIGURAÇÕES MANUAIS DE TEMA ESCURO ---
        chart = chart.configure_view(
            # Fundo da área do gráfico transparente
            fill='transparent',
            strokeWidth=0  # Remove a borda da visualização
        ).configure_axis(
            # Cor do texto e dos eixos
            domainColor='#FFFFFF',  # Cor da linha do eixo (ex: Y)
            gridColor='#555555',  # Cor das linhas de grade (ex: X)
            labelColor='#FFFFFF',  # Cor dos rótulos (ex: nomes das músicas)
            titleColor='#FFFFFF'  # Cor dos títulos dos eixos (ex: "Música")
        ).configure_legend(
            # Cor da legenda
            labelColor='#FFFFFF',
            titleColor='#FFFFFF'
        )

        st.altair_chart(chart, use_container_width=True, theme=None)

    else:
        st.info("Nenhum dado encontrado para as Top 5 músicas.")
   


#--------------------------------------------
#-------------------ARTISTA------------------
#--------------------------------------------
def plot_info_artista():
# --- 1. DESTAQUES GERAIS DA CATEGORIA ---
    st.subheader("Destaques da Categoria")
    df_mais_seguidores = q.get_art_mais_seguidores()
    if not df_mais_seguidores.empty:
        artista_nome = df_mais_seguidores.iloc[0]['nome']
        seguidores = df_mais_seguidores.iloc[0]['total_seguidores']
        st.metric(label="Artista com mais seguidores",
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


    artist_type = q.check_artist_type(id_artista)

    # ----- CASO 1: O ARTISTA É UM MÚSICO -----
    if artist_type == 'musico':
        st.markdown("---")
        st.subheader(f"Análise do Artista: {artista_escolhido}")

        col_metric_1, col_metric_2 = st.columns(2)

        # Métrica: Top 3 Músicas
        with col_metric_1:
            st.markdown("<h5>Top 3 Músicas Mais Ouvidas</h5>", unsafe_allow_html=True)
            df_top3_musicas = q.get_top3_musicas_art(id_artista)
            if not df_top3_musicas.empty:
                lista_musicas_formatada = ""
                for index, row in df_top3_musicas.reset_index().iterrows():
                    plays_text = "reprodução" if row['numero_reproducoes'] == 1 else "reproduções"
                    lista_musicas_formatada += f"{index + 1}. **{row['nome']}** ({row['numero_reproducoes']} {plays_text})\n"
                st.markdown(lista_musicas_formatada)
            else:
                st.info("Este artista não possui músicas em ranking.")

        # Métrica: Álbum Mais Salvo
        with col_metric_2:
            st.markdown("<h5>Álbum Mais Salvo</h5>", unsafe_allow_html=True)
            df_album_salvo = q.get_album_mais_salvo_do_artista(id_artista)
            if not df_album_salvo.empty:
                album_nome = df_album_salvo.iloc[0]['nome_do_album']
                salvos = df_album_salvo.iloc[0]['total_de_vezes_salvo']
                st.metric(label="Álbum Destaque",
                          value=album_nome,
                          delta=f"{salvos} salvamentos")
            else:
                st.info("Este artista não possui álbuns salvos.")

        st.markdown("---")

        # --- Discografia (Gráfico de Barras) ---
        st.subheader(f"Discografia de {artista_escolhido}")
        query_contagem_musicas = """
                    SELECT ct.nome AS nome_album, COUNT(m.id_da_musica) AS total_musicas
                    FROM Musica m
                    JOIN Album al ON m.id_album = al.id_album
                    JOIN Conteudo ct ON al.id_album = ct.id
                    WHERE ct.id_do_artista = %s
                    GROUP BY ct.nome
                    ORDER BY total_musicas DESC;
                """
        df_contagem = run_query(query_contagem_musicas, params=(id_artista,))
        if not df_contagem.empty:
            fig_bar = px.bar(
                df_contagem,
                x="nome_album", y="total_musicas",
                title="Contagem de Músicas por Álbum",
                labels={'nome_album': 'Álbum', 'total_musicas': 'Nº de Músicas'},
                text='total_musicas'
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                title_font_color='#FFFFFF', font_color='#FFFFFF',
                xaxis={'categoryorder': 'total descending'}
            )
            fig_bar.update_traces(textposition='outside', marker_color='#1ED760')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Este artista não possui músicas cadastradas em álbuns.")

        st.markdown("---")

        # --- Análise por Álbum (Dropdown Interativo) ---
        st.subheader("Análise por Álbum")
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
        else:
            album_escolhido = st.selectbox(
                "Selecione um álbum do artista:",
                df_albuns["nome_album"].tolist(),
                key="select_album_musico"  # Key única
            )
            id_album = int(df_albuns[df_albuns["nome_album"] == album_escolhido]["id_album"].iloc[0])

            st.subheader(f'Músicas escutadas do álbum "{album_escolhido}" ')
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
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#FFFFFF', legend_font_color='#FFFFFF',
                    title_font_color='#FFFFFF'
                )
                st.plotly_chart(fig)

    # ----- CASO 2: O ARTISTA É UM PODCASTER -----
    elif artist_type == 'podcaster':
        st.markdown("---")
        st.subheader(f"Análise do Artista: {artista_escolhido}")

        col_metric_1, col_metric_2 = st.columns(2)

        # Métrica: Top 3 Episódios
        with col_metric_1:
            st.markdown("<h5>Top 3 Episódios Mais Ouvidos</h5>", unsafe_allow_html=True)
            df_top3_episodios = q.get_top3_episodios_podcaster(id_artista)

            if not df_top3_episodios.empty:
                lista_episodios_formatada = ""
                for index, row in df_top3_episodios.reset_index().iterrows():
                    plays_text = "reprodução" if row['numero_reproducoes'] == 1 else "reproduções"
                    lista_episodios_formatada += f"{index + 1}. **{row['nome']}** ({row['numero_reproducoes']} {plays_text})\n"
                st.markdown(lista_episodios_formatada)
            else:
                st.info("Este podcaster não possui episódios em ranking.")

        # Métrica: Total de Seguidores do Podcast
        with col_metric_2:
            st.markdown("<h5>Total de Seguidores</h5>", unsafe_allow_html=True)
            df_seguidores = q.get_seguidores_podcast_artista(id_artista)

            if not df_seguidores.empty:
                total_seguidores = df_seguidores.iloc[0]['total_seguidores']
                st.metric(label="Seguidores",
                          value=f"{total_seguidores}")
            else:
                st.info("Nenhuma contagem de seguidores encontrada.")

        st.markdown("---")
        st.subheader("Distribuição de Reproduções por Episódio")

        # 1. Chamar a nova query
        df_all_eps = q.get_all_episode_plays_by_artist(id_artista)

        # 2. Verificar e plotar
        if df_all_eps.empty:
            st.info("Nenhuma reprodução registrada para os episódios deste podcaster.")
        else:
            fig_pie_eps = px.pie(
                df_all_eps,
                names="nome",
                values="numero_reproducoes",
                title=f"Reproduções de Episódios — {artista_escolhido}",
                hole=0.3  # Opcional: cria um gráfico de "rosca" (donut)
            )

            # 3. Aplicar o tema escuro
            fig_pie_eps.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#FFFFFF',
                legend_font_color='#FFFFFF',
                title_font_color='#FFFFFF'
            )
            st.plotly_chart(fig_pie_eps, use_container_width=True)


    # ----- CASO 3: ARTISTA SEM CONTEÚDO -----
    else:
        st.markdown("---")
        st.warning("Este artista não possui álbuns ou podcasts registrados no banco de dados.")


#--------------------------------------------
#-------------------USUARIO------------------
#--------------------------------------------

def plot_total_musicas(user_id_logado):
    df_total_musicas = q.get_total_musicas_usuario(user_id_logado)
    total_musicas = df_total_musicas.iloc[0]['total_musicas'] if not df_total_musicas.empty else 0
    
    st.metric("Total de Músicas Ouvidas", total_musicas)

def plot_tempo_total_escutado(user_id_logado):
    total_segundos = q.get_tempo_total_escutado_segundos(user_id_logado)
    if total_segundos is None:
        total_segundos = 0

    total_minutos = total_segundos // 60
    horas = total_minutos // 60
    minutos = total_minutos % 60

    st.metric("Horas ouvindo", f"{horas}h {minutos}m")

def plot_artista_favorito(user_id_logado):
    df_art_fav = q.get_top1_art_ouvido(user_id_logado)
    artista_fav = df_art_fav.iloc[0]['nome'] if not df_art_fav.empty else "N/A"
    st.metric("Artista favorito", artista_fav)

def plot_genero_musica_preferido(user_id_logado): ###### ALTERAR
    df_gen_album = q.get_genero_musica_ouvida(user_id_logado)
    genero_album_pref = df_gen_album.iloc[0]['genero'] if not df_gen_album.empty else "N/A"
    st.metric("Gênero de Música Preferido", genero_album_pref)

def plot_musica_favorita(user_id_logado):
    df_mus_fav = q.get_top1_musica_ouvida(user_id_logado)
    musica_fav = df_mus_fav.iloc[0]['nome'] if not df_mus_fav.empty else "N/A"
    # Rótulo em negrito
    st.markdown("**Música favorita**")

    # Valor (o nome da música) com fonte menor (ex: 20px)
    st.markdown(f"""
        <p style='font-size: 20px; color: #FFFFFF; margin-top: -10px;'>
            {musica_fav}
        </p>
        """, unsafe_allow_html=True)


def plot_top5_musicas_usuario(user_id_logado):
    df_top5 = q.get_top5_musicas_ouvidas(user_id_logado)

    if not df_top5.empty:
        df_top5 = df_top5.reset_index()

        fig_bar = px.bar(
            df_top5,
            x="numero_reproducoes",
            y="nome",
            orientation='h',  # Gráfico horizontal
            title="Top 5 músicas mais ouvidas",
            labels={'nome': 'Música', 'numero_reproducoes': 'Reproduções'},
            text='numero_reproducoes',

        )

        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_color='#FFFFFF',
            font_color='#FFFFFF',
            yaxis={'categoryorder': 'total ascending'}  # Ordena do maior para o menor
        )

        # Estilizar as barras
        fig_bar.update_traces(
            textposition='outside',
            marker_color='#1ED760'  # Verde Spotify
        )

        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Você ainda não possui um ranking de músicas.")