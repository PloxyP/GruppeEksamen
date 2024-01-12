import cv2
import pygame
import threading
from Mwelcome import welcome_message
import time

# Shared variable to signal eyes detection
eyes_detected = False

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

#looking_at_camera = False
played_sound = False  # Flag to track whether the sound has been played

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def welcome_sound():
    print("Welcome!")
    play_sound("check.mp3")

def goodbye_sound():
    print("Goodbye!")
    play_sound("check.mp3")

# Load the face and eye classifiers outside the loop
face_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/home/gruppesjov/opencv/data/haarcascades/haarcascade_eye.xml')

def face_detection():
    global eyes_detected
    
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            looking_at_camera = False
            played_sound = False  # Reset the flag when no faces are detected

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            roi_gray = gray[y:y+w, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 8)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)
                looking_at_camera = True
                eyes_detected = True
                event = threading.Event()
                threading.Thread(target=welcome_message, args=(eyes_detected,))

        #cv2.imshow('frame', frame)
        
        # Play sounds based on the flag and ensure it's played only once
        if looking_at_camera and not played_sound:
            welcome_sound()
            played_sound = True

        if not looking_at_camera and played_sound:
            goodbye_sound()
            played_sound = False
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def welcome_message(eyes_detected):
    pygame.init()  # Initialize the pygame library

    # Screen Config
    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    pygame.display.set_caption('Welcome Message')
    background_color = (0, 0, 0)
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(background_color)

        if eyes_detected:
            # Display "Scan your card" message
            welcome_message2 = font.render('Scan your card', True, (255, 255, 255))
            welcome_rect2 = welcome_message2.get_rect(center=(400, 240))
            screen.blit(welcome_message2, welcome_rect2)
            pygame.display.flip()
            time.sleep(5)  # Adjust the duration as needed
            eyes_detected = False  # Reset the variable after displaying the message
        else:
            # Display the first welcome message
            welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
            welcome_rect1 = welcome_message1.get_rect(center=(400, 240))
            screen.blit(welcome_message1, welcome_rect1)
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == "__main__":
    eyes_detected = False  # Initial value
    welcome_thread = threading.Thread(target=welcome_message, args=(eyes_detected,))


if __name__ == "__main__":
    face_thread = threading.Thread(target=face_detection)
    welcome_thread = threading.Thread(target=welcome_message, args=(eyes_detected,))

    # Start both threads
    face_thread.start()
    welcome_thread.start()

    # Wait for both threads to finish before exiting
    face_thread.join()
    welcome_thread.join()

   