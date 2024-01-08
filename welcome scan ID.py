import pygame
import time

# Initialisiere Pygame
pygame.init()

# Konfiguriere den Bildschirm
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
pygame.display.set_caption('Willkommensnachricht')

# Setze die Hintergrundfarbe
background_color = (0, 0, 0)
screen.fill(background_color)

# Setze die Schriftart und -größe
font = pygame.font.Font(None, 36)

# Erstelle die Willkommensnachricht
welcome_message = font.render('Welcome! Please log in using your ID-Card', True, (255, 255, 255))
welcome_rect = welcome_message.get_rect(center=(400, 240))

# Zeige die Willkommensnachricht an
screen.blit(welcome_message, welcome_rect)
pygame.display.flip()

# Warte für 5 Sekunden
time.sleep(8)

# Lösche die Willkommensnachricht
screen.fill(background_color)
pygame.display.flip()

# Warte für einen kurzen Moment, um sicherzustellen, dass die Anzeige aktualisiert wird
time.sleep(0.1)

# Beende Pygame
pygame.quit()
