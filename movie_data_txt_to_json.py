import json

def txt_to_json():
    movie_dict = {}
    with open('./resources/movie_watchlist.txt', 'r') as in_file:
        for line in in_file:
            movie_name = line.strip().title()
            print(movie_name)
            movie_dict[movie_name] = {
                'suggestedBy': "",
                'votes': 1,
                'IMDB': "",
            }
    with open('./resources/movie_watchlist.json', 'w+') as out_file:
        json.dump(movie_dict, out_file)

txt_to_json()