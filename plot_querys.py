import app
import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from db import run_query

#--------------------------------------------
#--------------------GERAL-------------------
#--------------------------------------------
def plot_top5_musicas_geral():
    try:
        df_top_musicas = app.get_top5_musicas_geral()
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
        # --- FIM DAS CONFIGURAÇÕES MANUAIS ---

        # A chamada DEVE incluir theme=None para respeitar nossa configuração manual
        st.altair_chart(chart, use_container_width=True, theme=None)

        with st.expander("Ver dados brutos"):
            st.dataframe(df_top_musicas, use_container_width=True)

    else:
        st.info("Nenhum dado encontrado para as Top 5 músicas.")
   


#--------------------------------------------
#-------------------ARTISTA------------------
#--------------------------------------------
def plot_info_artista():
# --- 1. DESTAQUES GERAIS DA CATEGORIA ---
    st.subheader("Destaques da Categoria")
    df_mais_seguidores = app.get_art_mais_seguidores()
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
        df_top3_musicas = app.get_top3_musicas_art(id_artista)  # Usando a função corrigida

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
        df_album_salvo = app.get_album_mais_salvo_do_artista(id_artista)
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






#--------------------------------------------
#-------------------USUARIO------------------
#--------------------------------------------