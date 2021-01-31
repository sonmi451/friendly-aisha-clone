'''
For getting files, directory structure is assumed to be:

- resources
-- .txt files
--- .json files
- robot
--- .py files

'''

import json
import random
import discord


def get_herb_laugh_from_file():
    herb_laugh = discord.File(f'../resources/11_herb_laugh.mp3')
    return herb_laugh


def get_random_friendly_advice_from_file():
    with open('../resources/friendly_robot_advice.txt') as f:
        friendly_robot_advice = [line.strip() for line in f]
    return friendly_robot_advice


def get_aoe_taunts_from_file():
    with open('../resources/aoe_taunts.json') as f:
        aoe_taunts = json.load(f)
    return aoe_taunts


def get_aoe_taunt(aoe_taunts, number):
    taunt = aoe_taunts.get(number)
    return taunt


def get_movie_watchlist_from_file():
    with open('../resources/movie_watchlist.txt', 'r') as f:
        movie_watchlist = [line.strip() for line in f if line.strip()]
    return movie_watchlist


def write_movie_to_file(movie):
    watchlist = get_movie_watchlist_from_file()
    if movie not in watchlist:
        with open('../resources/movie_watchlist.txt', 'a') as f:
            f.write(f'\n{movie}')


def remove_movie_from_file(movie):
    watchlist = get_movie_watchlist_from_file()
    with open('../resources/movie_watchlist.txt', 'w+') as out_file:
        for line in watchlist:
            if movie != line.strip():
                out_file.write(f'{line}\n')


def get_random_friendly_advice(friendly_robot_advice):
    random_friendly_message = random.choice(friendly_robot_advice)
    return random_friendly_message


def get_random_beep_boop():
    beeps_boops = ['beep boop!',
                   'boop beep!',
                   'boop!',
                   'beep!']
    random_beep = random.choice(beeps_boops)
    return random_beep
