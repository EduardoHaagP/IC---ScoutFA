import nflreadpy as nfl
import pandas as pd
from ydata_profiling import ProfileReport

# Load current season play-by-play data (returns a Polars DataFrame)
pbp_polars = nfl.load_pbp(2009)

# Convert to pandas DataFrame to make it compatible with ydata_profiling
pbp = pbp_polars.to_pandas()

print("First 5 records:", pbp.head())
profile2 = ProfileReport(pbp, title="Profiling Report - NFL - NFLready", explorative=True)

profile2.to_file("../testes_iniciais/NFLready/reports/report0.html")