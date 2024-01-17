import os
import pygame
import time
from multiprocessing import Process, Value


def welcome_message(eyes_detected,KortGodkendt,KortScannet,ExitGUI):
    pygame.init()  # Initialize the pygame library
    # Screen Config
    #screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption('Welcome Message')
    font = pygame.font.Font(None, 36)

    #Indenfor if
    welcome_message2 = font.render('Scan your card', True, (255, 255, 255))
    welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
    godkendt_message = font.render('Card Accepted!', True, (255, 255, 255))
    declined_message = font.render('Card Declined!', True, (255, 255, 255))
    welcome_rect = welcome_message2.get_rect(center=(400, 240))
    current_message = None  # Track the current displayed message

    while True:
        if eyes_detected.value and KortScannet.value == False:
            # Display "Scan your card" message
            if current_message != welcome_message2:
                current_message = welcome_message2
                DisplayText(welcome_message2, welcome_rect, screen)
                time.sleep(5)  # Adjust the duration as needed
                eyes_detected.value = False  # Reset the variable after displaying the message

        elif KortScannet.value == True and KortGodkendt.value == True:
            if current_message != godkendt_message:
                current_message = godkendt_message
                DisplayText(godkendt_message, welcome_rect, screen)
                time.sleep(5)  # Adjust the duration as needed
                eyes_detected.value = False  # Reset the variable after displaying the message
                KortScannet.value = False
                KortGodkendt.value = False
                
        elif KortScannet.value == True and KortGodkendt.value == False:
            if current_message != declined_message:
                current_message = declined_message
                DisplayText(declined_message, welcome_rect, screen)
                time.sleep(5)  # Adjust the duration as needed
                eyes_detected.value = False  # Reset the variable after displaying the message
                KortScannet.value = False
                KortGodkendt.value = False
        else:
            # Display the first welcome message
            if current_message != welcome_message1:
                current_message = welcome_message1
                DisplayText(welcome_message1, welcome_rect, screen)
                print(ExitGUI.value)

        if ExitGUI.value == True:
            screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
            print("FullscreenOn!")
            DisplayText(welcome_message1, welcome_rect, screen)
            ExitGUI.value = False


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
    KortGodkendt = Value('b', False)
    KortScannet = Value('b', False)
    ExitGUI = Value('b', False)
    welcome_process = Process(target=welcome_message, args=(eyes_detected,KortGodkendt,KortScannet,ExitGUI))

    # Start the process
    welcome_process.start()

    # Wait for the process to finish before exiting
    welcome_process.join()
