#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: operacion.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 06/Diciembre/2016

Este módulo contiene las funciones necesarias para realizar operaciones con y entre
matrices.
"""

#**************************************************************************************#

from metodos_numericos.error.errores import redondear
from metodos_numericos.excepcion.excepciones_metodos import DimensionNoCompatibleExcepcion, NumeroCifrasRedondeoExcepcion

#**************************************************************************************#

"""
Revisa si hay elementos repetidos en una lista.

Parámetros:
lista -- Lista que será revisada.

Valor devuelto: Verdadero si hay valores repetidos, falso de otro modo.
"""
def repeticionLista (lista):
    for i in range(0, len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True

    return False

#**************************************************************************************#

"""
Esta función encuentra el primer renglón de una matriz cuya entrada en la columna indicada
es distinta de 0.

Parámetros:
matriz -- Matriz donde se realizará la búsqueda.
indice_inicial -- Índice del renglón y de la columna donde se empieza la búsqueda.

Valor devuelto: índice encontrado o -1 en caso de que todas las entradas revisadas sean 0.
"""
def encontrarRenglonMenor (matriz, indice_inicial):
    for i in range(indice_inicial, len(matriz)):
        if matriz[i][indice_inicial] != 0:
            return i

    return -1

#**************************************************************************************#

"""
Esta función encuentra el renglón que contiene el mayor valor absoluto en la columna
indicada.

Parámetros:
matriz -- Matriz donde se realizará la búsqueda.
indice_inicial -- Índice del renglón y de la columna donde se empieza la búsqueda.

Valor devuelto: Índice donde se encontró el valor mayor.
"""
def encontrarRenglonMayor (matriz, indice_inicial):
    valor_mayor = indice_inicial

    for i in range(indice_inicial + 1, len(matriz)):
        if matriz[i][indice_inicial] > matriz[valor_mayor][indice_inicial]:
            valor_mayor = i

    return valor_mayor

#**************************************************************************************#

"""
Esta función encuentra el valor (absoluto) más grande en una lista con valores numéricos.

Parámetros:
lista -- Lista donde se buscará el valor más alto.

Valor devuelto: Valor absoluto del elemento más grande.
"""
def encontrarNumeroMayorLista (lista):
    mayor = lista[0]
    for i in range(0, len(lista)):
        if abs(lista[i]) > abs(mayor):
            mayor = lista[i]

    return abs(mayor)

#**************************************************************************************#

"""
Encuentra la entrada de mayor valor absoluto de una matriz.

Parámetros:
matriz -- Matriz que será analizada.

Valor devuelto: Valor absoluto de la entrada más grande.
"""
def encontrarNumeroMayorMatriz (matriz):
    mayor = matriz[0][0]
    for i in range(0, len(matriz)):
        for j in range(0, len(matriz[i])):
            if abs(matriz[i][j]) > abs(mayor):
                mayor = matriz[i][j]

    return abs(mayor)

#**************************************************************************************#

"""
Suma las entrada de un renglón de una matriz, saltándose la entrada en el índice
indicado.

Parámetros:
matriz -- Matriz que se utilizará.
i -- Renglón que se sumará.
indice_saltado -- Índice que no será tomado en cuenta en la sumatoria.

Valor devuelto: Sumatoria del renglón.
"""
def sumatoriaRenglon (matriz, i, indice_saltado):
    sumatoria = 0

    for j in range(0, indice_saltado):
        sumatoria = sumatoria + abs(matriz[i][j])

    for j in range(indice_saltado + 1, len(matriz[i])):
        sumatoria = sumatoria + abs(matriz[i][j])

    return sumatoria

#**************************************************************************************#

"""
Se encarga de verificar si alguna configuración de una matriz la deja diagonalmente dominante.
Se revisan todas las posibilidades. Los renglones de la matriz y el vector de términos independientes
son permutados si hace falta, pero únicamente cuando se encuentra una configuración válida.

Parámetros:
matriz -- Matriz que será revisada.
terminos_independientes -- Vector de términos independientes del SEL.

