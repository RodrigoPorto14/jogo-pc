from musica import *
from telajogo import *
from jogo import *

class Menu():
    
    def carregaJogo(self,janela,squares,circles,sound,idMusica):
        if(idMusica==0):
            musica = MusicaAritmetica(idMusica)
            return TelaJogoAritmetica(janela,circles,squares), JogoAritmetica(musica,sound)
        elif(idMusica==1):
            musica = MusicaPadroes(idMusica)
            return TelaJogoPadroes(janela,circles,squares), JogoPadroes(musica,sound) 

        musica = MusicaPadroes(idMusica)
        return TelaJogoSequencias(janela,circles,squares), JogoSequencias(musica,sound)  
        