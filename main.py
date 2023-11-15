import pandas as pd
from functions import *


def get_similar_movies(data, movie_title, n):
    useful_data = pd.DataFrame()

    useful_data['title'] = data.groupby('title')['title'].first().apply(remove_quotes_and_spaces_from_title)
    useful_data['year'] = useful_data['title'].apply(extract_year_from_title)
    useful_data['genres'] = data.groupby('title')['genres'].first().apply(get_genre_list)
    useful_data['rating'] = data.groupby('title')['rating'].median()
    useful_data['count'] = data.groupby('title')['rating'].count()

    useful_data['final_year_x'] = useful_data['year'].apply(lambda year: year / 10e4)
    useful_data['final_genres_y'] = useful_data['genres'].apply(get_final_genres)
    useful_data['final_rating_z'] = data.groupby('title').apply(get_final_rating)

    get_title_genres(useful_data['genres'].loc[useful_data['title'] == movie_title].values[0])

    movie_final_year = useful_data['final_year_x'].loc[useful_data['title'] == movie_title].values[0]
    movie_final_genres = useful_data['final_genres_y'].loc[useful_data['title'] == movie_title].values[0]
    movie_final_rating = useful_data['final_rating_z'].loc[useful_data['title'] == movie_title].values[0]

    useful_data['similarity_score'] = ((useful_data['final_rating_z'] - movie_final_rating) ** 2 +
                                       (useful_data['final_year_x'] - movie_final_year) ** 2 +
                                       (useful_data['final_genres_y'] - movie_final_genres) ** 2)

    return useful_data['similarity_score'].sort_values().head(n + 1)


movie_data = pd.read_csv('data/movies.csv')
rating_data = pd.read_csv('data/ratings.csv')

movie_title = input('Введите название фильма: ')
n = int(input('n = '))

merged_data = pd.merge(rating_data, movie_data, on='movieId')

print(get_similar_movies(merged_data[['title', 'genres', 'rating', 'timestamp']], movie_title, n))
