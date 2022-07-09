from pygame import mixer

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

class MusicaPadroes(Musica):
    def __init__(self, id):
        conteudo = super().__init__(id)
        self.sequencia=conteudo[0].split()
        self.amostraSequencia=conteudo[1].split()
        self.proximaForma=int(conteudo[2])
            


