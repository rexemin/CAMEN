#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: ventanas_ajuste.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016

Este módulo contiene todas las clases que definen las ventanas que permiten utilizar
los métodos numéricos de ajuste de curvas.
"""

#**************************************************************************************#

from tkinter import *

from utilidades.gestion.gestion_ajuste import *
from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de interpolación con diferencias divididas de Newton.
"""
class VentanaDiferencias(Toplevel):
    """
    Crea una VentanaDiferencias. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Diferencias divididas de Newton")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=2, column=3, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=80, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=2, column=0, columnspan=3, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarDiferenciasDivididas)
        btn_calcular.grid(row=1, column=0, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=3, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Para generar el polinomio sólo se requiere que ponga los puntos y evaluaciones conocidas" + \
        "\nen un archivo de texto en dos columnas. La primera con los puntos y la segunda con las evaluaciones." + \
        "\nCada dato debe ser separado con un espacio y cada renglón del archivo será tomado como una fila."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de diferencias divididas.
    Luego, muestra elementos visuales que permiten la evaluación de un punto.
    """
    def comenzarDiferenciasDivididas (self):
        self.t_salida.config(state=NORMAL)
        self.funcion = gestionDiferencias(self.e_archivo.get(), self.t_salida)

        if self.funcion != None:
            self.t_salida.config(state=DISABLED)
            self.lb_punto = Label(self, text="Punto de evaluación:")
            self.lb_punto.grid(row=3, column=0, sticky=W+E)

            self.e_punto = Entry(self)
            self.e_punto.grid(row=3, column=1, sticky=W+E)

            self.btn_evaluar = Button(self, text="Evaluar", command=self.evaluarPunto)
            self.btn_evaluar.grid(row=3, column=2, sticky=W+E)

            self.e_evaluacion = Entry(self, state="readonly")
            self.e_evaluacion.grid(row=4, column=0, columnspan=3, sticky=W+E)

    """
    Evalúa un punto en el último polinomio interpolante calculado.
    """
    def evaluarPunto (self):
        self.e_evaluacion.config(state=NORMAL)
        self.e_evaluacion.delete(0, END)

        try:
            punto = (float)(self.e_punto.get())
            self.e_evaluacion.insert(INSERT, "P(x) = " + str(self.funcion.evaluate({'x': punto})))
        except ValueError:
            self.e_evaluacion.insert(INSERT, "El punto introducido no es un número, por favor revise el campo.")
        except AttributeError:
            self.e_evaluacion.insert(INSERT, "No hay polinomio interpolante calculado actualmente, primero introduza un archivo de texto.")

        self.e_evaluacion.config(state="readonly")

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de interpolación con polinomio de Lagrange.
"""
class VentanaLagrange(Toplevel):
    """
    Crea una VentanaLagrange. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Polinomio de Lagrange")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=2, column=3, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=80, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=2, column=0, columnspan=3, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarLagrange)
        btn_calcular.grid(row=1, column=0, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=3, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Para generar el polinomio sólo se requiere que ponga los puntos y evaluaciones conocidas" + \
        "\nen un archivo de texto en dos columnas. La primera con los puntos y la segunda con las evaluaciones." + \
        "\nCada dato debe ser separado con un espacio y cada renglón del archivo será tomado como una fila."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de Lagrange.
    Luego, muestra elementos visuales que permiten la evaluación de un punto.
    """
    def comenzarLagrange (self):
        self.t_salida.config(state=NORMAL)
        self.funcion = gestionLagrange(self.e_archivo.get(), self.t_salida)

        if self.funcion != None:
            self.t_salida.config(state=DISABLED)
            self.lb_punto = Label(self, text="Punto de evaluación:")
            self.lb_punto.grid(row=3, column=0, sticky=W+E)

            self.e_punto = Entry(self)
            self.e_punto.grid(row=3, column=1, sticky=W+E)

            self.btn_evaluar = Button(self, text="Evaluar", command=self.evaluarPunto)
            self.btn_evaluar.grid(row=3, column=2, sticky=W+E)

            self.e_evaluacion = Entry(self, state="readonly")
            self.e_evaluacion.grid(row=4, column=0, columnspan=3, sticky=W+E)

    """
    Evalúa un punto en el último polinomio interpolante calculado.
    """
    def evaluarPunto (self):
        self.e_evaluacion.config(state=NORMAL)
        self.e_evaluacion.delete(0, END)

        try:
            punto = (float)(self.e_punto.get())
            self.e_evaluacion.insert(INSERT, "P(x) = " + str(self.funcion.evaluate({'x': punto})))
        except ValueError:
            self.e_evaluacion.insert(INSERT, "El punto introducido no es un número, por favor revise el campo.")
        except AttributeError:
            self.e_evaluacion.insert(INSERT, "No hay polinomio interpolante calculado actualmente, primero introduza un archivo de texto.")

        self.e_evaluacion.config(state="readonly")

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de regresión polinomial con mínimos cuadrados.
"""
class VentanaRegresion(Toplevel):
    """
    Crea una VentanaRegresion. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Regresión con mínimos cuadrados")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_grado = Label(self, text="Grado del polinomio:")
        lb_grado.grid(row=1, column=0, sticky=W+E)

        self.e_grado = Entry(self)
        self.e_grado.grid(row=1, column=1, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=2, column=3, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='5c', width=80, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=2, column=0, columnspan=3, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarRegresion)
        btn_calcular.grid(row=1, column=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=3, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "Para generar el polinomio sólo se requiere que ponga los puntos y evaluaciones conocidas" + \
        "\nen un archivo de texto en dos columnas. La primera con los puntos y la segunda con las evaluaciones." + \
        "\nCada dato debe ser separado con un espacio y cada renglón del archivo será tomado como una fila."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de regresión.
    Luego, muestra elementos visuales que permiten la evaluación de un punto.
    """
    def comenzarRegresion (self):
        self.t_salida.config(state=NORMAL)
        self.funcion = gestionRegresion(self.e_archivo.get(), self.e_grado.get(), self.t_salida)

        if self.funcion != None:
            self.t_salida.config(state=DISABLED)
            self.lb_punto = Label(self, text="Punto de evaluación:")
            self.lb_punto.grid(row=3, column=0, sticky=W+E)

            self.e_punto = Entry(self)
            self.e_punto.grid(row=3, column=1, sticky=W+E)

            self.btn_evaluar = Button(self, text="Evaluar", command=self.evaluarPunto)
            self.btn_evaluar.grid(row=3, column=2, sticky=W+E)

            self.e_evaluacion = Entry(self, state="readonly")
            self.e_evaluacion.grid(row=4, column=0, columnspan=3, sticky=W+E)

    """
    Evalúa un punto en el último polinomio de ajuste calculado.
    """
    def evaluarPunto (self):
        self.e_evaluacion.config(state=NORMAL)
        self.e_evaluacion.delete(0, END)

        try:
            punto = (float)(self.e_punto.get())
            self.e_evaluacion.insert(INSERT, "P(x) = " + str(self.funcion.evaluate({'x': punto})))
        except ValueError:
            self.e_evaluacion.insert(INSERT, "El punto introducido no es un número, por favor revise el campo.")
        except AttributeError:
            self.e_evaluacion.insert(INSERT, "No hay polinomio de ajuste calculado actualmente, primero introduza un archivo de texto.")

        self.e_evaluacion.config(state="readonly")

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#