Valor devuelto: Verdadero si la matriz es diagonalmente dominante, falso en caso contrario.
"""
def verificarDominanciaDiagonal (matriz, terminos_independientes):
    #Inicializa la lista de posiciones de los renglones de la matriz original.
    posiciones = [-1 for renglon in matriz]

    """
    El siguiente bloque revisa que entrada del renglón es dominante sobre el resto.
    Una vez que lo encuentra, guarda en la lista de posiciones el lugar donde debe
    posicionarse para que quede en la diagonal.
    El proceso se repite para cada renglón.
    """
    for i in range(0, len(matriz)):
        for j in range(0, len(matriz[i])):
            if abs(matriz[i][j]) > sumatoriaRenglon(matriz, i, j):
                posiciones[i] = j

        #Si de ninguna manera se puede obtener un lugar en la diagonal que cumpla
        #con la condición de convergencia.
        if posiciones[i] == -1:
            return False

    #Si hay valores repetidos, no se puede formar una matriz diagonalmente dominante.
    if (repeticionLista(posiciones)):
        return False
    else:
        matriz_auxiliar = copiarMatriz(matriz)
        b_auxiliar = copiarMatriz(terminos_independientes)

        #Reacomoda la matriz original con todos los cambios de renglón necesarios.
        for i in range(0, len(posiciones)):
            for j in range(0, len(matriz[i])):
                matriz[posiciones[i]][j] = matriz_auxiliar[i][j]
            terminos_independientes[posiciones[i]][0] = b_auxiliar[i][0]

    return True

#**************************************************************************************#

"""
Verifica que cada entrada de una matriz identidad aproximada esté por debajo de
una tolerancia del error. Aplica redondeo.

Parámetros:
identidad_aproximada -- Matriz identidad aproximada.
tolerancia -- Tolerancia para el error en la aproximación.
cifras_redondeo -- Cifras con las cuales se aplicará aritmética de redondeo.

Valor devuelto: verdadero si cada entrada está por debajo de la tolerancia, falso de otro modo.
"""
def verificarErrorIdentidad (identidad_aproximada, tolerancia, cifras_redondeo):
    #Crea la matriz identidad exacta.
    identidad = [[0 for columna in identidad_aproximada] for renglon in identidad_aproximada]
    for i in range(0, len(identidad)):
        identidad[i][i] = 1

    #Revisa entrada a entrada el error en la matriz identidad aproximada.
    i = 0
    for renglon in identidad:
        j = 0
        for columna in identidad:
            if abs(redondear(identidad[i][j] - identidad_aproximada[i][j], cifras_redondeo)) > tolerancia:
                return False;
            j = j + 1
        i = i + 1

    return True

#**************************************************************************************#

"""
Calcula el determinante de una matriz triangular superior multiplicando su diagonal.

Parámetros:
matriz -- Dirección de la matriz triangular superior.
p -- Número de pivoteos realizados en la eliminación.

Valor devuelto: Determinante de la matriz.
"""
def calcularDeterminanteTriangular (matriz, p):
    determinante = 1

    for i in range(0, len(matriz)):
        determinante = determinante * matriz[i][i]

    return pow(-1, p) * determinante

#**************************************************************************************#

"""
Esta función se encarga de permutar de lugar dos renglones de una misma matriz.

Parámetros:
matriz -- Matriz donde se permutarán los renglones.
renglon_uno -- Índice del primer renglón.
renglon_dos -- Índice del segundo renglón.
"""
def permutarRenglones (matriz, renglon_uno, renglon_dos):
    j = 0
    for columna in matriz[0]:
        auxiliar = matriz[renglon_uno][j]
        matriz[renglon_uno][j] = matriz[renglon_dos][j]
        matriz[renglon_dos][j] = auxiliar
        j = j + 1

#**************************************************************************************#

"""
Esta función realiza una operación elemental sobre algún renglón de una matriz.

Parámetros:
matriz -- Matriz donde se realizará la operación elemental.
i_operado -- Índice del renglón donde se aplicará la operación.
escalar -- Escalar por el que se multiplica el renglón operante.
i_operante -- Índice del renglón que opera sobre el otro.
"""
def operacionElementalRenglon (matriz, i_operado, escalar, i_operante):
    for j in range (0, len(matriz[i_operado])):
        matriz[i_operado][j] = matriz[i_operado][j] + escalar * matriz[i_operante][j]

#**************************************************************************************#

"""
Esta función realiza una operación elemental sobre algún renglón de una matriz con redondeo.

Parámetros:
matriz -- Matriz donde se realizará la operación elemental.
i_operado -- Índice del renglón donde se aplicará la operación.
escalar -- Escalar por el que se multiplica el renglón operante.
i_operante -- Índice del renglón que opera sobre el otro.
cifras_redondeo -- Cifras con las que se aplica una aritmética de redondeo.
"""
def operacionElementalRenglonRedondeo (matriz, i_operado, escalar, i_operante, cifras_redondeo):
    for j in range (0, len(matriz[i_operado])):
        matriz[i_operado][j] = redondear(matriz[i_operado][j], cifras_redondeo)
        matriz[i_operante][j] = redondear(matriz[i_operante][j], cifras_redondeo)
        matriz[i_operado][j] = redondear(matriz[i_operado][j] + redondear(escalar * matriz[i_operante][j], cifras_redondeo), cifras_redondeo)

#**************************************************************************************#

"""
Esta función se encarga de redondear todas las entradas de una matriz a k cifras.

