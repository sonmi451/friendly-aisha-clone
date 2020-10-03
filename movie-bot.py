import os

import requests
from bs4 import BeautifulSoup

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
BOT_USER_ID = os.getenv('BOT_USER_ID')
ADGENDA = os.getenv('GOOGLE_CALENDER')
DEBUG = True

bot = commands.Bot(command_prefix='a!')

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

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == SERVER:
            break
    print(f'{bot.user.name} has connected to Discord Server "{guild.name}!"\n')

@bot.command(name='schedule', help='...')
async def full_schedule(ctx):
    schedule = scrape_events_from_calender()
    print_schedule = format_full_schedule(schedule)
    await ctx.send(print_schedule)

@bot.command(name='next', help='...')
async def next_scheduled(ctx):
    schedule = scrape_events_from_calender()
    movie = next_movie(schedule)
    await ctx.send(movie)

bot.run(TOKEN)
