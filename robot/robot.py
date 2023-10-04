################################################################################
# IMPORTS

import asyncio
import os
import re
import discord
import DiscordUtils
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

from calendars import scrape_events_from_calender
from file_helpers import get_aoe_taunts_from_file, get_british_spellings_from_file, \
    get_friendly_advice_from_file, get_nerts_commentry_from_file, \
    get_rock_facts_from_file, get_tv_games_help_from_file, get_word_set_from_file, \
    get_toki_pona_words_from_file, get_regional_indicator_letters_from_file
from helpers import get_random_beep_boop, get_random, get_aoe_taunt, \
    toki_pona_translate
from wordle_helpers import *
from database_helpers import get_movie_watchlist, add_movie_to_watchlist, \
    remove_movie_from_watchlist, get_movie_by_upvotes
from embeds import embed_movie_watchlist, embed_movie_schedule, embed_shitemas_schedule, embed_games_schedule, \
    embed_github, embed_guess_the_soup_rules, embed_response, embed_shitemaster_email, embed_wordle

################################################################################
# LOAD ENVIRONMENT VARIABLES

load_dotenv()

DEBUG = os.getenv('DEBUG_MODE', default=False)
SHITE = os.getenv('SHITE', default=False)
SERVER = os.getenv('DISCORD_SERVER')
WADE_ID = os.getenv('WADE_ID', default=False)
BOT_USER_ID = os.getenv('BOT_USER_ID', default=False)
BOT_ROLE_ID = os.getenv('BOT_ROLE_ID', default=False)
MOVIE_AGENDA = os.getenv('MOVIE_AGENDA', default=False)
TV_GAMES_AGENDA = os.getenv('TV_GAMES_AGENDA', default=False)
SHITEMAS_AGENDA = os.getenv('SHITEMAS_AGENDA', default=False)
SHITEMASTER_EMAIL = os.getenv('SHITEMASTER_EMAIL', default=None)
DB_LOAD_DATA = os.getenv('DATABASE_INIT', default=False)

if DEBUG == '1':
    TOKEN = os.getenv('DISCORD_TOKEN_TEST')
else:
    TOKEN = os.getenv('DISCORD_TOKEN')

################################################################################
# LOAD FILES AS GLOBALS

FRIENDLY_ROBOT_ADVICE = get_friendly_advice_from_file()
AOE_TAUNTS_DICT = get_aoe_taunts_from_file()
ROCK_FACTS = get_rock_facts_from_file()
NERTS = get_nerts_commentry_from_file()
TV_GAMES_HELP = get_tv_games_help_from_file()
BRITISH_WORDS = get_british_spellings_from_file()
WORD_SET = get_word_set_from_file()
REGIONAL_INDICATOR_LETTERS = get_regional_indicator_letters_from_file()
TOKI_PONA_DICT = get_toki_pona_words_from_file()

################################################################################
# OTHER GLOBAL VARS

ALPHABET = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
TOKI_ALPHABET = [x for x in 'AEIOUPTKSMNLJW']
SHITEMASTER_HELP = ['shitemaster email', 'submit shitemaster', 'submit task',
                    'sm email', 'shitemasters assistant email',
                    'shitemaster\'s assistant email', 'shite email']

################################################################################
# LOAD DATABASE

DB_CLIENT = MongoClient("mongodb://database:27017/")
MOVIE_DATABASE = DB_CLIENT["movie_list"]
MOVIE_COLLECTION = MOVIE_DATABASE["movies"]
if DB_LOAD_DATA == '1':
    from database_helpers import load_movie_json_into_db
    print("Populate database")
    load_movie_json_into_db(MOVIE_COLLECTION)

################################################################################
# DISCORDS SETUP

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

if DEBUG == '1':
    client = commands.Bot(command_prefix='test$', intents=intents)
else:
    client = commands.Bot(command_prefix='$', intents=intents)

################################################################################
# EVENT REACTIONS


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            print(f"{client.user} has connected to Discord Server {guild.name}")
            break


