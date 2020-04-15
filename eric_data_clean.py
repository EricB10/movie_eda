import numpy as np
import pandas as pd
import json
import requests
import ast

from eric_keys import eric_omdb_key, eric_tmdb_key, eric_tmdb_token
from eric_test import *
from functions import *


# Open TMDB Details DF
df_det = pd.read_csv('TMDB_movie_details.csv', index_col='id').sort_index()

# Reformat TMDB Details Contries
df_det['countries']=df_det['production_countries'].apply(lambda x: ast.literal_eval(x))
df_det.drop('production_countries', axis=1, inplace=True)
df_det.keys()

# Open TMDB Top Rated DF
df_top = pd.read_csv('TMDB_toprated.csv', index_col='id').sort_index()

# Drop Adult (100% False)
df_top.drop('adult', axis=1, inplace=True)

# Merge DFs
combined_df = pd.merge(df_det, df_top, on='id')

# Drop Non-English
lan_filt = combined_df['original_language'] != 'en'
combined_df = combined_df.loc[lan_filt]

# Write Merged DF
combined_df.to_csv('clean_df.csv')

# Open Clean DF
df = pd.read_csv('clean_df.csv', index_col='id').sort_index()