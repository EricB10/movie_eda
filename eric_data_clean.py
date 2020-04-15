import numpy as np
import pandas as pd
import json
import requests
import ast



# Write Clean DF
df.to_csv('clean_df.csv')

# Open Clean DF
df = pd.read_csv('clean_df.csv', index_col='id').sort_index()



# Open TMDB Details DF
df_det = pd.read_csv('TMDB_movie_details.csv', index_col='id').sort_index()

# Reformat TMDB Details Contries
df_det['countries']=df_det['production_countries'].apply(lambda x: ast.literal_eval(x))
df_det.drop('production_countries', axis=1, inplace=True)
df_det.keys()

# Open TMDB Top Rated DF
df_top = pd.read_csv('TMDB_toprated.csv', index_col='id').sort_index()

# Drop Adult column (100% False)
df_top.drop('adult', axis=1, inplace=True)

# Merge DFs
df = pd.merge(df_det, df_top, on='id')

# Drop Non-English
lan_filt = df['original_language'] != 'en'
df = df.loc[lan_filt]

# Get only year from release date
df['year'] = df['release_date'].apply(lambda x: int(x[0:4]))
df.drop('release_date', axis=1, inplace=True)

# Drop movies before 1990
old_filt = df['year'] > 1990
df = df.loc[old_filt]



# Merge in revenue data
df1 = pd.read_csv('clean_df.csv', index_col='imdb_id')
df2 = pd.read_csv('cumulative_revenue.csv', index_col='imdb_id')
df = pd.merge(df, df2, on='imdb_id')

# Clean up revenue, remove cumulative_revenue
df['revenue'] = df['cumulative_revenue'].str.replace(',', '').str.replace('$','')
df.drop('cumulative_revenue', axis=1, inplace=True)