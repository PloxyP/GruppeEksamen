from tkinter import *
import requests
import json
from datetime import datetime, timedelta
import os
import pygame
import time
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import thingspeak
import multiprocessing
import simpleaudio

pygame.init()

read_cards = set()

# ThingSpeak channel details
channel_id = 2399393  
write_key = 'RS1DFZK1ZEULO72E'
total_reads = 0  # Initialize total reads counter

def play_sound(file_path):
    wave_obj = simpleaudio.WaveObject.from_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def welcome_sound():
    print("TEST HEJ")
    play_sound("check.mp3")

def declined_sound():
    print("TEST FARVEL")
    play_sound("declined.mp3")

#####################################
    

#Calendar teamup API og Dictionary 

def fetchEvents(api_url, headers, calendar_key):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)

    params = {
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d')
    }

    request_url = f"{api_url}/{calendar_key}/events"
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
        start_time = datetime.fromisoformat(event['start_dt']).strftime("%A, %B %d, %Y %H:%M")
        end_time = datetime.fromisoformat(event['end_dt']).strftime("%H:%M") if 'end_dt' in event else 'Unknown'
        event_title = event['title']
        event_description = event.get('description', 'No description available')
        event_location = event.get('location', 'No location specified')

        event_frame = Frame(scrollable_frame, bg='lightgrey', borderwidth=2, relief="groove")
        event_frame.pack(padx=20, pady=10, fill='x')

        Label(event_frame, text=f"{start_time} - {end_time} | {event_title}", font="Consolas 15 bold", bg='lightgrey').pack(anchor='w', padx=10, pady=5)
        Label(event_frame, text=f"Location: {event_location}", font="Consolas 12", bg='lightgrey').pack(anchor='w', padx=10, pady=2)
        Label(event_frame, text=f"Description: {event_description}", font="Consolas 12", bg='lightgrey', wraplength=500).pack(anchor='w', padx=10, pady=2)

    gui.mainloop()

#RFID Reader og Thingspeak datacollector
def read_rfid(reader, channel):
    global total_reads  # Declare total_reads as global
    try:
        print("Hold a card near the reader.")
        id, text = reader.read()
        print(id)

        # Send data to ThingSpeak for every read
        response = channel.update({'field1': 1})
        print("Data sent to ThingSpeak")

        # Increment total reads count
        total_reads += 1
        total_users_response = channel.update({'field2': total_reads})
        print(f"Total reads count updated on ThingSpeak: {total_reads}")

        return str(id)
    finally:
        GPIO.cleanup()

def rfid_function():
    api_url = "https://api.teamup.com"
    api_key = "699e02c0555e1804ea722d893851875e8444e8bf17199c8d8e46bc393a60f960"
    card_calendar_map = {
        '2054232593': 'kskp2dg3mpgu24n3ww',
        '2206210585': 'ks2yz86rfe8sj5nvq1',
        # Add more card IDs and their corresponding calendar keys
    }
    headers = {"Teamup-Token": api_key}
    reader = SimpleMFRC522()
    channel = thingspeak.Channel(id=channel_id, api_key=write_key)

    while True:
        try:
            card_id = read_rfid(reader, channel)
            print(f"Read card ID: {card_id}")

            if card_id in card_calendar_map:
                calendar_key = card_calendar_map[card_id]
                print(f"Fetching events for calendar key: {calendar_key}")
                events = fetchEvents(api_url, headers, calendar_key)
                if events:
                    welcome_sound()
                    showCalendar(events)
                else:
                    print("No events found or error in fetching events")
            else:
                print("Card not recognized")
                declined_sound()

            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)
            
if __name__ == '__main__':
    rfid_function()