#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: excepciones_metodos.py.
Autor: Iván A. Moreno Soto.
Fecha: 02/Diciembre/2016.

Este archivo define excepciones que son lanzadas cuando algún método numérico presenta
fallas al momento de ejecución.
"""

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada cuando se detecta que
un sistema de ecuaciones lineales no tiene solución única.
"""
class NoHaySolucionUnicaExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "La matriz no tiene solución única."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos de integración numérica
cuando reciben un número inválido de cifras para el redondeo.
"""
class NumeroCifrasRedondeoExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Se ha detectado un número inválido de cifras de redondeo. El proceso debe usar al menos 2."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos de integración numérica
cuando reciben un número inválido de particiones.
"""
class NumeroParticionesInvalidoExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Se ha detectado un número inválido de particiones. El proceso debe usar al menos 1 partición."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos que usen un máximo de
iteraciones y encuentren que reciben un número negativo.
"""
class IteracionesInvalidasExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Se ha detectado un número inválido de iteraciones. El proceso debe realizarse al menos 1 vez."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos que encuentren que un intervalo
no es válido.
"""
class IntervaloInvalidoExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "El intervalo no se encuentra en un orden correcto, no se puede realizar el proceso."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos que aproximan raíces
cuando no se encuentre una raíz en un intervalo de una función.
"""
class IntervaloSinRaizExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "No se ha encontrado raíz en el intervalo especificado, no se puede realizar el proceso."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada por los métodos cuando encuentran
que un número está muy cerca de cero y no es seguro continuar el proceso.
"""
class NumeroCercanoCeroExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Se ha encontrado que un número se encuentra debajo de la tolerancia permitida de la cercanía a 0."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada cuando algún método numérico
que ocupa calcular un polinomio de grado n recibe un valor menor a 0.
"""
class GradoPolinomioInvalidoExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "El grado del polinomio no puede ser menor a 0."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada cuando algún método numérico
alcanza el número máximo de iteraciones de manera no satisfactoria.
"""
class MetodoFallidoExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Se ha alcanzado el número máximo de iteraciones. El proceso ha concluido sin éxito."

#**************************************************************************************#

"""
Esta clase define una excepción cuyo propósito es ser lanzada cuando dos matrices no posean dimensiones
que permitan que se puedan operar.
"""
class DimensionNoCompatibleExcepcion(Exception):
    """
    Constructor de la excepción. Agrega un mensaje denotando la causa de que sea lanzada.
    """
    def __init__(self):
        self.mensaje = "Las matrices no poseen dimensiones que permitan que sean operadas."

#**************************************************************************************#
