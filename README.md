# CAMEN (CAlculadora de MÉtodos Numéricos)

Programa con GUI que implementa métodos numéricos para ajuste de funciones, integración definida, búsqueda de raíces y resolución de sistemas de ecuaciones lineales.

Este programa fue hecho como proyecto final para una materia llamada "Análisis Numérico I" en 2016. Ahora está disponible para cualquiera que desee usarlo o modificarlo.

## Dependencias

Esta calculadora está programada en python 2.7 y ocupa los siguientes módulos:
* Tkinter
* [py_expression_eval](https://github.com/Axiacore/py-expression-eval)

## Ejecución

Para ser ejecutada sólo es necesario utilizar el siguiente comando en una terminal (dentro de la carpeta src):
    python CAMEN.py

## Funcionalidad

### Búsqueda de raíces en funciones no lineales

Calcula aproximaciones a las raíces de una función no lineal por medio de:
* Bisección
* Regla falsa
* Punto fijo
* Newton-Raphson
* Secante

### Resolución de sistemas de ecuaciones lineales

Métodos con redondeo:
* Gauss simple
* Gauss-Jordan

Métodos sin redondeo:
* Gauss simple con pivoteo parcial
* Jacobi
* Gauss-Seidel
* Factorización en LU

### Ajuste de funciones con polinomios

Genera un polinomio interpolante con:
* Diferencias divididas de Newton
* Polinomio de Lagrange
* Regresión por medio de mínimos cuadrados

### Integración numérica

* Método de los trapecios
* Regla de Simpson
