import math
import random

x = []
y = []
tamanho = 7
iniX = 3
iniY = 3
desX = 6
desY = 6
v = caminho = []

for x in range(tamanho):
    linha = [] 
    for y in range(tamanho):
        linha.append(0)
        if(random.randint(0,2) == 1):
            linha[y] = -1
        else:
            linha[y] = 0
        if(iniX == x and iniY == y):
            linha[y] = 1
        elif(desX == x and desY == y):
            linha[y] = 3
    caminho.append(linha)
    
v[2][2] = -1
v[3][2] = -1
v[2][3] = -1
v[4][4] = -1
v[4][3] = -1
v[3][4] = -1

def hnDestino(estouX, estouY, destinoX, inicialY):
    return (round(math.sqrt(((destinoX-estouX)**2)+((inicialY-estouY)**2)),2))

def gnInicial(estouX, estouY, inicialX, inicialY):
    return(round(math.sqrt(((inicialX-estouX)**2)+((inicialY-estouY)**2)),2))

def fnAtual(g,h):
    return g+h

class Estado():
    def __init__(self, x, y, caminho):
        self.x = x
        self.y = y
        self.inicial = gnInicial(x,y,iniX,iniY)
        self.destino = hnDestino(x,y,desX,desY)
        self.atual = self.inicial+self.destino
        self.caminho = caminho
        self.caminho[x][y] = 1


def imprimr(caminho):
    for x in range(len(caminho)):
        for y in range(len(caminho)):
            print(caminho[x][y], end="")
            print("|", end="")
        print()

def criaEstado(iniX,iniY,v):
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 0):#Baixo
        print("Baixo")
        return Estado(iniX+1,iniY,v)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 0):#Cima
        print("Cima")
        return Estado(iniX-1,iniY,v)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 0):#Direita
        print("Direita")
        return Estado(iniX,iniY+1,v)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 0):#Esquerda
        print("Esquerda")
        return Estado(iniX,iniY-1,v)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 0):#45
        print("45")
        return Estado(iniX+1,iniY+1,v)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 0):#135
        print("135")
        return Estado(iniX+1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 0):#315
        print("315")
        return Estado(iniX-1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 0):#225
        print("225")
        return Estado(iniX-1,iniY-1,v)

imprimr(caminho)

c = criaEstado(iniX,iniY,caminho)

if(c != -1):
    print()
    for i in range(len(caminho)):
        print(c.caminho[i])
