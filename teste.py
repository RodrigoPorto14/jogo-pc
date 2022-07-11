import pygame
from pygame.locals import *
from sys import exit


pygame.init()

janela = pygame.display.set_mode((500,640))
circulo = pygame.image.load('assets/red-circle.png')
teste = pygame.image.load('assets/red-cap.png')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            print(pygame.mouse.get_focused())
        
    janela.fill((0,0,0))
    janela.blit(circulo,(200,200))
    janela.blit(teste,(209,208))
         
    pygame.display.flip()