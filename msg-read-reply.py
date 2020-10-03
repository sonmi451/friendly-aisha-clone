import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
BOT_USER_ID = os.getenv('BOT_USER_ID')
DEBUG = True

def get_random_friendly_advice():
    with open('friendly_robot_advice.txt') as f:
        friendly_robot_advice=[line.strip() for line in f]
    random_friendly_message=random.choice(friendly_robot_advice)
    return random_friendly_message

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
    print(f'{client.user} has connected to Discord Server "{guild.name}!"\n')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, it\'s nice to see you!'
    )

@client.event
async def on_message(message):
    if DEBUG:
        print(f"{message.author}\n {message.content}\n")

    if message.author == client.user:
        return

    if f'<@!{BOT_USER_ID}>' in message.content or f'<@{BOT_USER_ID}>' in message.content:
        await message.channel.send("Beep boop!")

    if 'robot' in message.content:
        friendly_message = get_random_friendly_advice()
        await message.channel.send(friendly_message)

client.run(TOKEN)
