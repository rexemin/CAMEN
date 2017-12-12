#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

"""
Nombre: main.py.
Autor: Iván A. Moreno Soto.
Fecha: 07/Diciembre/2016.

Este módulo contiene la función principal del programa.
"""

from Tkinter import *

from gui.menu import PanelPrincipal

"""
Crea la ventana principal e inicia el escuchador de eventos del programa.
"""
def main():
    root = Tk()

    root.title("CAMEN (CAlculadora de MÉtodos Numéricos) v1.0")

    ventana_principal = PanelPrincipal(root)

    root.mainloop()

#Ejecuta la función principal.
if __name__ == "__main__":
    main()
