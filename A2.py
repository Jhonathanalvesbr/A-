import math
from copy import deepcopy
import pygame
from pygame.locals import *
from sys import exit
import time

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
        self.image = pygame.transform.scale(self.image,(int(ratio/25)*3,int(ratio/25)*3))
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
        self.image = pygame.transform.scale(self.image,(int(ratio/25)*3,int(ratio/25)*3))
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
        self.image = pygame.transform.scale(self.image,(int(ratio/25)*3,int(ratio/25)*3))
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

ratio = 800

listaAberta = []
listaFechada = []
caminho = []
tamanho = int(ratio/100)
iniX = 0
iniY = 0
desX = 0
desY = 0
pygame.init()
pygame.display.set_caption('Game IA')
janela = pygame.display.set_mode((800,800))

for x in range(tamanho):
    linha = []
    for y in range(tamanho):
        linha.append(0)
    caminho.append(linha)


class Estado():
    parente = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = math.inf
        self.h = math.inf
        self.f = math.inf
            
def criaEstado(iniX,iniY):
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and caminho[iniX+1][iniY] == 0):#Baixo
        #print("Baixo")
        return Estado(iniX+1,iniY)
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and caminho[iniX-1][iniY] == 0):#Cima
        #print("Cima")
        return Estado(iniX-1,iniY)
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and caminho[iniX][iniY+1] == 0):#Direita
        #print("Direita")
        returnEstado(iniX,iniY+1)
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and caminho[iniX][iniY-1] == 0):#Esquerda
        #print("Esquerda")
        returnEstado(iniX,iniY-1)
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and caminho[iniX+1][iniY+1] == 0):#135
        #print("135")
        returnEstado(iniX+1,iniY+1)
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and caminho[iniX+1][iniY-1] == 0):#225
        #print("225")
        returnEstado(iniX+1,iniY-1)
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and caminho[iniX-1][iniY-1] == 0):#315
        #print("315")
        returnEstado(iniX-1,iniY-1)
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and caminho[iniX-1][iniY+1] == 0):#45
        #print("45")
        returnEstado(iniX-1,iniY+1)
    if(e != -1):
        return e
    else:
        return -1

def criarNo(q,i):
    if(q == -1):
        return
    iniX = q.x
    iniY = q.y
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and caminho[iniX+1][iniY] == 0 and i == 0):#Baixo
        #print("Baixo")
        return (Estado(iniX+1,iniY))
        
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and caminho[iniX-1][iniY] == 0 and i == 1):#Cima
        #print("Cima")
        return (Estado(iniX-1,iniY))
        
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and caminho[iniX][iniY+1] == 0 and i == 2):#Direita
        #print("Direita")
        return (Estado(iniX,iniY+1))
        
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and caminho[iniX][iniY-1] == 0 and i == 3):#Esquerda
        #print("Esquerda")
        return (Estado(iniX,iniY-1))
        
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and caminho[iniX+1][iniY+1] == 0 and i == 4):#135
        #print("135")
        return (Estado(iniX+1,iniY+1))
        
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and caminho[iniX+1][iniY-1] == 0 and i == 5):#225
        #print("225")
        return (Estado(iniX+1,iniY-1))
        
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and caminho[iniX-1][iniY-1] == 0 and i == 6):#315
        #print("315")
        return (Estado(iniX-1,iniY-1))
        
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and caminho[iniX-1][iniY+1] == 0 and i == 7):#45
        #print("45")
        return (Estado(iniX-1,iniY+1))

def win(e):
    if(e == -1):
        return -1
    iniX = e.x
    iniY = e.y
    if(iniX+1 >= 0 and iniY >= 0 and iniX+1 < tamanho and iniY < tamanho and caminho[iniX+1][iniY] == 3):#Baixo
        #print("Baixo")
        return (Estado(iniX+1,iniY))
        
    elif(iniX-1 >= 0 and iniY >= 0 and iniX-1 < tamanho and iniY < tamanho and caminho[iniX-1][iniY] == 3):#Cima
        #print("Cima")
        return (Estado(iniX-1,iniY))
        
    elif(iniX >= 0 and iniY+1 >= 0 and iniX < tamanho and iniY+1 < tamanho and caminho[iniX][iniY+1] == 3):#Direita
        #print("Direita")
        return (Estado(iniX,iniY+1))
        
    elif(iniX >= 0 and iniY-1 >= 0 and iniX < tamanho and iniY-1 < tamanho and caminho[iniX][iniY-1] == 3):#Esquerda
        #print("Esquerda")
        return (Estado(iniX,iniY-1))
        
    elif(iniX+1 >= 0 and iniY+1 >= 0 and iniX+1 < tamanho and iniY+1 < tamanho and caminho[iniX+1][iniY+1] == 3):#135
        #print("135")
        return (Estado(iniX+1,iniY+1))
        
    elif(iniX+1 >= 0 and iniY-1 >= 0 and iniX+1 < tamanho and iniY-1 < tamanho and caminho[iniX+1][iniY-1] == 3):#225
        #print("225")
        return (Estado(iniX+1,iniY-1))
        
    elif(iniX-1 >= 0 and iniY-1 >= 0 and iniX-1 < tamanho and iniY-1 < tamanho and caminho[iniX-1][iniY-1] == 3):#315
        #print("315")
        return (Estado(iniX-1,iniY-1))
        
    elif(iniX-1 >= 0 and iniY+1 >= 0 and iniX-1 < tamanho and iniY+1 < tamanho and caminho[iniX-1][iniY+1] == 3):#45
        #print("45")
        return (Estado(iniX-1,iniY+1))
    return -1
    
