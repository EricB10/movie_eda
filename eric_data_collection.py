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