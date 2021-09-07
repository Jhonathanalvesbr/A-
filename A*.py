import math
import random
from bisect import insort
from copy import deepcopy
import pygame
from pygame.locals import *
from sys import exit
import time

x = []
y = []
tamanho = 8
iniX = 0
iniY = 0
desX = tamanho-1
desY = tamanho-1
caminho = []
listaAberta = []
listaFechada = []

def zerar():
    global x
    global y
    global tamanho
    global iniX
    global iniY
    global desX
    global desY 
    global caminho
    global listaAberta
    global listaFechada

    x = []
    y = []
    tamanho = 8
    iniX = 0
    iniY = 0
    desX = tamanho-1
    desY = tamanho-1
    listaAberta = []
    listaFechada = []
    #print(len(caminho))
    if(len(caminho) > 0):
        for x in range(len(caminho)):
            for y in range(len(caminho)):
                if(caminho[x][y] == 2 or caminho[x][y] == 1):
                    caminho[x][y] = 0
    else:
        for x in range(tamanho):
            linha = [] 
            for y in range(tamanho):
                linha.append(0)
                linha[y] = 0
                #if(random.randint(0,2) == 1):
                #    linha[y] = -1
                if(iniX == x and iniY == y):
                    linha[y] = 0
                elif(desX == x and desY == y):
                    linha[y] = 3
            caminho.append(linha)
    

def hnDestino(estouX, estouY, destinoX, inicialY):
    return (round(math.sqrt(((destinoX-estouX)**2)+((inicialY-estouY)**2)),2))

class Estado():
    def __init__(self, x, y, caminho):
        self.x = x
        self.y = y
        self.destino = hnDestino(x,y,desX,desY)
        self.atual = 1 * (abs(self.x - desX) +abs(self.y - desY))
        self.caminho = caminho[:]
        if(self.caminho[x][y] != 1):
            self.caminho[x][y] = 2


def imprimir(caminho):
    caminho = caminho.caminho
    for x in range(len(caminho)):
        for y in range(len(caminho)):
            print(caminho[x][y], end="")
            print("|", end="")
        print()
    print()

def criaEstado(iniX,iniY,v,i):
    e = -1
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 0 and i == 0):#Baixo
        #print("Baixo")
        e =  Estado(iniX+1,iniY,v)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 0 and i == 1):#Cima
        #print("Cima")
        e =  Estado(iniX-1,iniY,v)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 0 and i == 2):#Direita
        #print("Direita")
        e = Estado(iniX,iniY+1,v)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 0 and i == 3):#Esquerda
        #print("Esquerda")
        e = Estado(iniX,iniY-1,v)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 0 and i == 4):#135
        #print("135")
        e = Estado(iniX+1,iniY+1,v)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 0 and i == 5):#225
        #print("225")
        e = Estado(iniX+1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 0 and i == 6):#315
        #print("315")
        e = Estado(iniX-1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 0 and i == 7):#45
        #print("45")
        e = Estado(iniX-1,iniY+1,v)
    if(e != -1):
        return e
    else:
        return -1

def win(e):
    if(e == -1):
        return -1
    iniX = e.x
    iniY = e.y
    v = e.caminho
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 3):#Baixo
        #print("Baixo")
        return e
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 3):#Cima
        #print("Cima")
        return e
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 3):#Direita
        #print("Direita")
        return e
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 3):#Esquerda
        #print("Esquerda")
        return e
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 3):#135
        #print("135")
        return e
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 3):#225
        #print("225")
        return e
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 3):#315
        #print("315")
        return e
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 3):#45
        #print("45")
        return e
    else:
        return -1

def winCasoBase(e):
    if(e == -1):
        return -1
    iniX = e.x
    iniY = e.y
    v = e.caminho
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 3):#Baixo
        #print("Baixo")
        return Estado(iniX+1,iniY,v)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 3):#Cima
        #print("Cima")
        return Estado(iniX-1,iniY,v)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 3):#Direita
        #print("Direita")
        return Estado(iniX,iniY+1,v)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 3):#Esquerda
        #print("Esquerda")
        return Estado(iniX,iniY-1,v)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 3):#135
        #print("135")
        return Estado(iniX+1,iniY+1,v)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 3):#225
        #print("225")
        return Estado(iniX+1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 3):#315
        #print("315")
        return Estado(iniX-1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 3):#45
        #print("45")
        return Estado(iniX-1,iniY+1,v)
    else:
        return -1

