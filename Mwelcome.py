#------------------------------IMPORTS----------------------------------------#
import pygame
import time
from multiprocessing import Process, Value

#-----------------------------FUNCTIONS---------------------------------------#
#Main function (Køre fra starten i multiprocess):
def welcome_message(eyes_detected,KortGodkendt,KortScannet,ExitGUI):
    pygame.init()                                                               #Pygame start
    #screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)            
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)           #Display indstillinger
    pygame.display.set_caption('Welcome Message')                               #Sæt caption
    font = pygame.font.Font(None, 36)                                           #Sæt font

    #Skærm beskeder instillinger:
    welcome_message2 = font.render('Scan your card', True, (255, 255, 255))
    welcome_message1 = font.render('Welcome!', True, (255, 255, 255))
    godkendt_message = font.render('Card Accepted!', True, (255, 255, 255))
    declined_message = font.render('Card Declined!', True, (255, 255, 255))
    welcome_rect = welcome_message2.get_rect(center=(400, 240))
    
    #Variabel til nuværende besked værdi
    current_message = None

    #Main loop:
    while True:
        
        #If statement hvis Kort er ulæst og øjne er detekteret
        if eyes_detected.value and KortScannet.value == False:                  
            if current_message != welcome_message2:
                current_message = welcome_message2                              #Sætter current message check til nuværende tekst
                DisplayText(welcome_message2, welcome_rect, screen)             #Sætter skærmtekst med parametre
                time.sleep(5)                                                   #Delay før ændring i tekst
                eyes_detected.value = False                                     #Reset multiprocess øjne detekteret check til False

        #Elif statement hvis kort er læst og godkendt
        elif KortScannet.value == True and KortGodkendt.value == True:
            if current_message != godkendt_message:
                current_message = godkendt_message                              #Sætter current message check til nuværende tekst
                DisplayText(godkendt_message, welcome_rect, screen)             #Sætter skærmtekst med parametre
                time.sleep(5)                                                   #Delay før ændring i tekst
                eyes_detected.value = False                                     #Reset multiprocess øjne detekteret check til False
                KortScannet.value = False                                       #Reset multiprocess kortscan check til False                             
                KortGodkendt.value = False                                      #Reset multiprocess kortgodkendt check til False  
        
        #Elif statement hvis kort er læst men ikke godkendt
        elif KortScannet.value == True and KortGodkendt.value == False:
            if current_message != declined_message:
                current_message = declined_message                              #Sætter current message check til nuværende tekst
                DisplayText(declined_message, welcome_rect, screen)             #Sætter skærmtekst med parametre
                time.sleep(5)                                                   #Delay før ændring i tekst
                eyes_detected.value = False                                     #Reset multiprocess øjne detekteret check til False
                KortScannet.value = False                                       #Reset multiprocess kortscan check til False
        
        else:
            if current_message != welcome_message1:
                current_message = welcome_message1                              #Sætter current message check til nuværende tekst
                DisplayText(welcome_message1, welcome_rect, screen)             #Sætter skærmtekst med parametre

        #If statement om GUI er exittet i Mgreetingbot.py
        if ExitGUI.value == True:
            screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)   #Display indstillinger
            DisplayText(welcome_message1, welcome_rect, screen)                 #Forny welcome besked
            ExitGUI.value = False                                               #Resetter GUI exit check til False

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()

#Display text instillinger
def DisplayText(Message, Rect, screen):
    background_color = (0, 0, 0)                                                #Variabel med farve værdi
    screen.fill(background_color)                                               #Sætter baggrunds farve
    screen.blit(Message, Rect)                                                  #Skriver tekst på baggrunden
    pygame.display.flip()                                                       #Updatere displayet

#----------------------------MAIN-----------------------------------------#
#Main statement:
if __name__ == "__main__":

    #Multiprocess variabler:
    eyes_detected = Value('b', False)
    KortGodkendt = Value('b', False)
    KortScannet = Value('b', False)
    ExitGUI = Value('b', False)

    #Sender variabel i form a objekt til kørende process function:
    welcome_process = Process(target=welcome_message, args=(eyes_detected,KortGodkendt,KortScannet,ExitGUI))    #Program: Mwelcome.py - Function: welcome_message - Objekt: eyes_detected, KortGodkendt, KortScannet, ExitGUI

    #Starter process:
    welcome_process.start()

    #Lukker process:
    welcome_process.join()
