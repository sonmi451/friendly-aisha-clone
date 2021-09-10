import discord


class AishaEmbed():
    '''Embed extensions.'''

    def __init__(self):
        self.cont = 1
        self.embed = None
        self.embeds = []

    def base_movie_embed(self, title_str, description):
        colour = colour = discord.Colour.random()
        if self.cont > 1:
            title = f'{title_str} ({self.cont})'
            description = 'More movies below'
        else:
            title = f'{title_str}'

        self.embed = discord.Embed(
            title=title, description=description, colour=colour)

    def embed_constrain(self, name, value=None):
        self.embeds.append(self.embed)
        self.base_movie_embed()
        if value:
            self.embed.add_field(name=name, value=value)

    def process_the(self):
        processed_movies = []
        for movie in self.all_movies:
            if movie[:4] == "The ":
                movie = movie[4:] + ", The"
            processed_movies.append(movie)
        self.all_movies = processed_movies

    def set_all_movies(self):
        count = 1
        alphabet = None
        value = ''
        self.process_the()
        for text in sorted(self.all_movies):
            name = text[0]

            if alphabet is None:
                alphabet = name
            embed_len = len(alphabet) + len(value) + \
                len(self.embed) + len(name)
            field_len = len(alphabet) + len(value) + len(text) + len(name)

            if embed_len > 5998:
                count += 1
                self.cont += 1
                self.embed_constrain(alphabet)

            if name != alphabet[0]:
                self.embed.add_field(name=alphabet, value=value)
                alphabet = name
                value = text
                continue

            if field_len > 1022:
                self.embed.add_field(name=alphabet, value=value)
                alphabet = f'{name} (cont...)'
                value = text
                continue

            if value:
                value += f'\n{text}'
            else:
                value = text

    def format_all_movies_embed(self, all_movies):
        self.all_movies = all_movies
        self.cont = 1
        self.embeds = []
        self.base_movie_embed(title_str='Movie Watchlist',
                              description='Movies in the pool of possible watches')

        self.set_all_movies()

        self.embeds.append(self.embed)

        return self.embeds


def embed_movie_watchlist(movie_watchlist):
    embedder = AishaEmbed()
    responses = embedder.format_all_movies_embed(movie_watchlist)
    return responses[0]


def embed_movie_schedule(schedule, first=False):
    formatted_schedule = discord.Embed(title='Movie Schedule')
    if not schedule:
        formatted_schedule.add_field(
            name='Empty schedule', value='Hmm, looks like nothing is scheduled!')
    else:
        if first:
            schedule = [schedule[0]]

        for day in schedule:
            formatted_schedule.add_field(name=day[0],
                                         value='\n'.join(
                                             [str(time + ': ' + description) for time, description in day[1].items()]),
                                         inline=False)

    formatted_schedule.add_field(name='Calender',
                                 value='[See the full calender of events online](https://calendar.google.com/calendar/u/0/embed?src=qjva8eaked6q9vdcgqkspqvseg@group.calendar.google.com)',
                                 inline=False)
    return formatted_schedule


def embed_shitemas_schedule(schedule, first=False):
    formatted_schedule = discord.Embed(title='SHITEMAS')
    if not schedule:
        formatted_schedule.add_field(
            name='Empty schedule', value='Hmm, looks like nothing is scheduled!')
    else:
        if first:
            schedule = [schedule[0]]

        for day in schedule:
            formatted_schedule.add_field(name=day[0],
                                         value='\n'.join(
                                             [str(time + ': ' + description) for time, description in day[1].items()]),
                                         inline=False)

    formatted_schedule.add_field(name='Calender',
                                 value='[See the full calender of events online](https://calendar.google.com/calendar/embed?src=c5ilkhfkd424ddm47unrfuvd9c%40group.calendar.google.com)',
                                 inline=False)
    return formatted_schedule


def embed_games_schedule(schedule):
    formatted_schedule = discord.Embed(title='TV Games')
    formatted_schedule.add_field(name='Every Wednesday at 8PM!',
                                 value='join Acres Greg in the TV games voice channel for socialising and games')
    for day in schedule:
        formatted_schedule.add_field(name=day[0],
                                     value='\n'.join(
                                         [str(description) for time, description in day[1].items()]),
                                     inline=False)
    return formatted_schedule


def embed_github():
    robot_response = discord.Embed()
    robot_response.add_field(name='See my Source Code:',
                             value='[https://github.com/sonmi451/friendly-aisha-clone](https://github.com/sonmi451/friendly-aisha-clone)',
                             inline=False)
    return robot_response


def embed_guess_the_soup_rules():
    formatted_rules = discord.Embed(title='The Rules of Guess the Soup')
    formatted_rules.add_field(name='1', value='Everything is a soup!',
                              inline=False)
    formatted_rules.add_field(name='2', value='Every soup probably contains onion and garlic',
                              inline=False)
    formatted_rules.add_field(name='3', value='Consider perl barley',
                              inline=False)
    return formatted_rules


def embed_response(title):
    response = discord.Embed(title=title)
    return response


def embed_shitemaster_email(email):
    description = f'As much video and photo evidence as possible should be provided to \
        the SHITEmaster’s assistant (Aisha!) before the task deadline. \
            This includes video of you reading out the tasks and how you do \
                the task(not just the finished task).\nAll evidence should be \
                    shared in Google Photos or email to **{email}** 🖖'
    sm_email = discord.Embed(title='Submit Your Shitemaster Tasks',
                             description=description)

    return sm_email
