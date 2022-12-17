import pygame
import math
from enums import Cena

class TelaTitulo():
    def __init__(self,janela,mouse):
        self.janela = janela
        self.mouse = mouse
        self.click = pygame.mixer.Sound('audios/click2.ogg')
        self.click.set_volume(0.2)
        self.imagens = {}
        self.imagens['background'] = pygame.image.load('images/menu/background.png')
        self.imagens['start'] = pygame.transform.scale(pygame.image.load('images/menu/start.png'),(150,150))
        self.imagens['start-on'] = pygame.transform.scale(pygame.image.load('images/menu/start-on.png'),(150,150))
        nomeJogo = 'SMARTDJ'
        for letra in nomeJogo:
            self.imagens[letra] = pygame.transform.scale(pygame.image.load('images/menu/'+letra+'.png'),(40,50))

    
    def desenhaTelaTitulo(self):
        self.janela.blit(self.imagens['background'],(0,0))
        self.desenhaNomeJogo()
        
        if(self.playSelecionado()):
            pygame.mouse.set_cursor(self.mouse['hand'])
            self.janela.blit(self.imagens['start-on'],(175,245))
        else:
            pygame.mouse.set_cursor(self.mouse['arrow'])

        self.janela.blit(self.imagens['start'],(175,245))
    
    def desenhaNomeJogo(self):
        self.janela.blit(self.imagens['S'],(115,175))
        self.janela.blit(self.imagens['M'],(155,175))
        self.janela.blit(self.imagens['A'],(195,175))
        self.janela.blit(self.imagens['R'],(235,175))
        self.janela.blit(self.imagens['T'],(265,176))
        self.janela.blit(self.imagens['D'],(315,175))
        self.janela.blit(self.imagens['J'],(355,178))
    
    def playPressionado(self):
        if(self.playSelecionado()):
            self.click.play()
            return Cena.MENU

        return Cena.TELATITULO

    def playSelecionado(self):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-250,2)+pow(my-320,2))<=62
        
