#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: exacto.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 06/Diciembre/2016

Este módulo contiene las funciones necesarias para resolver sistemas de ecuaciones lineales de manera
exacta.
"""

#**************************************************************************************#

from metodos_numericos.error.errores import redondear
from metodos_numericos.sel.operacion import *
from metodos_numericos.excepcion.excepciones_metodos import NoHaySolucionUnicaExcepcion, DimensionNoCompatibleExcepcion
from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, IteracionesInvalidasExcepcion, NumeroCifrasRedondeoExcepcion

from utilidades.impresion.matriz import imprimirMatriz

#**************************************************************************************#

"""
Esta es la función principal de la eliminación gaussiana simple con sustitución hacia atrás.
Maneja el proceso entero.

Parámetros:
matriz -- Arreglo bidimensional que contiene a la matriz aumentada del sistema.
vector_b -- Vector de términos independientes.
tolerancia -- Tolerancia para el error de las soluciones calculadas.
cifras_redondeo -- Cifras con las que se aplicará la aritmética de redondeo.
maximo_iteraciones -- Cantidad máxima de iteraciones que se realizará el proceso.
area_texto -- Área de texto donde se imprimirá el proceso.

Valor devuelto: Vector con las soluciones del sistema.

Lanza IteracionesInvalidasExcepcion si el número de iteraciones máximas es menor a 1.
Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
Lanza NoHaySolucionUnicaExcepcion si se encuentra que el SEL no tiene solución única.
Lanza MetodoFallidoExcepcion si se alcanza el número máximo de iteraciones sin éxito.
"""
def eliminacionGaussianaSimple (matriz, vector_b, tolerancia, cifras_redondeo, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    matriz_auxiliar = copiarMatriz(matriz) #Guarda la matriz original para su uso posterior.
    vector_b_auxiliar = copiarMatriz(vector_b)
    vector_soluciones = [[0] for renglon in matriz]
    vector_soluciones_aux = [[0] for renglon in matriz]

    for numero_iteraciones in range(1, maximo_iteraciones + 1):
        #Realiza la eliminación simple.
        for i in range(0, len(matriz) - 1):
            p = encontrarRenglonMenor(matriz, i)

            if p == -1:
                raise NoHaySolucionUnicaExcepcion
            elif p != i:
                permutarRenglones(matriz, i, p, len(matriz) + 1)
                permutarRenglones(vector_b, i, p, len(matriz) + 1)

            for j in range(i + 1, len(matriz)):
                multiplicador = redondear(redondear(matriz[j][i], cifras_redondeo) / redondear(matriz[i][i], cifras_redondeo), cifras_redondeo)
                operacionElementalRenglonRedondeo(matriz, j, -multiplicador, i, cifras_redondeo)
                operacionElementalRenglonRedondeo(vector_b, j, -multiplicador, i, cifras_redondeo) # !!!!!!

        area_texto.insert('end', "Matriz después de eliminación simple en la iteración " + str(numero_iteraciones) + ".\n")
        imprimirMatriz(matriz, area_texto)
        area_texto.insert('end', "Términos independientes después de eliminación simple en la iteración " + str(numero_iteraciones) + ".\n")
        imprimirMatriz(vector_b, area_texto)

        if matriz[len(matriz) - 1][len(matriz) - 1] == 0:
            raise NoHaySolucionUnicaExcepcion

        vector_soluciones_aux = sustitucionHaciaAtrasRedondeo(matriz, vector_b, cifras_redondeo)

        #Calcula el vector b aproximado.
        for i in range(0, len(vector_soluciones_aux)):
            vector_soluciones[i][0] = vector_soluciones_aux[i][0] # !!!!

        vector_b_aproximado = multiplicarMatricesRedondeo(matriz_auxiliar, vector_soluciones, cifras_redondeo)

        vector_errores = restarMatricesRedondeo(vector_b_aproximado, vector_b_auxiliar, cifras_redondeo)

        area_texto.insert('end', "\nAproximación de las soluciones del SEL actual en la iteración " + str(numero_iteraciones) + "\n")
        imprimirMatriz(vector_soluciones, area_texto)
        area_texto.insert('end', "\nVector de errores de la iteración actual:\n")
        imprimirMatriz(vector_errores, area_texto)

        if encontrarNumeroMayorMatriz(vector_errores) <= tolerancia:
            return vector_soluciones

        #Resetea la matriz.
        matriz = copiarMatriz(matriz_auxiliar)

        #Reemplaza los términos independientes de la matriz actual con los errores nuevos.
        for i in range(0, len(vector_b)):
            vector_b[i][0] = vector_errores[i][0]

        area_texto.insert('end', "\nMatriz que se usará en la siguiente iteración.\n")
        imprimirMatriz(matriz, area_texto)
        area_texto.insert('end', '\n')

    raise MetodoFallidoExcepcion

#**************************************************************************************#

"""
Aplica eliminación gaussiana con pivoteo parcial a una matriz para transformarla en
una matriz triangular superior.

