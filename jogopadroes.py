from jogo import *
from circulo import *
from enums import Forma,Lixo
from random import randint
import time

class JogoPadroes(Jogo):
    
    def __init__(self,musica,som):
        super().__init__(musica,som)
        self.timerCriacaoCirculo = 0
        self.posicaoCirculoEstourado = 640
        self.pontuacaoMaxima = 0

    def iniciaMusica(self):
        self.setProximo()
        return Cena.JOGO 

    def criaCirculos(self):
        if(not self.fimMusica(-self.tempoVidaCirculo(15)) and self.tempoCriacaoCirculo()):
            conteudos = self.getConteudos()
            cores = [0,1,2]
            qtdCirculos = randint(1,3)
            for i in range(qtdCirculos):
                distAdicional = randint(2,10)*10
                conteudo = randint(0,len(conteudos)-1)
                cor = randint(0,len(cores)-1)
                self.circulos.append(CirculoPadroes(conteudos[conteudo],65+160*cores[cor],distAdicional-150,cores[cor]))
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
                self.som['hit'].play()
                self.setSequencia(circulo.conteudo)
                self.setProximo()
                self.posicaoCirculoEstourado=circulo.y
                self.pontuacao+=1
                self.pontuacaoMaxima+=1

            else:
                self.som['miss'].play()
                self.pontuacao-=1
            
            self.circulos.remove(circulo)
    
    @abstractmethod
    def setSequencia(self,conteudo):
        pass

    @abstractmethod
    def setProximo(self):
        pass
        
    def passouCirculoCorreto(self,proximo):
        for circulo in self.circulos:
            if(not circulo.verificado and circulo.y==510 and circulo.conteudo==proximo and circulo.y<self.posicaoCirculoEstourado):
                self.som['miss'].play()
                self.pontuacaoMaxima+=1
                circulo.verificado=True
    
    def setPontuacao(self):
        if(self.pontuacaoMaxima>0):
            self.pontuacao = (self.pontuacao*100)//self.pontuacaoMaxima
        else:
            self.pontuacao = 0
    
    def pausaJogo(self):
        super().pausaJogo()
        self.timerCriacaoCirculo = time.time() - self.timerCriacaoCirculo
    
    @abstractmethod
    def getProximo(self):
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
        for i in range(-3,3):
            listaValores.append(valor+i)
        return listaValores
    
    def getProximo(self):
        return self.musica.proximo
    
    def setProximo(self):
        if(self.musica.valor=='fib'):
            self.musica.proximo = self.musica.operacao(self.musica.sequencia[-2],self.musica.sequencia[-1])
        elif(isinstance(self.musica.valor,str) and self.musica.valor.find('fig')!=-1):
            razao = self.musica.sequencia[-1] - self.musica.sequencia[-2]
            self.musica.proximo = self.musica.operacao(self.musica.sequencia[-1],razao+int(self.musica.valor[-1]))
        else:
            self.musica.proximo = self.musica.operacao(self.musica.sequencia[-1],self.musica.valor)
    
    def setSequencia(self,conteudo):
        self.musica.sequencia.append(conteudo)

class JogoFormas(JogoPadroes):

    def getConteudos(self):
        return [Forma.CIRCULO,Forma.QUADRADO,Forma.TRIANGULO]
    
    def getProximo(self):
        return self.musica.padrao[self.musica.proximo]
    
    def setProximo(self):
        if(self.musica.proximo+1<len(self.musica.padrao)):
            self.musica.proximo+=1
        else:
            self.musica.proximo=0
    
    def setSequencia(self,conteudo):
        formas = [Forma.CIRCULO,Forma.QUADRADO,Forma.TRIANGULO]
        if(len(self.musica.sequencia)>=len(self.musica.padrao)):
            self.musica.sequencia.clear()
            for i in range(len(self.musica.adicionais)):
                for j in range(self.musica.adicionais[i]):
                    forma = self.musica.padrao.index(formas[i])
                    self.musica.padrao.insert(forma,formas[i])

        self.musica.sequencia.append(conteudo)

class JogoReciclagem(JogoPadroes):
    
    def getConteudos(self):
        return [Lixo.PLASTICO,Lixo.PAPEL,Lixo.VIDRO,Lixo.METAL]
    
    def getProximo(self):
        return self.musica.sequencia
    
    def setSequencia(self, conteudo):
        self.sequencia = conteudo