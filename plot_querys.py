import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
import queries as q
from db import run_query

#--------------------------------------------
#--------------------GERAL-------------------
#--------------------------------------------

def plot_total_musicas():
    df_total_musicas = q.get_total_musicas_geral_count()
    total_musicas = df_total_musicas.iloc[0]['total'] if not df_total_musicas.empty else 0
    st.metric("🎵 Total de músicas", total_musicas)

def plot_total_artistas():
    df_total_artistas = q.get_total_artistas_geral_count()
    total_musicas = df_total_artistas.iloc[0]['total'] if not df_total_artistas.empty else 0
    st.metric("👥 Total de artistas", total_musicas)

def plot_total_album():
    df_total_album = q.get_total_album_geral_count()
    total_album = df_total_album.iloc[0]['total'] if not df_total_album.empty else 0
    st.metric("📀 Total de álbuns", total_album)

def plot_total_podcast():
    df_total_podcast = q.get_total_podcasts_geral_count()
    total_podcast = df_total_podcast.iloc[0]['total'] if not df_total_podcast.empty else 0
    st.metric("🎙️ Total de podcasts", total_podcast)

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
            background='transparent'
        ).interactive()

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
   

def plot_top_10_albuns():
    try:
        df_top_albuns = q.get_top_10_albuns_com_mais_faixas()
    except Exception as e:
        st.error(f"Erro ao carregar os dados dos álbuns: {e}")
        df_top_albuns = pd.DataFrame()

    if not df_top_albuns.empty:
        df_top_albuns = df_top_albuns.sort_values(by='total_de_musicas', ascending=False)

        # Criar o Gráfico de Barras com Altair
        chart = alt.Chart(df_top_albuns).mark_bar().encode(

            # Eixo X: Total de Músicas
            x=alt.X('total_de_musicas',
                    title='Total de Músicas (Faixas)',
                    axis=alt.Axis(format='d')
            ),

            # Eixo Y: Nome do Álbum
            y=alt.Y('nome',
                    title='Nome do Álbum',
                    sort='-x' # Ordena as barras do maior para o menor valor de x
            ),

            color=alt.value("#66A3FF"), # Cor azul fixa para todas as barras

            # Tooltip para exibir detalhes
            tooltip=[
                alt.Tooltip('nome', title='Álbum'),
                alt.Tooltip('total_de_musicas', title='Nº de Faixas', format='d')
            ]
        ).properties(
            height=400,
            background = 'transparent'
        ).interactive()

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

        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("Nenhum álbum encontrado para o ranking Top 10.")

def plot_top_5_albuns_salvos():
    try:
        df_top_albuns_salvos = q.get_top5_albuns_salvos()
    except Exception as e:
        st.error(f"Erro ao carregar os dados dos álbuns salvos: {e}")
        df_top_albuns_salvos = pd.DataFrame()

    if not df_top_albuns_salvos.empty:
        # 2. Ordenar o DataFrame
        df_top_albuns_salvos = df_top_albuns_salvos.sort_values(by='total_salvos', ascending=False)

        # 3. Criar o Gráfico de Barras com Altair
        chart = alt.Chart(df_top_albuns_salvos).mark_bar().encode(

            # Eixo X (Comprimento da Barra): Total de Salvamentos
            x=alt.X('total_salvos',
                    title='Total de Salvamentos',
                    # Formato com separador de milhar
                    axis=alt.Axis(format=',')
            ),

            # Eixo Y (Cada Barra): Nome do Álbum
            y=alt.Y('nome',
                    title='Nome do Álbum',
                    sort='-x' # Garante que o álbum com mais salvamentos fique no topo
            ),

            # Cor: Cor fixa ou usar a própria métrica como cor (intensidade)
            color=alt.value("#FF66B2"), # Cor rosa para destaque (pode ser qualquer cor)

            # Tooltip para exibir detalhes
            tooltip=[
                alt.Tooltip('nome', title='Álbum'),
                alt.Tooltip('total_salvos', title='Total de Salvamentos', format=',')
            ]
        ).properties(
            height=300,
            background='transparent'
        ).interactive()
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
        # Exibir o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("Nenhum dado de álbum salvo encontrado.")

