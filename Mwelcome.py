import pygame
import threading
import time

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def welcome_message():
    pygame.init()  # Initialize the pygame library

    # Screen Config
    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    pygame.display.set_caption('Welcome Message')
    background_color = (0, 0, 0)
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(background_color)

        # Update the message based on the presence of eyes
        if eyes_registered:
            message_text = "Scan your card"
        else:
            message_text = "Welcome!"

        welcome_message_text = font.render(message_text, True, (255, 255, 255))
        welcome_rect = welcome_message_text.get_rect(center=(400, 240))

        # Display the message
        screen.blit(welcome_message_text, welcome_rect)
        pygame.display.flip()

        # Pause for a moment
        time.sleep(5)  # Adjust the duration as needed

    # Clean up resources before exiting
    pygame.quit()

if __name__ == "__main__":
    eyes_registered = False  # Initialize the flag

    def face_detection():
        global eyes_registered
        while True:
            # ... (existing face detection code)

            # Update the eyes_registered flag based on the presence of eyes
            eyes_registered = len(eyes) > 0

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Start the face detection thread
    face_thread = threading.Thread(target=face_detection)
    face_thread.start()

    # Start the welcome message thread
    welcome_thread = threading.Thread(target=welcome_message)
    welcome_thread.start()

    # Wait for both threads to finish before exiting
    face_thread.join()
    welcome_thread.join()
