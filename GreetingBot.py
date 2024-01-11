import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess



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
