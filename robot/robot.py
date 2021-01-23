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
SHITE = False

client = commands.Bot(command_prefix='a?')


def get_random_friendly_advice():
    with open('friendly_robot_advice.txt') as f:
        friendly_robot_advice = [line.strip() for line in f]
    random_friendly_message = random.choice(friendly_robot_advice)
    return random_friendly_message


def get_random_beep_boop():
    beeps_boops = ['beep boop!',
                   'boop beep!',
                   'boop!',
                   'beep!']
    random_beep = random.choice(beeps_boops)
    return random_beep


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

    # if wade used AoE2 shortcut for lol, reply
    if message.author.id == 474091918050066432:
        # this dict should really be loaded once from a file or something
        aoe_dict = dict([(1,
                          'Yes.'),
                         (2,
                          'No.'),
                         (3,
                          'Food please.'),
                         (4,
                          'Wood please.'),
                         (5,
                          'Gold please.'),
                         (6,
                          'Stone please.'),
                         (7,
                          'Ahh!'),
                         (8,
                          'All hail, king of the losers!'),
                         (9,
                          'Ooh!'),
                         (10,
                          'I\'ll beat you back to Age of Empires.'),
                         (11,
                          '(Herb laugh)'),
                         (12,
                          'AGH, He rushed.'),
                         (13,
                          'Sure, blame it on your ISP.'),
                         (14,
                          'Start the game already!'),
                         (15,
                          'Don\'t point that thing at me!'),
                         (16,
                          'Enemy sighted!'),
                         (17,
                          'It is good to be the king.'),
                         (18,
                          'Monk! I need a monk!'),
                         (19,
                          'Long time, no siege.'),
                         (20,
                          'My granny could scrap better than that.'),
                         (21,
                          'Nice town, I\'ll take it.'),
                         (22,
                          'Quit touching me!'),
                         (23,
                          'Raiding party!'),
                         (24,
                          'Dadgum.'),
                         (25,
                          'Eh, smite me.'),
                         (26,
                          'The wonder, the wonder, the... no!'),
                         (27,
                          'You played two hours to die like this?'),
                         (28,
                          'Yeah, well, you should see the other guy.'),
                         (29,
                          'Roggan.'),
                         (30,
                          'Wololo.'),
                         (31,
                          'Attack an enemy now.'),
                         (32,
                          'Cease creating extra villagers.'),
                         (33,
                          'Create extra villagers.'),
                         (34,
                          'Build a navy.'),
                         (35,
                          'Stop building a navy.'),
                         (36,
                          'Wait for my signal to attack.'),
                         (37,
                          'Build a wonder.'),
                         (38,
                          'Give me your extra resources.'),
                         (39,
                          '(Ally sound)'),
                         (40,
                          '(Enemy sound)'),
                         (41,
                          '(Neutral sound)'),
                         (42,
                          'What age are you in?')])
        try:
            if int(chat_message) in aoe_dict:
                await message.channel.send(aoe_dict[int(chat_message)])
        except ValueError:
            pass

    # if you @ the bot it beeps or boops
    if any(id in chat_message for id in [BOT_USER_ID, BOT_ROLE_ID]):
        beep_boop = get_random_beep_boop()
        await message.channel.send(beep_boop)

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
