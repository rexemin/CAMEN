#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: ventanas_raiz.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016

Este módulo contiene todas las clases que definen las ventanas que permiten utilizar
cada método numérico para la aproximación de la raíz de funciones no lineales.
"""

#**************************************************************************************#

from Tkinter import *

from utilidades.gestion.gestion_no_lineales import *
from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de bisección.
"""
class VentanaBiseccion (Toplevel):
    """
    Crea una VentanaBiseccion. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de bisección")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_funcion = Label(self, text="Función:")
        lb_funcion.grid(row=0, column=0, sticky=W+E)

        self.e_funcion = Entry(self)
        self.e_funcion.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_lim_inf = Label(self, text="Límite inferior:")
        lb_lim_inf.grid(row=1, column=0, sticky=W+E)

        self.e_lim_inf = Entry(self)
        self.e_lim_inf.grid(row=1, column=1, sticky=W+E)

        lb_lim_sup = Label(self, text="Límite superior:")
        lb_lim_sup.grid(row=1, column=2, sticky=W+E)

        self.e_lim_sup = Entry(self)
        self.e_lim_sup.grid(row=1, column=3, sticky=W+E)

        lb_tolerancia = Label(self, text="Tolerancia para la cota del error: ")
        lb_tolerancia.grid(row=2, column=0, sticky=W+E)

        self.e_tolerancia = Entry(self)
        self.e_tolerancia.grid(row=2, column=1, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=2, column=2, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=2, column=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=180, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarBiseccion)
        btn_calcular.grid(row=3, column=1, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Introduza la expresión de la función utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp." + \
        "\nSe toma el valor absoluto de la tolerancia introducida."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de bisección.
    """
    def comenzarBiseccion (self):
        self.t_salida.config(state=NORMAL)
        gestionBiseccion(self.e_funcion.get(), self.e_lim_inf.get(), self.e_lim_sup.get(), self.e_tolerancia.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
de regla falsa.
"""
class VentanaReglaFalsa (Toplevel):
    """
    Crea una VentanaReglaFalsa. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de regla falsa")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_funcion = Label(self, text="Función:")
        lb_funcion.grid(row=0, column=0, sticky=W+E)

        self.e_funcion = Entry(self)
        self.e_funcion.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_lim_inf = Label(self, text="Límite inferior:")
        lb_lim_inf.grid(row=1, column=0, sticky=W+E)

        self.e_lim_inf = Entry(self)
        self.e_lim_inf.grid(row=1, column=1, sticky=W+E)

        lb_lim_sup = Label(self, text="Límite superior:")
        lb_lim_sup.grid(row=1, column=2, sticky=W+E)

        self.e_lim_sup = Entry(self)
        self.e_lim_sup.grid(row=1, column=3, sticky=W+E)

        lb_cifras = Label(self, text="Cifras significativas: ")
        lb_cifras.grid(row=2, column=0, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=1, to=20)
        self.sb_cifras.grid(row=2, column=1, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=2, column=2, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=2, column=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarReglaFalsa)
        btn_calcular.grid(row=3, column=1, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Introduza la expresión de la función utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de regla falsa.
    """
    def comenzarReglaFalsa (self):
        self.t_salida.config(state=NORMAL)
        gestionReglaFalsa(self.e_funcion.get(), self.e_lim_inf.get(), self.e_lim_sup.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
de punto fijo.
"""
class VentanaPuntoFijo (Toplevel):
    """
    Crea una VentanaPuntoFijo. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de punto fijo")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_funcion_f = Label(self, text="Función f(x):")
        lb_funcion_f.grid(row=0, column=0, sticky=W+E)

        self.e_funcion_f = Entry(self)
        self.e_funcion_f.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_funcion_g = Label(self, text="Función g(x):")
        lb_funcion_g.grid(row=1, column=0, sticky=W+E)

        self.e_funcion_g = Entry(self)
        self.e_funcion_g.grid(row=1, column=1, columnspan=3, sticky=W+E)

        lb_inicio = Label(self, text="Punto de inicio:")
        lb_inicio.grid(row=2, column=0, sticky=W+E)

        self.e_inicio = Entry(self)
        self.e_inicio.grid(row=2, column=1, sticky=W+E)

        lb_cifras = Label(self, text="Cifras significativas: ")
        lb_cifras.grid(row=2, column=2, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=1, to=20)
        self.sb_cifras.grid(row=2, column=3, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=3, column=0, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=3, column=1, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4c', width=90, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarPuntoFijo)
        btn_calcular.grid(row=3, column=2, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Introduza las expresiones de las funciones utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de punto fijo.
    """
    def comenzarPuntoFijo (self):
        self.t_salida.config(state=NORMAL)
        gestionPuntoFijo(self.e_funcion_f.get(), self.e_funcion_g.get(), self.e_inicio.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
de Newton-Raphson.
"""
class VentanaNewtonRaphson (Toplevel):
    """
    Crea una VentanaNewtonRaphson. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de Newton-Raphson")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_funcion = Label(self, text="Función f(x):")
        lb_funcion.grid(row=0, column=0, sticky=W+E)

        self.e_funcion = Entry(self)
        self.e_funcion.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_funcion_derivada = Label(self, text="Función f'(x):")
        lb_funcion_derivada.grid(row=1, column=0, sticky=W+E)

        self.e_funcion_derivada = Entry(self)
        self.e_funcion_derivada.grid(row=1, column=1, columnspan=3, sticky=W+E)

        lb_inicio = Label(self, text="Punto de inicio:")
        lb_inicio.grid(row=2, column=0, sticky=W+E)

        self.e_inicio = Entry(self)
        self.e_inicio.grid(row=2, column=1, sticky=W+E)

        lb_cifras = Label(self, text="Cifras significativas: ")
        lb_cifras.grid(row=2, column=2, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=1, to=20)
        self.sb_cifras.grid(row=2, column=3, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=3, column=0, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=3, column=1, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4c', width=120, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarNewtonRaphson)
        btn_calcular.grid(row=3, column=2, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Introduza las expresiones de las funciones utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de Newton-Raphson.
    """
    def comenzarNewtonRaphson (self):
        self.t_salida.config(state=NORMAL)
        gestionNewtonRaphson(self.e_funcion.get(), self.e_funcion_derivada.get(), self.e_inicio.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
de Secante.
"""
class VentanaSecante(Toplevel):
    """
    Crea una VentanaSecante. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de secante")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_funcion = Label(self, text="Función f(x):")
        lb_funcion.grid(row=0, column=0, sticky=W+E)

        self.e_funcion = Entry(self)
        self.e_funcion.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_inicio_a = Label(self, text="Punto de inicio (a):")
        lb_inicio_a.grid(row=1, column=0, sticky=W+E)

        self.e_inicio_a = Entry(self)
        self.e_inicio_a.grid(row=1, column=1, sticky=W+E)

        lb_inicio_b = Label(self, text="Punto de inicio (b):")
        lb_inicio_b.grid(row=1, column=2, sticky=W+E)

        self.e_inicio_b = Entry(self)
        self.e_inicio_b.grid(row=1, column=3, sticky=W+E)

        lb_cifras = Label(self, text="Cifras significativas: ")
        lb_cifras.grid(row=2, column=0, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=1, to=20)
        self.sb_cifras.grid(row=2, column=1, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=2, column=2, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=2, column=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=4, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=80, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=4, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarSecante)
        btn_calcular.grid(row=3, column=1, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Introduza la expresión de la función utilizando x para denotar la variable." + \
        "\nSe aceptan las operaciones básicas (+,-,*,/,^), PI, E, log, sin, cos, tan, asin, acos, atan y exp."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de Secante.
    """
    def comenzarSecante (self):
        self.t_salida.config(state=NORMAL)
        gestionSecante(self.e_funcion.get(), self.e_inicio_a.get(), self.e_inicio_b.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#
