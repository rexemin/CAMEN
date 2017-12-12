#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: regresion.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 04/Diciembre/2016.

Contiene el método encargado de calcular un polinomio de regresión por mínimos
cuadrados.
"""

#**************************************************************************************#

from py_expression_eval import Parser

from metodos_numericos.sel.exacto import doolittle, sustitucionHaciaAdelante, sustitucionHaciaAtras
from metodos_numericos.excepcion.excepciones_metodos import GradoPolinomioInvalidoExcepcion

#**************************************************************************************#

"""
Calcula un polinomio de ajuste para una función desconocida mediante regresión con mínimos cuadrados.

Parámetros:
datos_funcion -- Puntos y evaluaciones conocidas de la función contenidas en una matriz de 2 por n + 1.
grado_polinomio -- Grado del polinomio de regresión.

Valor devuelto: Tupla que contiene en su primer índice la expresión del polinomio generado en una cadena
de caracteres; en su segundo índice se encuentra el polinomio pasado por un parser para que pueda ser evaluado
en cualquier punto.

Lanza GradoPolinomioInvalidoExcepcion si el grado del polinomio es menor a 0.
"""
def regresionPolinomial (datos_funcion, grado_polinomio):
    if grado_polinomio < 0:
        raise GradoPolinomioInvalidoExcepcion

    matriz_polinomio = [[0 for j in range(0, grado_polinomio + 1)] for i in range(0, grado_polinomio + 1)]
    terminos_independientes = [[0] for i in range(0, grado_polinomio + 1)]

    for n in range(0, grado_polinomio + 1):
        sumatoria_potencia_x = 0
        sumatoria_y_x = 0

        for i in range(0, len(datos_funcion)):
            potencia_x = pow(datos_funcion[i][0], n)
            sumatoria_potencia_x = sumatoria_potencia_x + potencia_x
            sumatoria_y_x = sumatoria_y_x + (datos_funcion[i][1] * potencia_x)

        terminos_independientes[n][0] = sumatoria_y_x

        for i in range(0, n + 1):
            matriz_polinomio[i][n - i] = sumatoria_potencia_x

    for n in range(grado_polinomio + 1, 2 * grado_polinomio + 1):
        sumatoria_potencia_x = 0

        for i in range(0, len(datos_funcion)):
            potencia_x = pow(datos_funcion[i][0], n)
            sumatoria_potencia_x = sumatoria_potencia_x + potencia_x

        for i in range(n - grado_polinomio, grado_polinomio + 1):
            matriz_polinomio[i][n - i] = sumatoria_potencia_x

    #Resuelve el SEL de los coeficientes del polinomio.
    factorizacion_LU = doolittle(matriz_polinomio, terminos_independientes, 0.0005)
    solucion_Y = sustitucionHaciaAdelante(factorizacion_LU[0], terminos_independientes)
    coeficientes_polinomio = sustitucionHaciaAtras(factorizacion_LU[1], solucion_Y)

    expresion_polinomio = ""

    #Genera la cadena que contiene al polinomio.
    #Término independiente del polinomio, si es que hay.
    if abs(coeficientes_polinomio[0][0]) >= 0.00001:
        if coeficientes_polinomio[0][0] < 0:
            expresion_polinomio = expresion_polinomio + " - " + str(-coeficientes_polinomio[0][0])
        if coeficientes_polinomio[0][0] > 0:
            expresion_polinomio = expresion_polinomio + " + " + str(coeficientes_polinomio[0][0])

    #Resto de los términos del polinomio, no concatena a la expresión los términos que
    #son nulos.
    for i in range(1, len(coeficientes_polinomio)):
        if abs(coeficientes_polinomio[i][0]) > 0.00001:
            if coeficientes_polinomio[i][0] < 0:
                if coeficientes_polinomio[i][0] == -1:
                    expresion_polinomio = expresion_polinomio + " - "
                else:
                    expresion_polinomio = expresion_polinomio + " - " + str(-coeficientes_polinomio[i][0])
            if coeficientes_polinomio[i][0] > 0:
                if coeficientes_polinomio[i][0] == 1:
                    expresion_polinomio = expresion_polinomio + " + "
                else:
                    expresion_polinomio = expresion_polinomio + " + " + str(coeficientes_polinomio[i][0])

            expresion_polinomio = expresion_polinomio + "*x^" + str(i)

    parseador_polinomio = Parser()
    funcion_polinomio = parseador_polinomio.parse(expresion_polinomio)

    return expresion_polinomio, funcion_polinomio

#**************************************************************************************#
