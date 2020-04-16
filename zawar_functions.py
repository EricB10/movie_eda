import csv
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from zawar_keys import tapi_key
import time
import ast


def get_tmdb_toprated(params,api_key):
    url='https://api.themoviedb.org/3/movie/top_rated?api_key={}'.format(api_key)
    response=requests.get(url,params=params)
    return response.json()

def parse_toprated(toprated):
    parsed_data=[]
    for i in toprated['results']:
        data=[
            i['id'],i['title'],i['original_language'],i['vote_average'],i['vote_count'],i['popularity'],
            i['genre_ids'],i['release_date'],i['adult']
        ]
        parsed_data.append(data)
    return parsed_data

def save_data(file_name,data):
    with open(file_name, "a", newline="", encoding='utf-8') as a:
        writer = csv.writer(a)
        writer.writerows(data)
        

def get_movie_details(mov_id,api_key):
    url2='https://api.themoviedb.org/3/movie/{}?api_key={}'.format(mov_id,api_key)
    response=requests.get(url2)
    return response.json()

def parse_movie(mov_data):
    parsed_data=[
        mov_data['id'],mov_data['imdb_id'],mov_data['budget'],mov_data['revenue'],
        [genre['name'] for genre in mov_data['genres']],mov_data['original_title'],
        [c['name'] for c in mov_data['production_countries']],mov_data['runtime'],mov_data['status']
    ]
    return parsed_data


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