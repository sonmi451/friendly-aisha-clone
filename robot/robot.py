################################################################################
# IMPORT EXTERNAL PACKAGES

import asyncio
import os
import re
import discord
import DiscordUtils
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

################################################################################
# IMPORT LOCAL PACKAGES

from calendars import scrape_events_from_calender
from file_helpers import get_aoe_taunts_from_file, get_british_spellings_from_file, \
    get_friendly_advice_from_file, get_nerts_commentry_from_file, \
    get_rock_facts_from_file, get_tv_games_help_from_file, get_word_set_from_file, \
    get_toki_pona_words_from_file, get_regional_indicator_letters_from_file, get_vet_clinics_from_file
from helpers import get_random_beep_boop, get_random, get_aoe_taunt, \
    toki_pona_translate
from wordle_helpers import *
from database_helpers import get_movie_watchlist, add_movie_to_watchlist, \
    remove_movie_from_watchlist, get_movie_by_upvotes, export_movie_db_to_json, import_movie_json_to_db
from embeds import embed_movie_watchlist, embed_movie_schedule, embed_shitemas_schedule, embed_games_schedule, \
    embed_github, embed_guess_the_soup_rules, embed_response, embed_shitemaster_email, embed_wordle

################################################################################
# LOAD ENVIRONMENT VARIABLES

load_dotenv()

DEBUG = os.getenv('DEBUG_MODE', default=False)
SHITE = os.getenv('SHITE', default=False)
SERVER = os.getenv('DISCORD_SERVER')
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
VET_CLINICS = get_vet_clinics_from_file()

################################################################################
# OTHER GLOBAL VARS

ALPHABET = [x for x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
TOKI_ALPHABET = [x for x in 'AEIOUPTKSMNLJW']
SHITEMASTER_HELP = ['shitemaster email', 'submit shitemaster', 'submit task', 'sm email', 'shitemasters assistant email', 'shitemaster\'s assistant email', 'shite email']

################################################################################
# LOAD DATABASE

DB_CLIENT = MongoClient("mongodb://database:27017/")
MOVIE_DATABASE = DB_CLIENT["movie_list"]
MOVIE_COLLECTION = MOVIE_DATABASE["movies"]

################################################################################
# DISCORD BOT SETUP

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=intents)

################################################################################
# EVENT REACTIONS

@bot.event
async def on_member_join(member):
    welcome_message = f"""Wilkommen {member.name}, to the Socially Distant Club!
                          I am your Friendly Aisha Clone,
                          here to be most helpful <3
                          On Wednesdays at 8PM we play ~GAMES~ in voice chat
                          On Sunday evenings we watch movies"""
    await member.send(embed=welcome_message)

################################################################################
# SLASH COMMANDS
# https://fallendeity.github.io/discord.py-masterclass/slash-commands/

@bot.command()
async def sync(ctx: commands.Context) -> None:
    await ctx.bot.tree.sync()
    response = embed_response("Synced commands")
    await ctx.send(embed=response)

@bot.tree.command(name='ppl', description='ppl')
async def ppl(interaction: discord.Interaction):
    print("hello ppl!")
    for guild in bot.guilds:
        for member in guild.members:
            print(f"Member: {member}\nRoles:")
            for role in member.roles: print(f"> {role}")
    await interaction.response.send_message('Check the logs why don\'t you')


@bot.tree.command(name='addmovie', description='Add or upvote a movie on the watchlist')
async def add_movie(interaction: discord.Interaction, movie: str):
    movie_name = str(movie).title()
    movie_details = {
        '_id': movie_name,
        'suggestedBy': interaction.user.display_name,
        'votes': 1,
        'IMDB': "",
    }
    add_movie_to_watchlist(MOVIE_COLLECTION, movie_details)
    text = f"Thank you for your suggestion: {movie_name}!"
    response = embed_response(text)
    await interaction.response.send_message(embed=response)


@bot.tree.command(name='bubblewrap', description='Gimme some bubblewrap to pop')
async def bubblewrap(interaction: discord.Interaction):
    bubblerow = "||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop|| ||pop||\n"
    bubbles = f"Enjoy the bubblewrap:\n{bubblerow * 9}"
    await interaction.response.send_message(bubbles)


@bot.tree.command(name='delmovie', description='Remove a movie to the watchlist')
async def remove_movie(interaction: discord.Interaction, movie: str):
    movie_name = str(movie).title()
    remove_movie_from_watchlist(MOVIE_COLLECTION, movie_name)
    text = f"Removed movie from watchlist: {movie_name}!"
    response = embed_response(text)
    await interaction.response.send_message(embed=response)


@bot.tree.command(name='exportmovies', description='Exports movie db to json')
async def movie_export(interaction: discord.Interaction):
    export_movie_db_to_json(MOVIE_COLLECTION)
    await interaction.response.send_message('Exported movie list to file')


@bot.tree.command(name='github', description='See my insides on Github!')
async def github_url(interaction: discord.Interaction):
    url = embed_github()
    await interaction.response.send_message(embed=url)


@bot.tree.command(name='importmovies', description='Populates movie db')
async def movie_import(interaction: discord.Interaction):
    import_movie_json_to_db(MOVIE_COLLECTION)
    await interaction.response.send_message('Imported movie list')


@bot.tree.command(name='movies', description='Read the full movie schedule from the calendar')
async def full_schedule(interaction: discord.Interaction):
    schedule = await scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule)
    await interaction.response.send_message(embed=print_schedule)


