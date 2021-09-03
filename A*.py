import math
import random
from bisect import insort
from copy import deepcopy

x = []
y = []
tamanho = 7
iniX = 0
iniY = 0
desX = 6
desY = 6
v = caminho = []
historico = []

for x in range(tamanho):
    linha = [] 
    for y in range(tamanho):
        linha.append(0)
        linha[y] = 0
        if(random.randint(0,2) == 1):
            linha[y] = -1
        if(iniX == x and iniY == y):
            linha[y] = 1
        elif(desX == x and desY == y):
            linha[y] = 3
            
    caminho.append(linha)
    

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
        self.caminho = caminho[:]
        self.caminho[x][y] = 2


def imprimir(caminho):
    for x in range(len(caminho)):
        for y in range(len(caminho)):
            print(caminho[x][y], end="")
            print("|", end="")
        print()
    print()

def criaEstado(iniX,iniY,v,i):
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 0 and i == 0):#Baixo
        #print("Baixo")
        return Estado(iniX+1,iniY,v)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 0 and i == 1):#Cima
        #print("Cima")
        return Estado(iniX-1,iniY,v)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 0 and i == 2):#Direita
        #print("Direita")
        return Estado(iniX,iniY+1,v)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 0 and i == 3):#Esquerda
        #print("Esquerda")
        return Estado(iniX,iniY-1,v)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 0 and i == 4):#135
        #print("135")
        return Estado(iniX+1,iniY+1,v)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 0 and i == 5):#225
        #print("225")
        return Estado(iniX+1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 0 and i == 6):#315
        #print("315")
        return Estado(iniX-1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 0 and i == 7):#45
        #print("45")
        return Estado(iniX-1,iniY+1,v)
    else:
        return -1
    
def inserir(aux, lista):
    j = 0
    while(len(lista) > 0 and j < len(lista) and aux.atual > lista[j].atual):
        j += 1
    lista.insert(j,aux)
                
    return lista

def criarNo(iniX,iniY,v):
    lista = []
    caminho = deepcopy(v)
    for i in range(8):
        aux = criaEstado(iniX,iniY,caminho[:],i)
        if(aux != -1):
            j = 0
            existe = 1
            for k in range(len(historico)):
                if(k == aux.caminho):
                    existe = -1
            if(existe):
                historico.append(aux.caminho)
                while(len(lista) > 0 and j < len(lista) and aux.atual > lista[j].atual):
                    j += 1
                lista.insert(j,aux)
            caminho = deepcopy(v)
    return lista

imprimir(caminho)

class Arvore:
    def __init__(self, caminho, filho, altura):
        self.caminho = caminho
        self.altura = altura
        self.filho = filho
        
a = arvore = Arvore(v,criarNo(iniX,iniY,caminho), 0)

for i in range(len(arvore.filho)):
    aux = Arvore(arvore.filho[i].caminho,criarNo(arvore.filho[i].x,arvore.filho[i].y,arvore.filho[i].caminho),arvore.altura+1)
    print()
    print()
    imprimir(aux.caminho)
    imprimir(aux.filho[0].caminho)
    imprimir(aux.filho[1].caminho)
    print()
    print()


for i in range(len(arvore.filho)):
    for j in range(len(arvore.filho[i].caminho)):
        
        print(arvore.filho[i].caminho[j])
    print()



