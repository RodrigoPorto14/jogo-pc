from abc import abstractmethod
from enums import Cena
from pygame import mixer,mouse,key,K_q,K_w,K_e
import time
import math

class Jogo:
    def __init__(self,musica,som):
        self.musica = musica
        self.som = som
        self.timerMusica = 0
        self.circulos = []
        self.circulosBackup = []
        self.timerMovimentoCirculos = 0
        self.corAtual = (255,255,255)
        self.pontuacao = 0
        self.pause = True
        self.jogoIniciado = False

    def circuloEstourado(self):
        circulo = None
        if key.get_pressed()[K_q]:
            circulo = self.verificaColisao(65)
        if key.get_pressed()[K_w]:
            circulo = self.verificaColisao(225)
        if key.get_pressed()[K_e]:
            circulo = self.verificaColisao(385)

        return circulo
        
    def verificaColisao(self,x):
        for circulo in self.circulos:
            if(circulo.x==x and circulo.y>=470 and circulo.y<=500):
                self.corAtual = circulo.cor
                return circulo
        return None
    
    def verificaFimJogo(self):
        if(self.fimMusica(2)):
            self.setPontuacao()
            return Cena.ATUALIZAMENU
        return Cena.JOGO
    
    @abstractmethod
    def setPontuacao(self):
        pass
    
    def fimMusica(self,delay):
        return self.tempoMusica()>self.musica.duracao+delay
    
    def tempoMusica(self):
        return time.time()-self.timerMusica
    
    def tempoVidaCirculo(self,distBase):
        return (64+distBase)*self.musica.velocidade
    
    def playSelecionado(self):
        mx,my = mouse.get_pos()
        return math.sqrt(pow(mx-250,2)+pow(my-240,2))<=62 and not self.jogoIniciado
    
    def pauseSelecionado(self):
        mx,my = mouse.get_pos()
        return mx>=450 and mx<=480 and my>=15 and my<=50 and self.jogoIniciado
    
    def opcaoPauseSelecionado(self,x,y,raio):
        mx,my = mouse.get_pos()
        return math.sqrt(pow(mx-(x+raio),2)+pow(my-(y+raio),2))<=raio and self.jogoIniciado and self.pause
    
    def opcoesPause(self):
        for i in range(3):
            if(self.opcaoPauseSelecionado(100+i*100,280,40)):
                self.som['click'].play()
                if(i==0):
                    self.musica.audio.stop()
                    return Cena.MENU
                if(i==1):
                    self.pausaJogo()
                if(i==2):
                    self.musica.audio.stop()
                    return Cena.CARREGAJOGO

        return Cena.JOGO
                        
    def cliquePause(self):
        if(self.playSelecionado() or self.pauseSelecionado()):
            self.pausaJogo()

    def pausaJogo(self):
        if(self.jogoIniciado):
            if(self.pause):
                mixer.unpause()
            else:
                mixer.pause()
                self.som['click'].play()
        else:
            self.jogoIniciado=True
            self.som['play'].play()
            self.musica.audio.play()

        self.timerMovimentoCirculos = time.time() - self.timerMovimentoCirculos
        self.timerMusica = time.time() - self.timerMusica
        self.pause = not self.pause