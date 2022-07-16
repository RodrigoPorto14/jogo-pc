import pygame
from pygame.locals import *
from sys import exit
from enums import Cena
from fimdejogo import *
from menu import *
from telatitulo import *

pygame.init()

janela = pygame.display.set_mode((500,640))
imagensJogo = {} ; som = {} ; mouse = {}

with open('arquivos/imagens-jogo.txt','rt') as arq:
    while(linha := arq.readline().split()):
        nome = linha[0] ; x = int(linha[1]) ; y = int(linha[2])
        imagensJogo[nome] = pygame.transform.scale(pygame.image.load('images/jogo/'+nome+'.png'),(x,y))

mouse['arrow'] = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
mouse['hand'] = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

som['hit'] = pygame.mixer.Sound('audios/hit.wav')
som['miss'] = pygame.mixer.Sound('audios/miss.ogg')

cena = Cena.TELATITULO
telaTitulo = TelaTitulo(janela,mouse)
menu = Menu(janela,mouse)
fimDeJogo = FimDeJogo(janela,mouse)

idFase=3

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == MOUSEBUTTONDOWN:
            if(cena==Cena.TELATITULO):
                cena = telaTitulo.playPressionado()

            elif(cena==Cena.MENU):
                menu.botaoPagina()
                cena,idFase = menu.botaoFase()
            
            elif(cena==Cena.JOGO):
                jogo.cliquePause()
                cena = jogo.opcoesPause()
            
            elif(cena==Cena.FIMDEJOGO):
                cena,idFase = fimDeJogo.opcoesFimDeJogo(idFase)
            

    if(cena==Cena.TELATITULO):
        telaTitulo.desenhaTelaTitulo()

    elif(cena==Cena.MENU):
        menu.atualizaCursor()
        menu.desenhaMenu()
        
    elif(cena==Cena.CARREGAJOGO):
        telaJogo, jogo = menu.carregaJogo(janela,imagensJogo,som,mouse,idFase)
        cena = jogo.iniciaMusica()

    elif(cena==Cena.JOGO):
        cena = jogo.controlaJogo()
        telaJogo.desenha(jogo)
    
    elif(cena==Cena.ATUALIZAMENU):
        jogo.musica.audio.stop()
        cena = menu.atualizaMenu(idFase,jogo.pontuacao)
    
    elif(cena==Cena.FIMDEJOGO):
        fimDeJogo.desenhaFimDeJogo(jogo.pontuacao)
        
    pygame.display.flip()