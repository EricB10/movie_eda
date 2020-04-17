import numpy as np
import pandas as pd
import json
import requests
import ast



##### Data Frames #####

# Read CSV to DF
df = pd.read_csv('clean_df.csv', index_col='id').sort_index()
# Fix genre, country formatting ***MUST BE RUN IN NOTEBOOK***
df['genre_names']=df['genre_names'].apply(lambda x: ast.literal_eval(x)) # Run in notebook
df['countries']=df['countries'].apply(lambda x: ast.literal_eval(x)) # Run in notebook

# Write DF to CSV
df.to_csv('clean_df.csv')

# Create Language Lount df for plotting
lang_count_df = pd.DataFrame(language_count, columns=['language', 'count'])
lang_count_df.set_index('language', inplace=True)

# Create Top Five df for plotting
top_five_df = pd.DataFrame.from_dict(top_five_lang,orient='index')

# Make a Genres dataframe where columns 1 and 0 mean True or False
genre_df=df['genre_names'].apply(lambda x: pd.Series([1] * len(x), index=x)).fillna(0, downcast='infer')



##### Initial Data Clean, Merge #####

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

# Delete budget outlier data
filt_bgt = df['budget'] < 10000
df['budget'] = np.where(filt_bgt, np.nan, df['budget'])

# Delete revenue outlier data
filt_rev = df['revenue'] < 10000
df['revenue'] = np.where(filt_rev, np.nan, df['revenue'])

# Drop remaining profit outliers
df.drop([76758, 15362, 457955, 10353, 2395], inplace=True)

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



##### Data Visualizations #####

# Plot number of popular movies by language
lang_count_df.plot(kind='bar', legend=False, figsize=(10,6))
plt.title('Number of Popular non-English\nMovies by Language')
plt.xlabel(None)
plt.ylabel('Num of Movies')
plt.show()

# Plot median rating by language
top_five_df['median_avg_vote'].sort_values(ascending=False).plot(kind='bar', figsize=(10,6))
plt.title('Median Movie Rating of\nTop Five Languages')
plt.xlabel(None)
plt.ylabel('Med Rating (out of 10)')
plt.show()

# Plot median profit by language
(top_five_df['median_profit']/1000000).sort_values(ascending=False).plot(kind='bar', figsize=(10,6))
plt.title('Median Movie Profit of\nTop Five Languages')
plt.xlabel(None)
plt.ylabel('Med Profit (Millions)')
plt.savefig('med_profit_by_lang.png', dpi = 300)

# Plot median profit per decade for top 5 languages
(top_five_df[['90s_median_profit', '00s_median_profit', '10s_median_profit']]/1000000).sort_values(
    by='10s_median_profit',ascending=False).plot(kind='bar',figsize=(10,6))
plt.title('Median Profit per Decade\nof Top Five Languages')
plt.ylabel('Med Profit (Millions)')
plt.legend(labels=['1990s', '2000s', '2010s'])
plt.show()

# Plot median profit margin per decade for top 5 languages
top_five_df[['90s_median_profit_margin', '00s_median_profit_margin', '10s_median_profit_margin']].sort_values(
    by='10s_median_profit_margin',ascending=False).plot(kind='bar',figsize=(10,6))
plt.title('Median Profit Margin per Decade\nof Top Five Languages')
plt.ylabel('Med Profit Margin')
plt.legend(labels=['1990s', '2000s', '2010s'])
plt.ylim(-30,90)
plt.show()



##### Top Five Languages Analysis #####

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
    
# Add mean rating
for key, value in top_five_lang.items():
    top_five_lang[key]['mean_avg_vote'] = round(
        df.groupby('original_language')['avg_vote'].mean().loc[key], 1)
    
# Add median rating
for key, value in top_five_lang.items():
    top_five_lang[key]['median_avg_vote'] = round(
        df.groupby('original_language')['avg_vote'].median().loc[key], 1)
    
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

        
        
##### imdbpy scripts (not used) #####  
        
# Get updated budgets with imdbpy
imdb_list = list(df['imdb_id'])
budget_dict = {}
for movie in imdb_list:
    data = ia.get_movie(movie[2:])
    if 'box office' in data.keys():
        if 'Budget' in data['box office'].keys():
            budget_dict[movie] = int(''.join(filter(str.isdigit, data['box office']['Budget'])))
        else:
            budget_dict[movie] = np.nan
    else:
        budget_dict[movie] = np.nan

    
    
# TMDB popularity metric based on:

# Number of votes for the day
# Number of views for the day
# Number of users who marked it as a "favourite" for the day
    # Number of users who added it to their "watchlist" for the day
# Release date
# Number of total votes
# Previous days score