def inserir(lista, aux):
    j = 0
    while(len(lista) > 0 and j < len(lista) and aux.f >= lista[j].f):
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

def custo(x,y,desX,desY):
    return math.sqrt(pow((x - desX), 2.0)+pow((y - desY), 2.0))

def existe(lista,filho):
    if(len(lista) == 0):
        return -1
    for i in lista:
        if(i.x == filho.x and i.y == filho.y):
            return 1
    return -1

def get_f(filho):
      return filho.f

def busca():
    global listaAberta
    global listaFechada
    while(len(listaAberta) > 0):
        pai = listaAberta[0]
        listaFechada.append(pai)
        listaAberta.pop(0)
        w = win(pai)
        if(w != -1):
            print("Win")
            w.parente = pai
            return w
        for i in range(8):
            filho = criarNo(pai,i)
            if(filho != None and existe(listaAberta,filho) != 1 and existe(listaFechada, filho) != 1):
                filho.g = pai.g + 1.0
                filho.h = custo(filho.x,filho.y,desX,desY)
                filho.f = filho.g+filho.h
                filho.parente = pai
                inserir(listaAberta,filho)


def imprimirCaminho(e):
    a = e.parente
    while(a.parente != []):
        for x in range(tamanho):
            for y in range(tamanho):
                if(a.x == x and a.y == y):
                    print("2", end="")
                else:
                    print("0", end="")
            print()
        print()
        a = a.parente

def getCaminho(e):
    a = e.parente
    lista = []
    lista.append([e.y,e.x])
    while(a.parente != []):
        lista.append([a.y,a.x])
        a = a.parente
    return list(reversed(lista))


def caminhoVazio():
    for x in range(len(caminho)):
        for y in range(len(caminho)):
            if(caminho[x][y] == 3):
                return 1
    return -1

movimento = []
while True:
    #janela.fill(pygame.color(255,255,255))
    fim = time.time()
    if(fim-ini  > 0.5 and len(movimento) > 0 and caminhoVazio() == 1):
        if(pacMan.rect.x < movimento[0][0]*100):
            pacMan.angle = 0
        if(pacMan.rect.x > movimento[0][0]*100):
            pacMan.angle = 180
        if(pacMan.rect.y > movimento[0][1]*100):
            pacMan.angle = -90
        if(pacMan.rect.y > movimento[0][1]*100):
            pacMan.angle = 90
        
        ini = time.time()
        pacMan.rect.x = movimento[0][0]*100
        pacMan.rect.y =  movimento[0][1]*100
        p = []
        p.append(pacMan.rect.x)
        p.append(pacMan.rect.y)
        
        
        for i in comida:
            if(i.rect.collidepoint(p)):
                if(isinstance(i, Comida)):
                    todas_as_sprites.remove(i)
                    caminho[movimento[0][0]][movimento[0][1]] = 0
                    
        movimento.pop(0)
        if(len(movimento) == 0 and caminhoVazio() == 1):
            print(caminho)
            xTemp = iniY = int(pacMan.rect.x/100)
            yTemp = iniX = int(pacMan.rect.y/100)
            desX = int(xTemp)
            desY = int(yTemp)
            caminho[iniX][iniY] = 1
            if(caminhoVazio() == 1):
                listaAberta = []
                listaFechada = []
                e = Estado(iniX,iniY)
                listaAberta.append(e)
                e = busca()
                movimento = getCaminho(e)
                caminho[yTemp][xTemp] = 0
                    
    
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
            
        if(teclado[pygame.K_F5] and caminhoVazio() == 1):
            time.sleep(0.1)
            xTemp = iniY = int(pacMan.rect.x/100)
            yTemp = iniX = int(pacMan.rect.y/100)
            desX = int(xTemp)
            desY = int(yTemp)
            caminho[desY][desX] = 1
            for x in range(len(caminho)):
                for y in range(len(caminho)):
                    if(caminho[x][y] == 3):
                        desX = x
                        desY = y
                        break
                #print(int(pos[0]/100))
                #print(int(pos[1]/100))
                

                #print(pos)
            listaAberta = []
            listaFechada = []
            e = Estado(iniX,iniY)
            listaAberta.append(e)
            e = busca()
            movimento = getCaminho(e)
            caminho[yTemp][xTemp] = 0

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
                while(caminho[xTemp][yTemp] == 0):
                    caminho[xTemp][yTemp] = -1
                fantasma.append(Fantasma())
                fantasma[len(fantasma)-1].rect.y = xTemp*100
                fantasma[len(fantasma)-1].rect.x = yTemp*100
                todas_as_sprites.add(fantasma[len(fantasma)-1])
                
                #print(caminho)
                time.sleep(0.05)
            else:
                for i in fantasma:
                    if(i.rect.collidepoint(p)):
                        if(isinstance(i, Fantasma)):
                            todas_as_sprites.remove(i)
                            while(caminho[xTemp][yTemp] == -1):
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
                while(caminho[xTemp][yTemp] == 0):
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
                            while(caminho[xTemp][yTemp] == 3):
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
