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


def get_fanfare_from_file():
    fanfare = discord.File(f'../resources/fanfare.mp3')
    return fanfare


def get_random_friendly_advice_from_file():
    with open('../resources/friendly_robot_advice.txt') as f:
        friendly_robot_advice = [line.strip() for line in f]
    return friendly_robot_advice


def get_random_rock_facts_from_file():
    with open('../resources/rock_facts.txt') as f:
        rock_facts = [line.strip() for line in f]
    return rock_facts


def get_random_tv_game_help_from_file():
    with open('../resources/tv_games.txt') as f:
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


def get_random(list_of_things):
    random_friendly_message = random.choice(list_of_things)
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
