#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: menu.py.
Autor: Iván A. Moreno Soto.
Fecha: 07/Diciembre/2016.

Este módulo contiene la clase que definen los menús del programa.
"""

#**************************************************************************************#

from tkinter import *

from gui.ventanas_raiz import *
from gui.ventanas_lineales import *
from gui.ventanas_ajuste import *
from gui.ventanas_integracion import *

from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Define una ventana que contiene el menú principal del programa.
"""
class PanelPrincipal(Toplevel):
    """
    Crea un PanelPrincipal. Agrega todos los elementos del menú principal.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__ (self, padre):
        self.padre = padre

        #-----------------------------------------------------------------------------------------------------------------------#

        menubar = Menu(self.padre)
        menubar.add_command(label="Acerca de", command=self.mostrarAcerca)

        self.padre.config(menu=menubar)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_polinomio = Button(self.padre, text="Solución de funciones no lineales", command=self.mostrarVentanaNoLineales)
        btn_polinomio.grid(row=0, column=0, sticky=W+E)

        lb_polinomio = Label(self.padre, text="Para aproximar raíces de funciones no lineales.")
        lb_polinomio.grid(row=0, column=1, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_sel = Button(self.padre, text="Solución de sistemas de ecuaciones lineales", command=self.mostrarVentanaLineales)
        btn_sel.grid(row=1, column=0, sticky=W+E)

        lb_sel = Label(self.padre, text="Para encontrar el vector de soluciones de un sistema de ecuaciones lineales.")
        lb_sel.grid(row=1, column=1, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_ajuste = Button(self.padre, text="Ajuste de funciones desconocidas por medio de polinomios", command=self.mostrarVentanaAjuste)
        btn_ajuste.grid(row=2, column=0, sticky=W+E)

        lb_ajuste = Label(self.padre, text="Para ajustar con un polinomio a un conjunto de puntos de una función desconocida.")
        lb_ajuste.grid(row=2, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------

        btn_integracion = Button(self.padre, text="Integración numérica de funciones", command=self.mostrarVentanaIntegracion)
        btn_integracion.grid(row=3, column=0, sticky=W+E)

        lb_integracion = Label(self.padre, text="Para aproximar numéricamente la integral definida de una función conocida o desconocida.")
        lb_integracion.grid(row=3, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------

        btn_salir = Button(self.padre, text="Salir", command=self.padre.quit)
        btn_salir.grid(row=4, column=0, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------

    """
    Muestra información sobre el programa en una ventana de diálogo emergente.
    """
    def mostrarAcerca (self):
        INTRODUCCION = "Este programa es una recopilación de cada método numérico visto en Análisis Numérico I.\nPara usar cada método use los botones que se presentan en cada menú, siempre podrá regresar\na la ventana anterior con los botones de 'Regresar'.\nGracias por usar este programa.\nHecho por Iván Alejandro Moreno Soto."

        mostrarAviso(INTRODUCCION)

    """
    Oculta esta ventana.
    """
    def ocultar(self):
        self.padre.withdraw()

    """
    Muestra esta ventana.
    """
    def mostrar(self):
        self.padre.update()
        self.padre.deiconify()

    """
    Muestra la ventana que tiene el menú de soluciones de funciones no lineales.
    """
    def mostrarVentanaNoLineales (self):
        self.ocultar()
        ventana_auxiliar = VentanaNoLineales(self)

    """
    Muestra la ventana que tiene el menú de soluciones de sistemas de ecuaciones lineales.
    """
    def mostrarVentanaLineales (self):
        self.ocultar()
        ventana_auxiliar = VentanaLineales(self)

    """
    Muestra la ventana que tiene el menú de ajuste de curvas.
    """
    def mostrarVentanaAjuste (self):
        self.ocultar()
        ventana_auxiliar = VentanaAjuste(self)

    """
    Muestra la ventana que tiene el menú de integración numérica.
    """
    def mostrarVentanaIntegracion (self):
        self.ocultar()
        ventana_auxiliar = VentanaIntegracion(self)

#**************************************************************************************#

"""
Define una ventana que muestra el menú de métodos numéricos para la solución de funciones
no lineales.
"""
class VentanaNoLineales(Toplevel, object):
    """
    Crea una VentanaNoLineales. Agrega todos los botones que permiten accesar a los métodos
    numéricos.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__ (self, padre):
        super(VentanaNoLineales, self).__init__()

        self.padre = padre

        #-----------------------------------------------------------------------------------------------------------------------

        grupo_no_lineales = LabelFrame(self, text="Solución de funciones no lineales", padx=5, pady=5)
        grupo_no_lineales.grid(sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------

        btn_biseccion = Button(grupo_no_lineales, text="Método de bisección", command=self.mostrarVentanaBiseccion)
        btn_biseccion.grid(row=0, column=0, sticky=W+E)

        lb_biseccion = Label(grupo_no_lineales, text="Aproximación a la raíz de una función por medio de bisección.")
        lb_biseccion.grid(row=0, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regla = Button(grupo_no_lineales, text="Método de regla falsa", command=self.mostrarVentanaReglaFalsa)
        btn_regla.grid(row=1, column=0, sticky=W+E)

        lb_regla = Label(grupo_no_lineales, text="Aproximación a la raíz de una función por medio de regla falsa.")
        lb_regla.grid(row=1, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_punto_fijo = Button(grupo_no_lineales, text="Método de punto fijo", command=self.mostrarVentanaPuntoFijo)
        btn_punto_fijo.grid(row=2, column=0, sticky=W+E)

        lb_punto_fijo = Label(grupo_no_lineales, text="Aproximación a la raíz de una función por medio del punto fijo de otra función.")
        lb_punto_fijo.grid(row=2, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_newton = Button(grupo_no_lineales, text="Método de Newton-Raphson", command=self.mostrarVentanaNewtonRaphson)
        btn_newton.grid(row=3, column=0, sticky=W+E)

        lb_newton = Label(grupo_no_lineales, text="Aproximación a la raíz de una función por medio de Newton-Raphson.")
        lb_newton.grid(row=3, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_secante = Button(grupo_no_lineales, text="Método de la secante", command=self.mostrarVentanaSecante)
        btn_secante.grid(row=4, column=0, sticky=W+E)

        lb_secante = Label(grupo_no_lineales, text="Aproximación a la raíz de una función por medio de una secante.")
        lb_secante.grid(row=4, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=5, column=0, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

        #-----------------------------------------------------------------------------------------------------------------------#

    """
    Oculta esta ventana.
    """
    def ocultar(self):
        self.withdraw()

    """
    Muestra esta ventana.
    """
    def mostrar(self):
        self.deiconify()

    """
    Muestra la ventana que permite realizar el método de bisección.
    """
    def mostrarVentanaBiseccion (self):
        self.ocultar()
        ventana_auxiliar = VentanaBiseccion(self)

    """
    Muestra la ventana que permite realizar el método de regla falsa.
    """
    def mostrarVentanaReglaFalsa (self):
        self.ocultar()
        ventana_auxiliar = VentanaReglaFalsa(self)

    """
    Muestra la ventana que permite realizar el método de punto fijo.
    """
    def mostrarVentanaPuntoFijo (self):
        self.ocultar()
        ventana_auxiliar = VentanaPuntoFijo(self)

    """
    Muestra la ventana que permite realizar el método de Newton-Raphson.
    """
    def mostrarVentanaNewtonRaphson (self):
        self.ocultar()
        ventana_auxiliar = VentanaNewtonRaphson(self)

    """
    Muestra la ventana que permite realizar el método de secante.
    """
    def mostrarVentanaSecante (self):
        self.ocultar()
        ventana_auxiliar = VentanaSecante(self)

    """
    Cierra esta ventana y muestra el menú principal.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Define una ventana que muestra el menú de métodos numéricos para la solución de sistemas
de ecuaciones lineales.
"""
class VentanaLineales(Toplevel, object):
    """
    Crea una VentanaLineales. Agrega todos los botones que permiten accesar a los métodos
    numéricos.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__ (self, padre):
        super(VentanaLineales, self).__init__()

        self.padre = padre

        #-----------------------------------------------------------------------------------------------------------------------#

        grupo_lineales = LabelFrame(self, text="Solución de sistemas de ecuaciones lineales", padx=5, pady=5)
        grupo_lineales.grid(sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_gs = Button(grupo_lineales, text="Método gaussiano simple", command=self.mostrarVentanaGaussSimple)
        btn_gs.grid(row=0, column=0, sticky=W+E)

        lb_gs = Label(grupo_lineales, text="Aplica eliminación gaussiana simple con sustitución hacia atrás aplicando redondeo.")
        lb_gs.grid(row=0, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_gspp = Button(grupo_lineales, text="Método gaussiano simple con pivoteo parcial", command=self.mostrarVentanaGaussPP)
        btn_gspp.grid(row=1, column=0, sticky=W+E)

        lb_gspp = Label(grupo_lineales, text="Aplica eliminación gaussiana con pivoteo parcial y sustitución hacia atrás.")
        lb_gspp.grid(row=1, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_jordan = Button(grupo_lineales, text="Método de Gauss-Jordan", command=self.mostrarVentanaJordan)
        btn_jordan.grid(row=2, column=0, sticky=W+E)

        lb_jordan = Label(grupo_lineales, text="Aplica el método de Gauss-Jordan para encontrar la inversa del SEL y resolver con (A^1)b = X aplicando redondeo")
        lb_jordan.grid(row=2, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_jacobi = Button(grupo_lineales, text="Método iterativo de Jacobi", command=self.mostrarVentanaJacobi)
        btn_jacobi.grid(row=3, column=0, sticky=W+E)

        lb_jacobi = Label(grupo_lineales, text="Aplica el método iterativo de Jacobi iniciando con la solución trivial.")
        lb_jacobi.grid(row=3, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_seidel = Button(grupo_lineales, text="Método iterativo de Gauss-Seidel", command=self.mostrarVentanaSeidel)
        btn_seidel.grid(row=4, column=0, sticky=W+E)

        lb_seidel = Label(grupo_lineales, text="Aplica el método iterativo de Gauss-Seidel iniciando con la solución trivial.")
        lb_seidel.grid(row=4, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_lu = Button(grupo_lineales, text="Método de factorización en LU", command=self.mostrarVentanaFactorizacion)
        btn_lu.grid(row=5, column=0, sticky=W+E)

        lb_lu = Label(grupo_lineales, text="Factoriza el SEL en LU mediante el método directo de Doolittle.")
        lb_lu.grid(row=5, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=6, column=0, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

        #-----------------------------------------------------------------------------------------------------------------------#

    """
    Muestra la ventana que permite realizar Gauss simple.
    """
    def mostrarVentanaGaussSimple (self):
        self.ocultar()
        ventana_auxiliar = VentanaGaussSimple(self)

    """
    Muestra la ventana que permite realizar Gauss con pivoteo parcial.
    """
    def mostrarVentanaGaussPP (self):
        self.ocultar()
        ventana_auxiliar = VentanaGaussPivoteo(self)

    """
    Muestra la ventana que permite realizar Gauss-Jordan.
    """
    def mostrarVentanaJordan (self):
        self.ocultar()
        ventana_auxiliar = VentanaGaussJordan(self)

    """
    Muestra la ventana que permite realizar Jacobi.
    """
    def mostrarVentanaJacobi (self):
        self.ocultar()
        ventana_auxiliar = VentanaJacobi(self)

    """
    Muestra la ventana que permite realizar Gauss-Seidel.
    """
    def mostrarVentanaSeidel (self):
        self.ocultar()
        ventana_auxiliar = VentanaGaussSeidel(self)

    """
    Muestra la ventana que permite realizar fatorización en LU.
    """
    def mostrarVentanaFactorizacion (self):
        self.ocultar()
        ventana_auxiliar = VentanaFactorizacion(self)

    """
    Oculta esta ventana.
    """
    def ocultar(self):
        self.withdraw()

    """
    Muestra esta ventana.
    """
    def mostrar(self):
        self.deiconify()

    """
    Cierra esta ventana y muestra el menú principal.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Define una ventana que muestra el menú de métodos numéricos para el ajuste de funciones
desconocidas.
"""
class VentanaAjuste(Toplevel, object):
    """
    Crea una VentanaAjuste. Agrega todos los botones que permiten accesar a los métodos
    numéricos.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__ (self, padre):
        super(VentanaAjuste, self).__init__()

        self.padre = padre

        #-----------------------------------------------------------------------------------------------------------------------#

        grupo_ajuste = LabelFrame(self, text="Ajuste de funciones desconocidas por medio de polinomios", padx=5, pady=5)
        grupo_ajuste.grid(sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_newton = Button(grupo_ajuste, text="Diferencias divididas de Newton", command=self.mostrarVentanaDiferencias)
        btn_newton.grid(row=0, column=0, sticky=W+E)

        lb_newton = Label(grupo_ajuste, text="Polinomio interpolante generado con las diferencias divididas de Newton.")
        lb_newton.grid(row=0, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_lagrange = Button(grupo_ajuste, text="Polinomio de Lagrange", command=self.mostrarVentanaLagrange)
        btn_lagrange.grid(row=1, column=0, sticky=W+E)

        lb_lagrange = Label(grupo_ajuste, text="Polinomio interpolante generado con la forma de Lagrange.")
        lb_lagrange.grid(row=1, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regresion = Button(grupo_ajuste, text="Regresión por medio de mínimos cuadrados", command=self.mostrarVentanaRegresion)
        btn_regresion.grid(row=2, column=0, sticky=W+E)

        lb_regresion = Label(grupo_ajuste, text="Para ajustar con un polinomio a un conjunto de puntos de una función desconocida.")
        lb_regresion.grid(row=2, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=3, column=0, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

        #-----------------------------------------------------------------------------------------------------------------------#

    """
    Muestra la ventana que permite realizar interpolación con diferencias divididas de Newton.
    """
    def mostrarVentanaDiferencias (self):
        self.ocultar()
        ventana_auxiliar = VentanaDiferencias(self)

    """
    Muestra la ventana que permite realizar interpolación con el polinomio de Lagrange.
    """
    def mostrarVentanaLagrange (self):
        self.ocultar()
        ventana_auxiliar = VentanaLagrange(self)

    """
    Muestra la ventana que permite realizar regresión polinomial.
    """
    def mostrarVentanaRegresion (self):
        self.ocultar()
        ventana_auxiliar = VentanaRegresion(self)

    """
    Oculta esta ventana.
    """
    def ocultar(self):
        self.withdraw()

    """
    Muestra esta ventana.
    """
    def mostrar(self):
        self.deiconify()

    """
    Cierra esta ventana y muestra el menú principal.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#

"""
Define una ventana que muestra el menú de métodos numéricos para la integración numérica
de funciones conocidas y desconocidas.
"""
class VentanaIntegracion(Toplevel, object):
    """
    Crea una VentanaIntegracion. Agrega todos los botones que permiten accesar a los métodos
    numéricos.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__ (self, padre):
        super(VentanaIntegracion, self).__init__()

        self.padre = padre

        #-----------------------------------------------------------------------------------------------------------------------#

        grupo_integracion = LabelFrame(self, text="Integración numérica de funciones", padx=5, pady=5)
        grupo_integracion.grid(sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_trapecio = Button(grupo_integracion, text="Método de los trapecios", command=self.mostrarVentanaTrapecio)
        btn_trapecio.grid(row=0, column=0, sticky=W+E)

        lb_trapecio = Label(grupo_integracion, text="Integración numérica por medio del uso de trapecios.")
        lb_trapecio.grid(row=0, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_simpson = Button(grupo_integracion, text="Regla de Simpson", command=self.mostrarVentanaSimpson)
        btn_simpson.grid(row=1, column=0, sticky=W+E)

        lb_simpson = Label(grupo_integracion, text="Integración numérica por medio del uso de parábolas y cúbicas.")
        lb_simpson.grid(row=1, column=1, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=2, column=0, columnspan=2, sticky=W+E)

        #-----------------------------------------------------------------------------------------------------------------------#

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

        #-----------------------------------------------------------------------------------------------------------------------#

    """
    Muestra la ventana que permite realizar integración por trapecios..
    """
    def mostrarVentanaTrapecio (self):
        self.ocultar()
        ventana_auxiliar = VentanaTrapecio(self)

    """
    Muestra la ventana que permite realizar integración con reglas de Simpson.
    """
    def mostrarVentanaSimpson (self):
        self.ocultar()
        ventana_auxiliar = VentanaSimpson(self)

    """
    Oculta esta ventana.
    """
    def ocultar(self):
        self.withdraw()

    """
    Muestra esta ventana.
    """
    def mostrar(self):
        self.deiconify()

    """
    Cierra esta ventana y muestra el menú principal.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#
