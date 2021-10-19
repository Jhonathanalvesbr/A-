import random                                           #O(1)
import math                                             #O(1)

arr = ['Jhonathan Alves', 'Jhonathan Jhonathan', 'Jhonathan Carvalho',
       'cARVALHO ALVES', "Alves", "Carvalho", "Jhonathan",
       "Alves Jhonathan", "Carvalho Alves", "JAC"]      #O(1)

def caixaBaixa(arr):                                    #Caixa Baixa String
    for i in range(0,len(arr)):                         #O(n)
        arr[i] = arr[i].lower()                         #O(f(k))
    return arr                                          #       O( sum(f(k)) )

def desornenar(arr):                                    #Desordenar String
    count = 0                                           #O(1)
    for x in range(0, len(arr)):                        #   O(n)
        for y in range(0, len(arr)+1):                  #   O(n+1)
            for z in range(0, len(arr)):                #   O(n)
                r = math.floor(random.uniform(x,y));    #O(1)
                if(r <= y or r <= x or r <= y):         #   O( n*(n+1)*n )
                    count += 1                          #O(1)
                    aux = arr[z]                        #O(1)
                    arr[z] = arr[r]                     #O(1)
                    arr[r] = aux                        #O(1)
    print("Trocas desordenar: " + str(count))           #O(1)
    return arr                                          #       O( (n^2)*(n+1) )

def insertionSort(arr):                                 #Ordenar String - Insertion Sort
    count = 0                                           #O(1)
    arr = caixaBaixa(arr)                               #O( sum(f(k)) )
    arr = desornenar(arr)                               #   O( (n^2)*(n+1) )
    for i in range(1, len(arr)):                        #   O(n)
        key = arr[i]                                    #O(1)
        j = i-1                                         #O(1)
        while j >=0 and key < arr[j]:                   #O(n)   O(n*n)
                arr[j+1] = arr[j]                       #O(1)
                j -= 1                                  #O(1)
                count += 1                              #O(1)
        arr[j+1] = key                                  #O(1)
    print("Trocas Insertion Sort: " + str(count))       #O(1)
    return arr                                          #       O( (n^2)*(n+1) )

n = len(arr)                                            #O(1)
r = (n**2)*(n+1)                                        #O(1)
print("Ordenado: " + str(insertionSort(arr)))           #O(1)
print("Calculo de Trocas: " + str(r))                   #O(1)
