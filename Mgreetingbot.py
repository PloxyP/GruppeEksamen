from mfrc522 import SimpleMFRC522
import subprocess

# Define the card UID you want to trigger the other script
target_card_uid = "963693451522"

# Initialize the RFID reader
reader = SimpleMFRC522()

try:
    while True:
        print("Hold an RFID card near the reader...")
        
def read_rfid():
    reader = SimpleMFRC522()

        # Read the card and get its UID and text
        uid, text = reader.read()
    try:
        print("Hold a card near the reader.")
        id, text = reader.read()
        print("Card ID:", id)
        print("Card Text:", text)

        print(f"Card UID: {uid}")
        print(f"Card Text: {text}")
        # Replace '123456789' with the ID of your specific card
        if id == 963693451522:
            print("Opening Calendar.py")
            subprocess.run(["python", "Calendar.py"])

        if uid == target_card_uid:
            print("Target card detected! Running another script...")

            #Run Other script
            subprocess.run(['python', 'calendar.py'])

        # Wait for a moment to avoid rapid card detection
    finally:
        GPIO.cleanup()
        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated.")
finally:
    GPIO.cleanup()
if __name__ == "__main__":
    read_rfid()