import numpy as np
import pandas as pd
import json
import requests
import ast

# Read CSV to DF
df = pd.read_csv('clean_df.csv', index_col='id').sort_index()



##### Top Five Languages #####

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
    
# Add mean vote by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_vote'] = round(
            df.loc[filt1].loc[filt2]['avg_vote'].mean(), 1)
        
# Add median vote by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_vote'] = round(
            df.loc[filt1].loc[filt2]['avg_vote'].median(), 1)
        
# Add mean popularity by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_popularity'] = round(
            df.loc[filt1].loc[filt2]['popularity'].mean(), 1)
        
# Add median popularity by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_popularity'] = round(
            df.loc[filt1].loc[filt2]['popularity'].median(), 1)

# Add mean budget by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_budget'] = int(round(
            df.loc[filt1].loc[filt2]['budget'].mean()))
        
# Add median budget by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_budget'] = int(round(
            df.loc[filt1].loc[filt2]['budget'].median()))
        
# Add mean revenue by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_revenue'] = int(round(
            df.loc[filt1].loc[filt2]['revenue'].mean()))
        
# Add median revenue by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_revenue'] = int(round(
            df.loc[filt1].loc[filt2]['revenue'].median()))
        
# Add mean profit by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_profit'] = int(round(
            df.loc[filt1].loc[filt2]['profit'].mean()))
        
# Add median profit by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_profit'] = int(round(
            df.loc[filt1].loc[filt2]['profit'].median()))
        
# Add mean profit margin by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_mean_profit_margin'] = int(round(
            df.loc[filt1].loc[filt2]['profit_margin'].mean()))
        
# Add median profit margin by decade
for decade in ['90s', '00s', '10s']:
    for key, value in top_five_lang.items():
        filt1 = df[decade] == 1
        filt2 = df['original_language'] == key
        top_five_lang[key][f'{decade}_median_profit_margin'] = int(round(
            df.loc[filt1].loc[filt2]['profit_margin'].median()))
        

    

    
# TMDB popularity metric based on:

# Number of votes for the day
# Number of views for the day
# Number of users who marked it as a "favourite" for the day
    # Number of users who added it to their "watchlist" for the day
# Release date
# Number of total votes
# Previous days score