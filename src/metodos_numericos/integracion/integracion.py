#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: integracion.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 04/Diciembre/2016.

Este módulo contiene las funciones que permiten aproximar integrales de funciones
de manera numérica.
"""

#**************************************************************************************#

from metodos_numericos.excepcion.excepciones_metodos import NumeroParticionesInvalidoExcepcion

#**************************************************************************************#

"""
Verifica que los puntos de la tabulación de una función estén equidistantes.
Se da una tolerancia de 0.005 para el error.

Parámetros:
datos_funcion -- Puntos conocidos de la función.

Valor devuelto: Verdadero si todos los puntos son equidistantes, Falso de otro modo.
"""
def verificacionPuntosEquidistantes (datos_funcion):
    distancia_referencia = abs(datos_funcion[1][0] - datos_funcion[0][0])
    tolerancia = 0.005

    for punto in range(1, len(datos_funcion) - 1):
        distancia_actual = abs(datos_funcion[punto+1][0] - datos_funcion[punto][0])

        if abs(distancia_actual - distancia_referencia) > tolerancia:
            return False

    return True

#**************************************************************************************#

"""
Integra numéricamente una función conocida con el método del trapecio.

Parámetros:
funcion -- Función que será integrada. Debe estar parseada para que pueda ser evaluada en el proceso.
a -- Límite inferior de la integral.
b -- Límite superior de la integral.
n -- Número de trapecios que se usarán en la integración.

Valor devuelto: Valor aproximado de la integral definida en [a,b] de la función.

Lanza NumeroParticionesInvalidoExcepcion si el número de trapecios es menor a 1.
"""
def integracionTrapecioConocida (funcion, a, b, n):
    if n < 1:
        raise NumeroParticionesInvalidoExcepcion

    longitud_intervalo = b - a

    h = longitud_intervalo / n

    #Comienza a evaluar la función para calcular el área de los trapecios.
    evaluacion_lim_inferior = funcion.evaluate({'x': a}) #x_0.
    evaluacion_lim_superior = funcion.evaluate({'x': b}) #x_n.

    punto_actual = a + h #x_1.
    sumatoria_evaluaciones_medio = 0

    #Desde x_1 hasta x_(n-1).
    for punto in range(1, n):
        evaluacion_actual = funcion.evaluate({'x': punto_actual})
        sumatoria_evaluaciones_medio = sumatoria_evaluaciones_medio + evaluacion_actual
        punto_actual = punto_actual + h

    integral = longitud_intervalo * (evaluacion_lim_inferior + 2 * sumatoria_evaluaciones_medio + evaluacion_lim_superior) / (2 * n)

    return integral

#**************************************************************************************#

"""
Integra numéricamente una función desconocida con el método del trapecio.

Parámetros:
datos_funcion -- Datos tabulados de la función. Los puntos deben ser verificados antes
de utilizarse esta función.

Valor devuelto: Valor aproximado de la integral definida en [a,b] de la función.

Lanza NumeroParticionesInvalidoExcepcion si el número de trapecios es menor a 1.
"""
def integracionTrapecioDesconocida (datos_funcion):
    indice_ultimo_punto = len(datos_funcion) - 1
    n = len(datos_funcion) - 1

    if n < 1:
        raise NumeroParticionesInvalidoExcepcion

    longitud_intervalo = datos_funcion[indice_ultimo_punto][0] - datos_funcion[0][0]

    sumatoria_evaluaciones_medio = 0

    #Desde x_1 hasta x_(n-1).
    for punto in range(1, n):
        sumatoria_evaluaciones_medio = sumatoria_evaluaciones_medio + datos_funcion[punto][1]

    integral = longitud_intervalo * (datos_funcion[0][1] + 2 * sumatoria_evaluaciones_medio + datos_funcion[indice_ultimo_punto][1]) / (2 * n)

    return integral

#**************************************************************************************#

"""
Integra numéricamente una función conocida con las reglas de simpson 1/3 y 3/8.

Parámetros:
funcion -- Función que será integrada. Debe estar parseada para que pueda ser evaluada en el proceso.
a -- Límite inferior de la integral.
b -- Límite superior de la integral.
n -- Número de particiones que se usarán en la integración.

Valor devuelto: Valor aproximado de la integral definida en [a,b] de la función.