Parámetros:
matriz -- Dirección de la matriz donde se aplicará el proceso.

Valor devuelto: una tupla que contiene la matriz triangular superior resultante y
la cantidad de veces que se realizó un pivoteo parcial.

Lanza NoHaySolucionUnicaExcepcion si el proceso de eliminación falla.
"""
def eliminacionGaussianaPivoteoParcial (matriz):
    matriz_auxiliar = copiarMatriz(matriz)
    numero_pivoteos = 0

    #Realiza la eliminación con pivoteo parcial.
    for i in range(0, len(matriz) - 1):
        p = encontrarRenglonMayor(matriz_auxiliar, i)

        #El valor mayor de esa columna es 0.
        if matriz_auxiliar[p][i] == 0:
            raise NoHaySolucionUnicaExcepcion
        elif p != i:
            numero_pivoteos = numero_pivoteos + 1
            permutarRenglones(matriz_auxiliar, i, p)

        for j in range(i + 1, len(matriz)):
            multiplicador = matriz_auxiliar[j][i] / matriz_auxiliar[i][i]
            operacionElementalRenglon(matriz_auxiliar, j, -multiplicador, i)

    if matriz_auxiliar[len(matriz) - 1][len(matriz) - 1] == 0:
        raise NoHaySolucionUnicaExcepcion

    return matriz_auxiliar, numero_pivoteos

#**************************************************************************************#

"""
Calcula las soluciones de un SEL utilizando la matriz inversa del mismo para aproximar el
vector de soluciones hasta que se agoten las iteraciones o se encuentre una aproximación tolerable.

Parámetros:
matriz -- Matriz que contiene el SEL.
matriz_inversa -- Matriz inversa del SEL.
vector_independiente -- Vector de términos independientes del SEL.
tolerancia -- Tolerancia para el error de las aproximaciones.
cifras_redondeo -- Cifras con las cuales se aplicará aritmética de redondeo.
maximo_iteraciones -- Máximo de iteraciones del proceso.
area_texto -- Área de texto donde se imprimirá el proceso.

Valor devuelto: Vector que contiene las soluciones del SEL.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
Lanza IteracionesInvalidasExcepcion si el número de iteraciones máximas es menor a 1.
Lanza MetodoFallidoExcepcion si se alcanza el número máximo de iteraciones sin éxito.
"""
def calcularSolucionesGJ (matriz, matriz_inversa, vector_independiente, tolerancia, cifras_redondeo, maximo_iteraciones, area_texto):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    #A^(-1)b = x.
    soluciones = multiplicarMatricesRedondeo(matriz_inversa, vector_independiente, cifras_redondeo)

    #Ax = b
    vector_b_aproximado = multiplicarMatricesRedondeo(matriz, soluciones, cifras_redondeo)

    vector_errores = restarMatricesRedondeo(vector_b_aproximado, vector_independiente, cifras_redondeo)

    area_texto.insert('end', "\nIteración 1.\n")
    area_texto.insert('end', "Aproximación actual a las soluciones:\n")
    imprimirMatriz(soluciones, area_texto)
    area_texto.insert('end', "Vector de términos independientes actual:\n")
    imprimirMatriz(vector_b_aproximado, area_texto)
    area_texto.insert('end', "Vector de errores actual:\n")
    imprimirMatriz(vector_errores, area_texto)
    area_texto.insert('end', '\n')

    if (encontrarNumeroMayorMatriz(vector_errores) <= tolerancia):
        return soluciones

    for iteracion in range(2, maximo_iteraciones + 1):
        soluciones_auxiliares = multiplicarMatricesRedondeo(matriz_inversa, vector_errores, cifras_redondeo)
        soluciones = restarMatricesRedondeo(soluciones, soluciones_auxiliares, cifras_redondeo)

        vector_b_aproximado = multiplicarMatricesRedondeo(matriz, soluciones, cifras_redondeo)

        vector_errores = restarMatricesRedondeo(vector_b_aproximado, vector_independiente, cifras_redondeo)

        area_texto.insert('end', "\nIteración " + str(iteracion) + ".\n")
        area_texto.insert('end', "Aproximación actual a las soluciones:\n")
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', "Vector de términos independientes actual:\n")
        imprimirMatriz(vector_b_aproximado, area_texto)
        area_texto.insert('end', "Vector de errores actual:\n")
        imprimirMatriz(vector_errores, area_texto)
        area_texto.insert('end', '\n')

        if (encontrarNumeroMayorMatriz(vector_errores) <= tolerancia):
            return soluciones

    raise MetodoFallidoExcepcion

#**************************************************************************************#

"""
Factoriza una matriz A en matrices L y U mediante el método de factorización directa
de Doolittle con pivoteo parcial.

