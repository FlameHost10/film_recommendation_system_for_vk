import json

# читаем json файл с коэффициентами схожести фильмов
with open("data/genre_similarity.json", 'r') as json_file:
    map_ratio_genres = json.load(json_file)


def similarityCoefficientByGenre(our_genres):
    with open("data/title.txt", "r") as f:
        title_genres = f.readline().split()
        f.close()
    sum_c = 0  # некоторый коэффициент схожести для жанров 2 фильмов

    if len(title_genres) == 0 or len(our_genres) == 0:  # если нет жанра то по жанрам фильмы несовместимы
        return 0
    if title_genres == our_genres:  # если жанры одинаковы, то по жанрам фильмы идентичны
        return 1
    for i in title_genres:
        cur_sum = 0
        for j in our_genres:
            cur_sum += get_с(i, j)
        cur_sum = len(our_genres)
        sum_c += cur_sum
    return sum_c / len(title_genres) * 0.8


def union_minus_intersection(list1, list2):
    # хотим найти жанры, которые соответствуют только одному из двух фильмов
    union_result = list(set(list1 + list2))
    intersection_result = list(set(list1) & set(list2))
    difference = list(set(union_result) - set(intersection_result))
    return difference


def get_с(genre1, genre2):
    coefficient = 0
    index1 = map_ratio_genres['Genres'].index(genre1)
    coefficient += map_ratio_genres[genre2][index1]
    coefficient = 1 - coefficient  # возвращаем итоговый коэффициент в main.py
    # чем меньше коэффициент, тем более похожи жанры
    return coefficient


def get_title_genres(data_title_genres):
    with open("data/title.txt", "w") as f:
        f.write(' '.join(data_title_genres))
        f.close()
