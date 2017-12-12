#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: aviso.py.
Autor: Iván A. Moreno Soto.
Fecha: 07/Diciembre/2016.

Este módulo contiene una función que permite mostrar ventanas de diálogo emergentes.
"""

#**************************************************************************************#

from Tkinter import Toplevel, Label

#**************************************************************************************#

"""
Muestra una ventana de diálogo emergente.

Parámetros:
mensaje -- Mensaje que contendrá la ventana.
"""
def mostrarAviso (mensaje):
    dialogo = Toplevel()

    lb_mensaje = Label(dialogo, text=mensaje)
    lb_mensaje.pack()

#**************************************************************************************#
