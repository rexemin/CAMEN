#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: ventanas_lineales.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016

Este módulo contiene todas las clases que definen las ventanas que permiten utilizar
cada método para la solución de sistemas de ecuaciones lineales.
"""

#**************************************************************************************#

from tkinter import *

from utilidades.gestion.gestion_lineales import *
from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Esta clase define una ventana que contiene todo lo necesario para llevar a cabo el método
de eliminación gaussiana simple con sustitución hacia atrás.
"""
class VentanaGaussSimple (Toplevel):
    """
    Crea una VentanaGaussSimple. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Eliminación gaussiana simple")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_tolerancia = Label(self, text="Tolerancia para el error: ")
        lb_tolerancia.grid(row=1, column=0, sticky=W+E)

        self.e_tolerancia = Entry(self)
        self.e_tolerancia.grid(row=1, column=1, sticky=W+E)

        lb_cifras = Label(self, text="Cifras de redondeo:")
        lb_cifras.grid(row=1, column=2, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=2, to=20)
        self.sb_cifras.grid(row=1, column=3, sticky=W+E)

        lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        lb_max_iteraciones.grid(row=2, column=0, sticky=W+E)

        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.sb_max_iteraciones.grid(row=2, column=1, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=3, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=3, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarGaussSimple)
        btn_calcular.grid(row=2, column=2, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=4, column=1, columnspan=2, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación. Este método aplica el algoritmo para reducir errores de redondeo."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de Gauss simple.
    """
    def comenzarGaussSimple (self):
        self.t_salida.config(state=NORMAL)
        gestionGaussSimple(self.e_archivo.get(), self.e_tolerancia.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
de eliminación gaussiana con pivoteo parcial y sustitución hacia atrás.
"""
class VentanaGaussPivoteo(Toplevel):
    """
    Crea una VentanaGaussPivoteo. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de eliminación gaussiana con pivoteo parcial")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        self.lb_tolerancia = Label(self, text="Tolerancia para la cercanía a 0 del determinante:")
        self.lb_tolerancia.grid(row=1, column=0, sticky=W+E)

        self.e_tolerancia = Entry(self)
        self.e_tolerancia.grid(row=1, column=1, sticky=W+E)

        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarGaussPP)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=3, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=3, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_verificar = Button(self, text="Verificar", command=self.comenzarVerificacion)
        btn_verificar.grid(row=1, column=2, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=4, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación. Este método verifica si la matriz está bien condicionada calculando su determinante."
        mostrarAviso(AYUDA)

    """
    Toma los valores de los elementos gráficos y los manda a la gestión de verificación de condicionamiento.
    """
    def comenzarVerificacion (self):
        self.t_salida.config(state=NORMAL)
        self.matriz = gestionVerificacionDeterminante(self.e_archivo.get(), self.e_tolerancia.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

        if self.matriz != None:
            self.btn_calcular.grid(row=2, column=0, sticky=W+E)
        else:
            self.btn_calcular.grid_remove()

    """
    Manda la matriz calculada en la verificación y la manda a la gestión de la última parte
    de eliminación gaussiana con pivoteo parcial y sustitución hacia atrás.
    """
    def comenzarGaussPP (self):
        self.t_salida.config(state=NORMAL)
        gestionGaussPivoteo(self.matriz, self.t_salida)
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
de eliminacion de Gauss-Jordan.
"""
class VentanaGaussJordan(Toplevel):
    """
    Crea una VentanaGaussJordan. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método de eliminación de Gauss-Jordan")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        lb_cifras = Label(self, text="Cifras de redondeo:")
        lb_cifras.grid(row=1, column=0, sticky=W+E)

        self.sb_cifras = Spinbox(self, from_=2, to=20)
        self.sb_cifras.grid(row=1, column=1, sticky=W+E)

        self.lb_tolerancia_identidad = Label(self, text="Tolerancia para el error en la matriz identidad:")
        self.lb_tolerancia_identidad.grid(row=1, column=2, sticky=W+E)

        self.e_tolerancia_identidad = Entry(self)
        self.e_tolerancia_identidad.grid(row=1, column=3, sticky=W+E)

        self.lb_tolerancia_soluciones = Label(self, text="Tolerancia para el error en las soluciones:")
        self.e_tolerancia_soluciones = Entry(self)
        self.lb_max_iteraciones = Label(self, text="Número máximo de iteraciones del proceso:")
        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)
        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarSoluciones)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=5, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=5, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_verificar = Button(self, text="Verificar", command=self.comenzarVerificacion)
        btn_verificar.grid(row=2, column=1, columnspan=2, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=6, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación. Este método aplica el algoritmo para reducir errores de redondeo." + \
        "\nVerifica si la matriz está bien condicionada revisando el error de la matriz identidad al multiplicar la matriz por su inversa."
        mostrarAviso(AYUDA)

    """
    Toma los parámetros introducidos por el usuario y los manda a la gestión de verificación
    de condicionamiento.
    Luego muestra o remueve los elementos de la segunda parte.
    """
    def comenzarVerificacion (self):
        self.t_salida.config(state=NORMAL)
        self.matriz = gestionVerificacionIdentidad(self.e_archivo.get(), self.sb_cifras.get(), self.e_tolerancia_identidad.get(),self.t_salida)
        self.t_salida.config(state=DISABLED)

        if self.matriz != None:
            self.lb_tolerancia_soluciones.grid(row=3, column=0, sticky=W+E)
            self.e_tolerancia_soluciones.grid(row=3, column=1, sticky=W+E)
            self.lb_max_iteraciones.grid(row=3, column=2, sticky=W+E)
            self.sb_max_iteraciones.grid(row=3, column=3, sticky=W+E)
            self.btn_calcular.grid(row=4, column=1, columnspan=2, sticky=W+E)
        else:
            self.lb_tolerancia_soluciones.grid_remove()
            self.e_tolerancia_soluciones.grid_remove()
            self.lb_max_iteraciones.grid_remove()
            self.sb_max_iteraciones.grid_remove()
            self.btn_calcular.grid_remove()

    """
    Manda los parámetros del usuario a la segunda parte del proceso de Gauss-Jordan.
    """
    def comenzarSoluciones (self):
        self.t_salida.config(state=NORMAL)
        gestionGaussJordan(self.matriz[0], self.matriz[1], self.matriz[2], self.e_tolerancia_soluciones.get(), self.sb_cifras.get(), self.sb_max_iteraciones.get(), self.t_salida)
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
iterativo de Jacobi.
"""
class VentanaJacobi(Toplevel):
    """
    Crea una VentanaJacobi. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método iterativo de Jacobi")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=2, sticky=W+E)

        self.lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)

        self.lb_tolerancia = Label(self, text="Tolerancia para el error:")
        self.e_tolerancia = Entry(self)

        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarJacobi)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=3, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=3, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_verificar = Button(self, text="Verificar", command=self.comenzarVerificacion)
        btn_verificar.grid(row=0, column=3, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=4, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación. Este método verifica que la matriz sea diagonalmente dominante."
        mostrarAviso(AYUDA)

    """
    Toma los parámetros introducidos por el usuario y los manda a la gestión de verificación
    de condicionamiento.
    Luego muestra o remueve los elementos visuales de la segunda parte del proceso.
    """
    def comenzarVerificacion (self):
        self.t_salida.config(state=NORMAL)
        self.matriz = gestionVerificacionDominanciaDiagonal(self.e_archivo.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

        if self.matriz != None:
            self.lb_max_iteraciones.grid(row=1, column=0, sticky=W+E)
            self.sb_max_iteraciones.grid(row=1, column=1, sticky=W+E)
            self.lb_tolerancia.grid(row=1, column=2, sticky=W+E)
            self.e_tolerancia.grid(row=1, column=3, sticky=W+E)
            self.btn_calcular.grid(row=2, column=1, columnspan=2, sticky=W+E)
        else:
            self.lb_max_iteraciones.grid_remove()
            self.sb_max_iteraciones.grid_remove()
            self.lb_tolerancia.grid_remove()
            self.e_tolerancia.grid_remove()
            self.btn_calcular.grid_remove()

    """
    Obtiene el contenido de todos los campos de texto y los envía a la segunda parte de
    la gestión de Jacobi.
    """
    def comenzarJacobi (self):
        self.t_salida.config(state=NORMAL)
        gestionJacobi(self.matriz[0], self.matriz[1], self.sb_max_iteraciones.get(), self.e_tolerancia.get(), self.t_salida)
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
iterativo de Gauss-Seidel.
"""
class VentanaGaussSeidel(Toplevel):
    """
    Crea una VentanaGaussSeidel. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Método iterativo de Gauss-Seidel")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=2, sticky=W+E)

        self.lb_max_iteraciones = Label(self, text="Máximo de iteraciones:")
        self.sb_max_iteraciones = Spinbox(self, from_=1, to=500)

        self.lb_tolerancia = Label(self, text="Tolerancia para el error:")
        self.e_tolerancia = Entry(self)

        self.btn_calcular = Button(self, text="Calcular", command=self.comenzarGaussSeidel)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=3, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=3, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_verificar = Button(self, text="Verificar", command=self.comenzarVerificacion)
        btn_verificar.grid(row=0, column=3, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=4, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación. Este método verifica que la matriz sea diagonalmente dominante."
        mostrarAviso(AYUDA)

    """
    Toma los parámetros introducidos por el usuario y los manda a la gestión de verificación
    de condicionamiento.
    Luego muestra o remueve los elementos visuales de la segunda parte del proceso.
    """
    def comenzarVerificacion (self):
        self.t_salida.config(state=NORMAL)
        self.matriz = gestionVerificacionDominanciaDiagonal(self.e_archivo.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

        if self.matriz != None:
            self.lb_max_iteraciones.grid(row=1, column=0, sticky=W+E)
            self.sb_max_iteraciones.grid(row=1, column=1, sticky=W+E)
            self.lb_tolerancia.grid(row=1, column=2, sticky=W+E)
            self.e_tolerancia.grid(row=1, column=3, sticky=W+E)
            self.btn_calcular.grid(row=2, column=1, columnspan=2, sticky=W+E)
        else:
            self.lb_max_iteraciones.grid_remove()
            self.sb_max_iteraciones.grid_remove()
            self.lb_tolerancia.grid_remove()
            self.e_tolerancia.grid_remove()
            self.btn_calcular.grid_remove()

    """
    Obtiene el contenido de todos los campos de texto y los envía a la segunda parte de la
    gestión de Gauss-Seidel.
    """
    def comenzarGaussSeidel (self):
        self.t_salida.config(state=NORMAL)
        gestionGaussSeidel(self.matriz[0], self.matriz[1], self.sb_max_iteraciones.get(), self.e_tolerancia.get(), self.t_salida)
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
de factorización en LU.
"""
class VentanaFactorizacion(Toplevel):
    """
    Crea una VentanaFactorizacion. Agrega todos los elementos necesarios para capturar información
    del usuario.

    Parámetros:
    padre -- Ventana que está un nivel más arriba en la jerarquía de ventanas. Es quien manda a llamar
    a este constructor.
    """
    def __init__(self, padre):
        self.padre = padre
        Toplevel.__init__(self)
        self.title("Factorización en LU")

        menubar = Menu(self)
        menubar.add_command(label="Ayuda", command=self.mostrarAyuda)

        self.config(menu=menubar)

        lb_archivo = Label(self, text="Archivo de texto (con extensión .txt):")
        lb_archivo.grid(row=0, column=0, sticky=W+E)

        self.e_archivo = Entry(self)
        self.e_archivo.grid(row=0, column=1, columnspan=3, sticky=W+E)

        scb_salida = Scrollbar(self)
        scb_salida.grid(row=2, column=4, sticky=N+S)

        self.t_salida = Text(self, bd=5, padx=5, pady=5, tabs='4.3c', width=150, yscrollcommand=scb_salida.set)
        self.t_salida.grid(row=2, column=0, columnspan=4, sticky=W+E)
        self.t_salida.config(state=DISABLED)

        scb_salida.config(command=self.t_salida.yview)

        btn_calcular = Button(self, text="Calcular", command=self.comenzarFactorizacion)
        btn_calcular.grid(row=1, column=0, sticky=W+E)

        btn_regresar = Button(self, text="Regresar", command=self.alCerrar)
        btn_regresar.grid(row=3, column=0, columnspan=4, sticky=W+E)

        self.protocol("WM_DELETE_WINDOW", self.alCerrar)

    """
    Muestra instrucciones para este método en una ventana de diálogo emergente.
    """
    def mostrarAyuda (self):
        AYUDA = "El sistema de ecuaciones lineales es pasado a través de un archivo de texto que debe contener en la primera línea el número de ecuaciones." + \
        "\nDe la segunda línea en adelante debe contener los coeficientes de las incógnitas y los términos independientes separados por un espacio." + \
        "\nCada línea del archivo se tomará como una ecuación."
        mostrarAviso(AYUDA)

    """
    Obtiene el contenido de todos los campos de texto y los envía a la gestión de factorización en LU.
    """
    def comenzarFactorizacion (self):
        self.t_salida.config(state=NORMAL)
        gestionFactorizacion(self.e_archivo.get(), self.t_salida)
        self.t_salida.config(state=DISABLED)

    """
    Elimina esta ventana y muestra la padre.
    """
    def alCerrar(self):
        self.destroy()
        self.padre.mostrar()

#**************************************************************************************#
