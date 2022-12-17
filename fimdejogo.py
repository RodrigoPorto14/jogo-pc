import pygame
import math
from enums import Cena

class FimDeJogo():
    def __init__(self,janela,cursor):
        self.janela = janela
        self.cursor = cursor
        self.qtdOpcoes = 0
        self.fonte = pygame.font.SysFont('Courier New',32,True)
        self.click = pygame.mixer.Sound('audios/click3.ogg')
        self.imagens = {}
        self.imagens['background'] = pygame.image.load('images/menu/background.png')
        self.imagens['fimdejogo-window'] = pygame.image.load('images/menu/fimdejogo-window.png')
        self.imagens['star0'] = pygame.transform.scale(pygame.image.load('images/menu/star0.png'),(300,90))
        self.imagens['star1'] = pygame.transform.scale(pygame.image.load('images/menu/star1.png'),(300,90))
        self.imagens['star2'] = pygame.transform.scale(pygame.image.load('images/menu/star2.png'),(300,90))
        self.imagens['star3'] = pygame.transform.scale(pygame.image.load('images/menu/star3.png'),(300,90))
        self.imagens['home-off'] = pygame.transform.scale(pygame.image.load('images/jogo/home-off.png'),(80,80))
        self.imagens['home-on'] = pygame.transform.scale(pygame.image.load('images/jogo/home-on.png'),(80,80))
        self.imagens['restart-off'] = pygame.transform.scale(pygame.image.load('images/jogo/restart-off.png'),(80,80))
        self.imagens['restart-on'] = pygame.transform.scale(pygame.image.load('images/jogo/restart-on.png'),(80,80))
        self.imagens['next-off'] = pygame.transform.scale(pygame.image.load('images/menu/next-off.png'),(80,80))
        self.imagens['next-on'] = pygame.transform.scale(pygame.image.load('images/menu/next-on.png'),(80,80))
    
    def desenhaFimDeJogo(self,pontuacao):
        if(pontuacao==100):
            estrelas = 3
        elif(pontuacao>=80):
            estrelas = 2
        elif(pontuacao>=60):
            estrelas = 1
        else:
            estrelas = 0

        self.janela.blit(self.imagens['background'],(0,0))
        self.janela.blit(self.imagens['fimdejogo-window'],(50,120))
        estrela = 'star'+str(estrelas)
        self.janela.blit(self.imagens[estrela],(100,190))
        textoPontos = 'Pontos '+str(pontuacao)
        align = (400-len(textoPontos)*18)//2
        self.janela.blit(self.fonte.render(textoPontos,False,(255,255,255)),(50+align,310))
        self.desenhaOpcoes(estrelas)
    
    def desenhaOpcoes(self,estrelas):
        botao = ['home','restart','next']
        if(estrelas>0):
            self.qtdOpcoes = 3
        else:
            self.qtdOpcoes = 2

        cursor = False
        align = (400-self.qtdOpcoes*80-(self.qtdOpcoes-1)*30)//2
        for i in range(self.qtdOpcoes):
            if(self.opcaoSelecionado(50+align+i*110,370,40)):
                estado = '-on'
                cursor = True
            else:
                estado = '-off'
            self.janela.blit(self.imagens[botao[i]+estado],(50+align+i*110,370))
    
        if(cursor):
            pygame.mouse.set_cursor(self.cursor['hand'])
        else:
            pygame.mouse.set_cursor(self.cursor['arrow'])
        
    def opcaoSelecionado(self,x,y,raio):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-(x+raio),2)+pow(my-(y+raio),2))<=raio
    
    def opcoesFimDeJogo(self,idFase):
        align = (400-self.qtdOpcoes*80-(self.qtdOpcoes-1)*30)//2
        for i in range(self.qtdOpcoes):
            if(self.opcaoSelecionado(50+align+i*110,370,40)):
                self.click.play()
                if(i==0):
                    return (Cena.MENU,idFase)
                if(i==1):
                    return (Cena.CARREGAJOGO,idFase)
                if(i==2):
                    return (Cena.CARREGAJOGO,idFase+1)

        return (Cena.FIMDEJOGO,idFase)
