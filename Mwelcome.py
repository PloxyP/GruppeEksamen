import pygame
import time
from multiprocessing import Value

def welcome_message(eyes_detected):
    pygame.init()  # Initialize the pygame library

    # Screen Config
    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    pygame.display.set_caption('Welcome Message')
    background_color = (0, 0, 0)
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(background_color)

        if eyes_detected.value:
            # Display "Scan your card" message
            welcome_message2 = font.render('Scan your card', True, (255, 255, 255))
            welcome_rect2 = welcome_message2.get_rect(center=(400, 240))
            screen.blit(welcome_message2, welcome_rect2)
            pygame.display.flip()
            time.sleep(5)  # Adjust the duration as needed
            eyes_detected.value = False  # Reset the variable after displaying the message
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
    eyes_detected = Value('b', False)  # Initial value
    welcome_process = multiprocessing.Process(target=welcome_message, args=(eyes_detected,))
    welcome_process.start()

    welcome_process.join()