def plot_top_5_podcasts_seguidos():
    try:
        df_top_podcasts = q.get_top5_podcast_seguidos()
    except Exception as e:
        st.error(f"Erro ao carregar os dados dos podcasts: {e}")
        df_top_podcasts = pd.DataFrame()

    if not df_top_podcasts.empty:
        # 2. Ordenar o DataFrame (opcional, pois o SQL já ordena, mas garante a consistência)
        df_top_podcasts = df_top_podcasts.sort_values(by='total_seguidores', ascending=False)

        # 3. Criar o Gráfico de Barras com Altair
        chart = alt.Chart(df_top_podcasts).mark_bar().encode(

            # Eixo X (Comprimento da Barra): Total de Seguidores
            x=alt.X('total_seguidores',
                    title='Total de Seguidores',
                    # Formato com separador de milhar para melhor leitura
                    axis=alt.Axis(format=',')
            ),

            # Eixo Y (Cada Barra): Nome do Podcast
            y=alt.Y('nome',
                    title='Nome do Podcast',
                    sort='-x' # Garante que o podcast mais seguido fique no topo
            ),
            # Cor: Definida como um valor fixo
            color=alt.value("#9B59B6"), # Uma cor roxa para destaque (pode ser ajustada)

            # Tooltip para exibir detalhes
            tooltip=[
                alt.Tooltip('nome', title='Podcast'),
                alt.Tooltip('total_seguidores', title='Total de Seguidores', format=',')
            ]
        ).properties(
            height=300,
            background='transparent'
        ).interactive()
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

        # 4. Exibir o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)

    else:
        st.info("Nenhum dado de podcast seguido encontrado.")


#--------------------------------------------
#-------------------ARTISTA------------------
#--------------------------------------------
def plot_artista_mais_seguido():
    df_mais_seguidores = q.get_art_mais_seguidores()
    if not df_mais_seguidores.empty:
        artista_nome = df_mais_seguidores.iloc[0]['nome']
        seguidores = df_mais_seguidores.iloc[0]['total_seguidores']
        st.metric(label="Artista com mais seguidores",
                  value=artista_nome,
                  delta=f"{seguidores} seguidores")
    else:
        st.info("Não foi possível carregar o artista com mais seguidores.")

def plot_artista_mais_mus_publi():
    df_mais_music_publicada = q.get_art_mais_mus_publi()
    artista_music_publicada = df_mais_music_publicada.iloc[0]['nome_artista']
    num_musicas = df_mais_music_publicada.iloc[0]['numero_musicas']
    st.metric(label="Artista com mais músicas publicadas",
              value=artista_music_publicada,
              delta=f"{num_musicas} músicas")


def plot_info_artista():
    # --------- Dropdown de artista ---------
    st.subheader("Selecione um artista para análise")
    df_artistas = q.get_all_artists()
    artista_escolhido = st.selectbox(
        "Digite para filtrar artistas:",
        df_artistas["nome"].tolist()
    )

    id_artista = int(df_artistas[df_artistas["nome"] == artista_escolhido]["id_do_artista"].iloc[0])
    st.success(f"Artista selecionado: {artista_escolhido}")

    artist_type = q.check_artist_type(id_artista)

    # ----- O ARTISTA É UM MÚSICO -----
    if artist_type == 'musico':
        st.markdown("---")
        st.subheader(f"Análise do Artista: {artista_escolhido}")

        col_metric_1, col_metric_2 = st.columns(2)

        # Top 3 Músicas
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

        # Álbum Mais Salvo
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
        df_contagem = q.get_song_count_per_album(id_artista)
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
        df_albuns = q.get_albums_by_artist(id_artista)

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
            df_musicas = q.get_song_plays_by_album(id_album)
            if df_musicas['reproducoes'].sum() == 0:
                st.info("Este álbum ainda não tem nenhuma reprodução registrada.")
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

    # -----  O ARTISTA É UM PODCASTER -----
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

def plot_total_musicas_user(user_id_logado):
    df_total_musicas_user = q.get_total_musicas_usuario(user_id_logado)
    total_musicas_user = df_total_musicas_user.iloc[0]['total_musicas'] if not df_total_musicas_user.empty else 0
    
    st.metric("Total de Músicas Ouvidas", total_musicas_user)

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

    st.markdown("**Artista favorito**")

    # Valor (o nome da música) com fonte menor (ex: 20px)
    st.markdown(f"""
        <p style='font-size: 20px; color: #FFFFFF; margin-top: -10px;'>
            {artista_fav}
        </p>
        """, unsafe_allow_html=True)

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