@client.event
async def on_member_join(member):
    welcome_message = f"""Wilkommen {member.name}, to the Socially Distant Club!
                          I am your Friendly Aisha Clone,
                          here to be most helpful <3
                          On Wednesdays at 8PM we play ~GAMES~ in voice chat
                          On Sunday evenings we watch movies"""
    await member.send(embed=welcome_message)

################################################################################
# USER COMMANDS

@client.command(name='addmovie',
                help='Add or upvote a movie on the watchlist')
async def add_movie(ctx, *movie):
    if movie:
        movie = ' '.join(movie)
        movie_name = str(movie).title()
        movie_details = {
            '_id': movie_name,
            'suggestedBy': ctx.message.author.name,
            'votes': 1,
            'IMDB': "",
        }
        add_movie_to_watchlist(MOVIE_COLLECTION, movie_details)
        text = f"Thank you for your suggestion: {movie_name}!"
    else:
        text = "you wanna try: `$addmovie The Best Film in the World`"
    response = embed_response(text)
    await ctx.send(embed=response)


@client.command(name='bubblewrap',
                help='Gimme some bubblewrap to pop')
async def bubblewrap(ctx):
    bubblerow = "||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop||\n"
    bubbles = f"Enjoy the bubblewrap:\n{bubblerow * 9}"
    await ctx.send(bubbles)


@client.command(name='delmovie',
                help='Remove a movie to the watchlist')
async def remove_movie(ctx, *movie):
    if movie:
        movie = ' '.join(movie)
        movie_name = str(movie).title()
        remove_movie_from_watchlist(MOVIE_COLLECTION, movie_name)
        text = f"Removed movie from watchlist: {movie_name}!"
    else:
        text = "you wanna try: `$delmovie \"The Best Film in the World\"`"
    response = embed_response(text)
    await ctx.send(embed=response)


@client.command(name='github',
                help='See my insides on Github!')
async def github_url(ctx):
    url = embed_github()
    await ctx.send(embed=url)

