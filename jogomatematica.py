from jogo import *
from circulo import *
from random import randint, shuffle, sample
import time
import operator

class JogoAritmetica(Jogo):

    def __init__(self,musica,som):
        super().__init__(musica,som)
        self.pontos = 0
        self.condicao = ''
        self.metaPontos = 0
        self.rodada = 0
        self.timerRodada = 0
    
    def iniciaMusica(self):
        self.setPontos()
        self.criaCondicao()
        self.criaCirculos()
        self.criaMetaPontos()
        return Cena.JOGO
    
    def iniciaRodada(self):
        self.setPontos()
        self.criaCondicao()
        self.criaCirculos()
        self.criaMetaPontos()
        self.timerMovimentoCirculos = time.time()
        self.timerRodada = time.time()
    
    def setPontos(self):
        if(self.musica.inverso):
            self.pontos=self.metaPontos
        else:
            self.pontos=0
    
    def criaCondicao(self):
        self.condicao = self.musica.condicoes[self.rodada][0]
    
    def criaMetaPontos(self):
        if(len(self.musica.circulos)==18):
            self.metaPontos = randint(50,99)
        elif(self.musica.inverso and self.rodada%2==1):
            self.metaPontos=0
        elif(len(self.musica.condicoes[self.rodada])>1):
            self.metaPontos = int(self.musica.condicoes[self.rodada][1:])
        else:
            metaPontos = 0
            copiaCirculos = self.circulos[:]
            copiaCirculos.sort(reverse=True,key=lambda x: x.y)

            if(self.condicao=='>'):
                for circulo in copiaCirculos:
                    if(circulo.operacao(metaPontos,circulo.valor)>metaPontos):
                        metaPontos = circulo.operacao(metaPontos,circulo.valor)
                metaPontos-=1
            
            elif(self.condicao=='<'):
                for circulo in copiaCirculos:
                    if(circulo.operacao(metaPontos,circulo.valor)<metaPontos):
                        metaPontos = circulo.operacao(metaPontos,circulo.valor)
                metaPontos+=1
            
            else:
                qtdCirculos = len(self.circulos)
                qtdOperacoes = min(2+self.rodada//2,qtdCirculos-1)
                indices = list(range(qtdCirculos))
                indicesSortiados = sample(indices,qtdOperacoes)
                indicesSortiados.sort()

                for i in indicesSortiados:
                    metaPontos = copiaCirculos[i].operacao(metaPontos,copiaCirculos[i].valor)
            
            self.metaPontos=metaPontos
        
    def criaCirculos(self):
        self.circulos.clear()
        if(self.musica.inverso and self.rodada%2==1):
            circulos = self.circulosBackup[:]
            self.inverteOperacoes(circulos)
            circulos.reverse()
        else:
            circulos = self.musica.circulos[:]
            shuffle(circulos)
            self.circulosBackup = circulos[:]

        pos = self.getPosicaoInicial()
        posicaoBase = [pos,pos,pos]
        qtdCirculos = len(self.musica.circulos)
        cores = [0,1,2]
        
        for i in range(qtdCirculos):
            if((qtdCirculos%3==1 and i==qtdCirculos-1) or (qtdCirculos%3==2 and i>=qtdCirculos-2)):
                corAleatoria = randint(0,len(cores)-1)
                cor = cores[corAleatoria]
                cores.remove(cor)
            else:
                cor = i%3

            if(self.musica.inverso and self.rodada%2==1):
                distAdicional=50
            else:
                distAdicional = randint(2,6)*10

            x = 65+160*cor
            y = posicaoBase[cor]+distAdicional+50
            posicaoBase[cor]=y   
            self.circulos.append(CirculoAritmetica(circulos[i],x,y,int(cor)))
    
    def inverteOperacoes(self,circulos):
        inverso = {'+':'-','-':'+','x':'/','/':'x'}
        for i in range(len(circulos)):
            circulos[i] = circulos[i].replace(circulos[i][0],inverso[circulos[i][0]])

    def getPosicaoInicial(self):
        if(len(self.musica.circulos)==18):
            return -800
        else:
            return -300

    def passaRodada(self):
        if(self.fimRodada() and self.restaCondicoes(0)):
            if(self.condicaoCorreta()):
                self.pontuacao+=1
            if(self.restaCondicoes(1)):
                self.rodada+=1
                self.iniciaRodada()
            else:
                self.rodada+=1 
            
    def fimRodada(self):
        return time.time()-self.timerRodada>=self.tempoVidaCirculo(self.getPosicaoInicial()//-10)
    
    def restaCondicoes(self,add):
        return self.rodada+add<len(self.musica.condicoes)

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
            self.som['hit'].play()
            self.pontos = circulo.operacao(self.pontos,circulo.valor)
            self.circulos.remove(circulo)
    
    def setPontuacao(self):
        if(self.rodada>0):
            self.pontuacao = (self.pontuacao*100)//(self.rodada)
        else:
            self.pontuacao = 0

    def pausaJogo(self):
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