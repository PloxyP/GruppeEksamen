import cv2
import pygame
import time

pygame.init()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

looking_at_camera = False
played_sound = False  # Flag to track whether the sound has been played

# Screen Config
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
pygame.display.set_caption('Welcome Message')
background_color = (0, 0, 0)
screen.fill(background_color)
font = pygame.font.Font(None, 36)

# First Welcome Message
welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
welcome_rect1 = welcome_message1.get_rect(center=(400, 240))

# Display the first welcome message
screen.blit(welcome_message1, welcome_rect1)
pygame.display.flip()

# Wait for 5 seconds
time.sleep(3)

# Clear the screen for the second message
screen.fill(background_color)
pygame.display.flip()

# Wait for a short moment
time.sleep(0.1)

# Second Welcome Message
welcome_message2 = font.render('Please use your ID Card to log in', True, (255, 255, 255))
welcome_rect2 = welcome_message2.get_rect(center=(400, 240))

# Display the second welcome message
screen.blit(welcome_message2, welcome_rect2)
pygame.display.flip()

# Wait for 5 seconds
time.sleep(12)

# Clear the screen
screen.fill(background_color)
pygame.display.flip()

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

    cv2.imshow('frame', frame)

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

# Wait for a short moment
time.sleep(0.1)

# Quit Pygame
pygame.quit()

