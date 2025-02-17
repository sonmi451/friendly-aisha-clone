import json

def json_to_txt():
    with open('./resources/movie_watchlist.json', 'r') as in_file:
        movie_watchlist = json.load(in_file)
    movies = []
    for movie in movie_watchlist.keys():
        movies.append(movie)
    with open('./resources/movie_watchlist.txt', 'w') as out_file:
        out_file.write('\n'.join(movies))

json_to_txt()