def plot_top5_genero_musicas_ouvidas(user_id):
    df_top5_generos = q.get_top5_genero_musicas_ouvidas(user_id)
    if df_top5_generos.empty:
        st.info(f"O usuário com ID {user_id} não possui dados suficientes de reprodução de música para gerar o gráfico.")
    else:
        fig_pie_genero = px.pie(
            df_top5_generos,
            names="genero",                
            values="reproducoes_totais",   
            title="Distribuição dos 5 Gêneros Mais Ouvidos",
            hole=0.5,                       
            color_discrete_sequence=["#5DB7E4", "#1335BD", "#A51D2F", "#C98D44", '#007050'] 
        )

        # 3. Aplicar o tema escuro/transparente 
        fig_pie_genero.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font_color='#FFFFFF',
            legend_font_color='#FFFFFF',
            title_font_color='#FFFFFF',
            legend=dict(
                orientation="v",            # Orientação vertical (padrão)
                x=0.01,                     # Move a legenda para a esquerda (próximo à borda)
                y=0.5,                      # Centraliza verticalmente
                xanchor="left",             # Alinha o lado esquerdo da legenda em x
                yanchor="middle",           # Alinha o meio da legenda em y
                bgcolor='rgba(0,0,0,0)'     # Garante que o fundo da legenda seja transparente
            )
        )

        fig_pie_genero.update_traces(
            textinfo='percent+label', 
            textfont_color='#FFFFFF', 
            marker=dict(line=dict(color='#000000', width=1)) 
        )

        st.plotly_chart(fig_pie_genero, use_container_width=True)

def plot_top5_artistas_ouvidos(user_id_logado):
    df_top5 = q.get_top5_artistas_ouvidos(user_id_logado)

    if not df_top5.empty:
        df_top5 = df_top5.reset_index()

        fig_bar = px.bar(
            df_top5,
            x="reproducoes_totais",
            y="nome",
            orientation='h',  # Gráfico horizontal
            title="Top 5 artistas mais ouvidos",
            labels={'nome': 'Artista', 'reproducoes_totais': 'Reproduções'},
            text='reproducoes_totais',
        )

        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_color='#FFFFFF',
            font_color='#FFFFFF',
            
            xaxis=dict(
                tickfont=dict(color='#FFFFFF'), # Cor dos valores (ticks) do eixo X
                title=dict(font=dict(color='#FFFFFF')), # Cor do título do eixo X ("Reproduções")
                gridcolor='rgba(255, 255, 255, 0.2)' # Cor da linha de grade (opcional: cinza claro/transparente)
            ),
            yaxis=dict(
                categoryorder='total ascending',
                tickfont=dict(color='#FFFFFF'), # Cor dos valores (ticks) do eixo Y (nomes)
                title=dict(font=dict(color='#FFFFFF')) # Cor do título do eixo Y ("Artista")
            )
        )

        # Estilizar as barras
        fig_bar.update_traces(
            textposition='outside',
            marker_color="#1E5CD7", 
            textfont_color='#FFFFFF'
        )

        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Você ainda não possui um ranking de artistas.")

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
            
            xaxis=dict(
                tickfont=dict(color='#FFFFFF'), # Cor dos valores (ticks) do eixo X
                title=dict(font=dict(color='#FFFFFF')), # Cor do título do eixo X ("Reproduções")
                gridcolor='rgba(255, 255, 255, 0.2)' # Cor da linha de grade (opcional: cinza claro/transparente)
            ),
            yaxis=dict(
                categoryorder='total ascending',
                tickfont=dict(color='#FFFFFF'), # Cor dos valores (ticks) do eixo Y (nomes)
                title=dict(font=dict(color='#FFFFFF')) # Cor do título do eixo Y ("Artista")
            )
        )

        # Estilizar as barras
        fig_bar.update_traces(
            textposition='outside',
            marker_color='#1ED760',  # Verde Spotify
            textfont_color='#FFFFFF'
        )
        

        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Você ainda não possui um ranking de músicas.")