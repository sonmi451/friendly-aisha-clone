'''
For getting files, directory structure is assumed to be:

- resources
--- .txt files
--- .json files
- robot
--- .py files

'''

import discord
import json
import random
import re

MOVIE_WATCHLIST = '../resources/movie_watchlist.json'
# This caches words to speed up the bot
with open('../resources/words.json') as file:
    WORD_SET = json.load(file)


def get_herb_laugh_from_file():
    herb_laugh = discord.File('../resources/11_herb_laugh.mp3')
    return herb_laugh


def get_friendly_advice_from_file():
    with open('../resources/friendly_robot_advice.txt') as file:
        friendly_robot_advice = [line.strip() for line in file]
    return friendly_robot_advice


def get_rock_facts_from_file():
    with open('../resources/rock_facts.txt') as file:
        rock_facts = [line.strip() for line in file]
    return rock_facts


def get_tv_games_help_from_file():
    with open('../resources/tv_games.txt') as file:
        tv_games = [line.strip() for line in file]
    return tv_games


def get_nerts_commentry_from_file():
    with open('../resources/nerts_commentry.txt') as file:
        nerts_commentry = [line.strip() for line in file]
    return nerts_commentry


def get_aoe_taunts_from_file():
    with open('../resources/aoe_taunts.json') as file:
        aoe_taunts = json.load(file)
    return aoe_taunts


def get_aoe_taunt(aoe_taunts, number):
    taunt = aoe_taunts.get(number)
    return taunt


def read_watchlist_from_file():
    movie_watchlist = {}
    try:
        with open(MOVIE_WATCHLIST, 'r') as in_file:
            movie_watchlist = json.load(in_file)
    except FileNotFoundError as ex:
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


def britishify(string, british_to_american):
    for british_spelling, american_spelling in british_to_american.items():
        string = re.sub(
            f'(?<![a-zA-Z]){american_spelling}(?![a-z-Z])', british_spelling, string)
    return string


def get_british_spellings_from_file():
    with open('../resources/british_spellings.json') as file:
        british_spellings = json.load(file)
    return british_spellings


def get_word(british_to_american, word_len=5):
    wordle_words = [word for word in WORD_SET if len(word) == word_len]
    chosen_word = None
    while chosen_word == None:
        random_word = random.choice(wordle_words)
        if not random_word[0].isupper():
            chosen_word = random_word
    if random_word in british_to_american:
        random_word = britishify(random_word, british_to_american)
    return random_word


def check_answer(answer, word, leftover_alphabet):
    characters = list(answer.upper())
    squares_response = ''
    if len(characters) == len(word):
        correct = True
        wrong_len = False
        idx = 0
        leftover_alphabet = [
            x for x in leftover_alphabet if x not in characters]
        for letter in characters:
            if letter == word[idx]:
                squares_response += '🟩'
            elif letter in word:
                correct = False
                squares_response += '🟦'
            else:
                correct = False
                squares_response += '⬛'
            idx += 1
    else:
        correct = False
        wrong_len = True
    return correct, wrong_len, leftover_alphabet, squares_response


def get_wordle_stats():
    stats_msg = f'Play Wordle on Discord with a selection of {len(WORD_SET)} English words!'
    return stats_msg


def get_emoji_word(word):
    emojied_word = []
    for character in list(word.lower()):
        if character.isalpha():
            emojied_word += [f':regional_indicator_{character}:']
        else:
            emojied_word += [character]
    return ' '.join(emojied_word)
