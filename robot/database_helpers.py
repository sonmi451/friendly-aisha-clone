'''
Directory structure is assumed to be:

- data
--- mongodb database
- robot
--- .py files

'''
import json

def get_movie_watchlist(movie_collection):
    movies = []
    for movie in movie_collection.find():
        movies.append(movie['_id'])
    return sorted(movies)


def get_movie_by_upvotes(movie_collection):
    movies = []
    query = { "votes": { "$gt": 1 } }
    for movie in movie_collection.find(query):
        movies.append(movie['_id'])
    return sorted(movies)


def add_movie_to_watchlist(movie_collection, movie_details):
    movie_name = movie_details['_id']
    query = {"_id": movie_name}
    print(f"Looking for movie matching query: {query}")
    search_results = movie_collection.find(query)
    movie_found = False

    # look for record in collection
    for result in search_results:
        movie_found = True
        upvotes = result['votes']
        print(f"Movie {movie_name} has {upvotes} upvotes")
        break

    # either update record
    if movie_found:
        print(f"{movie_name} already in collection")
        new_upvotes = { "$set": { "votes": upvotes+1} }
        movie_collection.update_one(query, new_upvotes)

    # or add new record
    else:
        movie_collection.insert_one(movie_details)
        print(f"{movie_name} added to collection")


def remove_movie_from_watchlist(movie_collection, movie_name):
    query = {"_id": movie_name}
    print(f"Looking for movie matching query: {query}")
    search_results = movie_collection.find(query)
    movie_found = False

    # look for record in collection
    for result in search_results:
        movie_found = True
        break

    # if exists, delete record
    if movie_found:
        movie_collection.delete_one(query)


def import_movie_json_to_db(movie_collection):
    with open('../resources/movie_watchlist.json', 'r') as in_file:
        movie_watchlist = json.load(in_file)
        for movie in movie_watchlist.keys():
            temp_dict = movie_watchlist[movie]
            temp_dict['_id'] = movie
            add_movie_to_watchlist(movie_collection, temp_dict)


def import_movie_list_to_db(movie_collection):
    with open('../resources/movie_watchlist.txt', 'r') as in_file:
        movies = [line.lower().strip() for line in in_file]
        for movie in movies:
            temp_dict = {}
            temp_dict['_id'] = movie
            movie_collection.insert_one(temp_dict)
            print(f'Inserted new record for {movie}')


def export_movie_db_to_json(movie_collection):
    movies = {}
    for movie in movie_collection.find():
        movies[movie['_id']] = {'suggestedBy': movie['suggestedBy'], 'votes': movie['votes'], 'IMDB': movie['IMDB']}
    with open('../resources/movie_watchlist.json', 'w') as out_file:
        json.dump(movies, out_file)


def export_movie_db_to_list(movie_collection):
    movies = []
    for movie in movie_collection.find():
        movies.append(movie['_id'])
    with open('../resources/movie_watchlist.text', 'w') as out_file:
        out_file.write('\n'.join(movies))