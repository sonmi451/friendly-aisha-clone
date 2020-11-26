import requests
from bs4 import BeautifulSoup


def scrape_timed_events_from_calender(calender):
    events = []
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
                times = [event_time.text for event_time in event_times]
            event_summary = event.findAll("div", class_="event-summary")
            if event_summary:
                descriptions = [event.text for event in event_summary]
            oneline_event_list = [date, dict(zip(times, descriptions))]
            events.append(oneline_event_list)
    return events


def scrape_all_day_events_from_calender(calender):
    events = []
    adgenda_html = requests.get(calender)
    soup = BeautifulSoup(adgenda_html.text, 'html.parser')
    if not 'Nothing currently scheduled' in soup.text:
        adgenda_events = soup.select("body > div.view-container-border > div > div")
        for event in adgenda_events:
            event_text = event.text
            oneline_event_list = event_text.split('\n')
            events.append(oneline_event_list)
    return events
