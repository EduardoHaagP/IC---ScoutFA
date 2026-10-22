import kagglehub
import pandas as pd
import os
from ydata_profiling import ProfileReport

# Mostrar todas as colunas ao dar print
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

# Download do dataset
folder_path = kagglehub.dataset_download("maxhorowitz/nflplaybyplay2009to2016")
print("Arquivos baixados:", os.listdir(folder_path))

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado no diretório.")

file_path = os.path.join(folder_path, csv_files[0])
print(f"Carregando: {file_path}")

colunas_interesse = [
    # Identificação do jogo
    'GameID', 'Date', 'posteam', 'DefensiveTeam', 'HomeTeam', 'AwayTeam',
    # Situação da jogada
    'qtr', 'down', 'ydstogo', 'yrdline100', 'TimeSecs',
    'ScoreDiff', 'PosTeamScore', 'DefTeamScore',
    # Tipo e resultado da jogada
    'PlayType', 'PassAttempt', 'RushAttempt',
]

df = pd.read_csv(file_path, usecols=lambda c: c in colunas_interesse, low_memory=False)

# Avisa se alguma coluna não foi encontrada e garante a ordem
faltando = [c for c in colunas_interesse if c not in df.columns]
if faltando:
    print("⚠️ Colunas não encontradas:", faltando)
df = df[[c for c in colunas_interesse if c in df.columns]]

# Limpezas básicas
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['GameID'] = df['GameID'].astype(str)          # ID não é número
df = df.dropna(subset=['PlayType'])
df = df.drop_duplicates()

print(f"Shape final: {df.shape}")
print(df.head())

# Cria a pasta do relatório se não existir
output_dir = "./testes_iniciais/KagleDataset/reports"
os.makedirs(output_dir, exist_ok=True)

# Profiling
profile = ProfileReport(df, title="Profiling Report - NFL - Kagle", explorative=True)
profile.to_file(os.path.join(output_dir, "report1.html"))
print("Relatório salvo em:", os.path.join(output_dir, "report1.html"))