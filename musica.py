from re import L
from pygame import mixer
from lixo import *
import operator


class Musica:
    def __init__(self,id):
        musica = 'audios/musica'+str(id)+'.wav'
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

class MusicaFormas(Musica):
    def __init__(self, id):
        conteudo = super().__init__(id)
        self.padrao=conteudo[0].split()
        self.sequencia=conteudo[1].split()
        self.proximo=0

class MusicaNumero(Musica):
    def __init__(self, id):
        conteudo = super().__init__(id)
        operacoes = {"+":operator.add,"-":operator.sub,"x":operator.mul}
        self.operacao=operacoes[conteudo[0][0]]
        self.valor=int(conteudo[0][1:])
        self.sequencia=[]
        for numero in conteudo[1].split():
            self.sequencia.append(int(numero))

        self.proximo=int(self.operacao(self.sequencia[-1],self.valor))

class MusicaReciclagem(Musica):
    def __init__(self, id):
        tipo = super().__init__(id)[0].replace('\n','')
        lixeira = {'plastico':Lixo.PLASTICO,'papel':Lixo.PAPEL,'vidro':Lixo.VIDRO,'metal':Lixo.METAL,'organico':Lixo.ORGANICO}
        self.sequencia = lixeira[tipo]

            


