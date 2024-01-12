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

pygame.init()

read_cards = set()

# ThingSpeak channel details
channel_id = 2399393  
write_key = 'RS1DFZK1ZEULO72E'
total_reads = 0  # Initialize total reads counter

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def welcome_sound():
    print("Welcome!")
    play_sound("check.mp3")

#def goodbye_sound():
   # print("Goodbye!")
   # play_sound("check.mp3")
    



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
    # Initialize Pygame and set up the screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Adjust the size as needed
    pygame.display.set_caption("Teamup Calendar")
    clock = pygame.time.Clock()

    # Fonts and Colors
    font = pygame.font.SysFont(None, 36)
    text_color = (0, 0, 0)  # Black color
    background_color = (255, 255, 255)  # White background

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(background_color)

        # Display events
        y = 10  # Starting y position of the first event
        for event in events:
            start_time = datetime.fromisoformat(event['start_dt']).strftime("%A, %B %d, %Y %H:%M")
            end_time = datetime.fromisoformat(event['end_dt']).strftime("%H:%M") if 'end_dt' in event else 'Unknown'
            event_title = event['title']
            text_surface = font.render(f"{start_time} - {end_time} | {event_title}", True, text_color)
            screen.blit(text_surface, (10, y))
            y += 40  # Increase y for the next event

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

    pygame.quit()

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
                    showCalendar(events)
                else:
                    print("No events found or error in fetching events")
            else:
                print("Card not recognized")

            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)
            
if __name__ == '__main__':
    rfid_function()