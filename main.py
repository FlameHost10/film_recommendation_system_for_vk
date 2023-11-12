import pandas as pd


def get_similar_movies(data, title, n):
    #data = pd.merge(data, pd.DataFrame(data.groupby('title')['rating'].mean()), on='title')
    data2 = pd.DataFrame(data.groupby('title')['rating'].mean())
    data2['count'] = pd.DataFrame(data.groupby('title')['rating'].count())
    return data2


movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

merged_data = pd.merge(ratings, movies, on='movieId')

movie = input('Введите название фильма: ')
n = int(input('n = '))

print(get_similar_movies(merged_data[['title', 'genres', 'timestamp', 'rating']], movie, n))