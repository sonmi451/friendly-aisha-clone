'''
For getting files, directory structure is assumed to be:

- resources
--- .txt files
--- .json files
- robot
--- .py files

'''

import json
import random
import discord

MOVIE_WATCHLIST = '../resources/movie_watchlist.json'


def get_herb_laugh_from_file():
    herb_laugh = discord.File(f'../resources/11_herb_laugh.mp3')
    return herb_laugh

def get_herb_path():
    return '../resources/11_herb_laugh.mp3'

def get_random_friendly_advice_from_file():
    with open('../resources/friendly_robot_advice.txt') as f:
        friendly_robot_advice = [line.strip() for line in f]
    return friendly_robot_advice


def get_random_rock_facts_from_file():
    with open('../resources/rock_facts.txt') as f:
        rock_facts = [line.strip() for line in f]
    return rock_facts


def get_aoe_taunts_from_file():
    with open('../resources/aoe_taunts.json') as f:
        aoe_taunts = json.load(f)
    return aoe_taunts


def get_aoe_taunt(aoe_taunts, number):
    taunt = aoe_taunts.get(number)
    return taunt


def read_watchlist_from_file():
    movie_watchlist = {}
    try:
        with open(MOVIE_WATCHLIST, 'r') as in_file:
            movie_watchlist = json.load(in_file)
    except FileNotFoundError as e:
        write_watchlist_to_file(movie_watchlist)
    return movie_watchlist


def write_watchlist_to_file(watchlist):
    with open(MOVIE_WATCHLIST, 'w') as out_file:
        json.dump(watchlist, out_file)


def get_movie_watchlist():
    movie_watchlist = read_watchlist_from_file()
    movies = movie_watchlist.keys()
    return sorted(movies)


def get_movie_by_upvotes():
    movie_watchlist = read_watchlist_from_file()
    movies = movie_watchlist.keys()
    upvote_movies = filter(lambda x: movie_watchlist[x]['votes']
                           if movie_watchlist[x]['votes'] > 1 else None,
                           movie_watchlist)
    return sorted(upvote_movies,
                  key=lambda x: (movie_watchlist[x]['votes']),
                  reverse=True)


def add_movie_to_watchlist(movie_name, movie_details):
    watchlist = read_watchlist_from_file()
    if movie_name in watchlist.keys():
        num_votes = watchlist[movie_name].get('votes')
        watchlist[movie_name]['votes'] = num_votes+1
    else:
        watchlist[movie_name] = movie_details
    write_watchlist_to_file(watchlist)


def remove_movie_from_watchlist(movie_name):
    watchlist = read_watchlist_from_file()
    if movie_name in watchlist.keys():
        watchlist.pop(movie_name)
        write_watchlist_to_file(watchlist)


def get_random_friendly_advice(friendly_robot_advice):
    random_friendly_message = random.choice(friendly_robot_advice)
    return random_friendly_message


def get_random_rock_fact(rock_facts):
    random_rock_fact = random.choice(rock_facts)
    return random_rock_fact


def get_random_beep_boop():
    beeps_boops = ['beep boop!',
                   'boop beep!',
                   'boop!',
                   'beep!']
    random_beep = random.choice(beeps_boops)
    return random_beep
