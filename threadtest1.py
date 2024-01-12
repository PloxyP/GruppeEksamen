import cv2
import RPi.GPIO as GPIO
import pygame
import time
from mfrc522 import SimpleMFRC522
import threading
import subprocess

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

looking_at_camera = False
led_pin = 18  # Replace with the GPIO pin to which the LED is connected

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

def turn_on_led():
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_led():
    GPIO.output(led_pin, GPIO.LOW)

# Define a flag to signal the termination of the threads
terminate_threads = False

# Function for the computer vision and LED control thread
def camera_thread():
    global terminate_threads
    cap = cv2.VideoCapture(0)

# Load the face and eye classifiers outside the loop
face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    while not terminate_threads:
        ret, frame = cap.read()

    if len(faces) == 0:
        looking_at_camera = False

        if cv2.waitKey(1) == ord('q'):
            terminate_threads = True
            break

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
        roi_gray = gray[y:y+w, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
            looking_at_camera = True

    cv2.imshow('frame', frame)

    # Control LED based on the flag
    if looking_at_camera:
        turn_on_led()
    else:
        turn_off_led()

    if cv2.waitKey(1) == ord('q'):
        break

def rfid_thread():
    global terminate_threads

    pygame.init()

def read_rfid():
    reader = SimpleMFRC522()

    try:
        while not terminate_threads:
            read_rfid()
        print("Hold a card near the reader.")
        id, text = reader.read()
        print("Card ID:", id)
        print("Card Text:", text)
        

        # Replace '123456789' with the ID of your specific card
        if id == 2054232593:
            print("Opening Calendar.py")
            subprocess.run(["python", "Calendar.py"])

    
    finally:
        pygame.quit()
       
    # Start the threads
camera_thread = threading.Thread(target=camera_thread)
rfid_thread = threading.Thread(target=rfid_thread)

camera_thread.start()
rfid_thread.start()

# Wait for both threads to finish before cleaning up
camera_thread.join()
rfid_thread.join()

# Cleanup GPIO on exit
GPIO.cleanup()

    

if __name__ == "__main__":
    read_rfid()
# Cleanup GPIO on exit
GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()

# Wait for a short moment
time.sleep(0.1)

# Quit Pygame
pygame.quit()


