import os
import time
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TIME_FORMAT = "%H:%M"

def is_british_summer_time():
    os.environ['TZ'] = 'Europe/London'
    time.tzset()
    return time.localtime().tm_isdst

def scrape_events_from_calender(calender):
    # setup empty events list
    events = []

    if calender:

        # open selenium session to get page HTML
        browser = webdriver.Remote(command_executor="http://selenium:4444/wd/hub",
                                    desired_capabilities={
                                                "browserName": "chrome",
                                            })
  
        print('Open browser')
        browser.get(calender)
        agenda_button = browser.find_element(By.XPATH,"//div[@id='tab-controller-container-agenda']")
        agenda_button.click()
        time.sleep(1)
        agenda_html = browser.page_source
        browser.close()
        browser.quit()

        # scrape calender
        soup = BeautifulSoup(agenda_html, 'html.parser')
        if not 'Nothing currently scheduled' in soup.text:
            adgenda_events = soup.select("body > div#container > div.calendar-container > div#calendarContainer1 > div#viewContainer1 > div#agenda1 >div#agendaEventContainer1 > div#agendaScrollContent1 > div#eventContainer1 > div.day")
            for event in adgenda_events:
                date = ''
                times = []
                descriptions = []
                event_date = event.find("div", class_="date-label")
                if event_date:
                    date = event_date.text
                event_times = event.findAll("span", class_="event-time")
                if event_times:
                    times = [event_time.text if event_time.text != '' else 'All day' for event_time in event_times]
                    # if is_british_summer_time():
                    #     times = [(datetime.strptime(time, TIME_FORMAT) + timedelta(hours=1)).strftime(format=TIME_FORMAT) if time != 'All day' else 'All day' for time in times ]
                event_summary = event.findAll("span", class_="event-title")
                if event_summary:
                    descriptions = [event.text for event in event_summary]

                # format events details
                if date and times and descriptions:
                    oneline_event_list = [date, dict(zip(times, descriptions))]
                    events.append(oneline_event_list)
    return events
