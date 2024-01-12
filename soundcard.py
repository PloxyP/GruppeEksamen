import pygame
import time
from mfrc522 import SimpleMFRC522

pygame.init()

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