Parámetros:
matriz -- Matriz que será factorizada. Debe ser cuadrada.
terminos_independientes -- Términos independientes asociados a la matriz. Los renglones son permutados en el proceso.
tolerancia_cercania_cero -- Tolerancia de las entradas de las matrices para su cercanía a 0.

Valor devuelto: Tupla que contiene a las matrices L y U.

Lanza NoHaySolucionUnicaExcepcion si el proceso detecta alguna entrada menor a la tolerancia dada.
"""
def doolittle (matriz, terminos_independientes, tolerancia_cercania_cero):
    #Encuentra el primer pivote.
    p = encontrarRenglonMayor(matriz, 0)

    if abs(matriz[p][0]) <= tolerancia_cercania_cero:
        raise NoHaySolucionUnicaExcepcion

    if p != 0:
        permutarRenglones(matriz, 0, p)
        permutarRenglones(terminos_independientes, 0, p)

    #Inicialización de las matrices L, U.
    matriz_l = [[0 for columna in matriz] for renglon in matriz]
    matriz_u = [[0 for columna in matriz] for renglon in matriz]

    matriz_l[0][0] = 1
    matriz_u[0][0] = matriz[0][0]

    #Obtiene el primer renglón de U y la primera columna de L.
    for j in range(1, len(matriz)):
        matriz_u[0][j] = matriz[0][j]
        matriz_l[j][0] = matriz[j][0] / matriz_u[0][0]

    for i in range(1, len(matriz) - 1):
        valor_pivote = 0

        #Obtiene el i-ésimo pivote.
        for j in range(i, len(matriz)):
            pivote_auxiliar = 0

            suma_valores_conocidos = 0
            for k in range(0, i):
                suma_valores_conocidos = suma_valores_conocidos + matriz_l[j][k] * matriz_u[k][i]

            pivote_auxiliar = matriz[j][i] - suma_valores_conocidos

            if abs(pivote_auxiliar) > abs(valor_pivote):
                valor_pivote = pivote_auxiliar
                p = j

        if abs(valor_pivote) <= tolerancia_cercania_cero:
            raise NoHaySolucionUnicaExcepcion

        if p != i:
            permutarRenglones(matriz, i, p)
            permutarRenglones(terminos_independientes, i, p)
            permutarRenglones(matriz_l, i, p)

        matriz_l[i][i] = 1
        matriz_u[i][i] = valor_pivote

        #Obtiene el i-ésimo renglón de U y la i-ésima columna de L.
        for j in range(i + 1, len(matriz)):
            suma_valores_conocidos = 0
            for k in range(0, i):
                suma_valores_conocidos = suma_valores_conocidos + matriz_l[i][k] * matriz_u[k][j]

            matriz_u[i][j] = (matriz[i][j] - suma_valores_conocidos) / matriz_l[i][i]

            suma_valores_conocidos = 0
            for k in range(0, i):
                suma_valores_conocidos = suma_valores_conocidos + matriz_l[j][k] * matriz_u[k][i]

            matriz_l[j][i] = (matriz[j][i] - suma_valores_conocidos) / matriz_u[i][i]

    matriz_l[len(matriz) - 1][len(matriz) - 1] = 1

    suma_valores_conocidos = 0
    for k in range(0, len(matriz) - 1):
        suma_valores_conocidos = suma_valores_conocidos + matriz_l[len(matriz) - 1][k] * matriz_u[k][len(matriz) - 1]

    if abs((matriz[len(matriz) - 1][len(matriz) - 1] - suma_valores_conocidos)) <= tolerancia_cercania_cero:
        raise NoHaySolucionUnicaExcepcion

    matriz_u[len(matriz) - 1][len(matriz) - 1] = matriz[len(matriz) - 1][len(matriz) - 1] - suma_valores_conocidos

    return matriz_l, matriz_u

#**************************************************************************************#

"""
Realiza sustitución hacia adelante para encontrar las soluciones de un SEL luego de
que haya sido aplicado algún metodo de eliminación.

Parámetros:
matriz -- Dirección de la matriz que se resolverá. Debe ser triangular inferior.
terminos_independientes --Vector de términos independientes del SEL.

