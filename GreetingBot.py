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

    def logOff():
        gui.destroy()
        os.system("GreetingBot.py")

    Button(top_frame, text="Log Off", command=logOff, font="Consolas 12 bold", padx=10, pady=5).pack(side='right', padx=20, pady=20)

    # Scrollable Canvas
    canvas = Canvas(gui, bg='grey')
    scrollbar = Scrollbar(gui, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='grey')

    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # Track the drag start point
    def start_scroll(event):
        canvas.scan_mark(event.x, event.y)

    # Perform the scrolling
    def perform_scroll(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    canvas.bind("<Button-1>", start_scroll)
    canvas.bind("<B1-Motion>", perform_scroll)

    # Adding events to the scrollable_frame
    for event in events:
        # ... [Your existing code for adding events]

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