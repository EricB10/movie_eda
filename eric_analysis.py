# TMDB popularity metric based on:

# Number of votes for the day
# Number of views for the day
# Number of users who marked it as a "favourite" for the day
# Number of users who added it to their "watchlist" for the day
# Release date
# Number of total votes
# Previous days score



# Create list of num of movies by language
language_count = dict(df['original_language'].value_counts())
language_count = [(key, value) for key, value in language_count.items()]