import json

with open("data/genre_similarity.json", 'r') as json_file:
    map_ratio_genres = json.load(json_file)


def similarityCoefficientByGenre(our_genres):
    sum_c = 0
    with open("data/title.txt", "r") as f:
        title_genres = f.readline().split()
        f.close()
    if title_genres == our_genres:
        return 0
    diff = union_minus_intersection(title_genres, our_genres)
    if len(title_genres) >= len(our_genres):
        for i in diff:
            cur_sum = 0
            for j in our_genres:
                cur_sum += get_k(i, j)
            cur_sum = len(our_genres)
            sum_c += cur_sum
        return sum_c / len(diff) * 0.8
    if len(title_genres) < len(our_genres):
        for i in diff:
            cur_sum = 0
            for j in title_genres:
                cur_sum += get_k(i, j)
            cur_sum /= len(our_genres)
            sum_c += cur_sum
        return sum_c / len(diff) * 0.8


def union_minus_intersection(list1, list2):
    union_result = list(set(list1 + list2))
    intersection_result = list(set(list1) & set(list2))
    difference = list(set(union_result) - set(intersection_result))
    return difference


def get_k(genre1, genre2):
    coefficient = 0
    index1 = map_ratio_genres['Genres'].index(genre1)
    coefficient += map_ratio_genres[genre2][index1]
    coefficient = 1 - coefficient
    return coefficient


def get_title_genres(data_title_genres):
    with open("data/title.txt", "w") as f:
        f.write(' '.join(data_title_genres))
        f.close()
