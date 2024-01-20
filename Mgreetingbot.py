#------------------------------IMPORTS----------------------------------------#
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
from multiprocessing import Process, Value
from pydub import AudioSegment
from pydub.playback import play

#----------------------------GLOBAL SETUP-------------------------------------#
pygame.init()
read_cards = set()

# ThingSpeak channel details
channel_id = 2399393  
write_key = 'RS1DFZK1ZEULO72E'
total_reads = 0  # Initialize total reads counter

#Delt variabel
KortGodkendt = Value('b', False)
KortScannet = Value('b', False)
ExitGUI = Value('b', False)

#-----------------------------FUNCTIONS---------------------------------------#
def play_sound(file_path):
    try:
        sound = AudioSegment.from_file(file_path, format="wav")
        play(sound)
    except Exception as e:
        print(f"Error playing sound: {e}")

def welcome_sound():
    print("TEST HEJ")
    play_sound("check.wav")

def declined_sound():
    print("TEST FARVEL")
    play_sound("declined.wav")

#####################################
    

#Calendar teamup API og Dictionary 

def fetchEvents(api_url, headers, calendar_key):        #Henter kalenderdata fra teamup.com
    start_date = datetime.now()                         #datetime til brug af, fra hvornår henter vi data fra nu og 7 dage frem
    end_date = start_date + timedelta(days=7)

    params = {                                          #yderligere indeling i åååå-mm-dd på start og slut gennem datetime
        'startDate': start_date.strftime('%Y-%m-%d'),
        'endDate': end_date.strftime('%Y-%m-%d')
    }

    request_url = f"{api_url}/{calendar_key}/events"    #Sammensætter det ønsket endpoint. api_url er fixed men calendar_key er ud fra card_reads
    response = requests.get(request_url, headers=headers, params=params) #den endelig requst til teamup med endpoint, api key og datoer
    if response.status_code == 200:                     #API check om alt går som det skal.
        return json.loads(response.text)['events']
    else:
        print("Failed to fetch events")
        return []
    
def showCalendar(events, ExitGUI):                      #GUI funktion der laver viser et visuel layout
    gui = Tk()
    gui.config(background='grey')
    gui.title("Teamup Calendar")
    gui.attributes("-fullscreen", True) 

    # Frame for the Log Off button                      #sæt layout øverst og placering af Log Off knappen
    top_frame = Frame(gui, bg='grey')
    top_frame.pack(side='top', fill='x')

    def logOff(ExitGUI):                                #Når Log Off knappen bliver trykker lukker den kalenderen 
        ExitGUI.value = True                            #Bool som ændre statement i multiprocessing
        time.sleep(2)                                   #Tid til multiprocessing at reagerer
        gui.destroy()                                   #luk kalender layout ned
        GPIO.setmode(GPIO.BCM)                          #reset lyset op igen
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, GPIO.LOW)

    Button(top_frame, text="Log Off", command=lambda: logOff(ExitGUI), font="Consolas 12 bold", padx=10, pady=5).pack(side='right', padx=20, pady=20) #udsenende af Log Off

    #Scroll funktion på kalenderen
    canvas = Canvas(gui, bg='grey')
    scrollbar = Scrollbar(gui, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='grey')

    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

    # Funktion til scroll
    def start_scroll(event):
        canvas.scan_mark(event.x, event.y)

    # Udførelse af scoll i forhold til hvor meget du scroll
    def perform_scroll(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    canvas.bind("<Button-1>", start_scroll)
    canvas.bind("<B1-Motion>", perform_scroll)

    # Indsættelse af data i layout. description og locations ect fra teamup kalender
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

    gui.mainloop()          #GUI layout loop

#RFID Reader og Thingspeak datacollector
def read_rfid(reader, channel):                         #Fuktion for RFID læseren og data der sendes til thingspeak.com
    global total_reads                                  #Gøre total_reads til global
    try:
        print("Hold a card near the reader.")
        id, text = reader.read()                        #læser RFID og printer kortnummer = ID
        print(id)

        # Send data to ThingSpeak for every read
        response = channel.update({'field1': 1})
        print("Data sent to ThingSpeak")

        # Increment total reads count
        total_reads += 1
        total_users_response = channel.update({'field2': total_reads})
        print(f"Total reads count updated on ThingSpeak: {total_reads}")

        # Check if the ID is in the card_calendar_map and send its key to ThingSpeak
        if str(id) in card_calendar_map:
            calendar_key = card_calendar_map[str(id)]
            calendar_key_response = channel.update({'field3': id})
            print(f"Calendar key '{calendar_key}' sent to ThingSpeak for ID {id}")
        else:
            print(f"No calendar key found for ID {id}")

        return str(id)
    except Exception as e:
        print(f"Error: {e}")

        return str(id)
    finally:
        GPIO.cleanup() 

def rfid_function(KortGodkendt, KortScannet,ExitGUI):
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
                KortScannet.value = True
                if events:
                    KortGodkendt.value = True
                    welcome_sound()
                    showCalendar(events, ExitGUI)
                else:
                    print("No events found or error in fetching events")
            else:
                print("Card not recognized")
                KortScannet.value = True
                KortGodkendt.value = False
                declined_sound()

            time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)

#----------------------------MAIN-----------------------------------------#            
if __name__ == '__main__':
    rfid_function(KortGodkendt, KortScannet, ExitGUI)