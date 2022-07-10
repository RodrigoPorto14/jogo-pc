from abc import abstractmethod
from lixo import *
from random import randint
import pygame

class TelaJogo:
    def __init__(self,janela,imagens):
        self.janela = janela
        self.imagens = imagens
          
    def desenhaFundo(self):
        self.janela.fill((0,0,0))
    
    def desenhaQuadrados(self):
        square = ['red-square','green-square','blue-square']
        for i in range(3):
            self.janela.blit(self.imagens[square[i]],(50+160*i,470))
    
    @abstractmethod
    def desenhaCirculos(self,circulos):
        pass

    def desenhaHUD(self,corAtual):
        pygame.draw.rect(self.janela,corAtual,(10,0,480,10))
        pygame.draw.rect(self.janela,corAtual,(0,0,10,640))
        pygame.draw.rect(self.janela,corAtual,(10,630,480,10))
        pygame.draw.rect(self.janela,corAtual,(490,0,10,640))

        pygame.draw.rect(self.janela,corAtual,(10,560,480,10))
        pygame.draw.rect(self.janela,(0,0,0),(10,570,480,60))
    
    def desenha(self,circulos,corAtual):
        self.desenhaFundo()
        self.desenhaQuadrados()
        self.desenhaCirculos(circulos)
        self.desenhaHUD(corAtual)
      
class TelaJogoAritmetica(TelaJogo):

    def __init__(self,janela,imagens):
        super().__init__(janela,imagens)
        self.fonte = pygame.font.SysFont('Courier New',18,True)
        self.fonteGrande = pygame.font.SysFont('Courier New',32,True)
    
    def desenhaCirculos(self,circulos):
        circle = {(255,0,0):'red-circle',(0,255,0):'green-circle',(0,0,255):'blue-circle'}
        for circulo in circulos:
            self.janela.blit(self.imagens[circle[circulo.cor]],(circulo.x,circulo.y))
            tamanhoTexto = len(circulo.texto)*11
            align = (50-tamanhoTexto)/2
            self.janela.blit(self.fonte.render(circulo.texto,False,circulo.cor),(circulo.x+align,circulo.y+15))
    
    def desenhaCondicao(self,condicao,pontos,metaPontos):
        texto = "{} {} {}"
        texto = texto.format(pontos,condicao,metaPontos)
        tamanhoTexto = len(texto)*18
        align = (480-tamanhoTexto)/2
        self.janela.blit(self.fonteGrande.render(texto,False,(255,255,255)),(10+align,582))
    
    def desenha(self,jogo):
        super().desenha(jogo.circulos,jogo.corAtual)
        self.desenhaCondicao(jogo.condicao,jogo.pontos,jogo.metaPontos)

class TelaJogoPadroes(TelaJogo):
    def __init__(self,janela,imagens):
        super().__init__(janela,imagens)
    
    def desenhaCirculos(self,circulos):
        circle = {(255,0,0):'red-circle',(0,255,0):'green-circle',(0,0,255):'blue-circle'}
        for circulo in circulos:
            self.janela.blit(self.imagens[circle[circulo.cor]],(circulo.x,circulo.y))
            self.desenhaConteudo(circulo.conteudo,circulo.x,circulo.y,circulo.cor,circulo.id)
    
    @abstractmethod
    def desenhaConteudo(self,conteudo,x,y,cor,id):
        pass

    @abstractmethod
    def desenhaSequencia(self,sequencia):
        pass
    
    def desenha(self,jogo):
        super().desenha(jogo.circulos,jogo.corAtual)
        self.desenhaSequencia(jogo.musica.sequencia)

class TelaJogoFormas(TelaJogoPadroes):
    
    def desenhaConteudo(self,forma,x,y,cor,id):
        if(forma=='C'):
            pygame.draw.circle(self.janela,cor,(x+25,y+25),10)
        elif(forma=='Q'):
            pygame.draw.rect(self.janela,cor,(x+15,y+15,20,20))
        elif(forma=='T'):
            pygame.draw.polygon(self.janela,cor,[(x+25,y+13),(x+15,y+33),(x+35,y+33)])
    
    def desenhaSequencia(self,sequencia):
        qtdFormas = len(sequencia)
        qtdEspacos = qtdFormas-1
        tamanhoSequencia = qtdFormas*20 + qtdEspacos*5
        align = (480-tamanhoSequencia)/2

        for i in range(len(sequencia)):
            self.desenhaConteudo(sequencia[i],align-5+25*i,578,(255,255,255),0)


class TelaJogoNumeros(TelaJogoPadroes):

    def __init__(self,janela,imagens):
        super().__init__(janela,imagens)
        self.fonte = pygame.font.SysFont('Courier New',18,True) 
        self.fonteGrande = pygame.font.SysFont('Courier New',22,True)    

    def desenhaConteudo(self,numero,x,y,cor,id):
        numero = str(numero)
        tamanhoTexto = len(numero)*11
        align = (50-tamanhoTexto)/2
        self.janela.blit(self.fonte.render(numero,False,cor),(x+align,y+15))
    
    def desenhaSequencia(self,sequencia):
        while(len(sequencia)>8):
            sequencia.pop(0)
        texto = "["
        for numero in sequencia:
            texto+=str(numero)+','
        texto=texto[:-1]
        texto+="]"
        
        tamanhoTexto = len(texto)*13
        align = (480-tamanhoTexto)/2
        self.janela.blit(self.fonteGrande.render(texto,False,(255,255,255)),(10+align,585))

class TelaJogoReciclagem(TelaJogoPadroes):
    
    def desenhaConteudo(self,tipoLixo,x,y,cor,id):
        lixos = {Lixo.PAPEL: ['book','newspaper','box','paperwrap'],Lixo.VIDRO: ['glasses','winebottle','wineglass','mirror']}
        cores = {(255,0,0):'red',(0,255,0):'green',(0,0,255):'blue'}
        lixo = lixos[tipoLixo][id]
        corLixo = cores[cor]
        self.janela.blit(self.imagens[corLixo+'-'+lixo],(x+9,y+8))
    
    def desenhaSequencia(self,tipoLixo):
        lixeira = {Lixo.PAPEL:'paper',Lixo.VIDRO:'glass'}
        align = (480-50)/2
        self.janela.blit(self.imagens[lixeira[tipoLixo]],(10+align,575))
        
        



        