Lanza NumeroParticionesInvalidoExcepcion si el número de particiones es menor a 1.
"""
def integracionSimpsonConocida (funcion, a, b, n):
    if n < 1:
        raise NumeroParticionesInvalidoExcepcion

    h = (b - a) / n

    if (n % 2 == 0):
        area_cubica = 0
    else:
        #Empieza Simpson 3/8
        x_0 = a
        x_1 = a + h
        x_2 = a + 2*h
        x_3 = a + 3*h

        longitud_intervalo = x_3 - x_0

        area_cubica = longitud_intervalo * (funcion.evaluate({'x': x_0}) + 3*funcion.evaluate({'x': x_1}) + 3*funcion.evaluate({'x': x_2}) + funcion.evaluate({'x': x_3})) / 8

        #Desplaza Simpson 1/3 tres puntos.
        a = x_3
        n = n - 3

    longitud_intervalo = b - a
    #Empieza Simpson 1/3.
    evaluacion_lim_inferior = funcion.evaluate({'x': a}) #x_0.
    evaluacion_lim_superior = funcion.evaluate({'x': b}) #x_n.

    punto_actual_impar = a + h #x_1.
    punto_actual_par = a + 2*h #x_2.
    sumatoria_evaluaciones_par = 0
    sumatoria_evaluaciones_impar = 0

    #Desde x_1 hasta x_(n-1) impares.
    for punto in range(1, n, 2):
        evaluacion_actual = funcion.evaluate({'x': punto_actual_impar})
        sumatoria_evaluaciones_impar = sumatoria_evaluaciones_impar + evaluacion_actual
        punto_actual_impar = punto_actual_impar + 2*h

    #Desde x_2 hasta x_(n-2) pares.
    for punto in range(2, n - 1, 2):
        evaluacion_actual = funcion.evaluate({'x': punto_actual_par})
        sumatoria_evaluaciones_par = sumatoria_evaluaciones_par + evaluacion_actual
        punto_actual_par = punto_actual_par + 2*h

    integral = area_cubica + (longitud_intervalo * (evaluacion_lim_inferior + 4 * sumatoria_evaluaciones_impar + 2 * sumatoria_evaluaciones_par + evaluacion_lim_superior) / (3 * n))

    return integral

#**************************************************************************************#

"""
Integra numéricamente una función desconocida con las reglas de Simpson 1/3 y 3/8.

Parámetros:
datos_funcion -- Datos tabulados de la función. Los puntos deben ser verificados antes
de utilizarse esta función.

Valor devuelto: Valor aproximado de la integral definida en [a,b] de la función.

Lanza NumeroParticionesInvalidoExcepcion si el número de particiones es menor a 1.
"""
def integracionSimpsonDesconocida (datos_funcion):
    n = len(datos_funcion) - 1

    if n < 1:
        raise NumeroParticionesInvalidoExcepcion

    indice_ultimo_punto = len(datos_funcion) - 1
    h = (datos_funcion[indice_ultimo_punto][0] - datos_funcion[0][0]) / n

    if (n % 2 == 0):
        i_inicio = 0
        longitud_intervalo = datos_funcion[indice_ultimo_punto][0] - datos_funcion[0][0]
        area_cubica = 0
    else:
        #Empieza Simpson 3/8
        x_0 = datos_funcion[0][1]
        x_1 = datos_funcion[1][1]
        x_2 = datos_funcion[2][1]
        x_3 = datos_funcion[3][1]

        longitud_intervalo = datos_funcion[3][0] - datos_funcion[0][0]

        area_cubica = longitud_intervalo * (x_0 + 3*x_1 + 3*x_2 + x_3) / 8

        #Desplaza Simpson 1/3 tres puntos.
        i_inicio = 3
        n = n - 3
        longitud_intervalo = datos_funcion[indice_ultimo_punto][0] - datos_funcion[3][0]

    #Empieza Simpson 1/3.
    evaluacion_lim_inferior = datos_funcion[i_inicio][1] #x_0.
    evaluacion_lim_superior = datos_funcion[indice_ultimo_punto][1] #x_n.

    sumatoria_evaluaciones_par = 0
    sumatoria_evaluaciones_impar = 0

    #Desde x_1 hasta x_(n-1) impares.
    for punto in range(i_inicio + 1, len(datos_funcion), 2):
        sumatoria_evaluaciones_impar = sumatoria_evaluaciones_impar + datos_funcion[punto][1]

    #Desde x_2 hasta x_(n-2) pares.
    for punto in range(i_inicio + 2, len(datos_funcion) - 1, 2):
        sumatoria_evaluaciones_par = sumatoria_evaluaciones_par + datos_funcion[punto][1]

    integral = area_cubica + (longitud_intervalo * (evaluacion_lim_inferior + 4 * sumatoria_evaluaciones_impar + 2 * sumatoria_evaluaciones_par + evaluacion_lim_superior) / (3 * n))

    return integral

#**************************************************************************************#
