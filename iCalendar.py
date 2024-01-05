import tkinter as tk
from tkinter import scrolledtext
import requests
from icalendar import Calendar
from datetime import datetime

# Function to fetch and parse the iCalendar feed
def fetch_icalendar_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        ical_data = response.text
        cal = Calendar.from_ical(ical_data)
        return cal
    else:
        return None

# Function to display events
def display_events():
    ical_url = "https://ics.teamup.com/feed/ksexjkyiuc4rrib7am/0.ics"
    cal = fetch_icalendar_feed(ical_url)

    if cal:
        event_list.delete(1.0, tk.END)  # Clear previous events
        for event in cal.walk('vevent'):
            event_summary = event.get('summary')
            event_start = event.get('dtstart').dt
            event_end = event.get('dtend').dt
            event_list.insert(tk.END, f"Event: {event_summary}\n")
            event_list.insert(tk.END, f"Start: {event_start}\n")
            event_list.insert(tk.END, f"End: {event_end}\n\n")
    else:
        event_list.delete(1.0, tk.END)
        event_list.insert(tk.END, "Failed to fetch or parse the iCalendar feed.")

# Create a GUI window
root = tk.Tk()
root.title("iCalendar Feed Display")

# Create a button to refresh the feed
refresh_button = tk.Button(root, text="Refresh", command=display_events)
refresh_button.pack()

# Create a scrolled text widget to display events
event_list = scrolledtext.ScrolledText(root, width=40, height=15)
event_list.pack()

# Initial display of events
display_events()

# Start the GUI main loop
root.mainloop()
