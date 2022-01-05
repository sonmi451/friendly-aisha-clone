'''
For getting files, directory structure is assumed to be:

- resources
--- .txt files
--- .json files
- robot
--- .py files

'''

import asyncio
import discord
import json
import random
import re
from nltk.corpus import words

MOVIE_WATCHLIST = '../resources/movie_watchlist.json'
# This removes duplicates and caches this to speed up the bot
WORD_SET = set(words.words())


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


def check_answer(answer, word):
    characters = list(answer.upper())
    if len(characters) == len(word):
        response_str = ''
        correct = True
        wrong_len = False
        idx = 0
        for letter in characters:
            if letter == word[idx]:
                response_str += '🟩'
            elif letter in word:
                correct = False
                response_str += '🟦'
            else:
                correct = False
                response_str += '⬛'
            idx += 1
    else:
        response_str = 'Guesses must be the same length as the wordle'
        correct = False
        wrong_len = True
    return correct, response_str, wrong_len


def get_wordle_stats():
    stats_msg = f'Play Wordle on Discord with a selection of {len(WORD_SET)} English words!'
    return stats_msg


def get_emoji_word(word):
    emojied_word = ''
    for character in list(word.lower()):
        if character.isalpha():
            emojied_word += f':regional_indicator_{character}:'
        else:
            emojied_word += character
    return emojied_word


async def wait_for_answer(ctx, word, word_len):
    def check(m):
        '''
        Checks message is by original command user and in the same channel
        '''
        if m.channel != ctx.channel:
            return False
        if m.author != ctx.author:
            return False
        return True
    try:
        correct = False
        fail_count = 1
        while not correct:
            msg = await ctx.bot.wait_for('message', timeout=300, check=check)
            if msg:
                if msg.content[0] == '$':
                    # Skip bot commands
                    pass
                else:
                    correct, response_str, wrong_len = check_answer(
                        msg.content, word)
                    emoji_word = get_emoji_word(msg.content)
                    if correct:
                        await ctx.send(f'{emoji_word} - {fail_count}/{word_len+1}\n' + response_str + f'\nCorrect! The word was {word}')
                    else:
                        await ctx.send(f'{emoji_word} - {fail_count}/{word_len+1}\n' + response_str)
                    if (fail_count == word_len+1):
                        await ctx.send(f'Too many incorrect guesses. The word was {word}')
                        break
                    if not wrong_len:
                        fail_count += 1
    except asyncio.TimeoutError:
        await ctx.send(f'Wordle timed out. Guess quicker next time!\nThe word was {word}')
