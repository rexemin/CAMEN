#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: gestion_no_lineales.py.
Autor: Iván A. Moreno Soto.
Fecha: 01/Diciembre/2016

Este módulo contiene todas las funciones intermediarias entre los menús y los métodos numéricos de solución
de funciones no lineales.
"""

#**************************************************************************************#

from py_expression_eval import Parser

from utilidades.impresion.tabla import imprimirEncabezadoTabla, imprimirRenglonTabla

from metodos_numericos.raiz.biseccion import biseccion
from metodos_numericos.raiz.regla_falsa import reglaFalsa
from metodos_numericos.raiz.punto_fijo import puntoFijo
from metodos_numericos.raiz.newton_raphson import newtonRaphson
from metodos_numericos.raiz.secante import secante
from metodos_numericos.error.errores import calcularTolerancia
from metodos_numericos.excepcion.excepciones_metodos import *

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo la bisección.

Parámetros:
expresion -- Función a la que se busca la raiz.
lim_inf -- Límite inferior del intervalo de búsqueda.
lim_sup -- Límite superior del intervalo de búsqueda.
tol -- Tolerancia para la cota del error.
max_iteraciones -- Máximo de iteraciones a realizar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionBiseccion (expresion, lim_inf, lim_sup, tol, max_iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar la función, por favor revise el campo.\n")
        return

    try:
        limite_inferior = (float)(lim_inf)
        limite_superior = (float)(lim_sup)
        tolerancia = abs((float)(tol))
        maximo_iteraciones = (int)(max_iteraciones)

        imprimirEncabezadoTabla(['n', 'a_n', 'b_n', 'p_n', 'f(a)', 'f(p)', 'error'], area_texto)

        raiz = biseccion(funcion, limite_inferior, limite_superior, tolerancia, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "La aproximación a la raíz es: " + str(raiz) + ".")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except IteracionesInvalidasExcepcion as exc:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc.mensaje + "\n")
    except IntervaloInvalidoExcepcion as exc2:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc2.mensaje + "\n")
    except IntervaloSinRaizExcepcion as exc3:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc3.mensaje + "\n")
    except MetodoFallidoExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje + "\n")
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error.\n")

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo la regla falsa.

Parámetros:
expresion -- Función a la cual se busca la raiz.
lim_inf -- Límite inferior del intervalo de búsqueda.
lim_sup -- Límite superior del intervalo de búsqueda.
cifras -- Cifras significativas para el cálculo de la tolerancia.
max_iteraciones -- Máximo de iteraciones a realizar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionReglaFalsa (expresion, lim_inf, lim_sup, cifras, max_iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar la función, por favor revise el campo.\n")
        return

    try:
        limite_inferior = (float)(lim_inf)
        limite_superior = (float)(lim_sup)
        cifras_significativas = (int)(cifras)
        tolerancia = calcularTolerancia(cifras_significativas)
        maximo_iteraciones = (int)(max_iteraciones)

        imprimirEncabezadoTabla(['n', 'a_n', 'b_n', 'f(a_n)', 'f(b_n)', 'c_n', 'f(c_n)', 'error'], area_texto)

        raiz = reglaFalsa(funcion, limite_inferior, limite_superior, tolerancia, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "La aproximación a la raíz es: " + str(raiz) + ".")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except IteracionesInvalidasExcepcion as exc:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc.mensaje + "\n")
    except IntervaloInvalidoExcepcion as exc2:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc2.mensaje + "\n")
    except IntervaloSinRaizExcepcion as exc3:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc3.mensaje + "\n")
    except MetodoFallidoExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje + "\n")
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error.\n")

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo punto fijo.

Parámetros:
expresion_f -- Función a la cual se busca la raiz.
expresion_g -- Función a la cual se busca el punto fijo.
punto_inicio -- Punto de inicio de la búsqueda del punto fijo.
cifras -- Cifras significativas para el cálculo de la tolerancia.
max_iteraciones -- Máximo de iteraciones a realizar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionPuntoFijo (expresion_f, expresion_g, punto_inicio, cifras, max_iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion_f = parser.parse(expresion_f)
        funcion_g = parser.parse(expresion_g)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar las funciones, por favor revise los campos.\n")
        return

    try:
        inicio = (float)(punto_inicio)
        cifras_significativas = (int)(cifras)
        tolerancia = calcularTolerancia(cifras_significativas)
        maximo_iteraciones = (int)(max_iteraciones)

        imprimirEncabezadoTabla(['n', 'p_n', 'f(p_n)', 'error'], area_texto)

        raiz = puntoFijo(funcion_g, inicio, tolerancia, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "La aproximación a la raíz es: " + str(raiz) + ".")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except IteracionesInvalidasExcepcion as exc:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc.mensaje + "\n")
    except MetodoFallidoExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje + "\n")
    except Exception as exc3:
        area_texto.insert('end', "Ha ocurrido un error.\n" + exc3.message)

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo Newton-Raphson.

Parámetros:
expresion -- Función a la cual se busca la raiz.
expresion_derivada -- Derivada de la función anterior.
punto_inicio -- Punto de inicio de la búsqueda de Newton-Raphson.
cifras -- Cifras significativas para el cálculo de la tolerancia.
max_iteraciones -- Máximo de iteraciones a realizar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionNewtonRaphson (expresion, expresion_derivada, punto_inicio, cifras, max_iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
        derivada_funcion = parser.parse(expresion_derivada)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar las funciones, por favor revise los campos.\n")
        return

    try:
        inicio = (float)(punto_inicio)
        cifras_significativas = (int)(cifras)
        tolerancia = calcularTolerancia(cifras_significativas)
        maximo_iteraciones = (int)(max_iteraciones)

        imprimirEncabezadoTabla(['n', 'x_n', 'f(x_n)', 'f_derivada(x_n)', 'error'], area_texto)

        raiz = newtonRaphson(funcion, derivada_funcion, inicio, tolerancia, 0.0005, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "La aproximación a la raíz es: " + str(raiz) + ".")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except IteracionesInvalidasExcepcion as exc:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc.mensaje + "\n")
    except NumeroCercanoCeroExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje + "\n")
    except MetodoFallidoExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje + "\n")
    except Exception as exc4:
        area_texto.insert('end', "Ha ocurrido un error.\n" + exc4.message)

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo secante.

Parámetros:
expresion -- Función a la cual se busca la raiz.
a -- Primer punto de inicio de la búsqueda de secante.
b -- Segundo punto de inicio de la búsqueda de secante.
cifras -- Cifras significativas para el cálculo de la tolerancia.
max_iteraciones -- Máximo de iteraciones a realizar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionSecante (expresion, a, b, cifras, max_iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar las funciones, por favor revise los campos.\n")
        return

    try:
        inicio_a = (float)(a)
        inicio_b = (float)(b)
        cifras_significativas = (int)(cifras)
        tolerancia = calcularTolerancia(cifras_significativas)
        maximo_iteraciones = (int)(max_iteraciones)

        imprimirEncabezadoTabla(['n', 'x_n', 'f(x_n)', 'error'], area_texto)

        raiz = secante(funcion, inicio_a, inicio_b, tolerancia, 0.0005, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "La aproximación a la raíz es: " + str(raiz) + ".")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except IteracionesInvalidasExcepcion as exc:
        area_texto.delete('1.0', 'end')
        area_texto.insert('end', exc.mensaje + "\n")
    except NumeroCercanoCeroExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje + "\n")
    except MetodoFallidoExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje + "\n")
    except Exception as exc4:
        area_texto.insert('end', "Ha ocurrido un error.\n" + exc4.message)

#**************************************************************************************#
