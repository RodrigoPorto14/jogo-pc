from abc import abstractmethod
import pygame

class TelaJogo:
    def __init__(self,janela,circles,squares):
        cores = [(255,0,0),(0,255,0),(0,0,255)]
        self.janela = janela
        self.circles = {} ; self.squares = []
        for i in range(3):
            self.circles[cores[i]] = circles[i]
            self.squares.append(squares[i])
        
    def desenhaFundo(self):
        self.janela.fill((0,0,0))
    
    def desenhaQuadrados(self):
        for i in range(len(self.squares)):
            self.janela.blit(self.squares[i],(50+160*i,470))
    
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

    def __init__(self,janela,circles,squares):
        super().__init__(janela,circles,squares)
        self.fonte = pygame.font.SysFont('Courier New',18,True)
        self.fonteGrande = pygame.font.SysFont('Courier New',32,True)
    
    def desenhaCirculos(self,circulos):
        for circulo in circulos:
            self.janela.blit(self.circles[circulo.cor],(circulo.x,circulo.y))
            tamanhoTexto = len(circulo.texto)*6
            align = (38-tamanhoTexto)/2
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
    def __init__(self,janela,circles,squares):
        super().__init__(janela,circles,squares)
        self.fonte = pygame.font.SysFont('Courier New',18,True)
    
    def desenhaCirculos(self,circulos):
        for circulo in circulos:
            self.janela.blit(self.circles[circulo.cor],(circulo.x,circulo.y))
            self.desenhaForma(circulo.forma,circulo.x,circulo.y,circulo.cor)
    
    def desenhaForma(self,forma,x,y,cor):
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
            self.desenhaForma(sequencia[i],align-5+25*i,578,(255,255,255))

    def desenha(self,jogo):
        super().desenha(jogo.circulos,jogo.corAtual)
        self.desenhaSequencia(jogo.musica.amostraSequencia)

class TelaJogoSequencias(TelaJogoPadroes):

    def desenhaForma(self,forma,x,y,cor):
        tamanhoTexto = len(forma)*6
        align = (38-tamanhoTexto)/2
        self.janela.blit(self.fonte.render(forma,False,cor),(x+align,y+15))
    
    def desenhaSequencia(self,sequencia):
        while(len(sequencia)>12):
            sequencia.pop(0)
        texto = "["
        for numero in sequencia:
            texto+=numero+','
        texto=texto[:-1]
        texto+="]"
        tamanhoTexto = len(texto)*11
        align = (480-tamanhoTexto)/2
        self.janela.blit(self.fonte.render(texto,False,(255,255,255)),(10+align,582))
        



        