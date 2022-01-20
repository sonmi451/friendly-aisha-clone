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


def britishify(string, british_to_american, word_len):
    for british_spelling, american_spelling in british_to_american.items():
        if string == american_spelling:
            string = re.sub(
                f'(?<![a-zA-Z]){american_spelling}(?![a-z-Z])', british_spelling, string)
    if len(string) == word_len:
        return string
    else:
        return get_word(british_to_american, word_len)


def get_word(british_to_american, word_set, word_len=5):
    wordle_words = [word for word in word_set if len(word) == word_len]
    chosen_word = None
    while chosen_word == None:
        random_word = random.choice(wordle_words)
        if not random_word[0].isupper():
            chosen_word = random_word
    random_word = britishify(random_word, british_to_american, word_len)
    return random_word


def valid_word(word, word_set):
    if word in word_set:
        return True
    else:
        return False


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


def get_wordle_stats(message, word_set):
    stats_msg = (
        f'Play Wordle on Discord with a selection of {len(word_set)} English words!'
    )
    if len(message) > 1:
        try:
            word_len = int(message[1])
            wordle_words = [word for word in word_set if len(word) == word_len]
            stats_msg = f'There are {len(wordle_words)} English words with {word_len} letters in the Wordle dictionary.'
        except ValueError:
            pass
    return stats_msg


def get_emoji_word(word, regional_indicator_letters):
    emojied_word = [regional_indicator_letters.get(char.lower()) if regional_indicator_letters.get(char.lower()) else char for char in word]
    return ' '.join(emojied_word)
