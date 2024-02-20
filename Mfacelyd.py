#------------------------------IMPORTS----------------------------------------#
import cv2
from multiprocessing import Process, Value
from Mwelcome import welcome_message
from Mgreetingbot import rfid_function
import RPi.GPIO as GPIO

#----------------------------GLOBAL SETUP-------------------------------------#
#Multiprocess variabler:
eyes_detected = Value('b', False)       #Variabel for om øjne er detekteret i Mfacelyd.py
KortGodkendt = Value('b', False)        #Variabel for om kort er godkendt i Mgreetingbot.py
KortScannet = Value('b', False)         #Variabel for om kort er scannet i Mgreetingbot.py
ExitGUI = Value('b', False)             #Variabel for om GUI bliver exittet i Mgreetingbot.py

#Open CV indstillinger:
cap = cv2.VideoCapture(0)               #Index for valg af camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #Sat billede bredde
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #Sat billede højde
cap.set(cv2.CAP_PROP_FPS, 30)           #Sat billeder per sekund

#Globale variabler:
face_detected = False                   #Variabel for om ansigt er detekteret
led_on = False                          #Pin on/off check
led_pin = 24                            #GPIO pin (Ikke fysisk pin nummer)

#----------------------------FUNCTIONS-----------------------------------------#
#GPIO setup function:
def gpio_setup():
    GPIO.setmode(GPIO.BCM)              #Pin nummer sat til GPIO værdi.
    GPIO.setup(led_pin, GPIO.OUT)       #Pin mode sat til output
    GPIO.output(led_pin, GPIO.LOW)      #Start værdi sat som low(off)

#LED functioner:
def TurnLED_on():
    GPIO.output(led_pin, GPIO.HIGH)

def TurnLED_off():
    GPIO.output(led_pin, GPIO.LOW)

#Main function (Køre fra starten i multiprocess):
def face_detection(eyes_detected):
    global face_detected, led_on                            #Henter global variabler
    
    #Main loop:
    while True:
        ret, frame = cap.read()                             #Variabel med nuværende billede fra video enhed               
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      #Konvertere frame fra BGR til grayscale
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) #Bruger face_cascade til at detektere ansigter i billedet (1.3 = scaling factor så 30% reduktion, 5 = neighbor rektangler)
        
        #If statement for om ansigt er detekteret i billedet
        if len(faces) == 0:
            face_detected = False
        else:
            face_detected = True

        #For loop - face detection
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)    #Tegner firkanter på ansigter
            roi_gray = gray[y:y+w, x:x+w]                                   #Grey scale region of interrest
            roi_color = frame[y:y+h, x:x+w]                                 #Frame region of interrest
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)           #Bruger eye_cascade til at detektere øjne i billedet

            #For loop - øjen detektion 
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                if not eyes_detected.value:
                    eyes_detected.value = True                              #Multiprocess variabel ændring for øjen detektion

        #cv2.imshow('frame', frame)                                         #Live visning vindue af video preview (frames)

        #Turns on LED
        if face_detected == True and led_on == False:
            TurnLED_on()
            led_on = True

        if face_detected == False and led_on == True:
            TurnLED_off()
            led_on = False
        
    #     if cv2.waitKey(1) == ord('q'):
    #         break

    # cap.release()
    # cv2.destroyAllWindows()

#----------------------------MAIN-----------------------------------------#
#Main statement:
if __name__ == "__main__":
    
    #Henter face_cascade og eye_cascade til ansigts- og øjengenkendelse fra opencv til variabel:
    face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml') 
    eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')
    
    #Sender variabel i form a objekt til kørende process function:
    face_process = Process(target=face_detection, args=(eyes_detected,))                                        #Program: Mfacelys.py - Function: face_detection - Objekt: eyes_detected                                        
    welcome_process = Process(target=welcome_message, args=(eyes_detected,KortGodkendt,KortScannet,ExitGUI))    #Program: Mwelcome.py - Function: welcome_message - Objekt: eyes_detected, KortGodkendt, KortScannet, ExitGUI
    calender_process = Process(target=rfid_function, args=(KortGodkendt,KortScannet,ExitGUI))                   #Program: Mgreetingbot.py - Function: rfid_function - Objekt: KortGodkendt, KortScannet, ExitGUI

    #GPIO setup:
    gpio_setup()

    #Starter alle processer:
    face_process.start()
    welcome_process.start()
    calender_process.start()

    #Lukker alle processer:
    face_process.join()
    welcome_process.join()
    calender_process.join()

    #Rengører GPIOs:
    GPIO.cleanup()