def winFechada(e):
    if(e == -1):
        return -1
    iniX = e.x
    iniY = e.y
    v = e.caminho
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 1):#Baixo
        #print("Baixo")
        return e
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 1):#Cima
        #print("Cima")
        return e
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 1):#Direita
        #print("Direita")
        return e
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 1):#Esquerda
        #print("Esquerda")
        return e
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 1):#135
        #print("135")
        return e
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 1):#225
        #print("225")
        return e
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 1):#315
        #print("315")
        return e
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 1):#45
        #print("45")
        return e
    else:
        return -1
    
    
def inserir(lista, aux):
    j = 0
    while(len(lista) > 0 and j < len(lista) and aux.atual > lista[j].atual):
        j += 1
    lista.insert(j,aux)
                
    return lista

def criarNo(iniX,iniY,v):
    iniX = e.x
    iniY = e.y
    v = e.caminho
    lista = []
    caminho = deepcopy(v)
    global listaFechada
    global listaAberta
    for i in range(8):
        aux = criaEstado(iniX,iniY,caminho,i)
        if(aux != -1):
            existe = 1
            for k in listaAberta:
                if(k.caminho == aux.caminho):
                    existe = -1
                    break
            if(existe == 1):
                listaAberta = inserir(listaAberta,aux)
                lista = inserir(lista,aux)
            caminho = deepcopy(v)
    if(len(listaAberta) > 0):
        aux = listaAberta.pop(0)
    existe = 1
    
    
    if(aux != -1):
        for k in listaFechada:
            if(k.caminho == aux.caminho):
                existe = -1
                break
        
    if(existe == 1):
        #imprimir(aux)
        listaFechada.append(aux)



    if(win(aux)!= -1):
        aux = deepcopy(aux)
        aux.caminho[desX][desY] = 2
        aux.x = desX
        aux.y = desY
        listaFechada.append(aux)
        return -1
    return aux


'''
def teste(lista):
    j = 0
    k = 0
    a = -1
    b = -1
    while(j < len(lista)):
        k = 1
        while (k < len(lista)-1):
            if(lista[k+1].x == lista[k].x and lista[k+1].y == lista[k].y):
                if(a == -1):
                    a = j
                elif(b == -1):
                    l = []
                    print(a)
                    print(k)
                    print("")
                    i = a
                    while a <= k:
                        lista.pop(i)
                        a += 1
                    a = -1
                    #for i in lista:
                    #    imprimir(i)
                    k = 0
            k += 1
        a = -1
        
        j+= 1
    exit(0)
    return lista'''

def teste(lista):
    x = len(lista)-1
    k = []


    
    while(x >= 1):
        if(k == [] or 1*(abs(lista[x].x - iniX) + abs(lista[x].y - iniY)) < 1*(abs(k[len(k)-1].x - iniX) + abs(k[len(k)-1].y - iniY))):
            
            k.append(lista[x])
        x -= 1


    print(len(k))
    #for i in k:
    #    imprimir(i)
    k = [num for num in reversed(k)]
    
    
    return k


'''
zerar()
iniX = 7
iniY = 7
desX = 0
desY = 0
caminho[iniX][iniY] = 1
caminho[desX][desY] = 3
caminho[6][1] = -1
caminho[5][1] = -1
caminho[7][1] = -1
caminho[0][1] = -1

caminho[3][1] = -1
caminho[2][1] = -1
caminho[1][1] = -1



e = Estado(iniX,iniY,caminho)
imprimir(e)




if(winCasoBase(e) == -1): 
    while(e != -1):
        e = criarNo(e.x,e.y,e.caminho)
else:
    listaFechada.append(e)

print(len(listaFechada))
listaFechada = teste(listaFechada)


t = len(listaFechada)-1
while(t >= 0):
    if(winFechada(listaFechada[t]) != -1):
        break
    t -= 1
    
while(t >= 0):
    listaFechada.pop(0)
    t -= 1


    
for i in listaFechada:
    imprimir(i)


exit(0)


'''




