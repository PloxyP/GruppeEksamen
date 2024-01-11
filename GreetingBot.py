import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess

# Define the card UID you want to trigger the other script
target_card_uid = "963693451522"

# Initialize the RFID reader
reader = SimpleMFRC522()

try:
    while True:
        print("Hold an RFID card near the reader...")

        # Read the card and get its UID and text
        uid, text = reader.read()

        print(f"Card UID: {uid}")
        print(f"Card Text: {text}")

        if uid == target_card_uid:
            print("Target card detected! Running another script...")
            
            #Run Other script
            subprocess.run(['python', 'calendar.py'])

        # Wait for a moment to avoid rapid card detection
        GPIO.cleanup()
        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    GPIO.cleanup()
