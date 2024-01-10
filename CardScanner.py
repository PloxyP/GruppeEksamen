#Setup af RFID-RC522: Tilslut 3.3V til Ardunio 3.3V, GND til GND på Arduino, SDA til PIN 10, SCK til PIN 13, MOSI til PIN 11, MISO til PIN 12, RST til PIN 9
#Setup af LED lys Grøn: Tilslut 5V til "+" på breadboard, GND til "-" på breadboard, PIN 7 på Række A Linje 12 & Resistor på "-" til Række A Linje 11, korte ben til resistor
#Setup af LED lys Rød: Tilslut 5V til "+" på breadboard, GND til "-", PIN 6 til Række A Linje 18 & Resistor på "-" til Række A Linje 17, korte ben til resistor

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9
#define SS_PIN          10

#define GREEN_LED_PIN   7  // Change to the digital pin for your green LED
#define RED_LED_PIN     6  // Change to the digital pin for your red LED

import RPi.GPIO as GPIO
from mfrc522 import MFRC522

RST_PIN = 25  # Change to the GPIO pin for RST
SS_PIN = 8  # Change to the GPIO pin for SDA (SS)

GREEN_LED_PIN = 7
RED_LED_PIN = 6

allowed_card_uids = [
    [0x00, 0x7A, 0x71, 0x1A],
    [0x83, 0x84, 0x83, 0x08],
    [0x00, 0x83, 0x80, 0x1A]
]

welcome_messages = [
    "Welcome Kaan!",
    "Welcome Mattias!",
    "Welcome Jessica!"
]

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)

    MIFAREReader = MFRC522(SS_PIN, RST_PIN)

    print("RFID Reader Initialized")
    return MIFAREReader

def loop(MIFAREReader):
    try:
        print("Place a card near the reader...")
        while True:
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            if status == MIFAREReader.MI_OK:
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    card_uid = uid[:4]
                    print("Card UID: ", card_uid)

                    if check_card_uid(card_uid):
                        print(" - ", welcome_messages[get_card_index(card_uid)])
                        turn_on_green_led()
                        # Add your custom actions for this card here
                    else:
                        print(" - Access Denied")
                        turn_on_red_led()

                    # Avoid reading the same card repeatedly
                    while MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)[0] == MIFAREReader.MI_OK:
                        pass

                    turn_off_leds()

    except KeyboardInterrupt:
        GPIO.cleanup()

def check_card_uid(card_uid):
    # Compare the scanned card's UID with the allowed card UIDs
    for allowed_uid in allowed_card_uids:
        if card_uid == allowed_uid:
            return True  # Card UID matches one of the allowed cards
    return False  # Card UID doesn't match any allowed cards

def get_card_index(card_uid):
    # Get the index of the matched card in the allowed_card_uids array
    for j, allowed_uid in enumerate(allowed_card_uids):
        if card_uid == allowed_uid:
            return j  # Return the index of the matched card
    return 255  # Return an invalid index if no match is found

def turn_on_green_led():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_on_red_led():
    GPIO.output(RED_LED_PIN, GPIO.HIGH)

def turn_off_leds():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

if __name__ == "__main__":
    MIFAREReader = setup()
    loop(MIFAREReader)
