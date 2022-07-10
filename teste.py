import pygame
from pygame.locals import *
from sys import exit


pygame.init()

janela = pygame.display.set_mode((500,640))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            print(pygame.mouse.get_focused())
        

    
      
    pygame.display.flip()