import json

with open("data/genre_similarity.json", 'r') as json_file:
    map_ratio_genres = json.load(json_file)


def similarityCoefficientByGenre(genre1, genre2): #ВЫ ПРИНИМАЕТЕ ДВА СПИСКА ЛЯБЛЯБ
    coefficient = 0
    index1 = map_ratio_genres['Genres'].index(genre1)
    coefficient += map_ratio_genres[genre2][index1] #ТАК НЕ ПОЙДЕТ НАДО ПЕРЕДЕЛЫВАТЬ -----------------------------------
    coefficient = 1 - coefficient
    return coefficient
