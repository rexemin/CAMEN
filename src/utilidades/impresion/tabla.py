#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: tabla.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016

Este módulo contiene funciones que se encargan de imprimir tablas en áreas de texto.
"""

#**************************************************************************************#

"""
Imprime una tabla de datos. Utiliza la separación de tabulador que el área de texto
tiene.

Parámetros:
titulos -- Títulos de las columnas de la tabla.
datos -- Cada fila de la tabla. Deben estar en un arreglo bidimensional.
area_texto --  Área de texto donde será puesta la tabla.
"""
def imprimirTabla (titulos, datos, area_texto):
    imprimirEncabezadoTabla(titulos, area_texto)

    for fila in datos:
        imprimirRenglonTabla(fila, area_texto)

#**************************************************************************************#

"""
Imprime el encabezado de una tabla. Usa la separación de tabulador que el área de
texto tiene.

Parámetros:
titulos -- Títulos de las columnas de la tabla.
area_texto -- Área de texto donde será puesto el encabezado.
"""
def imprimirEncabezadoTabla (titulos, area_texto):
    encabezado = ""

    for elemento in titulos:
        encabezado = encabezado + elemento + "\t"

    area_texto.insert('end', encabezado + "\n", ('tabstyle', 'tabular'))

#**************************************************************************************#

"""
Imprime un renglón de manera tabulada. Usa la separación de tabulador que el área de
texto tiene.

Parámetros:
datos -- Valores de las columnas que serán imprimidas.
area_texto -- Área de texto donde serán puestos los datos.
"""
def imprimirRenglonTabla (datos, area_texto):
    renglon = ""

    for elemento in datos:
        renglon = renglon + str(elemento) + "\t"

    area_texto.insert('end', renglon + "\n", ('tabstyle', 'tabular'))

#**************************************************************************************#
