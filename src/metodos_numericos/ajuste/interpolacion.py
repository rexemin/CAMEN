#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: interpolacion.py.
Autor: Iván A. Moreno Soto.
Fecha: 04/Diciembre/2016.

Contiene los métodos que generan polinomios interpolantes por diferencias divididas de Newton y Lagrange.
"""

#**************************************************************************************#

from py_expression_eval import Parser

#**************************************************************************************#

"""
Interpola una función desconocida con un polinomio de grado n (dados n + 1 puntos conocidos)
mediante el método de diferencias divididas de Newton.

Parámetros:
datos_funcion -- Puntos y evaluaciones conocidas de la función contenidas en una matriz de 2 por n + 1.

Valor devuelto: Tupla que contiene en su primer índice la expresión del polinomio generado en una cadena
de caracteres; en su segundo índice se encuentra el polinomio pasado por un parser para que pueda ser evaluado
en cualquier punto.
"""
def interpolacionNewton (datos_funcion):
    #Grado del polinomio.
    n = len(datos_funcion) - 1

    #Crea la matriz que guardará todas las diferencias divididas.
    diferencias_divididas = [[0 for columna in range(0, n + 2)] for renglon in range(0, n + 1)]
    #Crea un arreglo para un polinomio de grado n.
    coeficientes_polinomio = [0 for punto in range(0, n + 1)]

    #Pasa los datos dados por el usuario a las primeras dos columnas de la tabla de diferencias divididas.
    i = 0
    for renglon in datos_funcion:
        j = 0
        for columna in renglon:
            diferencias_divididas[i][j] = columna
            j = j + 1
        i = i + 1

    #Calcula las diferencias divididas.
    for j in range(2, n + 2):
        for i in range(0, n + 2 - j):
            diferencias_divididas[i][j] = (diferencias_divididas[i+1][j-1] - diferencias_divididas[i][j-1]) / (diferencias_divididas[j+i-1][0] - diferencias_divididas[i][0])


    #Pasa el primer renglón de las diferencias divididas como coeficientes del polinomio de interpolación.
    indice_b = 0
    for indice_coeficiente in range(1, n + 2):
        coeficientes_polinomio[indice_b] = diferencias_divididas[0][indice_coeficiente]
        indice_b = indice_b + 1

    #Separa los puntos x_i en otro arreglo para crear el polinomio en la siguiente instrucción.
    puntos = [renglon[0] for renglon in datos_funcion]

    #Se crea un String que contiene al polinomio para que pueda ser parseado y después evaluado.
    expresion_polinomio = generarExpresionPolinomio(coeficientes_polinomio, puntos)

    parseador_polinomio = Parser()
    funcion_polinomio = parseador_polinomio.parse(expresion_polinomio)

    return expresion_polinomio, funcion_polinomio

#**************************************************************************************#

"""
Genera una cadena que contiene de manera estilizada todos los términos no nulos
de un polinomio dado por los coeficientes del mismo.
El polinomio generado es de la forma:
b_0 +/- b_1*(x - x_0) +/- b_2*(x - x_0)*(x - x_1) +/- ... +/- b_n*(x - x_0)...(x - x_(n-1))

Parámetros:
coeficientes -- Arreglo que contiene los coeficientes de cada término del polinomio.
puntos -- Puntos conocidos por los cuales el polinomio pasa.

Valor devuelto: Cadena que contiene la expresión generada del polinomio.
"""
def generarExpresionPolinomio (coeficientes, puntos):
    expresion_polinomio = ""

    #Término independiente del polinomio, si es que hay.
    if abs(coeficientes[0]) >= 0.0001:
        if coeficientes[0] < 0:
            expresion_polinomio = expresion_polinomio + " - " + str(-coeficientes[0])
        if coeficientes[0] > 0:
            expresion_polinomio = expresion_polinomio + " + " + str(coeficientes[0])

    #Resto de los términos del polinomio, no concatena a la expresión los términos que
    #son nulos.
    for i in range(1, len(coeficientes)):
        if abs(coeficientes[i]) >= 0.0001:
            if coeficientes[i] < 0:
                if coeficientes[i] == -1:
                    expresion_polinomio = expresion_polinomio + " - "
                else:
                    expresion_polinomio = expresion_polinomio + " - " + str(-coeficientes[i])
            if coeficientes[i] > 0:
                if coeficientes[i] == 1:
                    expresion_polinomio = expresion_polinomio + " + "
                else:
                    expresion_polinomio = expresion_polinomio + " + " + str(coeficientes[i])

            for j in range(0, i):
                expresion_polinomio = expresion_polinomio + "*(x"
                if puntos[j] >= 0:
                    expresion_polinomio = expresion_polinomio + " - " + str(puntos[j])
                else:
                    expresion_polinomio = expresion_polinomio + " + " + str(-puntos[j])
                expresion_polinomio = expresion_polinomio + ")"

    return expresion_polinomio

#**************************************************************************************#

"""
Interpola una función desconocida con un polinomio de grado n (dados n + 1 puntos conocidos)
mediante la interpolación de Lagrange.

Parámetros:
datos_funcion -- Puntos y evaluaciones conocidas de la función contenidas en una matriz de 2 por n + 1.

Valor devuelto: Tupla que contiene en su primer índice la expresión del polinomio generado en una cadena
de caracteres; en su segundo índice se encuentra el polinomio pasado por un parser para que pueda ser evaluado
en cualquier punto.
"""
def interpolacionLagrange (datos_funcion):
    expresion_polinomio = ""
    numero_puntos = len(datos_funcion)

    #Sumatoria de los términos.
    for i in range(0, numero_puntos):
        expresion_polinomio_aux = ""
        expresion_polinomio_aux = expresion_polinomio_aux + " + (" + str(datos_funcion[i][1]) + ")*("
        denominador_actual = 1

        #Primera parte de la productoria de términos de Lagrange.
        for j in range(0, i):
            denominador_actual = denominador_actual * (datos_funcion[i][0] - datos_funcion[j][0])
            expresion_polinomio_aux = expresion_polinomio_aux + "(x"

            if datos_funcion[j][0] >= 0:
                expresion_polinomio_aux = expresion_polinomio_aux + " - " + str(datos_funcion[j][0]) + ")*"
            else:
                expresion_polinomio_aux = expresion_polinomio_aux + " + " + str(-datos_funcion[j][0]) + ")*"

        #Segunda parte de la productoria de términos de Lagrange.
        for j in range(i + 1, numero_puntos):
            denominador_actual = denominador_actual * (datos_funcion[i][0] - datos_funcion[j][0])
            expresion_polinomio_aux = expresion_polinomio_aux + "(x"

            if datos_funcion[j][0] >= 0:
                expresion_polinomio_aux = expresion_polinomio_aux + " - " + str(datos_funcion[j][0]) + ")*"
            else:
                expresion_polinomio_aux = expresion_polinomio_aux + " + " + str(-datos_funcion[j][0]) + ")*"

        #Elimina el último asterisco que queda al final para que el parser no tenga problemas.
        ultimo_caracter = len(expresion_polinomio_aux) - 2
        expresion_polinomio_aux = expresion_polinomio_aux[:ultimo_caracter]

        expresion_polinomio_aux = expresion_polinomio_aux + "))/(" + str(denominador_actual) + ")"
        expresion_polinomio = expresion_polinomio + expresion_polinomio_aux

    parseador_polinomio = Parser()
    funcion_polinomio = parseador_polinomio.parse(expresion_polinomio)

    return expresion_polinomio, funcion_polinomio

#**************************************************************************************#