Parámetros:
matriz -- Matriz que será redondeada.
cifras_redondeo -- Cifras con las que se aplicará la aritmética de redondeo.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
"""
def redondearEntradasMatriz (matriz, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    i = 0
    for renglon in matriz:
        j = 0
        for columna in matriz[i]:
            matriz[i][j] = redondear(matriz[i][j], cifras_redondeo)
            j = j + 1
        i = i + 1

#**************************************************************************************#

"""
Escala cada renglón de una matriz.

Parámetros:
matriz -- Dirección de la matriz que será escalada.
"""
def escalarMatriz (matriz):
    for i in range(0, len(matriz)):
        #No revisa en los términos independientes.
        valor_mayor = encontrarNumeroMayorLista(matriz[i][:len(matriz[i])-1])

        if valor_mayor == 0:
            raise NoHaySolucionUnicaExcepcion

        for j in range(0, len(matriz[i])):
            matriz[i][j] = matriz[i][j] / valor_mayor

#**************************************************************************************#

"""
Escala cada renglón de una matriz aplicando redondeo.

Parámetros:
matriz -- Dirección de la matriz que será escalada.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
"""
def escalarMatrizRedondeo (matriz, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    for i in range(0, len(matriz)):
        #No revisa en los términos independientes.
        valor_mayor = encontrarNumeroMayorLista(matriz[i][:len(matriz[i])-1])

        if valor_mayor == 0:
            raise NoHaySolucionUnicaExcepcion

        for j in range(0, len(matriz[i])):
            matriz[i][j] = redondear(matriz[i][j], cifras_redondeo)
            valor_mayor = redondear(valor_mayor, cifras_redondeo)
            matriz[i][j] = redondear(matriz[i][j] / valor_mayor, cifras_redondeo)

#**************************************************************************************#

"""
Resta dos matrices de dimensiones iguales.

Parámetros:
matriz1 -- Matriz minuendo.
matriz2 -- Matriz sustraendo.

Valor devuelto: Matriz resultado de la diferencia.

Lanza DimensionNoCompatibleExcepcion si las matrices no tienen las mismas dimensiones.
"""
def restarMatrices (matriz1, matriz2):
    #Revisa que tengan las mismas dimensiones.
    if (len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0])):
        raise DimensionNoCompatibleExcepcion

    #Inicializa la matriz resultado con todas sus entradas en 0.
    resultado = [[0] for renglon in matriz1]

    i = 0
    for renglon in resultado:
        j = 0
        for columna in resultado[i]:
            resultado[i][j] = matriz1[i][j] - matriz2[i][j]
            j = j + 1

        i = i + 1

    return resultado

#**************************************************************************************#

"""
Resta dos matrices de dimensiones iguales aplicando redondeo.

Parámetros:
matriz1 -- Matriz minuendo.
matriz2 -- Matriz sustraendo.
cifras_redondeo -- Cifras con las que se aplicará el redondeo.

Valor devuelto: Matriz resultado de la diferencia.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
Lanza DimensionNoCompatibleExcepcion si las matrices no tienen las mismas dimensiones.
"""
def restarMatricesRedondeo (matriz1, matriz2, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    #Revisa que tengan las mismas dimensiones.
    if (len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0])):
        raise DimensionNoCompatibleExcepcion

    #Inicializa la matriz resultado con todas sus entradas en 0.
    resultado = [[0] for renglon in matriz1]

    i = 0
    for renglon in resultado:
        j = 0
        for columna in resultado[i]:
            resultado[i][j] = redondear(redondear(matriz1[i][j], cifras_redondeo) - redondear(matriz2[i][j], cifras_redondeo), cifras_redondeo)
            j = j + 1

        i = i + 1

    return resultado

#**************************************************************************************#

"""
Multiplica dos matrices.

Parámetros:
matriz1 -- Primer factor. Debe ser de dimensiones m*n.
matriz2 -- Segundo factor. Debe ser de dimensiones n*k.

Valor devuelto: Matriz producto, de dimensiones m*k.

