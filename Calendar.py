from tkinter import *
import requests
import json
from datetime import datetime, timedelta
import os

def fetchEvents():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)

    params = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(request_url, headers=headers, params=params)
    if response.status_code == 200:
        return json.loads(response.text)['events']
    else:
        print("Failed to fetch events")
        return []


def showCalendar(events):
    gui = Tk()
    gui.config(background='grey')
    gui.title("Teamup Calendar")
    gui.attributes("-fullscreen", True)

    # Frame for the Log Off button
    top_frame = Frame(gui, bg='grey')
    top_frame.pack(side='top', fill='x')

    # Place the Log Off button in the top frame
    def logOff():
        gui.destroy()
        os.system("python3 welcome.py")

    Button(top_frame, text="Log Off", command=logOff, font="Consolas 12 bold", padx=10, pady=5).pack(side='right', padx=20, pady=20)

    # Frame for the events
    events_frame = Frame(gui, bg='grey')
    events_frame.pack(expand=True, fill='both')

    for event in events:
        start_time = datetime.fromisoformat(event['start_dt']).strftime("%A, %B %d, %Y %H:%M")
        end_time = datetime.fromisoformat(event['end_dt']).strftime("%H:%M") if 'end_dt' in event else 'Unknown'
        event_title = event['title']
        event_description = event.get('description', 'No description available')
        event_location = event.get('location', 'No location specified')

        event_frame = Frame(events_frame, bg='lightgrey', borderwidth=2, relief="groove")
        event_frame.pack(padx=20, pady=10, fill='x')

        Label(event_frame, text=f"{start_time} - {end_time} | {event_title}", font="Consolas 15 bold", bg='lightgrey').pack(anchor='w', padx=10, pady=5)
        Label(event_frame, text=f"Location: {event_location}", font="Consolas 12", bg='lightgrey').pack(anchor='w', padx=10, pady=2)
        Label(event_frame, text=f"Description: {event_description}", font="Consolas 12", bg='lightgrey', wraplength=500).pack(anchor='w', padx=10, pady=2)

    gui.mainloop()





if __name__=='__main__':
    # Define your Teamup API URL and API key
    api_url = "https://api.teamup.com"
    api_key = "699e02c0555e1804ea722d893851875e8444e8bf17199c8d8e46bc393a60f960"
    calendar_key = "kskp2dg3mpgu24n3ww"
    request_url = f"{api_url}/{calendar_key}/events"
    headers = {"Teamup-Token": api_key}

    events = fetchEvents()
    showCalendar(events)
