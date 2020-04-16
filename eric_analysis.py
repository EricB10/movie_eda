import numpy as np
import pandas as pd
import json
import requests
import ast

df = pd.read_csv('clean_df.csv', index_col='id').sort_index()


# Create list of top languages by num of movies
language_count = dict(df['original_language'].value_counts())
language_count = [(key, value) for key, value in language_count.items()]

# Create dict for top five languages by num of movies
top_five_lang = {}
for x in language_count[0:5]:
    top_five_lang[x[0]] = {'movie_count':x[1]}

# Add mean vote count
for key, value in top_five_lang.items():
    top_five_lang[key]['mean_vote_count'] = int(round(
        df.groupby('original_language')['vote_count'].mean().loc[key]))
    
# Add median vote count
for key, value in top_five_lang.items():
    top_five_lang[key]['median_vote_count'] = int(round(
        df.groupby('original_language')['vote_count'].median().loc[key]))
    

    
# TMDB popularity metric based on:

# Number of votes for the day
# Number of views for the day
# Number of users who marked it as a "favourite" for the day
    # Number of users who added it to their "watchlist" for the day
# Release date
# Number of total votes
# Previous days score