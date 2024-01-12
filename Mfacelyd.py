import cv2
from multiprocessing import Process, Value
from Mwelcome import welcome_message
from Mgreetingbot import rfid_function
import RPi.GPIO as GPIO

# Shared variable to signal eyes detections
eyes_detected = Value('b', False)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

looking_at_camera = False
led_on = False
led_pin = 24  # GPIO pin for the LED, change it to your actual pinn

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, GPIO.LOW)

def welcome_led():
    print("Welcome!")
    GPIO.output(led_pin, GPIO.HIGH)

def goodbye_led():
    #print("Goodbye!")
    GPIO.output(led_pin, GPIO.LOW)

def face_detection(eyes_detected):
    global looking_at_camera, led_on
    
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            looking_at_camera = False

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                looking_at_camera = True
                eyes_detected.value = True
                if not led_on:
                    welcome_led()
                    led_on = True

        cv2.imshow('frame', frame)

        # Play sounds based on the flag and ensure it's played only once
        if not looking_at_camera and led_on:
            goodbye_led()
            led_on = False
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    eyes_detected = Value('b', False)  # Initial value
    face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')
    
    face_process = Process(target=face_detection, args=(eyes_detected,))
    welcome_process = Process(target=welcome_message, args=(eyes_detected,))
    program3_process = Process(target=rfid_function)  # Add this line

    # Start all processes
    face_process.start()
    welcome_process.start()
    program3_process.start()  # Add this line

    # Wait for all processes to finish before exiting
    face_process.join()
    welcome_process.join()
    program3_process.join()  # Add this line

    # Cleanup GPIO
    GPIO.cleanup()
