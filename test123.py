import cv2
import pygame
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess
from tkinter import *
import requests
import json
from datetime import datetime, timedelta
import os

pygame.init()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

looking_at_camera = False
played_sound = False  # Flag to track whether the sound has been played

# Screen Config
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
pygame.display.set_caption('Welcome Message')
background_color = (0, 0, 0)
screen.fill(background_color)
font = pygame.font.Font(None, 36)

# First Welcome Message
welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
welcome_rect1 = welcome_message1.get_rect(center=(400, 240))

# Display the first welcome message
screen.blit(welcome_message1, welcome_rect1)

# Scrollable Canvas
canvas = Canvas(gui, bg='grey')
scrollbar = Scrollbar(gui, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, bg='grey')

scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

pygame.display.flip()

# Wait for 5 seconds
time.sleep(3)

# Clear the screen for the second message
screen.fill(background_color)
pygame.display.flip()

# Wait for a short moment
time.sleep(0.1)

# Second Welcome Message
welcome_message2 = font.render('Please use your ID Card to log in', True, (255, 255, 255))
welcome_rect2 = welcome_message2.get_rect(center=(400, 240))

# Display the second welcome message
screen.blit(welcome_message2, welcome_rect2)
pygame.display.flip()

# Wait for 5 seconds
time.sleep(12)

# Clear the screen
screen.fill(background_color)
pygame.display.flip()

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

# State variable to track whether to show the welcome screen or calendar
show_welcome_screen = True

# Function to show the welcome screen
def show_welcome():
    global show_welcome_screen
    screen.fill(background_color)
    welcome_rect1 = welcome_message1.get_rect(center=(400, 240))
    screen.blit(welcome_message1, welcome_rect1)
    pygame.display.flip()
    show_welcome_screen = True

# Function to show the calendar
def show_calendar():
    global show_welcome_screen
    events = fetchEvents()
    showCalendar(events)
    show_welcome_screen = False

# ... (remaining functions remain unchanged)

# Main application loop
while True:
    # ... (previous code remains unchanged)

    # Play sounds based on the flag and ensure it's played only once
    if looking_at_camera and not played_sound:
        welcome_sound()
        played_sound = True
        # Check the state variable to decide whether to show the calendar
        if show_welcome_screen:
            show_welcome()
        else:
            show_calendar()

    if not looking_at_camera and played_sound:
        goodbye_sound()
        played_sound = False

    if cv2.waitKey(1) == ord('q'):
        break

    # Add a condition to reset the state and loop back to the welcome screen
    if not looking_at_camera and not show_welcome_screen:
        show_welcome_screen = True
        

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


if __name__=='__main__':
    # Define your Teamup API URL and API key
    api_url = "https://api.teamup.com"
    api_key = "699e02c0555e1804ea722d893851875e8444e8bf17199c8d8e46bc393a60f960"
    calendar_key = "kskp2dg3mpgu24n3ww"
    request_url = f"{api_url}/{calendar_key}/events"
    headers = {"Teamup-Token": api_key}

    events = fetchEvents()
    showCalendar(events)

def read_rfid():
    reader = SimpleMFRC522()

    try:
        print("Hold a card near the reader.")
        id, text = reader.read()
        print("Card ID:", id)
        print("Card Text:", text)

        # Replace '123456789' with the ID of your specific card
        if id == 2054232593:
            print("Opening Calendar.py")
            subprocess.run(["python", "Calendar.py"])

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    read_rfid()

# Load the face and eye classifiers outside the loop
face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        looking_at_camera = False
        played_sound = False  # Reset the flag when no faces are detected

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
            looking_at_camera = True

    cv2.imshow('frame', frame)

    # Play sounds based on the flag and ensure it's played only once
    if looking_at_camera and not played_sound:
        welcome_sound()
        played_sound = True

    if not looking_at_camera and played_sound:
        goodbye_sound()
        played_sound = False

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Wait for a short moment
time.sleep(0.1)

# Quit Pygame
pygame.quit()

