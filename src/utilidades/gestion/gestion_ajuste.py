#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: gestion_ajuste.py.
Autor: Iván A. Moreno Soto.
Fecha: 04/Diciembre/2016

Este módulo contiene todas las funciones intermediarias entre los menús y los métodos numéricos
de ajuste de curvas.
"""

#**************************************************************************************#

from py_expression_eval import Parser

from metodos_numericos.ajuste.interpolacion import *
from metodos_numericos.ajuste.regresion import *
from metodos_numericos.excepcion.excepciones_metodos import *

from utilidades.impresion.tabla import imprimirTabla

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo la interpolación por diferencias divididas de Newton.

Parámetros:
archivo -- Ruta del archivo que contiene puntos y evaluaciones de la función desconocida.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionDiferencias (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_funcion:
            datos_funcion = [list(map(float,line.split(' '))) for line in archivo_funcion if line.strip() != ""]
            encabezado = ["x_i", "f(x_i)"]

            area_texto.insert('end', "Datos capturados del archivo.")
            imprimirTabla(encabezado, datos_funcion, area_texto)

            polinomio_aproximacion = interpolacionNewton(datos_funcion)

            area_texto.insert('end', "\nPolinomio de interpolación calculado:" + polinomio_aproximacion[0])

            return polinomio_aproximacion[1]
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de los datos conocidos de la función. Se detectó un valor no numérico.")
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error.")

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo la interpolación por polinomio de Lagrange.

Parámetros:
archivo -- Ruta del archivo que contiene puntos y evaluaciones de la función desconocida.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionLagrange (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_funcion:
            datos_funcion = [list(map(float,line.split(' '))) for line in archivo_funcion if line.strip() != ""]
            encabezado = ["x_i", "f(x_i)"]

            area_texto.insert('end', "Datos capturados del archivo.")
            imprimirTabla(encabezado, datos_funcion, area_texto)

            polinomio_aproximacion = interpolacionLagrange(datos_funcion)

            area_texto.insert('end', "\nPolinomio de interpolación calculado:" + polinomio_aproximacion[0])

            return polinomio_aproximacion[1]
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de los datos conocidos de la función. Se detectó un valor no numérico.")
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error.")

#**************************************************************************************#

"""
Gestiona el parseo de los parámetros introducidos por el usuario y los utiliza para
llevar a cabo la regresión por mínimos cuadrados.

Parámetros:
archivo -- Ruta del archivo que contiene puntos y evaluaciones de la función desconocida.
grado_polinomio -- Grado del polinomio de ajuste.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionRegresion (archivo, grado_polinomio, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        grado = (int)(grado_polinomio)

        with open(archivo, 'r') as archivo_funcion:
            datos_funcion = [list(map(float,line.split(' '))) for line in archivo_funcion if line.strip() != ""]
            encabezado = ["x_i", "f(x_i)"]

            area_texto.insert('end', "Datos capturados del archivo.")
            imprimirTabla(encabezado, datos_funcion, area_texto)

            polinomio_aproximacion = regresionPolinomial(datos_funcion, grado)

            area_texto.insert('end', "\nPolinomio de ajuste calculado:" + polinomio_aproximacion[0])

            return polinomio_aproximacion[1]
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de los datos conocidos de la función o el grado del polinomio.")
    except GradoPolinomioInvalidoExcepcion as exc:
        area_texto.insert('end', exc.mensaje + "\n")
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error. " + exc2.message)

#**************************************************************************************#
