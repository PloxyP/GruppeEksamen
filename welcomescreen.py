import pygame
import time

pygame.init()

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
time.sleep(2)

# Clear the screen
screen.fill(background_color)
pygame.display.flip()

# Wait for a short moment
time.sleep(0.1)

# Quit Pygame
pygame.quit()
