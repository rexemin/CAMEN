#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: biseccion.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016.

Contiene la función que realiza el proceso de bisección.
"""

#**************************************************************************************#

from metodos_numericos.error.errores import calcularCotaError
from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, IntervaloSinRaizExcepcion
from metodos_numericos.excepcion.excepciones_metodos import IntervaloInvalidoExcepcion, IteracionesInvalidasExcepcion

from utilidades.impresion.tabla import imprimirRenglonTabla

#**************************************************************************************#

"""
Realiza el proceso de bisección. Si hay raíz, se realiza hasta que se encuentra
una aproximación tolerable o se alcanza el número máximo de iteraciones del proceso.
Si no hay raíz, detiene el proceso.

funcion -- Función donde se buscará la raíz, debe estar previamente parseada.
a -- Límite inferior del intervalo de búsqueda inicial.
b -- Límite superior del intervalo de búsqueda inicial.
tolerancia -- Tolerancia para la cota del error absoluto.
maximo_iteraciones -- Número máximo de iteraciones que se realizarán.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Valor devuelto: aproximación tolerable de la raíz de la función.

Lanza IteracionesInvalidasExcepcion si el número máximo de iteraciones es menor a 1.
Lanza IntervaloInvalidoExcepcion cuando a es mayor que b.
Lanza IntervaloSinRaizExcepcion cuando no se encuentra un cambio de signo en el intervalo.
Lanza MetodoFallidoExcepcion cuando se alcanza el número máximo de iteraciones y no se ha
encontrado una aproximación tolerable de la raíz.
"""
def biseccion(funcion, a, b, tolerancia, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    if (a > b):
        raise IntervaloInvalidoExcepcion

    #Utilizando el Teorema de Bolzano: si no hay cambio en el signo de las imágenes
    #de los extremos del intervalo, no hay raíz de la función.
    if (funcion.evaluate({'x': a}) * funcion.evaluate({'x': b})) > 0:
        raise IntervaloSinRaizExcepcion

    for i in range(1, maximo_iteraciones + 1):
        evaluacion_a = funcion.evaluate({'x': a})

        punto_medio = (a + b)/2
        evaluacion_pm = funcion.evaluate({'x': punto_medio})

        error = calcularCotaError(a, b)

        imprimirRenglonTabla([i, a, b, punto_medio, evaluacion_a, evaluacion_pm, error], area_texto)

        if evaluacion_pm == 0 or error <= tolerancia:
            return punto_medio

        if (evaluacion_a * evaluacion_pm) < 0:
            b = punto_medio
        else:
            a =punto_medio

    raise MetodoFallidoExcepcion

#**************************************************************************************#
