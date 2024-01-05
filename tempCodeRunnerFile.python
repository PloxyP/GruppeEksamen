import pygame
import time

# Initialisierung von Pygame
pygame.init()

# Konfiguration des Touchscreens und des Bildschirms
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
font = pygame.font.Font(None, 36)

def display_message(message):
    # Anzeige einer Nachricht auf dem Bildschirm
    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    # Begrüßungsnachrichten
    messages = ["Velkommen!", "God Morgen", "Viel Spaß mit Ihrem Raspberry Pi!"]

    try:
        # Schleife für die Anzeige der Begrüßungsnachrichten
        while True:
            for message in messages:
                display_message(message)
                time.sleep(2)  # Anzeigezeit pro Nachricht in Sekunden

    except KeyboardInterrupt:
        # Beenden, wenn Strg+C gedrückt wird
        pygame.quit()

if __name__ == "__main__":
    main()
