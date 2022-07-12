from enum import Enum

class Cena(Enum):
    TELATITULO = 0
    MENU = 1
    JOGO = 2
    FIMDEJOGO = 3

class Forma(Enum):
    CIRCULO = 0
    QUADRADO = 1
    TRIANGULO = 2

class Lixo(Enum):
    PLASTICO = 0
    PAPEL = 1
    VIDRO = 2
    METAL = 3
