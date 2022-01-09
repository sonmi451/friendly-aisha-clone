import json


# This caches words to speed up the bot
def get_word_set_from_file():
    with open('../resources/words.json') as file:
        word_set = json.load(file)
    return word_set 


def get_aoe_taunts_from_file():
    with open('../resources/aoe_taunts.json') as file:
        aoe_taunts = json.load(file)
    return aoe_taunts


def get_british_spellings_from_file():
    with open('../resources/british_spellings.json') as file:
        british_spellings = json.load(file)
    return british_spellings


def get_friendly_advice_from_file():
    with open('../resources/friendly_robot_advice.txt') as file:
        friendly_robot_advice = [line.strip() for line in file]
    return friendly_robot_advice


def get_nerts_commentry_from_file():
    with open('../resources/nerts_commentry.txt') as file:
        nerts_commentry = [line.strip() for line in file]
    return nerts_commentry


def get_regional_indicator_letters_from_file():
    with open('../resources/emoji_letters.json') as file:
        regional_indicator_letters = json.load(file)
    return regional_indicator_letters


def get_rock_facts_from_file():
    with open('../resources/rock_facts.txt') as file:
        rock_facts = [line.strip() for line in file]
    return rock_facts


def get_tv_games_help_from_file():
    with open('../resources/tv_games.txt') as file:
        tv_games = [line.strip() for line in file]
    return tv_games


def read_watchlist_from_file():
    movie_watchlist = {}
    try:
        with open('../resources/movie_watchlist.json', 'r') as in_file:
            movie_watchlist = json.load(in_file)
    except FileNotFoundError as ex:
        write_watchlist_to_file(movie_watchlist)
    return movie_watchlist


def write_watchlist_to_file(watchlist):
    with open('../resources/movie_watchlist.json', 'w') as out_file:
        json.dump(watchlist, out_file)
