import pygame
import time

def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def welcome_sound():
    print("Willkommen!")
    play_sound("check.mp3")  # Passe den Dateinamen an

def goodbye_sound():
    print("Auf Wiedersehen!")
    play_sound("abschied.mp3")  # Passe den Dateinamen an

if __name__ == "__main__":
    try:
        welcome_sound()
        # Hier kannst du deinen Hauptcode einfügen
        # Verbinde dich mit dem Bluetooth-Lautsprecher und führe die gewünschten Aktionen durch

        # Zum Beispiel:
        # dein_hauptcode_hier()

    except KeyboardInterrupt:
        # Fangen Sie die Tastaturunterbrechung ab (Ctrl+C) und spielen Sie den Abschiedston
        goodbye_sound() 
