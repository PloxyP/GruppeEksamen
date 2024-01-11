import pygame
import time

pygame.init()

# Screen Config
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
font = pygame.font.Font(None, 36)

def display_message(message):
    # show message on screen
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    # Messages
    messages = ["Velkommen!", "Please, log in using your ID-Card"]

    try:
        
        while True:
            for message in messages:
                display_message(message)
                time.sleep(4) 

    except KeyboardInterrupt:
        # Stop Code with pressing ctrl+c
        pygame.quit()

if __name__ == "__main__":
    main()
