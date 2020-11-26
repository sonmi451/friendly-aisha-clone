import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

from calendars import scrape_timed_events_from_calender, scrape_all_day_events_from_calender
from embeds import embed_movie_schedule, embed_shitemas_schedule, embed_games_schedule, embed_response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
BOT_USER_ID = os.getenv('BOT_USER_ID')
BOT_ROLE_ID = os.getenv('BOT_ROLE_ID')
MOVIE_AGENDA = os.getenv('MOVIE_AGENDA')
TV_GAMES_AGENDA = os.getenv('TV_GAMES_AGENDA')
SHITEMAS_AGENDA = os.getenv('SHITEMAS_AGENDA')

DEBUG = True

client = commands.Bot(command_prefix='a?')


def get_random_friendly_advice():
    with open('friendly_robot_advice.txt') as f:
        friendly_robot_advice=[line.strip() for line in f]
    random_friendly_message=random.choice(friendly_robot_advice)
    return random_friendly_message


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
    print(str(client.user) + " has connected to Discord Server " + str(guild.name))


@client.event
async def on_message(message):
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author == client.user:
        return

    # if wade used AoE2 shortcut for lol, reply
    if message.author.id == 474091918050066432:
        if '11' in chat_message:
            await message.channel.send("herb_laugh.mp4")

    if any(id in chat_message for id in [BOT_USER_ID, BOT_ROLE_ID]):
        await message.channel.send('Beep boop!')

    if 'robot' in chat_message:
        friendly_message = get_random_friendly_advice()
        await message.channel.send(friendly_message)

    if 'regulations' in chat_message:
        await message.channel.send('Praise be the regulations')

    if 'tv games schedule' in chat_message:
        schedule = scrape_all_day_events_from_calender(TV_GAMES_AGENDA)
        print_schedule = embed_games_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if 'movie schedule' in chat_message:
        schedule = scrape_timed_events_from_calender(MOVIE_AGENDA)
        print_schedule = embed_movie_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if 'shite schedule' in chat_message:
        schedule = scrape_timed_events_from_calender(SHITEMAS_AGENDA)
        print_schedule = embed_shitemas_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if 'shitemas' in chat_message:
        await message.channel.send('SHITEmas is the most wonderful time of the year.')

    await client.process_commands(message)


@client.command(name='movies', help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_movie_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule)
    await ctx.send(embed=print_schedule)


@client.command(name='movie', help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_movie_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule, first=True)
    await ctx.send(embed=print_schedule)


client.run(TOKEN)