Valor devuelto: un arreglo que contiene en orden las soluciones del sistema.
"""
def sustitucionHaciaAdelante (matriz, terminos_independientes):
    #Inicializa cada elemento en 0.
    vector_soluciones = [[0] for renglon in matriz]
    numero_ecuaciones = len(matriz)

    #Contador que permite saber que solución se está calculando.
    posicion_solucion = 0

    x_provisional = terminos_independientes[0][0] / matriz[0][0]
    vector_soluciones[posicion_solucion][0] = x_provisional
    posicion_solucion = posicion_solucion + 1

    for i in range(1, numero_ecuaciones):
        suma_x_anteriores = 0

        for j in range(0, i):
            suma_x_anteriores = suma_x_anteriores + (matriz[i][j] * vector_soluciones[j][0])

        x_provisional = (terminos_independientes[i][0] - suma_x_anteriores) / matriz[i][i]
        vector_soluciones[posicion_solucion][0] = x_provisional
        posicion_solucion = posicion_solucion + 1

    return vector_soluciones

#**************************************************************************************#

"""
Realiza sustitución hacia atrás para encontrar las soluciones de un SEL luego de
que haya sido aplicado algún metodo de eliminación.

Parámetros:
matriz -- Dirección de la matriz que se resolverá. Debe ser triangular superior.
terminos_independientes --Vector de términos independientes del SEL.

Valor devuelto: un arreglo que contiene en orden las soluciones del sistema.
"""
def sustitucionHaciaAtras (matriz, terminos_independientes):
    #Inicializa cada elemento en 0.
    vector_soluciones = [[0] for renglon in matriz]
    numero_ecuaciones = len(matriz)

    #Contador que permite saber que solución se está calculando.
    posicion_solucion = numero_ecuaciones - 1

    x_provisional = terminos_independientes[numero_ecuaciones - 1][0] / matriz[numero_ecuaciones - 1][numero_ecuaciones - 1]
    vector_soluciones[posicion_solucion][0] = x_provisional
    posicion_solucion = posicion_solucion - 1

    for i in range(numero_ecuaciones - 2, -1, -1):
        suma_x_anteriores = 0

        for j in range(numero_ecuaciones - 1, i, -1):
            suma_x_anteriores = suma_x_anteriores + (matriz[i][j] * vector_soluciones[j][0])

        x_provisional = (terminos_independientes[i][0] - suma_x_anteriores) / matriz[i][i]
        vector_soluciones[posicion_solucion][0] = x_provisional
        posicion_solucion = posicion_solucion - 1

    return vector_soluciones

#**************************************************************************************#

"""
Realiza sustitución hacia atrás con redondeo para encontrar las soluciones de un SEL luego de
que haya sido aplicado algún metodo de eliminación.

Parámetros:
matriz -- Dirección de la matriz que se resolverá. Debe ser triangular superior
terminos_independientes --Vector de términos independientes del SEL.
cifras_redondeo -- Cifras con las que se aplicará redondeo.

Valor devuelto: un arreglo que contiene en orden las soluciones del sistema.

Lanza NumeroCifrasRedondeoExcepcion si el número de cifras de redondeo es menor a 2.
"""
def sustitucionHaciaAtrasRedondeo (matriz, terminos_independientes, cifras_redondeo):
    if cifras_redondeo < 2:
        raise NumeroCifrasRedondeoExcepcion

    #Inicializa cada elemento en 0.
    vector_soluciones = [[0] for renglon in matriz]
    numero_ecuaciones = len(matriz)

    #Contador que permite saber que solución se está calculando.
    posicion_solucion = numero_ecuaciones - 1

    x_provisional = redondear(terminos_independientes[numero_ecuaciones - 1][0] / matriz[numero_ecuaciones - 1][numero_ecuaciones - 1], cifras_redondeo)
    vector_soluciones[posicion_solucion][0] = x_provisional
    posicion_solucion = posicion_solucion - 1

    for i in range(numero_ecuaciones - 2, -1, -1):
        suma_x_anteriores = 0

        for j in range(numero_ecuaciones - 1, i, -1):
            suma_x_anteriores = redondear(suma_x_anteriores + redondear(matriz[i][j] * vector_soluciones[j][0], cifras_redondeo), cifras_redondeo)

        x_provisional = redondear(redondear(terminos_independientes[i][0] - suma_x_anteriores, cifras_redondeo) / matriz[i][i], cifras_redondeo)
        vector_soluciones[posicion_solucion][0] = x_provisional
        posicion_solucion = posicion_solucion - 1

    return vector_soluciones

#**************************************************************************************#
