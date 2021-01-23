import json
import random

def get_random_friendly_advice_from_file():
    with open('friendly_robot_advice.txt') as f:
        friendly_robot_advice = [line.strip() for line in f]
    return friendly_robot_advice


def get_aoe_taunts_from_file():
    with open('aoe_taunts.json') as f:
        aoe_taunts = json.load(f)
    return aoe_taunts


def get_aoe_taunt(aoe_taunts, number):
    taunt = aoe_taunts.get(number)
    return taunt


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
