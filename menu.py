from musica import *
from telajogo import *
from jogomatematica import *
from jogopadroes import *

class Menu():
    
    def carregaJogo(self,janela,imagens,sound,idMusica):
        if(idMusica==0):
            musica = MusicaAritmetica(idMusica)
            return TelaJogoAritmetica(janela,imagens), JogoAritmetica(musica,sound)
        elif(idMusica==1):
            musica = MusicaFormas(idMusica)
            return TelaJogoFormas(janela,imagens), JogoFormas(musica,sound) 
        elif(idMusica==2):
            musica = MusicaNumero(idMusica)
            return TelaJogoNumeros(janela,imagens), JogoNumeros(musica,sound) 

        musica = MusicaReciclagem(idMusica)
        return TelaJogoReciclagem(janela,imagens), JogoReciclagem(musica,sound)
        