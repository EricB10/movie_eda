import numpy as np
import pandas as pd
import json
import requests

from eric_keys import eric_omdb_key, eric_tmdb_key, eric_tmdb_token
from eric_test import *
from functions import *


##### TMDB Details #####

# Open TMDB Top Rated DF
df_top = pd.read_csv('TMDB_toprated.csv')
print(len(df_top))
print(df_top.keys())

# Drop Adult
df_top.drop('adult', axis=1, inplace=True)

# Drop Non-English
lan_filt = df_top['original_language'] != 'en'
df_top = df_top.loc[lan_filt]

# Write Clean Top Rated DF
df_top.to_csv('clean_TMDB_toprated.csv', index=False)

# Open Clean Top Rated DF, Indexed
df_top = pd.read_csv('clean_TMDB_toprated.csv', index_col='title').sort_index()


##### TMDB Details #####

# Open TMDB Details DF
df_det = pd.read_csv('TMDB_movie_details.csv')
print(len(df_det))
print(df_det.keys())

# Reformat TMDB Details Contries
import ast
df_det['countries']=df_det['production_countries'].apply(lambda x: ast.literal_eval(x))
df_det.drop('production_countries', axis=1, inplace=True)