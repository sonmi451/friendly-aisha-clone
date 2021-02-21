import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

from calendars import scrape_timed_events_from_calender, scrape_all_day_events_from_calender
from helpers import get_random_friendly_advice_from_file, get_random_friendly_advice, \
    get_aoe_taunts_from_file, get_aoe_taunt, get_random_beep_boop, get_movie_watchlist, \
    get_herb_laugh_from_file, add_movie_to_watchlist, remove_movie_from_watchlist, \
    get_movie_by_upvotes
from embeds import embed_movie_watchlist, embed_movie_schedule, embed_shitemas_schedule, embed_games_schedule, \
    embed_github, embed_guess_the_soup_rules, embed_response

load_dotenv()


SERVER = os.getenv('DISCORD_SERVER')
BOT_USER_ID = os.getenv('BOT_USER_ID')
BOT_ROLE_ID = os.getenv('BOT_ROLE_ID')
MOVIE_AGENDA = os.getenv('MOVIE_AGENDA')
TV_GAMES_AGENDA = os.getenv('TV_GAMES_AGENDA')
SHITEMAS_AGENDA = os.getenv('SHITEMAS_AGENDA')

FRIENDLY_ROBOT_ADVICE = get_random_friendly_advice_from_file()
AOE_TAUNTS_DICT = get_aoe_taunts_from_file()
HERB_LAUGH = get_herb_laugh_from_file()

DEBUG = False
SHITE = False

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)

if DEBUG:
    TOKEN = os.getenv('DISCORD_TOKEN_22')
    client = commands.Bot(command_prefix='£', intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
    print(str(client.user) +
          " has connected to Discord Server " +
          str(guild.name))


@client.event
async def on_member_join(member):
    welcome_message = f"""Wilkommen {member.name}, to the Socially Distant Club!
                          I am your Friendly Aisha Clone, here to be most helpful <3
                          On Wednesdays at 8PM we play ~GAMES~ in voice chat
                          On Sunday evening we watch movies"""
    response = embed_response(welcome_message)
    await message.channel.send(embed=response)


@client.event
async def on_message(message):
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author == client.user:
        return

    # if Wade uses AoE shortcuts, reply with their meaning
    if message.author.id == 474091918050066432:
        if '11' in chat_message:
            await message.channel.send(file=HERB_LAUGH)
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

    if 'robot' in chat_message:
        friendly_message = get_random_friendly_advice(FRIENDLY_ROBOT_ADVICE)
        response = embed_response(friendly_message)
        await message.channel.send(embed=response)

    if 'regulations' in chat_message:
        response = embed_response('Praise be the regulations')
        await message.channel.send(embed=response)

    if 'rock' in chat_message and 'fact' in chat_message:
        await message.add_reaction(emoji='<:rockfact:772801261103742976>')

    if 'guess the soup' in chat_message:
        await message.add_reaction(emoji='<:soupguess:806255878902513724>')
        if 'rule' in chat_message:
            response = embed_guess_the_soup_rules()
            await message.channel.send(embed=response)

    if 'tv games schedule' in chat_message:
        schedule = scrape_all_day_events_from_calender(TV_GAMES_AGENDA)
        print_schedule = embed_games_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if 'movie schedule' in chat_message:
        schedule = scrape_timed_events_from_calender(MOVIE_AGENDA)
        print_schedule = embed_movie_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if SHITE:
        if 'shitemas' in chat_message:
            response = embed_response('SHITEmas is the most wonderful time of the year.')
            await message.channel.send(embed=response)

        await message.channel.send(embed=response)
        if 'shite schedule' in chat_message:
            schedule = scrape_timed_events_from_calender(SHITEMAS_AGENDA)
            print_schedule = embed_shitemas_schedule(schedule)
            await message.channel.send(embed=print_schedule)

    await client.process_commands(message)


@client.command(name='movies',
                help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_timed_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule)
    await ctx.send(embed=print_schedule)


@client.command(name='movie',
                help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_timed_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule, first=True)
    await ctx.send(embed=print_schedule)


@client.command(name='movielist',
                help='See the watchlist')
async def view_watchlist(ctx):
    watchlist = get_movie_watchlist()
    response = embed_movie_watchlist(watchlist)
    await ctx.send(embed=response)


@client.command(name='upvotelist',
                help='See the watchlist sorted by upvotes')
async def view_watchlist_upvote_sorted(ctx):
    watchlist = get_movie_by_upvotes()
    response = embed_movie_watchlist(watchlist)
    await ctx.send(embed=response)


@client.command(name='addmovie',
                help='Add or upvote a movie on the watchlist')
async def add_movie(ctx, movie):
    if movie:
        movie_name = str(movie).title()
        movie_details = {
            'suggestedBy': ctx.message.author.name,
            'votes': 1,
            'IMDB': "",
        }
        add_movie_to_watchlist(movie_name, movie_details)
        text=f"Thank you for your suggestion: {movie_name}!"
    else:
        text="you wanna try: `$addmovie \"The Best Film in the World\"`"
    response = embed_response(text)
    await ctx.send(embed=response)


@client.command(name='delmovie',
                help='Remove a movie to the watchlist')
async def remove_movie(ctx, movie):
    if movie:
        movie_name = str(movie).title()
        remove_movie_from_watchlist(movie_name)
        text=f"Removed movie from watchlist: {movie_name}!"
    else:
        text="you wanna try: `$delmovie \"The Best Film in the World\"`"
    response = embed_response(text)
    await ctx.send(embed=response)


@client.command(name='github',
                help='Github page for the repo')
async def github_url(ctx):
    github_url = embed_github()
    await ctx.send(embed=github_url)


@client.command(name='parrot',
                help='I\'ll repeat what you say')
async def parrot_speak(ctx, message):
    if message:
        response = embed_response(message)
        await ctx.send(embed=response)


@client.command(name='wade',
                help='Talk in AOE taunts!')
async def aoe_speak(ctx, taunt_num):
    taunt = get_aoe_taunt(AOE_TAUNTS_DICT, taunt_num)
    if taunt:
        response = embed_response(taunt)
        await ctx.send(embed=response)

client.run(TOKEN)
