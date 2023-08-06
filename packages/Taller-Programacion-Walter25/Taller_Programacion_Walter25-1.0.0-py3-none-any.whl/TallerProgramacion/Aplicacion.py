#Taller de programacion
#Crear un paquete en el cual usemos una aplicacion de numpy y subirlo a Pypi.org
#Jorge Sanchez 2204659 - Carlos Cala 2204549
import numpy as np


def ProductoEscalar(lista1,lista2):
    vector1,vector2= np.array(lista1),np.array(lista2)
    vectorf = np.empty((vector1.size,1))

    for i in range(vector1.size):
        vectorf[i] = vector1[i] * vector2[i]

    return vectorf.sum()

def VectoresOrtogonales(lista1,lista2):
    vector1,vector2= np.array(lista1),np.array(lista2)
    vectorf = np.empty((vector1.size,1))

    for i in range(vector1.size):
        vectorf[i] = vector1[i] * vector2[i]

    if vectorf.sum() == 0.0:
        print("Los vectores son ortogonales")
    else:
        print("Los vectores no son ortogonales")

def MagnitudVectorial(lista):
    vector = np.array(lista)
    vectorf = np.empty((vector.size,1))
    for i in range(vector.size):
        vectorf[i] = vector[i]**2
    return np.sqrt(vectorf.sum())

def VectoresParalelos(lista1,lista2):
    vector1,vector2= np.array(lista1),np.array(lista2)
    vectorf = np.empty((vector1.size,1))
    for i in range(vector1.size):
        try:
            with np.errstate(divide='ignore'):
                vectorf[i] = vector1[i]/vector2[i]
        except:
            vectorf[i] = 0

    for i in range(vectorf.size-1):
        if vectorf[i] == vectorf[i+1]:
            pass
        else: 
            print("No son paralelos")
            return
    print("Son paralelos")

def LinealmenteIndependiente(lista1,lista2,lista3):
    matrix = np.array((lista1,lista2,lista3))
    if np.linalg.det(matrix) == 0:
        print("Los vectores son  linealmente dependientes")
    else: print("Los vectores son linealmente independientes")

def funciones():
    print("""
La primera funcion es ProductoEscalar(), que permite obtener el escalar
de dos vectores de n componentes. (Ambos vectores deben tener el mismo numero de
componentes)

La segunda funcion es VectoresOrtogonales(), que permite saber si dos vectores
de n componentes son ortogonales.

La tercera funcion es MagnitudVectorial(), que permite conocer la magnitud de un 
vector de n componentes

La cuarta funcion es VectoresParalelos(), que permite saber si dos vectores 
de n componentes son paralelos.

La quinta funcion es LinealmenteIndependiente(), que permite saber si 3 vectores
de 3 componentes son Linealmente independientes.
    """)

def informacion():
    print("""
Este paquete tiene diferentes utilidades, en las cuales en
todas se hace uso de la libreria numpy, enfocandonos en 
las matrices y sus diversas aplicaciones, si deseas conocer
todas las funciones, usa la funcion : funciones()
""")