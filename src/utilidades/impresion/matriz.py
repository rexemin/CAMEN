#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: matriz.py.
Autor: Iván A. Moreno Soto.
Fecha: 06/Diciembre/2016

Este módulo contiene la función encargada de imprimir matrices en un área de texto.
"""

#**************************************************************************************#

"""
Esta función imprime las entradas de una matriz por renglones.

Parámetros:
matriz -- Matriz que será imprimida.
area_texto -- Área de texto donde será imprimida la matriz.
"""
def imprimirMatriz (matriz, area_texto):
    for renglon in matriz:
        for columna in renglon:
            area_texto.insert('end', str(columna) + "\t")
        area_texto.insert('end', '\n')

#**************************************************************************************#
