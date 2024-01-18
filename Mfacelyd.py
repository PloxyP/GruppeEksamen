import cv2
from multiprocessing import Process, Value
from Mwelcome import welcome_message
from Mgreetingbot import rfid_function
import RPi.GPIO as GPIO

#Delte variabler til multiprocessing
eyes_detected = Value('b', False)       #Variabel for om øjne er detekteret i Mfacelyd.py
KortGodkendt = Value('b', False)        #Variabel for om kort er godkendt i Mgreetingbot.py
KortScannet = Value('b', False)         #Variabel for om kort er scannet i Mgreetingbot.py
ExitGUI = Value('b', False)             #Variabel for om GUI bliver exittet i Mgreetingbot.py

#Open CV functioner:
cap = cv2.VideoCapture(0)               #Index for valg af camera

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #Sat billede bredde
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #Sat billede højde
cap.set(cv2.CAP_PROP_FPS, 30)           #Sat billeder per sekund

#Globale variabler
face_detected = False               #Variabel for om ansigt er detekteret
led_on = False                          #Pin on/off check
led_pin = 24                            #GPIO pin (Ikke fysisk pin nummer)

#GPIO startup:
GPIO.setmode(GPIO.BCM)                  #Pin nummer sat til GPIO værdi.
GPIO.setup(led_pin, GPIO.OUT)           #Pin mode sat til output
GPIO.output(led_pin, GPIO.LOW)          #Start værdi sat som low(off)

#Function til at tænde LED
def welcome_led():
    GPIO.output(led_pin, GPIO.HIGH)

#Function til at slukke LED
def goodbye_led():
    GPIO.output(led_pin, GPIO.LOW)

#Main function (Køre fra starten i multiprocess)
def face_detection(eyes_detected):
    global face_detected, led_on
    
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            face_detected = False
        else:
            face_detected = True

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                if not eyes_detected.value:
                    eyes_detected.value = True

        #cv2.imshow('frame', frame)

        #Turns on LED
        if face_detected == True and led_on == False:
            welcome_led()
            led_on = True

        if face_detected == False and led_on == True:
            goodbye_led()
            led_on = False
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#Main statement:
if __name__ == "__main__":
    face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')
    
    face_process = Process(target=face_detection, args=(eyes_detected,))
    welcome_process = Process(target=welcome_message, args=(eyes_detected,KortGodkendt,KortScannet,ExitGUI))
    program3_process = Process(target=rfid_function, args=(KortGodkendt,KortScannet,ExitGUI))  # Add this line

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
