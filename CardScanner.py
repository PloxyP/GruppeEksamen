#Setup af RFID-RC522: Tilslut 3.3V til Ardunio 3.3V, GND til GND på Arduino, SDA til PIN 10, SCK til PIN 13, MOSI til PIN 11, MISO til PIN 12, RST til PIN 9
#Setup af LED lys Grøn: Tilslut 5V til "+" på breadboard, GND til "-" på breadboard, PIN 7 på Række A Linje 12 & Resistor på "-" til Række A Linje 11, korte ben til resistor
#Setup af LED lys Rød: Tilslut 5V til "+" på breadboard, GND til "-", PIN 6 til Række A Linje 18 & Resistor på "-" til Række A Linje 17, korte ben til resistor

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN         9
#define SS_PIN          10

#define GREEN_LED_PIN   7  // Change to the digital pin for your green LED
#define RED_LED_PIN     6  // Change to the digital pin for your red LED

MFRC522 mfrc522(SS_PIN, RST_PIN);

#Define the UIDs of the allowed cards
byte allowedCardUIDs[][4] = {
  {0x00, 0x7A, 0x71, 0x1A},
  {0x83, 0x84, 0x83, 0x08},
  {0x00, 0x83, 0x80, 0x1A}
};

#Define the welcome messages for each card
const char* welcomeMessages[] = {
  "Welcome Kaan!",
  "Welcome Mattias!",
  "Welcome Jessica!"
};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  
  Serial.println("RFID Reader Initialized");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.print("Card UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
    }
    
    if (checkCardUID()) {
      Serial.print(" - ");
      Serial.println(welcomeMessages[getCardIndex()]);
      turnOnGreenLED();
      // Add your custom actions for this card here
    } else {
      Serial.println(" - Access Denied");
      turnOnRedLED();
    }

    delay(1000);  // Add a delay to avoid reading the same card repeatedly
    turnOffLEDs();
  }
}

bool checkCardUID() {
  // Compare the scanned card's UID with the allowed card UIDs
  for (byte j = 0; j < sizeof(allowedCardUIDs) / sizeof(allowedCardUIDs[0]); j++) {
    bool match = true;
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      if (mfrc522.uid.uidByte[i] != allowedCardUIDs[j][i]) {
        match = false;
        break;
      }
    }
    if (match) {
      return true;  // Card UID matches one of the allowed cards
    }
  }
  return false;  // Card UID doesn't match any allowed cards
}

byte getCardIndex() {
  // Get the index of the matched card in the allowedCardUIDs array
  for (byte j = 0; j < sizeof(allowedCardUIDs) / sizeof(allowedCardUIDs[0]); j++) {
    bool match = true;
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      if (mfrc522.uid.uidByte[i] != allowedCardUIDs[j][i]) {
        match = false;
        break;
      }
    }
    if (match) {
      return j;  // Return the index of the matched card
    }
  }
  return 255;  // Return an invalid index if no match is found
}

void turnOnGreenLED() {
  digitalWrite(GREEN_LED_PIN, HIGH);
}

void turnOnRedLED() {
  digitalWrite(RED_LED_PIN, HIGH);
}

void turnOffLEDs() {
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
}
