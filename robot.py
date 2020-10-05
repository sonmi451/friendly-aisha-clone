import os
import random

import discord
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
BOT_USER_ID = os.getenv('BOT_USER_ID')
BOT_ROLE_ID = os.getenv('BOT_ROLE_ID')
ADGENDA = os.getenv('GOOGLE_CALENDER')

DEBUG = True

client = commands.Bot(command_prefix='a?')


def scrape_events_from_calender():
    adgenda_html = requests.get(ADGENDA)
    soup = BeautifulSoup(adgenda_html.text, 'html.parser')
    adgenda_events = soup.select("body > div.view-container-border > div > div")
    events = []
    for event in adgenda_events:
        event_text = event.text
        oneline_event_text = event_text.replace('\n', ' ').replace('\r', '')
        events.append(oneline_event_text)
    return events


def format_full_schedule(schedule):
    return ',\n'.join(schedule)


def next_movie(schedule):
    return schedule[0]


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
    print(f'{client.user} has connected to Discord Server "{guild.name}!"\n')


@client.event
async def on_message(message):
    if DEBUG:
        print(f"{message.author}\n {message.content}\n")

    if message.author == client.user:
        return

    if any(id in message.content for id in [BOT_USER_ID, BOT_ROLE_ID]):
        await message.channel.send("Beep boop!")

    if 'robot' in message.content:
        friendly_message = get_random_friendly_advice()
        await message.channel.send(friendly_message)

    if 'movie schedule' in message.content:
        schedule = scrape_events_from_calender()
        print_schedule = format_full_schedule(schedule)
        await message.channel.send(print_schedule)

    await client.process_commands(message)


@client.command(name='movies', help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_events_from_calender()
    print_schedule = format_full_schedule(schedule)
    await ctx.send(print_schedule)


@client.command(name='movie', help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_events_from_calender()
    movie = next_movie(schedule)
    await ctx.send(movie)

client.run(TOKEN)
