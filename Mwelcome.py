import os
import pygame
import time
from multiprocessing import Process, Value

def welcome_message(eyes_detected):
    pygame.init()  # Initialize the pygame library

    # Screen Config
    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    pygame.display.set_caption('Welcome Message')
    font = pygame.font.Font(None, 36)

    #Indenfor if
    welcome_message2 = font.render('Scan your card', True, (255, 255, 255))
    welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
    welcome_rect = welcome_message2.get_rect(center=(400, 240))
    
    current_message = None  # Track the current displayed message

    while True:

        if eyes_detected.value:
            # Display "Scan your card" message
            if current_message != welcome_message2:
                current_message = welcome_message2
                DisplayText(welcome_message2, welcome_rect, screen)
                time.sleep(5)  # Adjust the duration as needed
                eyes_detected.value = False  # Reset the variable after displaying the message
        else:
            # Display the first welcome message
            if current_message != welcome_message1:
                current_message = welcome_message1
                DisplayText(welcome_message1, welcome_rect, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def DisplayText(Message, Rect, screen):
    background_color = (0, 0, 0)
    screen.fill(background_color)
    screen.blit(Message, Rect)
    pygame.display.flip()

if __name__ == "__main__":
    eyes_detected = Value('b', False)  # Initial value
    welcome_process = Process(target=welcome_message, args=(eyes_detected,))

    # Start the process
    welcome_process.start()

    # Wait for the process to finish before exiting
    welcome_process.join()
