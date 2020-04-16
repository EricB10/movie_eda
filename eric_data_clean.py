import numpy as np
import pandas as pd
import json
import requests
import ast



##### Primary DF #####

# Read CSV to DF
df = pd.read_csv('clean_df.csv', index_col='id').sort_index()

# Write DF to CSV
df.to_csv('clean_df.csv')

# Fix genre, country formatting ***MUST BE RUN IN NOTEBOOK***
df['genre_names']=df['genre_names'].apply(lambda x: ast.literal_eval(x)) # Run in notebook
df['countries']=df['countries'].apply(lambda x: ast.literal_eval(x)) # Run in notebook



##### Initial DF Clean, Merge #####

# Read TMDB Details DF
df_det = pd.read_csv('TMDB_movie_details.csv', index_col='id').sort_index()

# Fix countries column
df_det['countries']=df_det['production_countries']
df_det.drop('production_countries', axis=1, inplace=True)

# Read TMDB Top Rated DF
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

# Replace budget 0 values with NaN
df['budget'].replace(0, np.nan, inplace=True)

# Delete outlier budget data < $100
df['budget']=np.where(df['budget']<100,np.nan,df['budget'])

# Delete revenue outliers
filt_rev = df['revenue'] < 10000
df['revenue'] = np.where(filt_rev, np.nan, df['revenue'])

# Delete budget outliers
filt_bgt = df['budget'] < 10000
df['budget'] = np.where(filt_bgt, np.nan, df['budget'])

# Spell out languages
language_dict = {
    'fr':'French',
    'it':'Italian',
    'ja':'Japanese',
    'es':'Spanish',
    'de':'German',
    'ko':'Korean',
    'cn':'Chinese',
    'pt':'Portuguese',
    'zh':'Chinese',
    'da':'Danish',
    'sv':'Swedish',
    'ru':'Russian',
    'hi':'Hindi',
    'no':'Norwegian',
    'fa':'Farsi',
    'nl':'Dutch',
    'th':'Thai',
    'id':'Indonesian',
    'tr':'Turkish',
    'pl':'Polish',
    'sr':'Serbian',
    'hu':'Hungarian',
    'te':'Telugu',
    'ar':'Arabic',
    'el':'Greek',
    'fi':'Finnish',
    'et':'Estonian',
    'la':'Latin',
    'bs':'Bosnian',
    'ro':'Romanian',
    'nb':'Norwegian',
    'eu':'Basque'    
}
df['original_language'] = df['original_language'].map(language_dict)



##### Merge Scraped Revenue DF #####

# Merge in revenue data
df1 = pd.read_csv('clean_df.csv', index_col='imdb_id')
df2 = pd.read_csv('cumulative_revenue.csv', index_col='imdb_id')
df = pd.merge(df, df2, on='imdb_id')

# Clean up revenue, remove cumulative_revenue
df['revenue'] = df['cumulative_revenue'].str.replace(',', '').str.replace('$','')
df.drop('cumulative_revenue', axis=1, inplace=True)



##### Create More Columns #####

# Create 90s column
filt90_1 = df['year'] >= 1990
filt90_2 = df['year'] < 2000
df['90s']=np.where(filt90_1 & filt90_2,1,0)

# Create 00s column
filt00_1 = df['year'] >= 2000
filt00_2 = df['year'] < 2010
df['00s']=np.where(filt00_1 & filt00_2,1,0)

# Create 10s column
filt10_1 = df['year'] >= 2010
filt10_2 = df['year'] < 2020
df['10s']=np.where(filt10_1 & filt10_2,1,0)

# Add profit, profit margin columns
df['profit'] = df['revenue'] - df['budget']
df['profit_margin'] = 100 * df['profit'] / df['revenue']
df['profit_margin'] = round(df['profit_margin'], 1)