import pygame
from pygame.locals import *
from sys import exit
from cena import *
from menu import *

pygame.init()

janela = pygame.display.set_mode((500,640))
circles = [] ; squares = [] ; sound = {}
circles.append(pygame.image.load('assets/red-circle.png'))
circles.append(pygame.image.load('assets/green-circle.png'))
circles.append(pygame.image.load('assets/blue-circle.png'))
squares.append(pygame.image.load('assets/red-square.png'))
squares.append(pygame.image.load('assets/green-square.png'))
squares.append(pygame.image.load('assets/blue-square.png'))
sound['hit'] = pygame.mixer.Sound('audios/hit.wav')
sound['miss'] = pygame.mixer.Sound('audios/miss.ogg')
cena = Cena.MENU
menu = Menu()
idMusica=2

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if(cena==Cena.JOGO):
                jogo.pausaJogo()

    if(cena==Cena.TELATITULO):
        pass

    elif(cena==Cena.MENU):
        telaJogo, jogo = menu.carregaJogo(janela,squares,circles,sound,idMusica)
        cena = jogo.iniciaMusica()

    elif(cena==Cena.JOGO):
        cena = jogo.controlaJogo()
        telaJogo.desenha(jogo)
    
    elif(cena==Cena.FIMDEJOGO):
        jogo.musica.audio.stop()
        janela.fill((0,0,0))
        
    pygame.display.flip()