@client.command(name='movies',
                help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    # schedule = await scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule()
    await ctx.send(embed=print_schedule)


@client.command(name='movie',
                help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    # schedule = await scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(first=True)
    await ctx.send(embed=print_schedule)


@client.command(name='movielist',
                help='See the watchlist')
async def view_watchlist(ctx):
    watchlist = get_movie_watchlist(MOVIE_COLLECTION)
    responses = embed_movie_watchlist(watchlist)
    if len(responses) > 1:
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(
            ctx, timeout=60)
        await paginator.run(responses)
    else:
        await ctx.send(content='', embed=responses[0])


@client.command(name='parrot',
                help='I\'ll repeat what you say')
async def parrot_speak(ctx, *message):
    if message:
        response = embed_response(' '.join(message))
        await ctx.send(embed=response)


@client.command(name='ponawordle',
                help='Play toki pona wordle in Discord')
async def musi_nimi(ctx, *message):
    if message:
        try:
            word_len = int(message[0])
        except:
            word_len = 4
    else:
        word_len = 4
    try:
        toki_pona_words= [*TOKI_PONA_DICT.keys()]
        toki_pona_length_words= [word for word in toki_pona_words if len(word) == word_len]
        word = get_random(toki_pona_length_words).upper()
        response = embed_wordle(
            {'Wordle!': f'Guessing a {word_len} character toki pona word in {word_len+1} guesses...'})
        await ctx.send(embed=response)
        await wait_for_answer(ctx, word, word_len, toki_pona_words, REGIONAL_INDICATOR_LETTERS, TOKI_ALPHABET)
    except Exception as error:
        response_text = wordle_exception(error, DEBUG)
        response = embed_wordle({'A wordley error!': response_text})
        await ctx.send(embed=response)


@client.command(name='shitemaster',
                help='Recieve a DM of the Shitemaster submission info')
async def full_schedule(ctx):
    embed = embed_shitemaster_email(SHITEMASTER_EMAIL)
    await ctx.author.send('', embed=embed)


@client.command(name='toki',
                help='toki pona translator')
async def toki_translate(ctx, *message):
    if message:
        english = toki_pona_translate(' '.join(message), TOKI_PONA_DICT)
        print(english)
        response = embed_response(english)
        await ctx.send(embed=response)


@client.command(name='tvgames',
                help='What and when are tv games?')
async def full_schedule(ctx):
    schedule = None
    # schedule = await scrape_events_from_calender(TV_GAMES_AGENDA)
    print_schedule = embed_games_schedule(schedule)
    ctx.author.send(embed=print_schedule)


@client.command(name='upvotelist',
                help='See the watchlist sorted by upvotes')
async def view_watchlist_upvote_sorted(ctx):
    watchlist = get_movie_by_upvotes(MOVIE_COLLECTION)
    response = embed_movie_watchlist(watchlist)
    await ctx.send(embed=response)


@client.command(name='wade',
                help='Talk in AOE taunts!')
async def aoe_speak(ctx, taunt_num):
    taunt = get_aoe_taunt(AOE_TAUNTS_DICT, taunt_num)
    if taunt:
        response = embed_response(taunt)
        await ctx.send(embed=response)


@client.command(name='wordle',
                help='Play wordle in Discord')
async def play_wordle(ctx, *message):
    if message:
        if message[0] == "stats":
            response = embed_wordle(
                {"Wordle Stats": get_wordle_stats(message, WORD_SET)}
            )
            await ctx.send(embed=response)
            return
        try:
            word_len = int(message[0])
        except:
            word_len = 5
    else:
        word_len = 5
    try:
        word = get_word(BRITISH_WORDS, WORD_SET, word_len).upper()
        response = embed_wordle(
            {'Wordle!': f'Guessing a {word_len} character word in {word_len+1} guesses...'})
        await ctx.send(embed=response)
        await wait_for_answer(ctx, word, word_len, WORD_SET, REGIONAL_INDICATOR_LETTERS, ALPHABET)
    except Exception as error:
        if DEBUG == '1':
            response_text = ' Debug mode error details:\n```' + str(e) + '```'
        response_text = wordle_exception(error, DEBUG)
        response = embed_wordle({'A wordley error!': response_text})
        await ctx.send(embed=response)


################################################################################
# WORDLE HELPER

async def wait_for_answer(ctx, word, word_len, word_set, emoji_letters, alphabet):
    emoji_correct_word = get_emoji_word(word, emoji_letters)
    tag_user = ctx.author.mention

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
        fail_count = 0
        leftover_alphabet = alphabet
        past_guesses = []
        while not correct:
            msg = await ctx.bot.wait_for('message', timeout=500, check=check)
            player = f'{msg.author}'
            player_title = f'{player.split("#")[0]}\'s Wordle!'
            guess = msg.content.lower()
            emoji_guess_word = get_emoji_word(
                msg.content.lower(), emoji_letters)
            if msg:
                if guess[0] == '$':
                    # Skip bot commands
                    pass
                elif not valid_word(guess, word_set):
                    wordle_invalid_word = {
                        player_title: f'{emoji_guess_word} is not in the dictionary. Please guess again.'}
                    await ctx.send(content=tag_user, embed=embed_wordle(wordle_invalid_word))
                else:
                    correct, wrong_len, leftover_alphabet, squares_response = check_answer(
                        guess, word, leftover_alphabet)
                    # Setup only for valid guesses
                    if not wrong_len:
                        fail_count += 1
                        emoji_alphabet = get_emoji_word(
                            ''.join(leftover_alphabet),
                            emoji_letters)
                        past_guesses += [f'{emoji_guess_word} | {squares_response}']
                        past_guesses_string = '\n'.join(past_guesses)
                        common_response_text = f'{past_guesses_string} - {fail_count}/{word_len+1}'
                    # Respond
                    if correct:
                        wordle_success = {player_title: f'{common_response_text}',
                                          'Correct!': f'The word was {emoji_correct_word}'}
                        await ctx.send(content=tag_user, embed=embed_wordle(wordle_success))
                        return
                    elif wrong_len:
                        wordle_bad_word = {
                            player_title: f'Your guesses must be {word_len} letters long! Try again!'}
                        await ctx.send(content=tag_user, embed=embed_wordle(wordle_bad_word))
                    elif (fail_count == word_len+1):
                        wordle_fail = {player_title: f'{common_response_text}',
                                       'Incorrect!': f'The correct word was {emoji_correct_word}'}
                        await ctx.send(content=tag_user, embed=embed_wordle(wordle_fail))
                        break
                    else:
                        wordle_guess_again = {player_title: f'{common_response_text}',
                                              'Unused Letters': emoji_alphabet}
                        await ctx.send(content=tag_user, embed=embed_wordle(wordle_guess_again))
    except asyncio.TimeoutError:
        wordle_timeout_error = {
            'A wordley timeout': f'Guess quicker next time!\nThe word was {emoji_correct_word}'}
        await ctx.send(content=tag_user, embed=embed_wordle(wordle_timeout_error))

################################################################################
# RESPONSES TO TEXT

@client.event
async def on_message(message):
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author == client.user:
        return

    # if Wade uses AoE shortcuts, reply with their meaning
    if WADE_ID and message.author.id == WADE_ID:
        taunt = get_aoe_taunt(AOE_TAUNTS_DICT, chat_message)
        if taunt:
            response = embed_response(taunt)
            await message.channel.send(embed=response)

    # if you @ the bot it beeps or boops
    if any(id in chat_message for id in [BOT_USER_ID, BOT_ROLE_ID]):
        beep_boop = get_random_beep_boop()
        response = embed_response(beep_boop)
        await message.channel.send(embed=response)

    if 'orb' in chat_message and 'i have counted' not in chat_message:
        orbified_message = re.sub('[aeiou]', 'orb', chat_message)
        await message.channel.send(orbified_message)

    if 'nerts' in chat_message:
        response = get_random(NERTS)
        response = embed_response(response)
        await message.channel.send(embed=response)

    if 'robot' in chat_message:
        friendly_message = get_random(FRIENDLY_ROBOT_ADVICE)
        response = embed_response(friendly_message)
        await message.channel.send(embed=response)

    if 'regulations' in chat_message:
        response = embed_response('Praise be the regulations')
        await message.channel.send(embed=response)

    if 'rock' in chat_message and 'fact' in chat_message:
        rock_message = get_random(ROCK_FACTS)
        response = embed_response(rock_message)
        await message.channel.send(embed=response)

    if 'guess' in chat_message and 'soup' in chat_message:
        response = embed_guess_the_soup_rules()
        await message.channel.send(embed=response)

    if 'tv' in chat_message and 'game' in chat_message:
        tv_games_help = get_random(TV_GAMES_HELP)
        response = embed_response(tv_games_help)
        await message.channel.send(embed=response)

    if 'movie schedule' in chat_message:
        # schedule = await scrape_events_from_calender(MOVIE_AGENDA)
        print_schedule = embed_movie_schedule()
        await message.channel.send(embed=print_schedule)

    if any(x in chat_message.lower() for x in SHITEMASTER_HELP):
        embed = embed_shitemaster_email(SHITEMASTER_EMAIL)
        await message.author.send('', embed=embed)

    if SHITE == '1':
        if 'shitemas' in chat_message:
            response = embed_response(
                'SHITEmas is the most wonderful time of the year.')
            await message.channel.send(embed=response)

        if 'shite schedule' in chat_message:
            schedule = None
            # schedule = await scrape_events_from_calender(SHITEMAS_AGENDA)
            print_schedule = embed_shitemas_schedule(schedule, SHITEMAS_AGENDA)
            await message.channel.send(embed=print_schedule)

    await client.process_commands(message)

################################################################################
# RUN THE ROBOT

client.run(TOKEN)