@bot.tree.command(name='movie', description='Reads the next scheduled movie schedule from the calendar')
async def next_scheduled(interaction: discord.Interaction):
    schedule = await scrape_events_from_calender(MOVIE_AGENDA)
    print_schedule = embed_movie_schedule(schedule, first=True)
    await interaction.response.send_message(embed=print_schedule)


@bot.tree.command(name='movielist', description='See the watchlist')
async def view_watchlist(interaction: discord.Interaction):
    watchlist = get_movie_watchlist(MOVIE_COLLECTION)
    responses = embed_movie_watchlist(watchlist)
    if len(responses) > 1:
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(interaction, timeout=60)
        await paginator.run(responses)
    else:
        await interaction.response.send_message(content='', embed=responses[0])


@bot.tree.command(name='parrot', description='I\'ll repeat what you say')
async def parrot_speak(interaction: discord.Interaction, sentance: str):
    response = embed_response(sentance)
    await interaction.response.send_message(embed=response)


@bot.tree.command(name='shitemaster', description='Recieve a DM of the Shitemaster submission info')
async def full_schedule(interaction: discord.Interaction):
    embed = embed_shitemaster_email(SHITEMASTER_EMAIL)
    await interaction.response.send_message('', embed=embed)


@bot.tree.command(name='toki', description='toki pona translator')
async def toki_translate(interaction: discord.Interaction, sentance: str):
    english = toki_pona_translate(' '.join(sentance), TOKI_PONA_DICT)
    print(english)
    response = embed_response(english)
    await interaction.response.send_message(embed=response)


@bot.tree.command(name='tvgames', description='What and when are tv games?')
async def full_schedule(interaction: discord.Interaction):
    schedule = None
    print_schedule = embed_games_schedule(schedule)
    await interaction.response.send_message(embed=print_schedule)


@bot.tree.command(name='wade', description='Talk in AOE taunts!')
async def aoe_speak(interaction: discord.Interaction, taunt: str):
    taunt = get_aoe_taunt(AOE_TAUNTS_DICT, taunt)
    if taunt:
        response = embed_response(taunt)
        await interaction.response.send_message(embed=response)

################################################################################
# PREFIX COMMANDS (WORDLE)

@bot.command(name='wordle',
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

@bot.command(name='ponawordle',
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

@bot.event
async def on_message(message: discord.Message) -> None: 
    chat_message = message.content.lower()

    if DEBUG:
        print(str(message.author) + '\n' + str(chat_message))

    if message.author.bot:
        return
    
    if bot.user.mentioned_in(message):
        beep_boop = get_random_beep_boop()
        response = embed_response(beep_boop)
        await message.channel.send(embed=response)

    # VETS NOW
    # check if anyone from vets now is here right now
    if 'vets now' in chat_message:
        await message.channel.send("There is no one from Vets Now here right now.")

    vet_clinics_in_message = [clinic.title() for clinic in VET_CLINICS if(clinic in chat_message)]
    if vet_clinics_in_message:
        if len(vet_clinics_in_message) is 1:
            vet_clinic = vet_clinics_in_message[0]
            print(vet_clinic)
            if vet_clinic == 'Manchester':
                response = "There is a Vets Now clinic in a repurposed car dealership that is right next to Besses o'th'Barn tram stop on the Manchester Metrolink, in Whitefield, within the Metropolitan Borough of Bury."
            else:
                response =f"There is a Vets Now clinic in {vet_clinic}"
            await message.channel.send(response)
        elif len(vet_clinics_in_message) is 2:
            await message.channel.send(f"There are Vets Now clinics in {' and '.join(vet_clinics_in_message)}")
        else:
            response = f"There are Vets Now clinics in: {', '.join(vet_clinics_in_message)}"
            await message.channel.send(response)
        return

    # if '11' in chat_message:
    #     taunt = get_aoe_taunt(AOE_TAUNTS_DICT, '11')
    #     if taunt:
    #         response = embed_response(taunt)
    #         await message.channel.send(embed=response)

    if 'frog' in chat_message:
        await message.channel.send("it's a frog takeover!")

    if 'orb' in chat_message and 'i have counted' not in chat_message:
        orbified_message = re.sub('[aeiou]', 'orb', chat_message)
        await message.channel.send(orbified_message)

    if 'nerts' in chat_message:
        response = get_random(NERTS)
        response = embed_response(response)
        await message.channel.send(embed=response)

    if 'robot' in chat_message:
        friendly_message = get_random(FRIENDLY_ROBOT_ADVICE)
        await message.channel.send(friendly_message)

    if 'regulations' in chat_message:
        await message.channel.send('Praise be the regulations')

    if 'rock' in chat_message and 'fact' in chat_message and ':rock_fact:' not in chat_message:
        rock_message = get_random(ROCK_FACTS)
        response = embed_response(rock_message)
        await message.channel.send(embed=response)

    if 'guess' in chat_message and 'soup' in chat_message and 'rules' in chat_message:
        response = embed_guess_the_soup_rules()
        await message.channel.send(embed=response)

    if 'tv' in chat_message and 'game' in chat_message:
        tv_games_help = get_random(TV_GAMES_HELP)
        await message.channel.send(tv_games_help)

    if 'movie schedule' in chat_message:
        schedule = await scrape_events_from_calender(MOVIE_AGENDA)
        print_schedule = embed_movie_schedule(schedule)
        await message.channel.send(embed=print_schedule)

    if any(x in chat_message for x in SHITEMASTER_HELP):
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

    await bot.process_commands(message)

################################################################################
# RUN THE BOT

bot.run(TOKEN)