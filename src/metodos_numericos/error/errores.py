#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: errores.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016.

Contiene las funciones que calculan errores absolutos y relativos, así como redondeo y normalización.
"""

#**************************************************************************************#

from math import modf
from math import ceil
from math import floor

#**************************************************************************************#

"""
Calcula el error absoluto (verdadero o aproximado) para dos valores numéricos.

Parámetros:
a -- Valor actual de una aproximación o valor real de un proceso.
b -- Valor anterior de una aproximación o valor aproximado actual (cuando el error es verdadero.)

Valor devuelto: Valor del error absoluto.
"""
def calcularErrorAbsoluto(a, b):
    return abs(a - b)

#**************************************************************************************#

"""
Calcula el error relativo (verdadero o aproximado) para dos valores numéricos.

Parámetros:
a -- Valor actual de una aproximación o valor real de un proceso.
b -- Valor anterior de una aproximación o valor aproximado actual (cuando el error es verdadero.)

Valor devuelto: Valor del error relativo.
"""
def calcularErrorRelativo(a, b):
    return abs((a - b) / a)

#**************************************************************************************#

"""
Calcula la cota del error absoluto para la bisección en un intervalo [a,b].

Parámetros:
a -- Límite inferior del intervalo.
b -- Límite superior del intervalo.

Valor devuelto: Valor de la cota del error absoluto.
"""
def calcularCotaError(a, b):
    return (b-a)/2

#**************************************************************************************#

"""
Calcula la tolerancia del error para un método numérico cuando se tiene un número de cifras significativas.

Parámetros:
cifras_significativas -- Número de cifras significativas del método numérico.

Valor devuelto: Valor de la tolerancia.
"""
def calcularTolerancia(cifras_significativas):
    return 5 * pow(10, -cifras_significativas)

#**************************************************************************************#

"""
Normaliza un número a la forma 0.d_1d_2...d_n

Parámetros:
n -- Número que será normalizado.

Valor devuelto: Dupla que contiene el número normalizado y la cantidad de posiciones que se recorrió el punto decimal.
"""
def normalizar(n):
    posiciones_desplazadas = 0

    if n != 0:
        if abs(n) >= 1:
            while abs(n) >= 1:
                n = n * 0.1
                posiciones_desplazadas = posiciones_desplazadas + 1
        else:
            while abs(n) < 0.1:
                n = n * 10
                posiciones_desplazadas = posiciones_desplazadas - 1

    n_normalizado = [n, posiciones_desplazadas]

    return n_normalizado

#**************************************************************************************#

"""
Aplica una aritmética de redondeo a k cifras significativas a un número.

Parámetros:
n -- Número que será redondeado.
cifras_significativas -- Cifras que se utilizarán para aplicar la aritmética de redondeo.

Valor devuelto: Número redondeado.
"""
def redondear (n, cifras_significativas):
    n_normalizado = normalizar(n)
    n = n_normalizado[0]
    posiciones_desplazadas = n_normalizado[1]

    n = n * pow(10, cifras_significativas)

    n = round(n)

    n = n * pow(10, posiciones_desplazadas - cifras_significativas)

    return n

#**************************************************************************************#