pygame.init()
pygame.display.set_caption('Game IA')
janela = pygame.display.set_mode((800,800))


class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('1.png'))
        self.sprites.append(pygame.image.load('2.png'))
        self.sprites.append(pygame.image.load('3.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = 100,100

        for i in range(len(self.sprites)):
            self.image = self.sprites[i]
            self.image = pygame.transform.rotate(self.image,200)
            
    def update(self):
        self.atual = self.atual + 0.005
        if self.atual >= len(self.sprites):
            self.atual = 0
        
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(32*3,32*3))
        self.image = pygame.transform.rotate(self.image,self.angle)
        
    
    def angulo(self,angle):
        self.angle = angle

        
    def angulo(self,angle):
        self.angle = angle

    def cima(self):
        self.rect.move_ip(0,-100)

    def baixo(self):
        self.rect.move_ip(0,100)

    def esquerda(self):
        self.rect.move_ip(-100,0)

    def direita(self):
        self.rect.move_ip(100,0)


class Fantasma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('f1.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = 100,100

        for i in range(len(self.sprites)):
            self.image = self.sprites[i]
            self.image = pygame.transform.rotate(self.image,200)
            
    def update(self):
        self.atual = self.atual + 0.005
        if self.atual >= len(self.sprites):
            self.atual = 0
        
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(32*3,32*3))
        self.image = pygame.transform.rotate(self.image,self.angle)
        
    
    def angulo(self,angle):
        self.angle = angle


class Comida(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('c1.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.angle = 0
        self.rect = self.image.get_rect()

        for i in range(len(self.sprites)):
            self.image = self.sprites[i]
            self.image = pygame.transform.rotate(self.image,200)
            
    def update(self):
        self.atual = self.atual + 0.005
        if self.atual >= len(self.sprites):
            self.atual = 0
        
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(32*3,32*3))
        self.image = pygame.transform.rotate(self.image,self.angle)
        
        

todas_as_sprites = pygame.sprite.Group()
fantasma = []
comida = []
pacMan = PacMan()
pacMan.rect.x = 0
pacMan.rect.y = 600
todas_as_sprites.add(pacMan)
fim = time.time()
ini = time.time()

zerar()
caminho[desX][desY] = 0
while True:
    #janela.fill(pygame.color(255,255,255))
    fim = time.time()
    if(fim-ini  > 0.5 and len(listaFechada) > 0):
        if(pacMan.rect.x < listaFechada[0].y*100):
            pacMan.angle = 0
        if(pacMan.rect.x > listaFechada[0].y*100):
            pacMan.angle = 180
        if(pacMan.rect.y > listaFechada[0].x*100):
            pacMan.angle = -90
        if(pacMan.rect.y > listaFechada[0].x*100):
            pacMan.angle = 90

            
        
        ini = time.time()
        pacMan.rect.x = listaFechada[0].y*100
        pacMan.rect.y =  listaFechada[0].x*100
        p = []
        p.append(pacMan.rect.x)
        p.append(pacMan.rect.y)

        
        for i in comida:
            if(i.rect.collidepoint(p)):
                if(isinstance(i, Comida)):
                    todas_as_sprites.remove(i)
                    caminho[listaFechada[0].x][listaFechada[0].y] = 0
                    
        #print(caminho)
        listaFechada.pop(0)
        if(len(listaFechada) == 0):
            
            zerar()
            xTemp = iniY = int(pacMan.rect.x/100)
            yTemp = iniX = int(pacMan.rect.y/100)
            desX = int(xTemp)
            desY = int(yTemp)
            caminho[iniX][iniY] = 1
            if(caminho[desX][desY] != -1):
                caminho[iniX][iniY] = 2
                e = -1
                for x in range(len(caminho)):
                    for y in range(len(caminho)):
                        if(caminho[x][y] == 3):
                            desX = x
                            desY = y
                            e = 1
                            break

                    
                    #print(int(pos[0]/100))
                    #print(int(pos[1]/100))
                    

                    #print(pos)
                if(e != -1):
                    
                    #print(int(pos[0]/100))
                    #print(int(pos[1]/100))
                    

                    #print(pos)
                    e = Estado(iniX,iniY,caminho)
                    
                    t = winCasoBase(e)
                    if(t == -1): 
                        while(e != -1):
                            e = criarNo(e.x,e.y,e.caminho)

                        t = len(listaFechada)-1
                        while(t >= 0):
                            if(winFechada(listaFechada[t]) != -1):
                                break
                            t -= 1

                        while(t >= 0):
                            listaFechada.pop(0)

                            t -= 1
                        
                    else:
                        listaFechada.append(t)

                    listaFechada = teste(listaFechada)
                    


                    ini = time.time()
                    caminho[desX][desY] = 0
                    
                    #print("============")
                    #for i in listaFechada:
                    #    imprimir(i)
                    #imprimir(listaFechada[len(listaFechada)-1])
                    #print("MAT")
                    #for i in listaFechada:
                        #print(i.x)
                        #print(i.y)
                        #pacMan.rect.x = i.x*100
                        #pacMan.rect.y = i.y*100
                        #print("")
    
    for event in pygame.event.get():
        teclado = pygame.key.get_pressed()
        if(teclado[pygame.K_LEFT]):
            if(pacMan.rect.x > 0):
                if(caminho[int(pacMan.rect.y/100)][int(pacMan.rect.x/100)-1] != -1):
                    pacMan.esquerda()
                    p = []
                    p.append(pacMan.rect.x)
                    p.append(pacMan.rect.y)
                    pacMan.angulo(180)
                    for i in comida:
                        if(i.rect.collidepoint(p)):
                            if(isinstance(i, Comida)):
                                todas_as_sprites.remove(i)
                                caminho[int(p[1]/100)][int(p[0]/100)] = 0
        if(teclado[pygame.K_RIGHT]):
            if(pacMan.rect.x < 700):
                if(caminho[int(pacMan.rect.y/100)][int(pacMan.rect.x/100)+1] != -1):
                    pacMan.direita()
                    p = []
                    p.append(pacMan.rect.x)
                    p.append(pacMan.rect.y)
                    pacMan.angulo(0)
                    for i in comida:
                        if(i.rect.collidepoint(p)):
                            if(isinstance(i, Comida)):
                                todas_as_sprites.remove(i)
                                caminho[int(p[1]/100)][int(p[0]/100)] = 0
        if(teclado[pygame.K_UP]):
            if(pacMan.rect.y > 0):
                if(caminho[int(pacMan.rect.y/100)-1][int(pacMan.rect.x/100)] != -1):
                    pacMan.cima()
                    p = []
                    p.append(pacMan.rect.x)
                    p.append(pacMan.rect.y)
                    pacMan.angulo(90)
                    for i in comida:
                        if(i.rect.collidepoint(p)):
                            if(isinstance(i, Comida)):
                                todas_as_sprites.remove(i)
                                caminho[int(p[1]/100)][int(p[0]/100)] = 0
        if(teclado[pygame.K_DOWN]):
            if(pacMan.rect.y < 700):
                if(caminho[int(pacMan.rect.y/100)+1][int(pacMan.rect.x/100)] != -1):
                    pacMan.baixo()
                    p = []
                    p.append(pacMan.rect.x)
                    p.append(pacMan.rect.y)
                    pacMan.angulo(-90)
                    for i in comida:
                        if(i.rect.collidepoint(p)):
                            if(isinstance(i, Comida)):
                                todas_as_sprites.remove(i)
                                caminho[int(p[1]/100)][int(p[0]/100)] = 0

        
        
        
        if event.type == QUIT:
            pygame.quit()
            exit()
            
        if(teclado[pygame.K_F5]):
            zerar()
            xTemp = iniY = int(pacMan.rect.x/100)
            yTemp = iniX = int(pacMan.rect.y/100)
            desX = int(xTemp)
            desY = int(yTemp)
            caminho[desY][desX] = 1
            e = -1
            for x in range(len(caminho)):
                for y in range(len(caminho)):
                    if(caminho[x][y] == 3):
                        desX = x
                        desY = y
                        e = 1
                        break
                #print(int(pos[0]/100))
                #print(int(pos[1]/100))
                

                #print(pos)
            e = Estado(iniX,iniY,caminho)
                    
            t = winCasoBase(e)
            if(t == -1): 
                while(e != -1):
                    e = criarNo(e.x,e.y,e.caminho)

                t = len(listaFechada)-1
                while(t >= 0):
                    if(winFechada(listaFechada[t]) != -1):
                        break
                    t -= 1

                while(t >= 1):
                    listaFechada.pop(0)
                    print("s")
                    t -= 1
                        
            else:
                listaFechada.append(t)

            listaFechada = teste(listaFechada)
                    


            ini = time.time()
            caminho[desX][desY] = 0
                
                #print("============")
                #for i in listaFechada:
                #    imprimir(i)
                #imprimir(listaFechada[len(listaFechada)-1])
                #print("MAT")
                #for i in listaFechada:
                    #print(i.x)
                    #print(i.y)
                    #pacMan.rect.x = i.x*100
                    #pacMan.rect.y = i.y*100
                    #print("")

   
        if(pygame.mouse.get_pressed()[0] == True):
            time.sleep(0.05)
            pos = pygame.mouse.get_pos()
            xTemp = int(pos[1]/100)
            yTemp = int(pos[0]/100)
            p = []
            p.append(yTemp*100)
            p.append(xTemp*100)
            if(caminho[xTemp][yTemp] == 0):
                fantasma.append(Fantasma())
                fantasma[len(fantasma)-1].rect.y = xTemp*100
                fantasma[len(fantasma)-1].rect.x = yTemp*100
                todas_as_sprites.add(fantasma[len(fantasma)-1])
                caminho[xTemp][yTemp] = -1
                #print(caminho)
                time.sleep(0.05)
            else:
                for i in fantasma:
                    if(i.rect.collidepoint(p)):
                        if(isinstance(i, Fantasma)):
                            todas_as_sprites.remove(i)
                            caminho[xTemp][yTemp] = 0
                            time.sleep(0.05)
                            

        if(pygame.mouse.get_pressed()[2] == True):
            time.sleep(0.05)
            pos = pygame.mouse.get_pos()
            xTemp = int(pos[1]/100)
            yTemp = int(pos[0]/100)
            p = []
            p.append(yTemp*100)
            p.append(xTemp*100)
            if(caminho[xTemp][yTemp] == 0):
                caminho[xTemp][yTemp] = 3
                comida.append(Comida())
                comida[len(comida)-1].rect.y = xTemp*100
                comida[len(comida)-1].rect.x = yTemp*100
                todas_as_sprites.add(comida[len(comida)-1])
                time.sleep(0.05)
            else:
                for i in comida:
                    if(i.rect.collidepoint(p)):
                        if(isinstance(i, Comida)):
                            todas_as_sprites.remove(i)
                            caminho[xTemp][yTemp] = 0
                            time.sleep(0.05)
                            
 


            
        #if event.type == pygame.KEYDOWN:
          #if event.key == K_LEFT:
              #iniX = pacMan.rect.x
              #iniY = pacMan.rect.y
              #print(pacMan.rect.x)
              #print(pacMan.rect.y)
              #print("")
    
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 700), (800, 700), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 600), (800, 600), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 500), (800, 500), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 400), (800, 400), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 300), (800, 300), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 200), (800, 200), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (0, 100), (800, 100), 1)

  


    pygame.draw.line(janela, pygame.Color(255,255,255), (100, 0), (100, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (200, 0), (200, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (300, 0), (300, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (400, 0), (400, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (500, 0), (500, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (600, 0), (600, 800), 1)
    pygame.draw.line(janela, pygame.Color(255,255,255), (700, 0), (700, 800), 1)
    
    
    todas_as_sprites.draw(janela)
    todas_as_sprites.update()
    
    pygame.display.update()
    janela.fill((0,0,0))


    
    
    import math
from copy import deepcopy

listaAberta = []
listaFechada = []
caminho = []
tamanho = 8
iniX = 7
iniY = 0
desX = 0
desY = 7

for x in range(tamanho):
    linha = [] 
    for y in range(tamanho):
        linha.append(0)
        linha[y] = 0
        if(iniX == x and iniY == y):
            linha[y] = 1
        elif(desX == x and desY == y):
            linha[y] = 3
    caminho.append(linha)

caminho[0][6] = -1
caminho[1][6] = -1
caminho[2][6] = -1
caminho[3][6] = -1

class Estado():
    parente = []
    def __init__(self, x, y, caminho):
        self.x = x
        self.y = y
        self.g = math.inf
        self.h = math.inf
        self.f = math.inf
        self.caminho = caminho[:]
        if(self.caminho[x][y] != 1):
            self.caminho[x][y] = 2
            
def criaEstado(iniX,iniY,v):
    e = -1
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 0):#Baixo
        #print("Baixo")
        e =  Estado(iniX+1,iniY,v)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 0):#Cima
        #print("Cima")
        e =  Estado(iniX-1,iniY,v)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 0):#Direita
        #print("Direita")
        e = Estado(iniX,iniY+1,v)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 0):#Esquerda
        #print("Esquerda")
        e = Estado(iniX,iniY-1,v)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 0):#135
        #print("135")
        e = Estado(iniX+1,iniY+1,v)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 0):#225
        #print("225")
        e = Estado(iniX+1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 0):#315
        #print("315")
        e = Estado(iniX-1,iniY-1,v)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 0):#45
        #print("45")
        e = Estado(iniX-1,iniY+1,v)
    if(e != -1):
        return e
    else:
        return -1

