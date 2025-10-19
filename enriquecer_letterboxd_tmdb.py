import pandas as pd
import tmdbsimple as tmdb
import time
from tqdm import tqdm
import os
from dotenv import load_dotenv
from typing import List, Any, Tuple 

# =========================================================================
# 1. CONFIGURAÇÃO E VARIÁVEIS DE AMBIENTE
# =========================================================================

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Nomes dos arquivos
WATCHED_INPUT = 'watched.csv'
WATCHLIST_INPUT = 'watchlist.csv'
WATCHED_OUTPUT = 'watched_enriquecido.csv'
WATCHLIST_OUTPUT = 'watchlist_enriquecida.csv'

# URL base para o pôster no tamanho 'w500'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Atraso para respeitar os limites de requisição da API (100ms)
PAUSA_ENTRE_REQUISICOES = 0.1

# Inicializa a API do TMDB
if not TMDB_API_KEY:
    print("ERRO: A chave da API do TMDB não foi encontrada. Defina TMDB_API_KEY.")
    exit()
tmdb.API_KEY = TMDB_API_KEY

# Define as colunas que serão adicionadas ao DataFrame
COLUNAS_TMDB = [
    'Gênero_TMDB', 'URL_Pôster_TMDB', 'País_Origem_TMDB', 'Duração_Minutos', 
    'Idioma_Original', 'Nota_Média_TMDB', 'Popularidade_TMDB', 
    'Bilheteria_USD', 'Orçamento_USD', 'Tagline',
    'Diretor', 'Elenco_Principal'
]
# =========================================================================

def buscar_detalhes_tmdb(title: str, year: str) -> Tuple[Any, ...]:
    """
    Busca detalhes do filme, créditos e links no TMDB.

    Args:
        title: O título do filme.
        year: O ano de lançamento do filme (para busca mais precisa).

    Returns:
        Uma tupla contendo os 12 valores de COLUNAS_TMDB ou None's em caso de falha.
    """
    
    # Preenche a lista de resultados com None para garantir o tamanho correto
    resultado = [None] * len(COLUNAS_TMDB)
    movie_id = None

    # 1. BUSCA INICIAL POR TÍTULO E ANO
    try:
        search = tmdb.Search()
        response = search.movie(query=title, year=year)
        
        if response['results']:
            movie_id = response['results'][0]['id']
        else:
            return tuple(resultado) # Filme não encontrado
            
    except Exception as e:
        print(f"[{title} ({year})]: Erro na busca inicial: {e}")
        return tuple(resultado)
    
    # 2. BUSCA DE CRÉDITOS (DIRETOR E ELENCO)
    cast_names = []
    director_name = None

    if movie_id:
        try:
            credits = tmdb.Movies(movie_id).credits()
            
            # Elenco Principal (Top 3 Atores)
            for actor in credits.get('cast', [])[:3]:
                cast_names.append(actor['name'])
                
            # Diretor
            for crew_member in credits.get('crew', []):
                if crew_member.get('job') == 'Director':
                    director_name = crew_member['name']
                    break # Pega apenas o primeiro diretor
                    
        except Exception as e:
            print(f"[{title} ({year})]: Erro ao buscar créditos: {e}")

    # 3. BUSCA DE DETALHES GERAIS
    if movie_id:
        try:
            movie = tmdb.Movies(movie_id)
            details = movie.info()
            
            # Extração e formatação dos detalhes
            genres = ", ".join([g['name'] for g in details.get('genres', [])])
            poster_path = details.get('poster_path')
            image_url = f"{POSTER_BASE_URL}{poster_path}" if poster_path else None
            countries = ", ".join([c['name'] for c in details.get('production_countries', [])])
            
            # Monta a tupla de resultados na ordem de COLUNAS_TMDB
            resultado = (
                genres,
                image_url,
                countries,
                details.get('runtime'),
                details.get('original_language'),
                details.get('vote_average'),
                details.get('popularity'),
                details.get('revenue'),
                details.get('budget'),
                details.get('tagline'),
                director_name,
                ", ".join(cast_names) # Elenco Principal (Top 3)
            )
            
        except Exception as e:
            print(f"[{title} ({year})]: Erro ao buscar detalhes: {e}")
            
    return tuple(resultado)

def processar_arquivo(input_file: str, output_file: str):
    """
    Carrega o CSV do Letterboxd, enriquece com dados do TMDB e salva o resultado.
    
    Args:
        input_file: O nome do arquivo CSV de entrada (watched.csv ou watchlist.csv).
        output_file: O nome do arquivo CSV de saída enriquecido.
    """
    
    if not os.path.exists(input_file):
        print(f"\nATENÇÃO: Arquivo '{input_file}' não encontrado. Pulando este arquivo.")
        return

    print(f"\n{'='*50}\nIniciando o processamento: {input_file}\n{'='*50}")
    
    # 1. LEITURA E PREPARAÇÃO DO DATAFRAME
    try:
        # Tenta ler o CSV, assumindo o formato padrão do Letterboxd
        df = pd.read_csv(input_file)
        
        # Remoção de linhas nulas e conversão de tipos
        df.dropna(subset=['Name', 'Year'], inplace=True)
        df['Year'] = df['Year'].astype(int).astype(str) # Garante ano como string inteira
        
        print(f"Total de {len(df)} filmes/entradas para enriquecer.")
    except Exception as e:
        print(f"ERRO fatal ao ler o arquivo {input_file}: {e}")
        return

    # 2. INICIALIZA COLUNAS NO DATAFRAME
    for col in COLUNAS_TMDB:
        df[col] = None
    
    # 3. LOOP DE ENRIQUECIMENTO DE DADOS
    # O tqdm fornece a barra de progresso
    for index, row in tqdm(df.iterrows(), total=len(df), desc=f"Enriquecendo {input_file}"):
        
        # Chamada à API e atribuição
        tmdb_data = buscar_detalhes_tmdb(row['Name'], row['Year'])
        
        # Atribui os dados retornados de forma segura
        for i, col in enumerate(COLUNAS_TMDB):
            df.at[index, col] = tmdb_data[i]
        
        # Pausa para respeitar os limites da API
        time.sleep(PAUSA_ENTRE_REQUISICOES)

    # 4. SALVAR O NOVO ARQUIVO CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\nNOVO ARQUIVO CRIADO: '{output_file}'")
    print(f"{'-'*50}")


# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    
    # Processa filmes assistidos
    processar_arquivo(WATCHED_INPUT, WATCHED_OUTPUT)
    
    # Processa a watchlist
    processar_arquivo(WATCHLIST_INPUT, WATCHLIST_OUTPUT)

    print("\n✅ Processamento de dados CONCLUÍDO! ✅")
   