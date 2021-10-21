class No:
     def __init__(self, key, dir, esq):
          self.item = key
          self.dir = dir
          self.esq = esq
r = []
class Tree:
     global r
     def __init__(self):
          self.root = No(None,None,None)
          self.root = None

     def inOrder(self, atual):
         if atual != None:
              self.inOrder(atual.esq)
              r.append(atual.item)
              print(atual.item,end=" ")
              self.inOrder(atual.dir)
  
     def preOrder(self, atual):
         if atual != None:
              print(atual.item,end=" ")
              self.preOrder(atual.esq)
              self.preOrder(atual.dir)
       
     def posOrder(self, atual):
         if atual != None:
              self.posOrder(atual.esq)
              self.posOrder(atual.dir)
              print(atual.item,end=" ")

     def inserir(self, v):
          novo = No(v,None,None) # cria um novo Nó
          if self.root == None:
               self.root = novo
          else: # se nao for a raiz
               atual = self.root
               while True:
                    anterior = atual
                    if v <= atual.item: # ir para esquerda
                         atual = atual.esq
                         if atual == None:
                                anterior.esq = novo
                                return
                    # fim da condição ir a esquerda
                    else: # ir para direita
                         atual = atual.dir
                         if atual == None:
                                 anterior.dir = novo
                                 return
                    # fim da condição ir a direita
        

while True:
    try:
        n = input()
        arvore = n.split(" ")
        p = arvore[1].find(arvore[0][0])
        s = ""
        s+= arvore[1][p]
        for i in range(1,len(arvore[0])):
            s+= arvore[0][i]
        print(s)
        '''pos = s[len(s)-1]
        p = 1
        while True:
            if(arvore[0][p+1] == pos):
                break
            s+= arvore[0][p]
            p += 1
        '''
        arv = Tree()
        i = 0
        while(i < len(arvore[1])):
            arv.inserir(arvore[1][i])
            i += 1
        arv.inOrder(arv.root)

        while(len(r) >= 0):
            print(r[0])
            r.pop(0)
            print(r[1])
            r.pop(1)
        
        break
    except:
        break
       
    

