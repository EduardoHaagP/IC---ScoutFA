import nflreadpy as nfl
import pandas as pd
import polars as pl

# Ajustar o pandas para mostrar todas as colunas no terminal
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("A carregar dados de play-by-play...")
# 1. Carregar os dados da temporada de 2024 (podes alterar para 2023, 2022, etc.)
df_pbp = nfl.load_pbp([2024])

# 2. Filtrar apenas jogadas válidas de passe e corrida da época regular
jogadas = df_pbp.filter(
    (df_pbp['season_type'] == 'REG') & 
    (df_pbp['play_type'].is_in(['pass', 'run']))
)

# Exportar todas as colunas disponíveis para as primeiras 5 jogadas
amostra_play_by_play = jogadas.head(5)
arquivo_csv = '5_jogadas_play_by_play.csv'
amostra_play_by_play.write_csv(arquivo_csv)
print(f"{amostra_play_by_play.width} colunas das primeiras 5 jogadas exportadas para {arquivo_csv}")

# 3. Selecionar colunas situacionais e pré-snap cruciais para scouting
colunas_interesse = [
    'game_id', 'posteam', 'defteam', 'qtr', 'down', 'ydstogo', 
    'yardline_100', 'score_differential', 'shotgun', 'no_huddle', 
    'play_type'
]

for coluna_opcional in ('offense_formation', 'defenders_in_box'):
    if coluna_opcional in jogadas.columns:
        colunas_interesse.insert(-1, coluna_opcional)

df_scouting = jogadas[colunas_interesse]

# 4. Exibir os resultados
print(f"\nTotal de jogadas (Passe/Corrida) analisadas: {len(df_scouting)}")

print("\n--- Primeiras 5 jogadas do dataset ---")
print(df_scouting.head())

print("\n--- Distribuição de chamadas (Passe vs Corrida) ---")
distribuicao = (
    df_scouting['play_type']
    .value_counts()
    .with_columns(
        (pl.col('count') / pl.col('count').sum() * 100)
        .round(1)
        .alias('percentagem')
    )
)
print(distribuicao)

if 'offense_formation' in df_scouting.columns:
    print("\n--- Formações Ofensivas mais comuns registadas ---")
    print(df_scouting['offense_formation'].value_counts())
else:
    print("\n--- Formações Ofensivas ---")
    print("A coluna offense_formation não está disponível neste dataset.")