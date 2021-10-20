import random                                           #O(1)
import math                                             #O(1)
import time
import os
import csv

def criaNumeros(qnt):                                   #O(1)
    vet = []                                            #O(1)
    for k in range(1,qnt+1):                            #   O(n)
        vet.append(k)                                   #O(1)
    return vet                                          #       O(n)

def criaNumerosAleatorios(qnt):                         #O(1)
    vet = []                                            #O(1)
    for k in range(qnt):                                #   O(n)
        vet.append(str(random.randint(0, qnt)))         #O(1)
    return vet                                          #       O(n)

def criaPalavras(qnt):                                     
    vet = []                                            
    for k in range(qnt):                                
        palavra = ""
        for i in range(random.randint(5,10)):
            palavra = palavra + chr(random.randint(65,90))
        vet.append(palavra)
    return vet

def criaFrases(qnt):                                     
    vet = []
    lista = ["A", "C", "G", "T"]
    for p in range(qnt):
        frase = ""
        for k in range(random.randint(1000,2000)):                                
            frase += random.choice(lista)
        vet.append(frase)
    return vet    

def desornenar(arr):                                    #Desordenar String
    #count = 0                                           #O(1)
    for x in range(0, len(arr)):                        #   O(n)
        for y in range(0, len(arr)+1):                  #   O(n+1)
            for z in range(0, len(arr)):                #   O(n)
                r = int(random.uniform(x,y));           #O(1)
                if(r <= x or r <= y):                   #   O( n*(n+1)*n )
                    #count += 1                          #O(1)
                    aux = arr[z]                        #O(1)
                    arr[z] = arr[r]                     #O(1)
                    arr[r] = aux                        #O(1)
    #print("Trocas desordenar: " + str(count))           #O(1)
    return ""                                           #        O( (n^2)*(n+1) )
    return arr                                          #       O( (n^2)*(n+1) )

def insertionSort(arr):                                 #Ordenar String - Insertion Sort
    #count = 0                                           #O(1)
    arr = desornenar(arr)                               #   O( (n^2)*(n+1) )
    for i in range(1, len(arr)):                        #   O(n)
        key = arr[i]                                    #O(1)
        j = i-1                                         #O(1)
        while j >=0 and key < arr[j]:                   #O(n)   O(n*n)
                arr[j+1] = arr[j]                       #O(1)
                j -= 1                                  #O(1)
                #count += 1                              #O(1)
        arr[j+1] = key                                  #O(1)
    #print("Trocas Insertion Sort: " + str(count))       #O(1)
    return arr                                          #       O( (n^2)*(n+1) )

cmp = criaNumeros(500)                                  #O(1)


arr = [10,20,40,80,160,320]                                  #O(n)
#print(i)                                            #O(1)
        n = len(arr)                                        #O(1)
        r = (n**2)*(n+1)                                    #O(1)
        a = time.time()                                     #O(1)
        insertionSort(arr)
        #print("Ordenado!" + str(insertionSort(arr)))       #O( (n^2)*(n+1) )
        b = time.time()                                     #O(1)
        #print("Calculo de comparações: " + str(r))          #O(1)
        #print("Time: "+str(b-a))                            #O(1)
        #print("")                                           #O(1)
        arq.writerow([i,r,(b-a)])


'''
with open('Numeros.csv', 'w', encoding='UTF-8', newline='') as arquivo:
    arq = csv.writer(arquivo)
    arq.writerow(["N", "Comparações", "Tempo"])
    for i in cmp:                                           #O(n)
        arr = criaNumerosAleatorios(i)                                  #O(n)
        #print(i)                                            #O(1)
        n = len(arr)                                        #O(1)
        r = (n**2)*(n+1)                                    #O(1)
        a = time.time()                                     #O(1)
        insertionSort(arr)
        #print("Ordenado!" + str(insertionSort(arr)))       #O( (n^2)*(n+1) )
        b = time.time()                                     #O(1)
        #print("Calculo de comparações: " + str(r))          #O(1)
        #print("Time: "+str(b-a))                            #O(1)
        #print("")                                           #O(1)
        arq.writerow([i,r,(b-a)])
arquivo.close()
print("Numeros")
with open('Palavras.csv', 'w', encoding='UTF-8', newline='') as arquivo:
    arq = csv.writer(arquivo)
    arq.writerow(["N", "Comparações", "Tempo"])
    for i in cmp:                                           #O(n)
        arr = criaPalavras(i)                               #O(n)
        #print(i)                                            #O(1)
        n = len(arr)                                        #O(1)
        r = (n**2)*(n+1)                                    #O(1)
        a = time.time()                                     #O(1)
        insertionSort(arr)
        #print("Ordenado!" + str(insertionSort(arr)))       #O( (n^2)*(n+1) )
        b = time.time()                                     #O(1)
        #print("Calculo de comparações: " + str(r))          #O(1)
        #print("Time: "+str(b-a))                            #O(1)
        #print("")                                           #O(1)
        arq.writerow([i,r,(b-a)])
arquivo.close()
print("Palavras")
with open('Frases.csv', 'w', encoding='UTF-8', newline='') as arquivo:
    arq = csv.writer(arquivo)
    arq.writerow(["N", "Comparações", "Tempo"])
    for i in cmp:                                           #O(n)
        arr = criaFrases(i)                               #O(n)
        #print(i)                                            #O(1)
        n = len(arr)                                        #O(1)
        r = (n**2)*(n+1)                                    #O(1)
        a = time.time()                                     #O(1)
        insertionSort(arr)
        #print("Ordenado!" + str(insertionSort(arr)))       #O( (n^2)*(n+1) )
        b = time.time()                                     #O(1)
        #print("Calculo de comparações: " + str(r))          #O(1)
        #print("Time: "+str(b-a))                            #O(1)
        #print("")                                           #O(1)
        
        arq.writerow([i,r,(b-a)])
arquivo.close()
print("Frases")
'''
