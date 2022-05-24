#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: punto_fijo.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 03/Diciembre/2016.

Contiene la función que realiza el proceso de punto fijo.
"""

#**************************************************************************************#

from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, IteracionesInvalidasExcepcion
from metodos_numericos.error.errores import calcularErrorRelativo

from utilidades.impresion.tabla import imprimirRenglonTabla

#**************************************************************************************#

"""
Esta función se encarga de implementar el método de punto fijo para una función.

Parámetros:
funcion -- Función donde se buscará el punto fijo. Debe ser una expresión previamente
procesada por un parser.
punto_inicio -- Punto donde comienza el proceso de punto fijo.
tolerancia -- Tolerancia del error para los cálculos.
maximo_iteraciones -- Máximo de iteraciones permitidas para que el proceso sea exitoso.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Lanza IteracionesInvalidasExcepcion si el número máximo de iteraciones es menor a 1.
Lanza MetodoFallidoExepcion cuando se alcanza el número máximo de iteraciones y no se ha
encontrado una aproximación tolerable de la raíz.
"""
def puntoFijo(funcion, punto_inicio, tolerancia, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    #Primera iteración del punto fijo.
    punto_actual = funcion.evaluate({'x': punto_inicio})

    imprimirRenglonTabla([0, punto_inicio, punto_actual, ''], area_texto)

    if punto_actual == punto_inicio:
        return punto_actual

    for i in range(1, maximo_iteraciones + 1):
        punto_anterior = punto_actual

        punto_actual = funcion.evaluate({'x': punto_anterior})

        error = calcularErrorRelativo(punto_actual, punto_anterior)

        imprimirRenglonTabla([i, punto_anterior, punto_actual, error], area_texto)

        if punto_actual == punto_anterior or error <= tolerancia:
            return punto_actual

    #El procedimiento ha fallado.
    raise MetodoFallidoExcepcion

#**************************************************************************************#
