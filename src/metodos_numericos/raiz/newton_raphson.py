#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: newton_raphson.py.
Autor: Iván Alejandro Moreno Soto.
Fecha: 03/Diciembre/2016.

Contiene la función que realiza el proceso de Newton-Raphson.
"""

#**************************************************************************************#

from metodos_numericos.excepcion.excepciones_metodos import MetodoFallidoExcepcion, NumeroCercanoCeroExcepcion, IteracionesInvalidasExcepcion
from metodos_numericos.error.errores import calcularErrorRelativo

from utilidades.impresion.tabla import imprimirRenglonTabla

#**************************************************************************************#

"""
Esta función se encarga de implementar el método de Newton-Rapson para una función.

Parámetros:
funcion -- Función donde se buscará la raíz. Debe ser una expresión previamente
procesada por un parser.
derivada_funcion -- Derivada de la función anterior; también debe ser procesada previamente por un parser.
punto_inicio -- Punto de inicio del proceso.
tolerancia -- Tolerancia del error para los cálculos.
tolerancia_derivada -- Tolerancia para la cercanía a 0 de la evaluación de la derivada de la función.
maximo_iteraciones -- Máximo de iteraciones permitidas para que el proceso sea exitoso.
area_texto -- Área de texto donde se imprimirá cada iteración del método.

Lanza IteracionesInvalidasExcepcion si el número máximo de iteraciones es menor a 1.
Lanza NumeroCercanoCeroExcepcion cuando la evaluación actual de la derivada se encuentra debajo de la tolerancia.
Lanza MetodoFallidoExepcion cuando se alcanza el número máximo de iteraciones y no se ha
encontrado una aproximación tolerable de la raíz.
"""
def newtonRaphson(funcion, derivada_funcion, punto_inicio, tolerancia, tolerancia_derivada, maximo_iteraciones, area_texto):
    if maximo_iteraciones < 1:
        raise IteracionesInvalidasExcepcion

    punto_actual = punto_inicio
    evaluacion_funcion = funcion.evaluate({'x': punto_actual})
    evaluacion_derivada = derivada_funcion.evaluate({'x': punto_actual})

    imprimirRenglonTabla([0, punto_actual, evaluacion_funcion, evaluacion_derivada, ''], area_texto)

    if evaluacion_funcion == 0:
        return punto_actual

    if abs(evaluacion_derivada) <= tolerancia_derivada:
        raise NumeroCercanoCeroExcepcion

    for i in range(1, maximo_iteraciones + 1):
        punto_anterior = punto_actual

        punto_actual = punto_anterior - (evaluacion_funcion/evaluacion_derivada)

        evaluacion_funcion = funcion.evaluate({'x': punto_actual})
        evaluacion_derivada = derivada_funcion.evaluate({'x': punto_actual})

        error = calcularErrorRelativo(punto_actual, punto_anterior)

        imprimirRenglonTabla([i, punto_actual, evaluacion_funcion, evaluacion_derivada, error], area_texto)

        if evaluacion_funcion == 0 or error <= tolerancia:
            return punto_actual

        if abs(evaluacion_derivada) <= tolerancia_derivada:
            raise NumeroCercanoCeroExcepcion

    #El procedimiento ha fallado.
    raise MetodoFallidoExcepcion

#**************************************************************************************#
