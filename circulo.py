import operator
from random import randint

class Circulo:
    def __init__(self,x,y,cor):
        cores = [(255,0,0),(0,255,0),(0,0,255)]
        self.x = x
        self.y = y
        self.cor = cores[cor]

class CirculoAritmetica(Circulo):
    def __init__(self,texto, x, y, cor):
        super().__init__(x, y, cor)
        operacoes = {"+":operator.add,"-":operator.sub,"x":operator.mul,"/":operator.floordiv}
        self.texto = texto
        self.operacao = operacoes[texto[0]]
        self.valor = int(texto[1:])
           
class CirculoPadroes(Circulo):
    def __init__(self, conteudo, x, y, cor):
        super().__init__(x, y, cor)
        self.conteudo = conteudo
        self.verificado = False
        self.id=randint(0,3)    