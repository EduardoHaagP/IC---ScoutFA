import sys

import pandas as pd

ENTRADA_PADRAO = "notebook/Data/Dados.csv"
SAIDA_PADRAO = "notebook/Data/DadosFiltradosParaAnaliseExploratoria.csv"

# Nome final -> coluna(s) de origem no CSV original
COLUNAS_FINAIS = [
    "posteam",
    "home",
    "ydstogo",
    "qtr",
    "down",
    "shotgun",
    "nohuddle",
    "scorediff",
    "goaltogo",
    "yardline_100",
    "yardline90",
    "play_type",
]

# Franquias que mudaram de sigla ao longo dos anos -> sigla atual
SIGLAS = {"JAC": "JAX", "SD": "LAC", "STL": "LA"}

# Classes mantidas no alvo
CLASSES = ["run", "pass"]


def construir_variaveis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Padroniza siglas ANTES de calcular 'home', que compara posteam com home_team
    df["posteam"] = df["posteam"].replace(SIGLAS)
    if "home_team" in df.columns:
        df["home_team"] = df["home_team"].replace(SIGLAS)

    out = pd.DataFrame(index=df.index)

    # posteam: time com a posse de bola
    out["posteam"] = df["posteam"]

    # home: 1 se o time com a posse joga em casa
    if "Home" in df.columns:
        out["home"] = df["Home"]
    else:
        out["home"] = (df["posteam"] == df["home_team"]).astype(int)

    # ydstogo: jardas para o first down
    out["ydstogo"] = df["ydstogo"]

    # qtr: quarto da jogada
    out["qtr"] = df["qtr"]

    # down: down da jogada
    out["down"] = df["down"]

    # shotgun e nohuddle: dummies
    out["shotgun"] = df["shotgun"]
    out["nohuddle"] = df["nohuddle"]

    # scorediff: placar do time com a posse menos o do adversário
    if "ScoreDiff" in df.columns:
        out["scorediff"] = df["ScoreDiff"]
    else:
        out["scorediff"] = df["posteam_score"] - df["defteam_score"]

    # goaltogo: jogada em situação de goal-to-go
    out["goaltogo"] = df["goal_to_go"]

    # yardline_100: posição da posse em relação à end zone
    out["yardline_100"] = df["yardline_100"]

    # yardline90: 1 se a posse começa a até 10 jardas da própria end zone
    if "yardline90" in df.columns:
        out["yardline90"] = df["yardline90"]
    else:
        out["yardline90"] = (df["yardline_100"] >= 90).astype(int)

    # play_type: padroniza texto e mantém apenas run e pass
    out["play_type"] = df["play_type"].astype(str).str.lower().str.strip()
    out = out[out["play_type"].isin(CLASSES)]

    return out[COLUNAS_FINAIS]


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else ENTRADA_PADRAO
    saida = sys.argv[2] if len(sys.argv) > 2 else SAIDA_PADRAO

    df = pd.read_csv(entrada)
    resultado = construir_variaveis(df)
    resultado.to_csv(saida, index=False)
    print(f"OK: {len(resultado)} linhas, {resultado.shape[1]} colunas -> {saida}")
    print(f"Equipes distintas em posteam: {resultado['posteam'].nunique()}")


if __name__ == "__main__":
    main()