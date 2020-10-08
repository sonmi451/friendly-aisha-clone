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
    events = []
    adgenda_html = requests.get(ADGENDA)
    soup = BeautifulSoup(adgenda_html.text, 'html.parser')
    if not 'Nothing currently scheduled' in soup.text:
        adgenda_events = soup.select("body > div.view-container-border > div > div")
        for event in adgenda_events:
            event_text = event.text
            oneline_event_list = event_text.split('\n')
            events.append(oneline_event_list)
    return events


def embed_schedule(schedule, first=False):
    formattd_schedule = discord.Embed(title='Agenda')
    if not schedule:
        formattd_schedule.add_field(name='Agenda', value='Hmm, looks like nothing is scheduled!')
    else:
        if first:
            schedule = [schedule[0]]

        for event in schedule:
            formattd_schedule.add_field(name=event[1] + ' - ' + event[0],
                                        value=event[2],
                                        inline=False)

    formattd_schedule.add_field(name='Online Schedule',
                                value='[See the calender online](' + ADGENDA + ')',
                                inline=False)
    return formattd_schedule


def embed_response(text):
    robot_response = discord.Embed(title='Beep boop!')
    robot_response.add_field(name='a?', value=text)
    return robot_response


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
    # print(f'{client.user} has connected to Discord Server "{guild.name}!"\n')
    print(str(client.user) + " has connected to Discord Server " + str(guild.name))


@client.event
async def on_message(message):
    if DEBUG:
        # print(f"{message.author}\n {message.content}\n")
        print(str(message.author) + '\n' + str(message.content))

    if message.author == client.user:
        return

    if any(id in message.content for id in [BOT_USER_ID, BOT_ROLE_ID]):
        await message.channel.send(embed=embed_response("Beep boop!"))

    if 'robot' in message.content:
        friendly_message = get_random_friendly_advice()
        await message.channel.send(embed=embed_response(friendly_message))

    if 'regulations' in message.content.lower():
        await message.channel.send(embed=embed_response('Praise be the regulations'))

    if 'movie schedule' in message.content:
        schedule = scrape_events_from_calender()
        print_schedule = embed_schedule(schedule)
        await message.channel.send(embed=print_schedule)
    await client.process_commands(message)


@client.command(name='movies', help='Read the full movie schedule from the calendar')
async def full_schedule(ctx):
    schedule = scrape_events_from_calender()
    print_schedule = embed_schedule(schedule)
    await ctx.send(embed=print_schedule)


@client.command(name='movie', help='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(ctx):
    schedule = scrape_events_from_calender()
    print_schedule = embed_schedule(schedule, first=True)
    await ctx.send(embed=print_schedule)

client.run(TOKEN)
