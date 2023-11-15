import json
from datetime import datetime
from math import sqrt


def remove_quotes_and_spaces_from_title(movie_title):
    if movie_title[0] == movie_title[-1] and movie_title[0] == '"':
        return movie_title[1:-1].strip()

    return movie_title.strip()


def extract_year_from_title(movie_title):
    try:
        return int(movie_title[-5:-1])
    except ValueError:
        return 0


def get_genre_list(genres):
    if genres == '(no genres listed)':
        return []

    return genres.split('|')


def get_final_rating(data):
    rating = 10e10 * data['rating'] / (datetime.timestamp(datetime.now()) - data['timestamp'])

    return rating.median() * sqrt(rating.count()) / 10e5


with open('data/genre_similarity.json', 'r') as file:
    genre_data = json.load(file)


def get_final_genres(movie2_genres):
    with open('data/title.txt', "r") as file:
        movie1_genres = file.readline().split()

    result = 0

    if len(movie1_genres) == 0 or len(movie2_genres) == 0:
        return 0

    if movie1_genres == movie2_genres:
        return 1

    for genre1 in movie1_genres:
        current = 0

        for genre2 in movie2_genres:
            current += get_с(genre1, genre2)

        current /= len(movie2_genres)
        result += current

    return result / len(movie1_genres) * .8


def union_minus_intersection(list1, list2):
    # хотим найти жанры, которые соответствуют только одному из двух фильмов
    union_result = list(set(list1 + list2))
    intersection_result = list(set(list1) & set(list2))
    difference = list(set(union_result) - set(intersection_result))
    return difference


def get_с(genre1, genre2):
    coefficient = 0
    index1 = genre_data['Genres'].index(genre1)
    coefficient += genre_data[genre2][index1]
    coefficient = 1 - coefficient  # возвращаем итоговый коэффициент в main.py
    # чем меньше коэффициент, тем более похожи жанры
    return coefficient


def get_title_genres(data_title_genres):
    with open("data/title.txt", "w") as f:
        f.write(' '.join(data_title_genres))
        f.close()