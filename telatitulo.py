import pygame
import math
from enums import Cena

class TelaTitulo():
    def __init__(self,janela,mouse):
        self.janela = janela
        self.mouse = mouse
        self.imagens = {}
        self.imagens['background'] = pygame.image.load('images/menu/background.png')
        self.imagens['start'] = pygame.transform.scale(pygame.image.load('images/menu/start.png'),(150,150))
        self.imagens['start-on'] = pygame.transform.scale(pygame.image.load('images/menu/start-on.png'),(150,150))
    
    def desenhaTelaTitulo(self):
        self.janela.blit(self.imagens['background'],(0,0))
        
        if(self.playSelecionado()):
            pygame.mouse.set_cursor(self.mouse['hand'])
            self.janela.blit(self.imagens['start-on'],(175,245))
        else:
            pygame.mouse.set_cursor(self.mouse['arrow'])

        self.janela.blit(self.imagens['start'],(175,245))
    
    def playPressionado(self):
        if(self.playSelecionado()):
            return Cena.MENU

        return Cena.TELATITULO

    def playSelecionado(self):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-250,2)+pow(my-320,2))<=62
        
