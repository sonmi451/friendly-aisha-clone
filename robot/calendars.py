import os
import time
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup

TIME_FORMAT = "%H:%M"

def is_british_summer_time():
    os.environ['TZ'] = 'Europe/London'
    time.tzset()
    return time.localtime().tm_isdst

def scrape_events_from_calender(calender):
    events = []
    if calender:
        adgenda_html = requests.get(calender)
        soup = BeautifulSoup(adgenda_html.text, 'html.parser')
        if not 'Nothing currently scheduled' in soup.text:
            adgenda_events = soup.select("body > div.view-container-border > div > div")
            for event in adgenda_events:
                date = ''
                event_date = event.find("div", class_="date")
                if event_date:
                    date = event_date.text
                event_times = event.findAll("td", class_="event-time")
                if event_times:
                    times = [event_time.text if event_time.text != '' else 'All day' for event_time in event_times]
                    if is_british_summer_time():
                        times = [(datetime.strptime(time, TIME_FORMAT) + timedelta(hours=1)).strftime(format=TIME_FORMAT) if time != 'All day' else 'All day' for time in times ]
                event_summary = event.findAll("div", class_="event-summary")
                if event_summary:
                    descriptions = [event.text for event in event_summary]
                oneline_event_list = [date, dict(zip(times, descriptions))]
                events.append(oneline_event_list)
    return events
