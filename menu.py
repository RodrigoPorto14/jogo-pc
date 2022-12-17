import pickle
from musica import *
from telajogo import *
from jogomatematica import *
from jogopadroes import *
import math

class Menu():
    
    def __init__(self,janela,cursor):
        self.janela=janela
        self.cursor=cursor
        self.click = pygame.mixer.Sound('audios/click3.ogg')
        self.click.set_volume(0.2)
        self.fonte = pygame.font.SysFont('Courier New',24,True)
        self.fonteGrande = pygame.font.SysFont('Courier New',52,True)
        self.pagina = 1
        self.imagens = {}
        with open('arquivos/imagens-menu.txt','rt') as arq:
            while(linha := arq.readline().split()):
                nome = linha[0] ; x = int(linha[1]) ; y = int(linha[2])
                self.imagens[nome] = pygame.transform.scale(pygame.image.load('images/menu/'+nome+'.png'),(x,y))
   
        try:
            with open('arquivos/save.bin','rb') as arq:
                self.fases = pickle.load(arq)
        except:
            with open('arquivos/save.bin','wb') as arq:
                self.fases = [-1] * 24
                self.fases[0] = 0
                pickle.dump(self.fases,arq)

    
    def desenhaMenu(self):
        self.desenhaCabeçalho()
        self.desenhaFases()
        self.desenhaBotoesPagina()
        
    def desenhaFases(self):
        for i in range(4):
            for j in range(3):
                idFase = (self.pagina-1)*12 + i*3+j
                if(self.fases[idFase]==-1):
                    self.janela.blit(self.imagens['lock'],(115+120*j,125+120*i))
                else:
                    mx,my = pygame.mouse.get_pos()
                    if(self.faseOn(i,j,mx,my)):
                        cor = (114,75,255)
                    else:
                        cor = (255,255,255)

                    textoFase = str(idFase+1)
                    star = 'star'+str(self.fases[idFase])
                    self.janela.blit(self.imagens[star],(100+120*j,160+120*i))
                    align = (60-len(textoFase)*30)//2
                    self.janela.blit(self.fonteGrande.render(textoFase,False,cor),(align+100+120*j,110+120*i))

    def desenhaCabeçalho(self):
        self.janela.blit(self.imagens['background'],(0,0))
        self.janela.blit(self.imagens['top-bar'],(0,0))
        #self.janela.blit(self.fonteGrande.render("MENU",False,(255,255,255)),(200,25))

        if(self.voltarOn()):
            self.janela.blit(self.imagens['back-on'],(15,15))
        else:
            self.janela.blit(self.imagens['back-off'],(15,15))

        self.janela.blit(self.imagens['star'],(370,25))
        placarEstrelas = str(self.getEstrelas())+'/'+str(self.getTotalEstrelas())
        align = (70-len(placarEstrelas)*14)//2
        self.janela.blit(self.fonte.render(placarEstrelas,False,(255,255,255)),(410+align,30))

    def getEstrelas(self):
        estrelas=0
        for fase in self.fases:
            if(fase<0):
                break
            estrelas+=fase
        return estrelas
    
    def getTotalEstrelas(self):
        return len(self.fases)*3
    
    def desenhaBotoesPagina(self):
        if(not self.primeiraPagina()):
            if(self.voltarPaginaOn()):
                self.janela.blit(self.imagens['prev-page-on'],(25,300))
            else:
                self.janela.blit(self.imagens['prev-page-off'],(25,300))

        if(not self.ultimaPagina()):
            if(self.proximaPaginaOn()):
                self.janela.blit(self.imagens['next-page-on'],(425,300))
            else:
                self.janela.blit(self.imagens['next-page-off'],(425,300))
        
        numPaginas = len(self.fases)//12
        align = (500-(2*numPaginas-1)*10)//2
        for i in range(numPaginas):
            if(i+1==self.pagina):
                self.janela.blit(self.imagens['page-nav-on'],(align+20*i,590))
            else:
                self.janela.blit(self.imagens['page-nav-off'],(align+20*i,590))
            
    def primeiraPagina(self):
        return self.pagina==1
    
    def ultimaPagina(self):
        return self.pagina*12==len(self.fases)
    
    def botaoPagina(self):
        if(self.proximaPaginaOn()):
            self.click.play()
            self.pagina+=1
        
        if(self.voltarPaginaOn()):
            self.click.play()
            self.pagina-=1
    
    def botaoFase(self):

        if(self.voltarOn()):
            self.click.play()
            return (Cena.TELATITULO,0)

        mx,my = pygame.mouse.get_pos()
        for i in range(4):
            for j in range(3):
                if(self.faseOn(i,j,mx,my)):
                    self.click.play()
                    idFase = (self.pagina-1)*12 + i*3+j
                    return (Cena.CARREGAJOGO,idFase)

        return (Cena.MENU,0)

    def atualizaCursor(self):
        if(self.voltarOn() or self.proximaPaginaOn() or self.voltarPaginaOn() or self.algumaFaseOn()):
            pygame.mouse.set_cursor(self.cursor['hand'])
        else:
            pygame.mouse.set_cursor(self.cursor['arrow'])
    
    def voltarOn(self):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-40,2)+pow(my-40,2))<=25
    
    def proximaPaginaOn(self):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-450,2)+pow(my-325,2))<=25 and not self.ultimaPagina()
    
    def voltarPaginaOn(self):
        mx,my = pygame.mouse.get_pos()
        return math.sqrt(pow(mx-50,2)+pow(my-325,2))<=25 and not self.primeiraPagina()
    
    def algumaFaseOn(self):
        mx,my = pygame.mouse.get_pos()
        for i in range(4):
            for j in range(3):
                if(self.faseOn(i,j,mx,my)):
                    return True
        return False
    
    def faseOn(self,i,j,mx,my):
        idFase = (self.pagina-1)*12 + i*3+j
        return mx>=100+j*120 and mx<=160+j*120 and my>=110+i*120 and my<=180+i*120 and self.fases[idFase]>=0


    def atualizaMenu(self,idFase,pontos):
        if(pontos==100):
            self.fases[idFase]=max(self.fases[idFase],3)
        elif(pontos>=80):
            self.fases[idFase]=max(self.fases[idFase],2)
        elif(pontos>=60):
            self.fases[idFase]=max(self.fases[idFase],1)
        else:
            self.fases[idFase]=max(self.fases[idFase],0)
        
        if(idFase+1<len(self.fases) and self.fases[idFase]>0 and self.fases[idFase+1]==-1):
            self.fases[idFase+1]=0
        
        with open('arquivos/save.bin','wb') as arq:
            pickle.dump(self.fases,arq)

        return Cena.FIMDEJOGO

    def carregaJogo(self,janela,imagens,sound,mouse,idMusica):
        self.janela.fill((0,0,0))
        if(idMusica%4==0):
            musica = MusicaAritmetica(idMusica)
            return TelaJogoAritmetica(janela,imagens,mouse), JogoAritmetica(musica,sound)
        elif(idMusica%4==1):
            musica = MusicaFormas(idMusica)
            return TelaJogoFormas(janela,imagens,mouse), JogoFormas(musica,sound) 
        elif(idMusica%4==2):
            musica = MusicaNumero(idMusica)
            return TelaJogoNumeros(janela,imagens,mouse), JogoNumeros(musica,sound) 

        musica = MusicaReciclagem(idMusica)
        return TelaJogoReciclagem(janela,imagens,mouse), JogoReciclagem(musica,sound)
        