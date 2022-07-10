from abc import abstractmethod
from circulo import *
from cena import *
from lixo import *
from random import randint, shuffle, sample
import time
import pygame
import operator

class Jogo:
    def __init__(self,musica,sound):
        self.musica = musica
        self.sound = sound
        self.timerMusica = 0
        self.circulos = []
        self.timerMovimentoCirculos = 0
        self.corAtual = (255,255,255)
        self.pontuacao = 0
        self.pause = True

    def circuloEstourado(self):
        circulo = None
        if pygame.key.get_pressed()[pygame.K_q]:
            circulo = self.verificaColisao(65)
        if pygame.key.get_pressed()[pygame.K_w]:
            circulo = self.verificaColisao(225)
        if pygame.key.get_pressed()[pygame.K_e]:
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
        if(pygame.mixer.get_busy()):
            if(self.pause):
                pygame.mixer.unpause()
            else:
                pygame.mixer.pause()
        else:
            self.musica.audio.play()

        self.timerMovimentoCirculos = time.time() - self.timerMovimentoCirculos
        self.timerMusica = time.time() - self.timerMusica
        self.pause = not self.pause

    
class JogoAritmetica(Jogo):

    def __init__(self,musica,sound):
        super().__init__(musica,sound)
        self.pontos = 0
        self.metaPontos = 0
        self.rodada = 0
        self.timerRodada = 0
    
    def iniciaMusica(self):
        #self.musica.audio.play()
        self.pontos=0
        self.criaCondicao()
        self.criaCirculos()
        self.criaMetaPontos()
        print(self.rodada,self.pontuacao)
        #self.timerMusica = time.time()
        #self.iniciaRodada()
        return Cena.JOGO
    
    def iniciaRodada(self):
        self.pontos=0
        self.criaCondicao()
        self.criaCirculos()
        self.criaMetaPontos()
        self.timerMovimentoCirculos = time.time()
        self.timerRodada = time.time()
    
    def criaCondicao(self):
        self.condicao = self.musica.condicoes[self.rodada]
    
    def criaMetaPontos(self):
        metaPontos = 0
        qtdCirculos = len(self.circulos)
        qtdOperacoes = min(2+self.rodada//2,qtdCirculos-1)
        copiaCirculos = self.circulos[:]
        copiaCirculos.sort(reverse=True,key=lambda x: x.y)
        indices = list(range(qtdCirculos))
        indicesSortiados = sample(indices,qtdOperacoes)
        indicesSortiados.sort()

        for i in indicesSortiados:
            metaPontos = copiaCirculos[i].operacao(metaPontos,copiaCirculos[i].valor)
        
        if(self.condicao=='>'):
            metaPontos-=1
        if(self.condicao=='<'):
            metaPontos+=1
        
        self.metaPontos=metaPontos
        
        
    def criaCirculos(self):
        self.circulos.clear()
        posicaoBase = [-300,-300,-300]
        qtdCirculos = len(self.musica.circulos)
        circulos = self.musica.circulos[:]
        shuffle(circulos)
        cores = [0,1,2]
        
        for i in range(qtdCirculos):
            if((qtdCirculos%3==1 and i==qtdCirculos-1) or (qtdCirculos%3==2 and i>=qtdCirculos-2)):
                corAleatoria = randint(0,len(cores)-1)
                cor = cores[corAleatoria]
                cores.remove(cor)
            else:
                cor = i%3
            distAdicional = randint(2,6)*10
            x = 65+160*cor
            y = posicaoBase[cor]+distAdicional+50
            posicaoBase[cor]=y   
            self.circulos.append(CirculoAritmetica(circulos[i],x,y,int(cor)))

    def passaRodada(self):
        if(self.fimRodada()):
            if(self.condicaoCorreta()):
                self.pontuacao+=1
            if(self.restaCondicoes()):
                self.rodada+=1
                self.iniciaRodada() 
            else:
                self.timerRodada=0 
    
    def fimRodada(self):
        return time.time()-self.timerRodada>=self.tempoVidaCirculo(30)
    
    def restaCondicoes(self):
        return self.rodada+1<len(self.musica.condicoes)

    def condicaoCorreta(self):
        operador = {'>': operator.gt,'<': operator.lt,'=':operator.eq}
        return operador[self.condicao](self.pontos,self.metaPontos)

    def moveCirculos(self):
        if(time.time()-self.timerMovimentoCirculos>=self.musica.velocidade):
            for circulo in self.circulos:
                circulo.y+=10
            self.timerMovimentoCirculos=time.time()
    
    def atualizaPontos(self):
        circulo = self.circuloEstourado()
        if(circulo!=None):
            self.sound['hit'].play()
            self.pontos = circulo.operacao(self.pontos,circulo.valor)
            self.circulos.remove(circulo)
    
    def setPontuacao(self):
        self.pontuacao = (self.pontuacao*100)//(self.rodada+1)
    
    def pausaJogo(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            super().pausaJogo()
            self.timerRodada = time.time() - self.timerRodada
        
    def controlaJogo(self):
        if(not self.pause):
            self.passaRodada()
            self.moveCirculos()
            self.atualizaPontos()
            return self.verificaFimJogo()
        else:
            return Cena.JOGO


class JogoPadroes(Jogo):
    
    def __init__(self,musica,sound):
        super().__init__(musica,sound)
        self.timerCriacaoCirculo = 0
        self.posicaoCirculoEstourado = 640
        self.pontuacaoMaxima = 0

    def iniciaMusica(self):
        #self.musica.audio.play()
        #self.timerMusica = time.time()
        #self.timerMovimentoCirculos=time.time()
        #self.timerCriacaoCirculo=time.time()
        return Cena.JOGO 

    def criaCirculos(self):
        if(not self.fimMusica(-self.tempoVidaCirculo(15)) and self.tempoCriacaoCirculo()):
            conteudos = self.getConteudos()
            id = randint(0,3)
            cores = [0,1,2]
            qtdCirculos = randint(1,3)
            for i in range(qtdCirculos):
                distAdicional = randint(2,10)*10
                conteudo = randint(0,len(conteudos)-1)
                cor = randint(0,len(cores)-1)
                self.circulos.append(CirculoPadroes(conteudos[conteudo],65+160*cores[cor],distAdicional-150,cores[cor],id))
                cores.remove(cores[cor])
            self.timerCriacaoCirculo=time.time()
    
    @abstractmethod
    def getConteudos(self):
        pass
    
    def tempoCriacaoCirculo(self):
        return time.time()-self.timerCriacaoCirculo>=15*self.musica.velocidade
    
    def removeCirculos(self):
        for circulo in self.circulos:
            if(circulo.y>640):
                self.circulos.remove(circulo)
    
    def moveCirculos(self):
        if(time.time()-self.timerMovimentoCirculos>=self.musica.velocidade):
            for circulo in self.circulos:
                circulo.y+=10
            if(self.posicaoCirculoEstourado<640):
                self.posicaoCirculoEstourado+=10
            self.timerMovimentoCirculos=time.time()
    
    def verificaEstouro(self,proximo):
        circulo = self.circuloEstourado()
        if(circulo!=None):
            if(circulo.conteudo==proximo):
                self.sound['hit'].play()
                self.setProximo()
                self.setSequencia(circulo.conteudo)
                self.posicaoCirculoEstourado=circulo.y
                self.pontuacao+=1
                self.pontuacaoMaxima+=1

            else:
                self.sound['miss'].play()
                self.pontuacao-=1
            
            self.circulos.remove(circulo)
    
    def setSequencia(self,conteudo):
        self.musica.sequencia.append(conteudo)
        
    def passouCirculoCorreto(self,proximo):
        for circulo in self.circulos:
            if(not circulo.verificado and circulo.y==510 and circulo.conteudo==proximo and circulo.y<self.posicaoCirculoEstourado):
                self.sound['miss'].play()
                self.pontuacaoMaxima+=1
                circulo.verificado=True
    
    def setPontuacao(self):
        self.pontuacao = max((self.pontuacao*100)//self.pontuacaoMaxima,0)
    
    def pausaJogo(self):
        if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
            super().pausaJogo()
            self.timerCriacaoCirculo = time.time() - self.timerCriacaoCirculo
    
    @abstractmethod
    def getProximo(self):
        pass

    @abstractmethod
    def setProximo(self):
        pass
      
    def controlaJogo(self):
        if(not self.pause):
            self.criaCirculos()
            self.removeCirculos()
            self.moveCirculos()
            self.verificaEstouro(self.getProximo())
            self.passouCirculoCorreto(self.getProximo())
            return self.verificaFimJogo()
        else:
            return Cena.JOGO

class JogoNumeros(JogoPadroes):

    def getConteudos(self):
        valor = self.musica.proximo
        listaValores = []
        for i in range(-4,4):
            listaValores.append(valor+i)
        return listaValores
    
    def getProximo(self):
        return self.musica.proximo
    
    def setProximo(self):
        self.musica.proximo = self.musica.operacao(self.musica.proximo,self.musica.valor)

class JogoFormas(JogoPadroes):

    def getConteudos(self):
        return ['C','Q','T']
    
    def getProximo(self):
        return self.musica.padrao[self.musica.proximo]
    
    def setProximo(self):
        if(self.musica.proximo+1<len(self.musica.padrao)):
            self.musica.proximo+=1
        else:
            self.musica.proximo=0
        
        if(len(self.musica.sequencia)>=len(self.musica.padrao)):
            self.musica.sequencia.clear()

class JogoReciclagem(JogoPadroes):
    
    def getConteudos(self):
        return [Lixo.VIDRO,Lixo.PAPEL]
    
    def getProximo(self):
        return self.musica.sequencia
    
    def setSequencia(self, conteudo):
        self.sequencia = conteudo
    

        
        
    

        





            


        

