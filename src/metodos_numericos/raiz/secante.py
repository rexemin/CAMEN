#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: secante.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 03/Diciembre/2016.

Contiene la función que realiza el proceso de la secante.
"""

#**************************************************************************************#

from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, NumeroCercanoCeroExcepcion, IteracionesInvalidasExcepcion
from metodos_numericos.error.errores import calcularErrorRelativo

from utilidades.impresion.tabla import imprimirRenglonTabla

#**************************************************************************************#

"""
Esta función se encarga de implementar el método de la secante para una función.

Parámetros:
funcion -- Función donde se buscará la raíz. Debe ser una expresión previamente
procesada por un parser.
a -- Punto de inicio del proceso.
b -- Punto de inicio del proceso.
tolerancia -- Tolerancia del error para los cálculos.
tolerancia_secante -- Tolerancia para la cercanía a ser horizontal de la secante.
maximo_iteraciones -- Máximo de iteraciones permitidas para que el proceso sea exitoso.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Lanza IteracionesInvalidasExcepcion si el número máximo de iteraciones es menor a 1.
Lanza NumeroCercanoCeroExcepcion cuando la secante se encuentra por debajo de la tolerancia.
Lanza MetodoFallidoExepcion cuando se alcanza el número máximo de iteraciones y no se ha
encontrado una aproximación tolerable de la raíz.
"""
def secante(funcion, a, b, tolerancia, tolerancia_secante, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    punto_anterior_2 = a
    punto_anterior_1 = b

    evaluacion_funcion_anterior_2 = funcion.evaluate({'x': punto_anterior_2})
    evaluacion_funcion_anterior_1 = funcion.evaluate({'x': punto_anterior_1})

    imprimirRenglonTabla([0, punto_anterior_2, evaluacion_funcion_anterior_2, ''], area_texto)
    imprimirRenglonTabla([1, punto_anterior_1, evaluacion_funcion_anterior_1, ''], area_texto)

    if evaluacion_funcion_anterior_2 == 0:
        return punto_anterior_2

    if evaluacion_funcion_anterior_1 == 0:
        return punto_anterior_1

    for i in range(1, maximo_iteraciones + 1):
        diferencia_evaluaciones = evaluacion_funcion_anterior_1 - evaluacion_funcion_anterior_2

        if abs(diferencia_evaluaciones) <= tolerancia_secante:
            raise NumeroCercanoCeroExcepcion

        punto_actual = punto_anterior_2 - ( ( evaluacion_funcion_anterior_2 * (punto_anterior_1 - punto_anterior_2) ) / diferencia_evaluaciones)

        evaluacion_funcion_anterior_2 = evaluacion_funcion_anterior_1
        evaluacion_funcion_anterior_1 = funcion.evaluate({'x': punto_actual})

        error = calcularErrorRelativo(punto_actual, punto_anterior_1)

        imprimirRenglonTabla([i, punto_actual, evaluacion_funcion_anterior_1, error], area_texto)

        if evaluacion_funcion_anterior_1 == 0 or error <= tolerancia:
            return punto_actual

        punto_anterior_2 = punto_anterior_1
        punto_anterior_1 = punto_actual

    #El procedimiento ha fallado.
    raise MetodoFallidoExcepcion

#**************************************************************************************#
