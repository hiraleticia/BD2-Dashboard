import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px
from db import run_query

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


def check_artist_type(id_artista):
    #Verifica se um artista tem conteúdo de podcast ou de álbum.
    query_podcast = """
        SELECT EXISTS (
            SELECT 1
            FROM Podcast p
            JOIN Conteudo c ON p.id_podcast = c.id
            WHERE c.id_do_artista = %s
        );
    """
    df_podcast = run_query(query_podcast, (id_artista,))
    if not df_podcast.empty and df_podcast.iloc[0]['exists']:
        return 'podcaster'

    # Verifica se existe algum álbum associado a este artista
    query_album = """
        SELECT EXISTS (
            SELECT 1
            FROM Album a
            JOIN Conteudo c ON a.id_album = c.id
            WHERE c.id_do_artista = %s
        );
    """
    df_album = run_query(query_album, (id_artista,))
    if not df_album.empty and df_album.iloc[0]['exists']:
        return 'musico'
    return 'desconhecido'

def get_top3_episodios_podcaster(id_artista):
    # Retorna os top 3 episódios mais ouvidos de um podcaster
    query = """
    SELECT
        e.nome,
        ee.numero_reproducoes
    FROM EscutaEpisodio ee
    JOIN Episodio e ON ee.id_episodio = e.id_episodio
    JOIN Podcast p ON e.id_podcast = p.id_podcast
    JOIN Conteudo c ON p.id_podcast = c.id
    WHERE c.id_do_artista = %s
    ORDER BY ee.numero_reproducoes DESC
    LIMIT 3;
    """
    return run_query(query, (id_artista,))


def get_seguidores_podcast_artista(id_artista):
    # Retorna o total de seguidores dos podcasts de um artista
    query = """
    SELECT
        COUNT(sp.id_da_conta) AS total_seguidores
    FROM SeguePodcast sp
    JOIN Podcast p ON sp.id_podcast = p.id_podcast
    JOIN Conteudo c ON p.id_podcast = c.id
    WHERE c.id_do_artista = %s;
    """
    return run_query(query, (id_artista,))


def get_all_episode_plays_by_artist(id_artista):
    # Retorna as reproduções dos episódios de um podcaster
    query = """
    SELECT
        e.nome,
        ee.numero_reproducoes
    FROM EscutaEpisodio ee
    JOIN Episodio e ON ee.id_episodio = e.id_episodio
    JOIN Podcast p ON e.id_podcast = p.id_podcast
    JOIN Conteudo c ON p.id_podcast = c.id
    WHERE c.id_do_artista = %s AND ee.numero_reproducoes > 0
    ORDER BY ee.numero_reproducoes DESC;
    """
    return run_query(query, (id_artista,))

def get_all_artists():
    query = """
        SELECT a.id_do_artista, c.nome
        FROM Artista a
        JOIN Conta c ON a.id_do_artista = c.id
        ORDER BY c.nome;
    """
    return run_query(query)

def get_song_count_per_album(id_artista):
    query = """
        SELECT ct.nome AS nome_album, COUNT(m.id_da_musica) AS total_musicas
        FROM Musica m
        JOIN Album al ON m.id_album = al.id_album
        JOIN Conteudo ct ON al.id_album = ct.id
        WHERE ct.id_do_artista = %s
        GROUP BY ct.nome
        ORDER BY total_musicas DESC;
    """
    return run_query(query, (id_artista,))

def get_albums_by_artist(id_artista):
    query = """
        SELECT al.id_album, ct.nome AS nome_album
        FROM Album al
        JOIN Conteudo ct ON al.id_album = ct.id
        WHERE ct.id_do_artista = %s
        ORDER BY nome_album;
    """
    return run_query(query, (id_artista,))

def get_song_plays_by_album(id_album):
    query = """
        SELECT m.nome AS musica,
               COUNT(em.id_da_conta) AS reproducoes
        FROM Musica m
        LEFT JOIN EscutaMusica em
               ON m.id_da_musica = em.id_da_musica
        WHERE m.id_album = %s
        GROUP BY m.nome
        ORDER BY reproducoes DESC;
    """
    return run_query(query, (id_album,))

# ------ TAB GERAL ------

def get_total_musicas_geral_count():
    query = "SELECT COUNT(*) AS total FROM Musica;"
    return run_query(query)


def get_total_artistas_geral_count():
    query = "SELECT COUNT(*) AS total FROM Artista;"
    return run_query(query)

def get_total_album_geral_count():
    query = "SELECT COUNT(*) AS total FROM Album;"
    return run_query(query)

def get_total_podcasts_geral_count():
    query = "SELECT COUNT(*) AS total FROM Podcast;"
    return run_query(query)

def get_top5_musicas_geral():
    # 5 musicas mais ouvidas no spotify
    query = """
    SELECT
        M.nome AS Nome_da_Musica,
        C.nome AS Nome_do_Album,
        SUM(EM.numero_reproducoes) AS Total_de_Reproducoes
    FROM EscutaMusica EM
        JOIN Musica M ON EM.id_da_musica = M.id_da_musica
        JOIN Album A ON M.id_album = A.id_album
        JOIN Conteudo C ON A.id_album = C.id
    GROUP BY M.id_da_musica, M.nome, C.nome
    ORDER BY Total_de_Reproducoes DESC
    LIMIT 5;"""

    return run_query(query)


def get_top_10_albuns_com_mais_faixas():
    # Busca o ranking de top 10 álbuns com mais músicas
    query = """
        SELECT ct.nome,
        COUNT(m.id_da_musica) AS total_de_musicas
        FROM Musica AS m
        JOIN Album AS al ON m.id_album = al.id_album
        JOIN Conteudo AS ct ON al.id_album = ct.id
        GROUP BY ct.nome
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

def get_art_mais_mus_publi():
    # Artista com o maior número de músicas publicadas
    query = '''
    SELECT MIN(Conta.nome) AS nome_artista
    FROM Artista, Conta, Conteudo, Album, Musica
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


def get_genero_musica_ouvida(user_id):
    # Gênero de album mais ouvido pelo usuário
    query = '''
    SELECT Musica.genero, 
    SUM(EscutaMusica.numero_reproducoes) AS reproducoes_totais
        FROM EscutaMusica 
        JOIN Musica ON EscutaMusica.id_da_musica = Musica.id_da_musica
        WHERE EscutaMusica.id_da_conta = %s
        GROUP BY Musica.genero
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
        LIMIT 5;'''
    return run_query(query, (user_id,))

def get_tempo_total_escutado_segundos(user_id):
    query = """
    SELECT SUM(EXTRACT(EPOCH FROM M.tempo_de_duracao) * EM.numero_reproducoes) AS total_segundos
        FROM EscutaMusica EM
        JOIN Musica M ON EM.id_da_musica = M.id_da_musica
        WHERE EM.id_da_conta = %s;"""

    df = run_query(query, (user_id,))

    # Se o usuário não ouviu nada, o SUM retornará Nulo (None)
    if df.empty or pd.isna(df.iloc[0]['total_segundos']):
        return 0  # Retorna 0 segundos

    # Retorna o total de segundos como um inteiro
    return int(df.iloc[0]['total_segundos'])