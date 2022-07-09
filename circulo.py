import operator

class Circulo:
    def __init__(self,x,y,cor):
        cores = [(255,0,0),(0,255,0),(0,0,255)]
        self.x = x
        self.y = y
        self.cor = cores[cor]

class CirculoAritmetica(Circulo):
    def __init__(self,texto, x, y, cor):
        super().__init__(x, y, cor)
        operacoes = {"+":operator.add,"-":operator.sub,"x":operator.mul}
        self.texto = texto
        self.operacao = operacoes[texto[0]]
        self.valor = int(texto[1:])
           
class CirculoPadroes(Circulo):
    def __init__(self, forma, x, y, cor):
        super().__init__(x, y, cor)
        self.forma = forma
        self.verificado = False

        