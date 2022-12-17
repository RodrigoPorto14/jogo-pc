from pygame import mixer
from enums import Forma,Lixo
from random import shuffle
import operator

class Musica:
    def __init__(self,id):
        musica = 'audios/musica'+str(id)+'.ogg'
        self.audio = mixer.Sound(musica)
        self.audio.set_volume(0.5)
        with open('arquivos/musicas.txt','rt') as arq:
            conteudo = arq.readlines()[id].split('|')
            self.velocidade=float(conteudo[0])
            self.duracao=int(conteudo[1]) 
            return conteudo[2:]

class MusicaAritmetica(Musica):
    def __init__(self, id):
        conteudo = super().__init__(id)
        self.circulos=conteudo[0].split()
        self.condicoes=conteudo[1].split()
        shuffle(self.condicoes)
        self.inverso = bool(int(conteudo[2]))
        
class MusicaFormas(Musica):
    def __init__(self, id):
        def conversorForma(letra):
            forma = {'C':Forma.CIRCULO,'Q':Forma.QUADRADO,'T':Forma.TRIANGULO}
            return forma[letra]

        conteudo = super().__init__(id)
        self.padrao = list(map(conversorForma,conteudo[0].split()))
        self.adicionais = list(map(lambda x:int(x),conteudo[1].split()))
        self.sequencia = list(map(conversorForma,conteudo[2].split()))
        self.proximo=-1

class MusicaNumero(Musica):
    def __init__(self, id):
        conteudo = super().__init__(id)
        operacoes = {"+":operator.add,"-":operator.sub,"x":operator.mul,'/':operator.floordiv}
        self.operacao=operacoes[conteudo[0][0]]
        self.valor=conteudo[0][1:]
        if(self.valor.isnumeric()):
            self.valor=int(self.valor)
        
        self.sequencia = list(map(lambda x:int(x),conteudo[1].split()))
        self.proximo=0

class MusicaReciclagem(Musica):
    def __init__(self, id):
        tipo = super().__init__(id)[0].replace('\n','')
        lixeira = {'plastico':Lixo.PLASTICO,'papel':Lixo.PAPEL,'vidro':Lixo.VIDRO,'metal':Lixo.METAL}
        self.sequencia = lixeira[tipo]