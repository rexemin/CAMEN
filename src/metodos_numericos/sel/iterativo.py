#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: iterativo.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 06/Diciembre/2016

Este módulo contiene las funciones necesarias para resolver sistemas de ecuaciones lineales
con métodos iterativos.
"""

#**************************************************************************************#

from metodos_numericos.sel.operacion import multiplicarMatrices, restarMatrices, encontrarNumeroMayorMatriz
from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, IteracionesInvalidasExcepcion

from utilidades.impresion.matriz import imprimirMatriz

#**************************************************************************************#

"""
Realiza el método iterativo de Jacobi para la resolución de un SEL. No se aplica una
aritmética de redondeo.

Parámetros:
matriz -- Matriz asociada al SEL.
terminos_independientes -- Vector de términos independientes del SEL.
tolerancia -- Tolerancia para el error en la exactitud de las soluciones.
maximo_iteraciones -- Número máximo de iteraciones que se llevarán a cabo.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Valor devuelto: Vector que contiene las soluciones aproximadas del SEL.

Lanza IteracionesInvalidasExcepcion si el número de iteraciones máximas es menor a 1.
Lanza MetodoFallidoExepcion si se alcanza el número máximo de iteraciones sin éxito.
"""
def jacobi (matriz, terminos_independientes, tolerancia, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    soluciones_anteriores = [[0] for renglon in matriz]
    soluciones_actuales = [[0] for renglon in matriz]

    for iteracion in range(1, maximo_iteraciones + 1):
        for i in range(0, len(matriz)):
            sumatoria = 0

            for j in range(0, i):
                sumatoria = sumatoria + (matriz[i][j] * soluciones_anteriores[j][0])

            for j in range(i + 1, len(matriz)):
                sumatoria = sumatoria + (matriz[i][j] * soluciones_anteriores[j][0])

            soluciones_actuales[i][0] = (terminos_independientes[i][0] - sumatoria) / matriz[i][i]

        b_aproximado = multiplicarMatrices(matriz, soluciones_actuales)
        errores = restarMatrices(terminos_independientes, b_aproximado)

        for i in range(0, len(errores)):
            errores[i][0] = abs((errores[i][0] / terminos_independientes[i][0]) * 100)

        area_texto.insert('end', "Iteración " + str(iteracion) + ".\n")
        area_texto.insert('end', "Soluciones aproximadas en esta iteración:\n")
        imprimirMatriz(soluciones_actuales, area_texto)
        area_texto.insert('end', '\n')
        area_texto.insert('end', "Errores en esta iteración:\n")
        imprimirMatriz(errores, area_texto)
        area_texto.insert('end', '\n')

        if encontrarNumeroMayorMatriz(errores) <= tolerancia:
            return soluciones_actuales

        for i in range(0, len(terminos_independientes)):
            soluciones_anteriores[i][0] = soluciones_actuales[i][0]

    raise MetodoFallidoExcepcion

#**************************************************************************************#

"""
Realiza el método iterativo de Gauss-Seidel para la resolución de un SEL. No aplica
aritmética de redondeo.

Parámetros:
matriz -- Matriz asociada al SEL.
terminos_independientes -- Vector de términos independientes del SEL.
tolerancia -- Tolerancia para el error en la exactitud de las soluciones.
maximo_iteraciones -- Número máximo de iteraciones que se llevarán a cabo.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Valor devuelto: Vector que contiene las soluciones aproximadas del SEL.

Lanza IteracionesInvalidasExcepcion si el número de iteraciones máximas es menor a 1.
Lanza MetodoFallidoExepcion si se alcanza el número máximo de iteraciones sin éxito.
"""
def gaussSeidel (matriz, terminos_independientes, tolerancia, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    soluciones = [[0] for renglon in matriz]

    for iteracion in range(1, maximo_iteraciones + 1):
        for i in range(0, len(matriz)):
            sumatoria = 0

            #Suma las x.
            for j in range(0, i):
                sumatoria = sumatoria + (matriz[i][j] * soluciones[j][0])

            for j in range(i + 1, len(matriz)):
                sumatoria = sumatoria + (matriz[i][j] * soluciones[j][0])

            soluciones[i][0] = (terminos_independientes[i][0] - sumatoria) / matriz[i][i]

        b_aproximado = multiplicarMatrices(matriz, soluciones)
        errores = restarMatrices(terminos_independientes, b_aproximado)

        for i in range(0, len(errores)):
            errores[i][0] = abs((errores[i][0] / terminos_independientes[i][0]) * 100)

        area_texto.insert('end', "Iteración " + str(iteracion) + ".\n")
        area_texto.insert('end', "Soluciones aproximadas en esta iteración:\n")
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', '\n')
        area_texto.insert('end', "Errores en esta iteración:\n")
        imprimirMatriz(errores, area_texto)
        area_texto.insert('end', '\n')

        if encontrarNumeroMayorMatriz(errores) <= tolerancia:
            return soluciones

    raise MetodoFallidoExcepcion

#**************************************************************************************#
