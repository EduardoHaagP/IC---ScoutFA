import nflreadpy as nfl
import pandas as pd
from data_profiling import ProfileReport

# Load current season play-by-play data (returns a Polars DataFrame)
pbp_polars = nfl.load_pbp(2009)


# Convert to pandas DataFrame to make it compatible with ydata_profiling
pbp = pbp_polars.to_pandas()

pbp_filtered = pbp[
    [
        # Contexto da jogada
        "qtr",
        "half_seconds_remaining",
        "score_differential",
        "down",
        "ydstogo",
        "yardline_100",

        # Formação / comportamento pré-snap
        "shotgun",
        "no_huddle",

        # Resultado / tipo da jogada
        "play_type",

        # Times
        "posteam",
        "defteam",
        "home_team",
        "away_team",
    ]
]

print("First 5 records:", pbp_filtered.head())
profile2 = ProfileReport(pbp_filtered, title="Profiling Report - NFL - NFLready", explorative=True)
    
profile2.to_file("./testes_iniciais/NFLready/reports/report1.html")