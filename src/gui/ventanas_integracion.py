#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: ventanas_integracion.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016

Este módulo contiene todas las clases que definen las ventanas que permiten utilizar
los métodos numéricos de integración numérica.
"""

#**************************************************************************************#

from Tkinter import *

from utilidades.gestion.gestion_integracion import *
from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de integración numérica con el método de trapecios.
"""
class VentanaTrapecio(Toplevel):
    """
    Crea una VentanaTrapecio. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Integración numérica con trapecios")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        self.opcion = 1

        self.rbtn_funcion = Radiobutton(self, text="Función conocida", variable=self.opcion, value=1, command=self.mostrarFuncion)
        self.rbtn_funcion.grid(row=0, column=0, columnspan=2, sticky=W+E)

        self.rbtn_tabla = Radiobutton(self, text="Función desconocida", variable=self.opcion, value=0, command=self.mostrarTexto)
        self.rbtn_tabla.grid(row=0, column=2, columnspan=2, sticky=W+E)

        #Se declaran los elementos que se utilizarán.
        self.lb_funcion = Label(self, text="Función:")
        self.e_funcion = Entry(self)
        self.lb_lim_inf = Label(self, text="Límite inferior: ")
        self.e_lim_inf = Entry(self)
        self.lb_lim_sup = Label(self, text="Límite superior: ")
        self.e_lim_sup = Entry(self)
        self.lb_trapecios = Label(self, text="Cantidad de trapecios:")
        self.sb_trapecios = Spinbox(self, from_=1, to=2000)
        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarIntegracion)

        self.lb_texto = Label(self, text="Archivo de texto (con extensión .txt):")
        self.e_texto = Entry(self)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=95, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Para una función conocida introduza la expresión utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp." + \
        "\nPara integrar una función desconocida es necesario que ponga los valores conocidos en un" + \
        "\narchivo de texto con dos columnas. En la primera van los puntos y en la segunda las evaluaciones." + \
        "\nLos puntos deben estar a la misma distancia uno del otro, de lo contrario no se podrá integrar."
        mostrarAviso(AYUDA)

    """
    Muestra los elementos necesarios para integrar numéricamente una función conocida.
    """
    def mostrarFuncion (self):
        self.opcion = 1
        self.lb_texto.grid_remove()
        self.e_texto.grid_remove()
        self.lb_funcion.grid(row=1, column=0, sticky=W+E)
        self.e_funcion.grid(row=1, column=1, columnspan=3, sticky=W+E)
        self.lb_lim_inf.grid(row=2, column=0, sticky=W+E)
        self.e_lim_inf.grid(row=2, column=1, sticky=W+E)
        self.lb_lim_sup.grid(row=2, column=2, sticky=W+E)
        self.e_lim_sup.grid(row=2, column=3, sticky=W+E)
        self.lb_trapecios.grid(row=3, column=0, sticky=W+E)
        self.sb_trapecios.grid(row=3, column=1, sticky=W+E)
        self.btn_calcular.grid(row=3, column=2, columnspan=2, sticky=W+E)

    """
    Muestra los elementos necesarios para introducir el nombre de un archivo de texto para
    la integración de una función desconocida.
    """
    def mostrarTexto (self):
        self.opcion = 0
        self.lb_funcion.grid_remove()
        self.e_funcion.grid_remove()
        self.lb_lim_inf.grid_remove()
        self.e_lim_inf.grid_remove()
        self.lb_lim_sup.grid_remove()
        self.e_lim_sup.grid_remove()
        self.lb_trapecios.grid_remove()
        self.sb_trapecios.grid_remove()
        self.btn_calcular.grid_remove()

        self.lb_texto.grid(row=1, column=0, sticky=W+E)
        self.e_texto.grid(row=1, column=1, columnspan=3, sticky=W+E)
        self.btn_calcular.grid(row=2, column=0, columnspan=1, sticky=W+E)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión del método de
    trapecios.
    """
    def comenzarIntegracion (self):
        self.t_salida.config(state=NORMAL)
        if self.opcion == 1:
            gestionTrapecioConocida(self.e_funcion.get(), self.e_lim_inf.get(), self.e_lim_sup.get(), self.sb_trapecios.get(), self.t_salida)
        else:
            gestionTrapecioDesconocida(self.e_texto.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de integración numérica con las reglas de Simpson.
"""
class VentanaSimpson(Toplevel):
    """
    Crea una VentanaSimpson. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Integración numérica con reglas de Simpson")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        self.opcion = 1

        self.rbtn_funcion = Radiobutton(self, text="Función conocida", variable=self.opcion, value=1, command=self.mostrarFuncion)
        self.rbtn_funcion.grid(row=0, column=0, columnspan=2, sticky=W+E)

        self.rbtn_tabla = Radiobutton(self, text="Función desconocida", variable=self.opcion, value=0, command=self.mostrarTexto)
        self.rbtn_tabla.grid(row=0, column=2, columnspan=2, sticky=W+E)

        #Se declaran los elementos que se utilizarán.
        self.lb_funcion = Label(self, text="Función:")
        self.e_funcion = Entry(self)
        self.lb_lim_inf = Label(self, text="Límite inferior: ")
        self.e_lim_inf = Entry(self)
        self.lb_lim_sup = Label(self, text="Límite superior: ")
        self.e_lim_sup = Entry(self)
        self.lb_particiones = Label(self, text="Cantidad de particiones:")
        self.sb_particiones = Spinbox(self, from_=1, to=2000)
        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarIntegracion)

        self.lb_texto = Label(self, text="Archivo de texto (con extensión .txt):")
        self.e_texto = Entry(self)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=95, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Para una función conocida introduza la expresión utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp." + \
        "\nPara integrar una función desconocida es necesario que ponga los valores conocidos en un" + \
        "\narchivo de texto con dos columnas. En la primera van los puntos y en la segunda las evaluaciones." + \
        "\nLos puntos deben estar a la misma distancia uno del otro, de lo contrario no se podrá integrar."
        mostrarAviso(AYUDA)

    """
    Muestra los elementos necesarios para integrar numéricamente una función conocida.
    """
    def mostrarFuncion (self):
        self.opcion = 1
        self.lb_texto.grid_remove()
        self.e_texto.grid_remove()
        self.lb_funcion.grid(row=1, column=0, sticky=W+E)
        self.e_funcion.grid(row=1, column=1, columnspan=3, sticky=W+E)
        self.lb_lim_inf.grid(row=2, column=0, sticky=W+E)
        self.e_lim_inf.grid(row=2, column=1, sticky=W+E)
        self.lb_lim_sup.grid(row=2, column=2, sticky=W+E)
        self.e_lim_sup.grid(row=2, column=3, sticky=W+E)
        self.lb_particiones.grid(row=3, column=0, sticky=W+E)
        self.sb_particiones.grid(row=3, column=1, sticky=W+E)
        self.btn_calcular.grid(row=3, column=2, columnspan=2, sticky=W+E)

    """
    Muestra los elementos necesarios para introducir el nombre de un archivo de texto para
    la integración de una función desconocida.
    """
    def mostrarTexto (self):
        self.opcion = 0
        self.lb_funcion.grid_remove()
        self.e_funcion.grid_remove()
        self.lb_lim_inf.grid_remove()
        self.e_lim_inf.grid_remove()
        self.lb_lim_sup.grid_remove()
        self.e_lim_sup.grid_remove()
        self.lb_particiones.grid_remove()
        self.sb_particiones.grid_remove()
        self.btn_calcular.grid_remove()

        self.lb_texto.grid(row=1, column=0, sticky=W+E)
        self.e_texto.grid(row=1, column=1, columnspan=3, sticky=W+E)
        self.btn_calcular.grid(row=2, column=0, columnspan=1, sticky=W+E)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión del método de
    reglas de Simpson.
    """
    def comenzarIntegracion (self):
        self.t_salida.config(state=NORMAL)
        if self.opcion == 1:
            gestionSimpsonConocida(self.e_funcion.get(), self.e_lim_inf.get(), self.e_lim_sup.get(), self.sb_particiones.get(), self.t_salida)
        else:
            gestionSimpsonDesconocida(self.e_texto.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#
