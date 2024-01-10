import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

def read_rfid():
    reader = SimpleMFRC522()

    try:
        print("Hold a card near the reader.")
        id, text = reader.read()
        print("Card ID:", id)
        print("Card Text:", text)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    read_rfid()