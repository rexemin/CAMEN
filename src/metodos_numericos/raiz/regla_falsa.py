#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: regla_falsa.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016.

Contiene la función que realiza el proceso de regla falsa.
"""

#**************************************************************************************#

from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, IntervaloSinRaizExcepcion
from metodos_numericos.excepcion.excepciones_metodos import IntervaloInvalidoExcepcion, IteracionesInvalidasExcepcion
from metodos_numericos.error.errores import calcularErrorRelativo

from utilidades.impresion.tabla import imprimirRenglonTabla

#**************************************************************************************#

"""
Realiza el proceso de regla falsa. Si hay raíz, se realiza hasta que se encuentra
una aproximación tolerable o se alcanza el número máximo de iteraciones del proceso.

funcion -- Función donde se buscará la raíz, debe estar previamente parseada.
a -- Límite inferior del intervalo de búsqueda inicial.
b -- Límite superior del intervalo de búsqueda inicial.
tolerancia -- Tolerancia para el error en la precisión.
maximo_iteraciones -- Número máximo de iteraciones que se realizarán.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Valor devuelto: aproximación tolerable de la raíz de la función.

Lanza IteracionesInvalidasExcepcion si el número máximo de iteraciones es menor a 1.
Lanza IntervaloInvalidoExcepcion cuando a es mayor que b.
Lanza IntervaloSinRaizExcepcion cuando no se encuentra un cambio de signo en el intervalo.
Lanza MetodoFallidoExepcion cuando se alcanza el número máximo de iteraciones y no se ha
encontrado una aproximación tolerable de la raíz.
"""
def reglaFalsa(funcion, a, b, tolerancia, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    if (a > b):
        raise IntervaloInvalidoExcepcion

    #Utilizando el Teorema de Bolzano: si no hay cambio en el signo de las imágenes
    #de los extremos del intervalo, no hay raíz de la función.
    if (funcion.evaluate({'x': a}) * funcion.evaluate({'x': b})) > 0:
        raise IntervaloSinRaizExcepcion

    #Primera iteración de la regla falsa.
    evaluacion_a = funcion.evaluate({'x': a})
    evaluacion_b = funcion.evaluate({'x': b})

    c = a - evaluacion_a * ((b - a) / (evaluacion_b - evaluacion_a))
    evaluacion_c = funcion.evaluate({'x': c})

    imprimirRenglonTabla([1, a, b, evaluacion_a, evaluacion_b, c, evaluacion_c, ''], area_texto)

    if evaluacion_c == 0:
        return c

    if (evaluacion_a * evaluacion_c) < 0:
        b = c
    else:
        a = c

    for i in range(2, maximo_iteraciones + 1):
        evaluacion_a = funcion.evaluate({'x': a})
        evaluacion_b = funcion.evaluate({'x': b})

        c_anterior = c

        c = a - evaluacion_a * ((b - a) / (evaluacion_b - evaluacion_a))
        evaluacion_c = funcion.evaluate({'x': c})

        error = calcularErrorRelativo(c, c_anterior)

        imprimirRenglonTabla([i, a, b, evaluacion_a, evaluacion_b, c, evaluacion_c, error], area_texto)

        if evaluacion_c == 0 or error <= tolerancia:
            return c

        if (evaluacion_a * evaluacion_c) < 0:
            b = c
        else:
            a = c

    #El procedimiento ha fallado.
    raise MetodoFallidoExcepcion

#**************************************************************************************#
