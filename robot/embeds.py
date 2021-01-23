import discord


def embed_movie_schedule(schedule, first=False):
    formatted_schedule = discord.Embed(title='Movie Schedule')
    if not schedule:
        formatted_schedule.add_field(name='Empty schedule', value='Hmm, looks like nothing is scheduled!')
    else:
        if first:
            schedule = [schedule[0]]

        for day in schedule:
            formatted_schedule.add_field(name=day[0],
                                        value='\n'.join([str(time + ': ' + description) for time, description in day[1].items()]),
                                        inline=False)

    formatted_schedule.add_field(name='Calender',
                                value='[See the full calender of events online](https://calendar.google.com/calendar/u/0/embed?src=qjva8eaked6q9vdcgqkspqvseg@group.calendar.google.com)',
                                inline=False)
    return formatted_schedule


def embed_shitemas_schedule(schedule, first=False):
    formatted_schedule = discord.Embed(title='SHITEMAS')
    if not schedule:
        formatted_schedule.add_field(name='Empty schedule', value='Hmm, looks like nothing is scheduled!')
    else:
        if first:
            schedule = [schedule[0]]

        for day in schedule:
            formatted_schedule.add_field(name=day[0],
                                        value='\n'.join([str(time + ': ' + description) for time, description in day[1].items()]),
                                        inline=False)

    formatted_schedule.add_field(name='Calender',
                                value='[See the full calender of events online](https://calendar.google.com/calendar/embed?src=c5ilkhfkd424ddm47unrfuvd9c%40group.calendar.google.com)',
                                inline=False)
    return formatted_schedule


def embed_games_schedule(schedule):
    formatted_schedule = discord.Embed(title='TV Games')
    formatted_schedule.add_field(name='Every Wednesday at 8PM!', value='join Acres Greg in the TV games voice channel for socialising and games')
    for day in schedule:
        formatted_schedule.add_field(name=day[0],
                                    value='\n'.join(day[1:]),
                                    inline=False)
    return formatted_schedule


def embed_github():
    robot_response = discord.Embed()
    robot_response.add_field(name='See my Source Code:',
                            value='[https://github.com/sonmi451/friendly-aisha-clone](https://github.com/sonmi451/friendly-aisha-clone)',
                            inline=False)
    return robot_response


def embed_response(message):
    robot_response = discord.Embed(title=message)
    return robot_response
