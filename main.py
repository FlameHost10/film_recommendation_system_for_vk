import pandas as pd
from math import sqrt
from datetime import datetime


def get_year(title):
    try:
        return int(title[-5:-1])
    except ValueError:
        return 0


def get_genres(genres):
    if genres == '(no genres listed)':
        return []
    return genres.split('|')


def get_k_rating(data):
    rating = 10e10 * data['rating'] / (datetime.timestamp(datetime.now()) - data['timestamp'])
    if rating.count() < 10:
        return rating.mean() * sqrt(rating.count())
    return rating.median() * sqrt(rating.count())


def get_s(data):
    return sqrt(data)


def get_similar_movies(data, title, n):
    df = pd.DataFrame()

    df['title'] = data.groupby('title')['title'].first()
    df['year'] = data.groupby('title')['title'].first().apply(get_year)
    #df['genres'] = data.groupby('title')['genres'].first().apply(get_genres)
    df['rating'] = data.groupby('title')['rating'].median()
    df['count'] = data.groupby('title')['rating'].count()
    df['k_rating'] = data.groupby('title').apply(get_k_rating)

    year = get_year(title)
    k_rating = df['k_rating'].loc[df['title'] == title].values[0]

    df['s'] = (df['k_rating'] - k_rating) ** 2 + (df['year'] - year) ** 2
    df['s'] = df['s'].apply(get_s)

    return df[['k_rating', 's']].sort_values(by='s').head(n + 1)


movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

movie = input('Введите название фильма: ')
n = int(input('n = '))

merged_data = pd.merge(ratings, movies, on='movieId')

print(get_similar_movies(merged_data[['title', 'genres', 'rating', 'timestamp']], movie, n))
