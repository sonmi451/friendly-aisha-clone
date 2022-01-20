'''
For getting files, directory structure is assumed to be:

- resources
--- .txt files
--- .json files
- robot
--- .py files

'''

import random
import re


def toki_pona_translate(toki_pona, toki_pona_dict):
    english = []
    toki_pona_list = toki_pona.split(' ')
    for word in toki_pona_list:
        english_word = toki_pona_dict.get(word.lower())
        if english_word:
            english.append(english_word)
    if english:
        return ' '.join(english)
    return "that's not a toki pona sentance!"


def get_aoe_taunt(aoe_taunts, number):
    taunt = aoe_taunts.get(number)
    return taunt


def get_random(list_of_things):
    random_thing = random.choice(list_of_things)
    return random_thing


def get_random_beep_boop():
    beeps_boops = ['beep boop!',
                   'boop beep!',
                   'boop!',
                   'beep!']
    random_beep = random.choice(beeps_boops)
    return random_beep
