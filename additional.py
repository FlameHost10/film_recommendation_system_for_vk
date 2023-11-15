import pandas as pd
from functions import *
from datetime import datetime


def get_similar_movies(data, movie_final_year, genres, n):
    useful_data = pd.DataFrame()

    useful_data['title'] = data.groupby('title')['title'].first().apply(remove_quotes_and_spaces_from_title)
    useful_data['year'] = useful_data['title'].apply(extract_year_from_title)
    useful_data['genres'] = data.groupby('title')['genres'].first().apply(get_genre_list)
    useful_data['rating'] = data.groupby('title')['rating'].median()
    useful_data['count'] = data.groupby('title')['rating'].count()

    useful_data['final_year_x'] = useful_data['year'].apply(lambda year: year / 10e4)
    useful_data['final_genres_y'] = useful_data['genres'].apply(get_final_genres)

    get_title_genres(genres)

    useful_data['similarity_score'] = ((useful_data['final_year_x'] - movie_final_year) ** 2 +
                                       (useful_data['final_genres_y'] - 1) ** 2)

    return useful_data['similarity_score'].sort_values().head(n)


def get_interesting_movies(data, userId, n):
    data = data.loc[data['userId'] == userId]
    data['k'] = 10e10 * data['rating'] / (datetime.timestamp(datetime.now()) - data['timestamp'])

    genres1 = list()
    genres2 = list()
    year1 = 0
    year2 = 0
    for i in data.sort_values(by='k', ascending=False).head(n).values:
        if i[3] >= 4:
            genres1 += get_genre_list(i[2])
            year1 += extract_year_from_title(i[1])
        else:
            genres2 += get_genre_list(i[2])
            year2 += extract_year_from_title(i[1])


    #if genres1:
    return get_similar_movies(data, year1 / n / 10e4, genres1, n)

    #return get_similar_movies(data, )


movie_data = pd.read_csv('data/movies.csv')
rating_data = pd.read_csv('data/ratings.csv')

userId = int(input('Введите userId: '))
n = int(input('n = '))

merged_data = pd.merge(rating_data, movie_data, on='movieId')

print(get_interesting_movies(merged_data[['userId', 'title', 'genres', 'rating', 'timestamp']], userId, n))