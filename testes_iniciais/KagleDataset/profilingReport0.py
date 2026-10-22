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

df = pd.read_csv(file_path, low_memory=False)

# Cria a pasta do relatório se não existir
output_dir = "./testes_iniciais/KagleDataset/reports"
os.makedirs(output_dir, exist_ok=True)

# Profiling
profile = ProfileReport(df, title="Profiling Report - NFL - Kagle", explorative=True)
profile.to_file(os.path.join(output_dir, "report0.html"))
print("Relatório salvo em:", os.path.join(output_dir, "report0.html"))