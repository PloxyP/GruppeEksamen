import pygame
import threading
import time

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def welcome_message():
    pygame.init()  # Initialize the pygame library

    while True:
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

if __name__ == "__main__":
    welcome_message()
