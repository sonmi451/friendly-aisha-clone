import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

from calendars import scrape_timed_events_from_calender, scrape_all_day_events_from_calender
from helpers import get_random_friendly_advice_from_file, get_random_friendly_advice, \
    get_aoe_taunts_from_file, get_aoe_taunt, get_random_beep_boop
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
SHITE = False

FRIENDLY_ROBOT_ADVICE = get_random_friendly_advice_from_file()
AOE_TAUNTS_DICT = get_aoe_taunts_from_file()

client = commands.Bot(command_prefix='a?')


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
    print(str(client.user) +
          " has connected to Discord Server " +
          str(guild.name))


@client.event
async def on_message(message):
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author == client.user:
        return

    # if Wade uses AoE shortcuts, reply with their meaning
    if message.author.id == 474091918050066432:
        taunt = get_aoe_taunt(AOE_TAUNTS_DICT, chat_message)
        if taunt:
            await message.channel.send(taunt)
        elif ' 11' in chat_message or '11 ' in chat_message:
            await message.channel.send("herb_laugh.mp4")


    # if you @ the bot it beeps or boops
    if any(id in chat_message for id in [BOT_USER_ID, BOT_ROLE_ID]):
        beep_boop = get_random_beep_boop()
        await message.channel.send(beep_boop)

    if 'robot' in chat_message:
        friendly_message = get_random_friendly_advice(FRIENDLY_ROBOT_ADVICE)
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

    if SHITE:
        if 'shitemas' in chat_message:
            await message.channel.send('SHITEmas is the most wonderful time of the year.')

        if 'shite schedule' in chat_message:
            schedule = scrape_timed_events_from_calender(SHITEMAS_AGENDA)
            print_schedule = embed_shitemas_schedule(schedule)
            await message.channel.send(embed=print_schedule)

    await client.process_commands(message)


@client.command(name='movies',
                help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_movie_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule)
    await ctx.send(embed=print_schedule)


@client.command(name='movie',
                help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_movie_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule, first=True)
    await ctx.send(embed=print_schedule)


client.run(TOKEN)
