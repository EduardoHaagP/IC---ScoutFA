import nflreadpy as nfl

print("A carregar os dados de Play-by-Play e Participação da época 2024...")

# 1. Carregar as duas tabelas da temporada desejada (2024)
df_pbp = nfl.load_pbp([2024])
df_part = nfl.load_participation([2024])

# 2. Filtrar no PBP apenas jogadas de passe e corrida da época regular
pbp_filtrado = df_pbp.filter(
    (df_pbp['season_type'] == 'REG') &
    (df_pbp['play_type'].is_in(['pass', 'run']))
)

# 3. Preparar a tabela de participação para o cruzamento (merge)
# No nflreadpy, 'nflverse_game_id' na participação corresponde ao 'game_id' do PBP
df_part_renomeado = df_part.rename({'nflverse_game_id': 'game_id'})

# Colunas de participação que queremos adicionar ao dataset
colunas_part = [
    'game_id', 
    'play_id', 
    'offense_formation',   # Ex: SHOTGUN, SINGLEBACK, I_FORM
    'offense_personnel',   # Ex: 11 Personnel (1 RB, 1 TE, 3 WR)
    'defense_personnel',   # Ex: Nickel (4 DL, 2 LB, 5 DB)
    'defenders_in_box'    # N.º de defensores na caixa antes do snap
]

# Cruzar as duas tabelas usando game_id e play_id como chave
dados_completos = pbp_filtrado.join(
    df_part_renomeado.select(colunas_part),
    on=['game_id', 'play_id'],
    how='left'
)

# 4. Selecionar as colunas finais para o modelo de scouting / previsão pré-snap
colunas_finais = [
    'game_id', 
    'play_id', 
    'posteam',             # Equipa ao ataque
    'defteam',             # Equipa na defesa
    'qtr',                 # Periodo / Quarter
    'down',                # Descida (1, 2, 3, 4)
    'ydstogo',             # Jardas para a 1ª descida
    'yardline_100',        # Posição no campo (distância para o golo)
    'score_differential',  # Diferença no marcador
    'shotgun',             # Formação em shotgun (1/0)
    'no_huddle',           # Ataque sem reunião (1/0)
    'offense_formation',   # Formação tática
    'offense_personnel',   # Pessoal em campo (ofensivo)
    'defense_personnel',   # Pessoal em campo (defensivo)
    'defenders_in_box',    # Defensores na caixa
    'play_type'            # Alvo a prever ('pass' ou 'run')
]

colunas_disponiveis = [
    coluna for coluna in colunas_finais if coluna in dados_completos.columns
]
df_scouting = dados_completos.select(colunas_disponiveis)

# 5. Guardar os dados num ficheiro CSV
nome_ficheiro = "nfl_scouting_data_2024.csv"
df_scouting.write_csv(nome_ficheiro)

print(f"\nConcluído com sucesso! {len(df_scouting)} jogadas foram guardadas em '{nome_ficheiro}'.")
print("\nPrimeiras 5 linhas do dataset gerado:")
print(df_scouting.head())   