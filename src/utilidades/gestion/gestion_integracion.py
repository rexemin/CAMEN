#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: gestion_integracion.py.
Autor: Iván A. Moreno Soto.
Fecha: 05/Diciembre/2016

Este módulo contiene todas las funciones intermediarias entre los menús y los métodos numéricos de integración.
"""

#**************************************************************************************#

from py_expression_eval import Parser

from utilidades.impresion.tabla import imprimirTabla

from metodos_numericos.integracion.integracion import *
from metodos_numericos.excepcion.excepciones_metodos import *

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar el método de trapecios con una función conocida.

Parámetros:
expresion -- Función a la cual se busca la integral.
a -- Límite inferior de la integral.
b -- Límite superior de la integral.
trapecios -- Cantidad de trapecios a usar.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionTrapecioConocida (expresion, a, b, trapecios, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar la función, por favor revise los campos.\n")
        return

    try:
        lim_inferior = (float)(a)
        lim_superior = (float)(b)

        if lim_inferior < lim_superior:
            numero_trapecios = (int)(trapecios)

            integral = integracionTrapecioConocida(funcion, lim_inferior, lim_superior, numero_trapecios)

            area_texto.insert('end', '\n')
            area_texto.insert('end', "La aproximación a la integral es: " + str(integral) + ".")
        else:
            area_texto.insert('end', "El límite superior debe ser mayor al inferior, por favor revise los campos.")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except NumeroParticionesInvalidoExcepcion as exc:
        area_texto.insert('end', exc.mensaje + "\n")
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error.\n" + exc2.message)

#**************************************************************************************#

"""
Gestiona la lectura de un archivo de texto para llevar a cabo el método de trapecios para
una función desconocida.

Parámetros:
archivo -- Ruta del archivo que contiene puntos y evaluaciones de la función desconocida.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionTrapecioDesconocida (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_funcion:
            datos_funcion = [list(map(float,line.split(' '))) for line in archivo_funcion if line.strip() != ""]
            encabezado = ["x_i", "f(x_i)"]

            area_texto.insert('end', "Datos capturados del archivo.")
            area_texto.insert('end', '\n')
            imprimirTabla(encabezado, datos_funcion, area_texto)

            integral = integracionTrapecioDesconocida(datos_funcion)

            area_texto.insert('end', '\n')
            area_texto.insert('end', "La aproximación a la integral es: " + str(integral) + ".")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de los datos conocidos de la función o el grado del polinomio.")
    except NumeroParticionesInvalidoExcepcion as exc:
        area_texto.insert('end', exc.mensaje + "\n")
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error. " + exc2.message)

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo el método de reglas de Simpson con una función conocida.

Parámetros:
expresion -- Función a la cual se busca la integral.
a -- Límite inferior de la integral.
b -- Límite superior de la integral.
n -- Cantidad de particiones del intervalo.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionSimpsonConocida (expresion, a, b, n, area_texto):
    area_texto.delete('1.0', 'end')

    parser = Parser()

    try:
        funcion = parser.parse(expresion)
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error al procesar la función, por favor revise los campos.\n")
        return

    try:
        lim_inferior = (float)(a)
        lim_superior = (float)(b)

        if lim_inferior < lim_superior:
            particiones = (int)(n)

            integral = integracionSimpsonConocida(funcion, lim_inferior, lim_superior, particiones)

            area_texto.insert('end', '\n')
            area_texto.insert('end', "La aproximación a la integral es: " + str(integral) + ".")
        else:
            area_texto.insert('end', "El límite superior debe ser mayor al inferior, por favor revise los campos.")
    except ValueError:
        area_texto.insert('end', "Uno o más de los valores introducidos no son numéricos. Por favor revise los campos.\n")
    except NumeroParticionesInvalidoExcepcion as exc:
        area_texto.insert('end', exc.mensaje + "\n")
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error.\n" + exc2.message)

#**************************************************************************************#

"""
Gestiona la lectura de un archivo de texto para llevar a cabo las reglas de Simpson para una
función desconocida.

Parámetros:
archivo -- Ruta del archivo que contiene puntos y evaluaciones de la función desconocida.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionSimpsonDesconocida (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_funcion:
            datos_funcion = [list(map(float,line.split(' '))) for line in archivo_funcion if line.strip() != ""]
            encabezado = ["x_i", "f(x_i)"]

            area_texto.insert('end', "Datos capturados del archivo.")
            area_texto.insert('end', '\n')
            imprimirTabla(encabezado, datos_funcion, area_texto)

            integral = integracionSimpsonDesconocida(datos_funcion)

            area_texto.insert('end', '\n')
            area_texto.insert('end', "La aproximación a la integral es: " + str(integral) + ".")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de los datos conocidos de la función o el grado del polinomio.")
    except NumeroParticionesInvalidoExcepcion as exc:
        area_texto.insert('end', exc.mensaje + "\n")
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error. " + exc2.message)

#**************************************************************************************#