def criarNo(q):
    iniX = q.x
    iniY = q.y
    v = q.caminho
    e = []
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 0):#Baixo
        #print("Baixo")
        e.append(Estado(iniX+1,iniY,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 0):#Cima
        #print("Cima")
        e.append(Estado(iniX-1,iniY,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 0):#Direita
        #print("Direita")
        e.append(Estado(iniX,iniY+1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 0):#Esquerda
        #print("Esquerda")
        e.append(Estado(iniX,iniY-1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 0):#135
        #print("135")
        e.append(Estado(iniX+1,iniY+1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 0):#225
        #print("225")
        e.append(Estado(iniX+1,iniY-1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 0):#315
        #print("315")
        e.append(Estado(iniX-1,iniY-1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 0):#45
        #print("45")
        e.append(Estado(iniX-1,iniY+1,deepcopy(v)))
        e[len(e)-1].parente = q
    if(e != []):
        return e
    else:
        return -1


def win(e):
    if(e == -1):
        return -1
    iniX = e.x
    iniY = e.y
    v = e.caminho
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and v[iniX+1][iniY] == 3):#Baixo
        #print("Baixo")
        return e
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and v[iniX-1][iniY] == 3):#Cima
        #print("Cima")
        return e
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and v[iniX][iniY+1] == 3):#Direita
        #print("Direita")
        return e
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and v[iniX][iniY-1] == 3):#Esquerda
        #print("Esquerda")
        return e
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and v[iniX+1][iniY+1] == 3):#135
        #print("135")
        return e
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and v[iniX+1][iniY-1] == 3):#225
        #print("225")
        return e
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and v[iniX-1][iniY-1] == 3):#315
        #print("315")
        return e
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and v[iniX-1][iniY+1] == 3):#45
        #print("45")
        return e
    else:
        return -1
    
