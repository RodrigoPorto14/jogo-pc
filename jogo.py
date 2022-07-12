from abc import abstractmethod
from enums import Cena
from pygame import mixer,key,K_q,K_w,K_e
import time

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
            print(self.pontuacao)
            return Cena.FIMDEJOGO
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
    
    def pausaJogo(self):
        if(self.jogoIniciado):
            if(self.pause):
                mixer.unpause()
            else:
                mixer.pause()
        else:
            self.jogoIniciado=True
            self.musica.audio.play()

        self.timerMovimentoCirculos = time.time() - self.timerMovimentoCirculos
        self.timerMusica = time.time() - self.timerMusica
        self.pause = not self.pause