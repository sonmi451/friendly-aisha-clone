import json

def update_movie_list_file():
    movie_dict = {}
    with open('../resources/movie_watchlist.txt', 'r') as in_file:
        for line in in_file:
            print(line)
            movie_dict[line.strip().title()] = {
                'suggestedBy': 'Sonmi451',
                'votes': 1,
                'IMDB': "",
            }
    with open('../resources/movie_watchlist.json', 'w+') as out_file:
        json.dump(movie_dict, out_file)

update_movie_list_file()
