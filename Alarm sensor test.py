import threading
import winsound 
import time

# Define note frequencies for a basic jazz jingle
c_major_chord = [261.63, 329.63, 392.00]  # C4, E4, G4
f_major_chord = [349.23, 440.00, 523.25]  # F4, A4, C5
g_major_chord = [392.00, 493.88, 587.33]  # G4, B4, D5

import cv2
import imutils 
#husk import: pip install opencv-python imutils 

cap= cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HIGHT, 480)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def Welcome_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("Person entered the room")
        winsound.Beep(int(c_major_chord[0]), 300)
        time.sleep(0.1)
        winsound.Beep(int(c_major_chord[1]), 300)
        time.sleep(0.1)
        winsound.Beep(int(c_major_chord[2]), 300)
        time.sleep(0.3)

        winsound.Beep(int(f_major_chord[0]), 300)
        time.sleep(0.1)
        winsound.Beep(int(f_major_chord[1]), 300)
        time.sleep(0.1)
        winsound.Beep(int(f_major_chord[2]), 300)
        time.sleep(0.3)

        winsound.Beep(int(g_major_chord[0]), 300)
        time.sleep(0.1)
        winsound.Beep(int(g_major_chord[1]), 300)
        time.sleep(0.1)
        winsound.Beep(int(g_major_chord[2]), 300)
        time.sleep(0.3)
    alarm = False

while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.TRESH_BINARY[1])
        start_frame = frame_bw
        if threshold.sum() > 300:
            alarm_cpunter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=Welcome_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q)"):
        alarm_mode = False
        break

cap.release()
cv2.destroyALLWindows()
