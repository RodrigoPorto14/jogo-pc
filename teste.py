import pygame
from pygame.locals import *
from sys import exit


pygame.init()

janela = pygame.display.set_mode((500,640))
fundo = pygame.image.load('images/menu/fundo.png')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            print(pygame.mouse.get_focused())
        
    janela.fill((0,0,0))
    pygame.draw.rect(janela,(255,0,0),(200,200,100,100))
    janela.blit(fundo,(0,0))
         
    pygame.display.flip()