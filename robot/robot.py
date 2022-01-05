################################################################################
# IMPORTS

import os
import re
import discord
import DiscordUtils
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

from calendars import scrape_events_from_calender
from helpers import get_random_beep_boop, get_random, get_aoe_taunt, \
    get_friendly_advice_from_file, get_aoe_taunts_from_file, \
    get_herb_laugh_from_file, get_nerts_commentry_from_file, \
    get_rock_facts_from_file, get_tv_games_help_from_file, \
    get_british_spellings_from_file, get_word, get_wordle_stats, wait_for_answer
from database_helpers import get_movie_watchlist, add_movie_to_watchlist, \
    remove_movie_from_watchlist, get_movie_by_upvotes
from embeds import embed_movie_watchlist, embed_movie_schedule, embed_shitemas_schedule, embed_games_schedule, \
    embed_github, embed_guess_the_soup_rules, embed_response, embed_shitemaster_email

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
# LOAD FILES

FRIENDLY_ROBOT_ADVICE = get_friendly_advice_from_file()
AOE_TAUNTS_DICT = get_aoe_taunts_from_file()
ROCK_FACTS = get_rock_facts_from_file()
NERTS = get_nerts_commentry_from_file()
TV_GAMES_HELP = get_tv_games_help_from_file()
BRITISH_WORDS = get_british_spellings_from_file()

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

if DEBUG == '1':
    client = commands.Bot(command_prefix='test$')
else:
    client = commands.Bot(command_prefix='$', intents=intents)

################################################################################
# COMMANDS ETC


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


@client.event
async def on_message(message):
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author == client.user:
        return

    # if Wade uses AoE shortcuts, reply with their meaning
    if WADE_ID and message.author.id == WADE_ID:
        if re.search(r'(^|\D)(1{2})(\D|$)', chat_message):
            herb_laugh = get_herb_laugh_from_file()
            await message.channel.send(file=herb_laugh)
        else:
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
        await message.add_reaction(emoji='<:rockfact:772801261103742976>')
        rock_message = get_random(ROCK_FACTS)
        response = embed_response(rock_message)
        await message.channel.send(embed=response)

    if 'guess the soup' in chat_message:
        await message.add_reaction(emoji='<:soupguess:806255878902513724>')
        if 'rule' in chat_message:
            response = embed_guess_the_soup_rules()
            await message.channel.send(embed=response)

    if 'tv' in chat_message and 'game' in chat_message and 'help' in chat_message:
        tv_games_help = get_random(TV_GAMES_HELP)
        response = embed_response(tv_games_help)
        await message.channel.send(embed=response)

    if 'tv games schedule' in chat_message:
        schedule = scrape_events_from_calender(TV_GAMES_AGENDA)
        print_schedule = embed_games_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if 'movie schedule' in chat_message:
        schedule = scrape_events_from_calender(MOVIE_AGENDA)
        print_schedule = embed_movie_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    sm_assistant_msgs = ['shitemaster email', 'submit shitemaster', 'submit task',
                         'sm email', 'shitemasters assistant email',
                         'shitemaster\'s assistant email', 'shite email']
    if any(x in chat_message.lower() for x in sm_assistant_msgs):
        embed = embed_shitemaster_email(SHITEMASTER_EMAIL)
        await message.author.send('', embed=embed)

    if SHITE == '1':
        if 'shitemas' in chat_message:
            response = embed_response(
                'SHITEmas is the most wonderful time of the year.')
            await message.channel.send(embed=response)

        if 'shite schedule' in chat_message:
            schedule = scrape_events_from_calender(SHITEMAS_AGENDA)
            print_schedule = embed_shitemas_schedule(schedule)
            await message.channel.send(embed=print_schedule)

    await client.process_commands(message)


@client.command(name='movies',
                help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule)
    await ctx.send(embed=print_schedule)


@client.command(name='movie',
                help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule, first=True)
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


@client.command(name='upvotelist',
                help='See the watchlist sorted by upvotes')
async def view_watchlist_upvote_sorted(ctx):
    watchlist = get_movie_by_upvotes(MOVIE_COLLECTION)
    response = embed_movie_watchlist(watchlist)
    await ctx.send(embed=response)


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
                help='Github page for the repo')
async def github_url(ctx):
    github_url = embed_github()
    await ctx.send(embed=github_url)


@client.command(name='bubblewrap',
                help='Gimme some bubblewrap to pop')
async def bubblewrap(ctx):
    bubblerow = "||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop||\n"
    bubbles = f"Enjoy the bubblewrap:\n{bubblerow * 9}"
    await ctx.send(bubbles)


@client.command(name='parrot',
                help='I\'ll repeat what you say')
async def parrot_speak(ctx, *message):
    if message:
        response = embed_response(' '.join(message))
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
        if message[0] == 'stats':
            await ctx.send(get_wordle_stats())
        try:
            word_len = int(message[0])
        except:
            word_len = 5
    else:
        word_len = 5
    try:
        word = get_word(BRITISH_WORDS, word_len).upper()
        await ctx.send(f'Guessing a {word_len} character word in {word_len+1} guesses...')
        await wait_for_answer(ctx, word, word_len)
    except Exception as e:
        await (ctx.send('Found no words of that length'))

################################################################################
# RUN THE ROBOT

client.run(TOKEN)
