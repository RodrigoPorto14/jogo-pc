import pygame
from pygame.locals import *
from sys import exit
from enums import Cena
from menu import *

pygame.init()

janela = pygame.display.set_mode((500,640))
imagens = {} ; som = {}

with open('arquivos/imagens.txt','rt') as arq:
    while(nome := arq.readline().replace('\n','')):
        imagens[nome] = pygame.image.load('assets/'+nome+'.png')

som['hit'] = pygame.mixer.Sound('audios/hit.wav')
som['miss'] = pygame.mixer.Sound('audios/miss.ogg')
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
        telaJogo, jogo = menu.carregaJogo(janela,imagens,som,idMusica)
        cena = jogo.iniciaMusica()

    elif(cena==Cena.JOGO):
        cena = jogo.controlaJogo()
        telaJogo.desenha(jogo)
    
    elif(cena==Cena.FIMDEJOGO):
        jogo.musica.audio.stop()
        janela.fill((0,0,0))
        
    pygame.display.flip()