Lanza DimensionNoCompatibleExcepcion si las dimensiones de las matrices no son m*n y n*k.
"""
def multiplicarMatrices (matriz1, matriz2):
    #Revisa que tengan dimensiones correctas.
    if len(matriz1[0]) != len(matriz2):
        raise DimensionNoCompatibleExcepcion

    #Inicializa la matriz resultado de m*k con ceros.
    matriz_resultado = [[0 for columna in matriz2[0]] for renglon in matriz1]

    i = 0

    for renglon in matriz_resultado:
        j = 0
        for columna in matriz_resultado[i]:
            for k in range(0, len(matriz1[i])):
                matriz_resultado[i][j] = matriz_resultado[i][j] + matriz1[i][k] * matriz2[k][j]
            j = j + 1
        i = i + 1

    return matriz_resultado

#**************************************************************************************#

"""
Multiplica dos matrices aplicando redondeo.

Parámetros:
matriz1 -- Primer factor. Debe ser de dimensiones m*n.
matriz2 -- Segundo factor. Debe ser de dimensiones n*k.
cifras_redondeo --

Valor devuelto: Matriz producto, de dimensiones m*k.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
Lanza DimensionNoCompatibleExcepcion si las dimensiones de las matrices no son m*n y n*k.
"""
def multiplicarMatricesRedondeo (matriz1, matriz2, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    #Revisa que tengan dimensiones correctas.
    if len(matriz1[0]) != len(matriz2):
        raise DimensionNoCompatibleExcepcion

    #Inicializa la matriz resultado de m*k con ceros.
    matriz_resultado = [[0 for columna in matriz2[0]] for renglon in matriz1]

    i = 0

    for renglon in matriz_resultado:
        j = 0
        for columna in matriz_resultado[i]:
            for k in range(0, len(matriz1[i])):
                matriz1[i][k] = redondear(matriz1[i][k], cifras_redondeo)
                matriz2[k][j] = redondear(matriz2[k][j], cifras_redondeo)
                matriz_resultado[i][j] = redondear(matriz_resultado[i][j] + redondear(matriz1[i][k] * matriz2[k][j], cifras_redondeo), cifras_redondeo)
            j = j + 1
        i = i + 1

    return matriz_resultado

#**************************************************************************************#

"""
Calcula la matriz inversa de alguna matriz aplicando redondeo.

Parámetros:
matriz -- Matriz que será invertida.
cifras_redondeo -- Cifras que se utilizarán para redondear.

Valor devuelto: Matriz inversa.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
Lanza NoHaySolucionUnicaExcepcion si no se puede invertir la matriz.
"""
def invertirMatrizRedondeo (matriz, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    matriz_auxiliar = copiarMatriz(matriz)
    m = len(matriz_auxiliar)

    #Agrega la matriz identidad en la matriz aumentada.
    for i in range(0, m):
        for j in range(0, m):
            matriz_auxiliar[i].append(0)
        matriz_auxiliar[i][i+m] = 1

    #Realiza la eliminación hacia arriba y hacia abajo con pivoteo parcial.
    i = 0

    for renglon in matriz_auxiliar:
        p = encontrarRenglonMayor(matriz_auxiliar, i)

        #El valor mayor de esa columna es 0.
        if matriz_auxiliar[p][i] == 0:
            raise NoHaySolucionUnicaExcepcion
        elif p != i:
            permutarRenglones(matriz_auxiliar, i, p)

        #Normaliza el renglon de la matriz.
        normalizacion = redondear(matriz_auxiliar[i][i], cifras_redondeo)
        for j in range(i, len(matriz_auxiliar[i])):
            matriz_auxiliar[i][j] = redondear(redondear(matriz_auxiliar[i][j], cifras_redondeo) / normalizacion, cifras_redondeo)

        #Hacia abajo.
        for j in range(i + 1, len(matriz_auxiliar)):
            multiplicador = redondear(matriz_auxiliar[j][i] / matriz_auxiliar[i][i], cifras_redondeo)
            operacionElementalRenglonRedondeo(matriz_auxiliar, j, -multiplicador, i, cifras_redondeo)

        #Hacia arriba.
        for j in range(i - 1, -1, -1):
            multiplicador = redondear(matriz_auxiliar[j][i] / matriz_auxiliar[i][i], cifras_redondeo)
            operacionElementalRenglonRedondeo(matriz_auxiliar, j, -multiplicador, i, cifras_redondeo)

        i = i + 1

    #Pasa la segunda mitad de la matriz auxiliar a una nueva matriz.
    matriz_inversa = [renglon[m:] for renglon in matriz_auxiliar]

    return matriz_inversa

#**************************************************************************************#

"""
Esta función copia los contenidos de una matriz y los regresa, para que sean asignados a
otra matriz.

Parámetros:
matriz -- Matriz que será copiada.

Valor devuelto: Matriz con los contenidos copiados.
"""
def copiarMatriz (matriz):
    copia = [renglon[:] for renglon in matriz]

    return copia

#**************************************************************************************#