def inserir(lista, aux):
    j = 0
    while(len(lista) > 0 and j < len(lista) and aux.f > lista[j].f):
        j += 1
    lista.insert(j,aux)

    return lista

def imprimir(caminho):
    caminho = caminho.caminho
    for x in range(len(caminho)):
        for y in range(len(caminho)):
            print(caminho[x][y], end="")
            print("|", end="")
        print()
    print()

e = criaEstado(iniX,iniY,caminho)
e.f = 0
e.g = 0
e.h = 0
listaAberta.append(e)

def custo(x,y,desX,desY):
    return math.sqrt(pow((x - desX), 2.0)+pow((y - desY), 2.0));

def busca():
    global listaAberta
    while(len(listaAberta) > 0):
        q = -1
        i = 0
        pai = listaAberta[0]
        listaFechada.append(pai)
        if(win(pai) != -1):
            return pai
        filho = criarNo(pai)
        listaAberta.pop(0)
        for i in filho:
            i.g = gNew = pai.g + 1.0
            i.h = hNew = custo(i.x,i.y,desX,desY)
            i.f = fNew = gNew+hNew
            existe = -1
            for x in listaAberta:
                if(x.parente == pai.parente):
                    existe = 1
                    break
            if(existe == -1):
                listaAberta = inserir(listaAberta,i)
                
busca()
