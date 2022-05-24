# CAMEN (CAlculadora de MÉtodos Numéricos)

Programa con GUI que implementa métodos numéricos para ajuste de funciones, integración definida, búsqueda de raíces y resolución de sistemas de ecuaciones lineales.

Este programa fue hecho como proyecto final para una materia llamada "Análisis Numérico I" en 2016. Ahora está disponible para cualquiera que desee usarlo o modificarlo.

## Dependencias

Esta calculadora fue programada originalmente en python 2.7.x
([la versión compatible con Python 2 está en este commit](https://github.com/rexemin/CAMEN/tree/9a30e8c7fefb7ca8a08ef96b47c726821910e705)), 
pero ahora está porteada a Python
3.x. Ocupa los siguientes módulos:
* Tkinter
* [py_expression_eval](https://github.com/Axiacore/py-expression-eval)

### Tkinter

Para poder usar la GUI, es necesario tener Tkinter instalado en el sistema operativo.
En [este enlace](https://www.tcl.tk/software/tcltk/) hay instrucciones para hacerlo, 
y en [este otro](https://docs.python.org/3/library/tkinter.html#module-tkinter) hay 
información para validar la instalación.

### py_expression_eval

Para instalar este paquete solo es necesario usar `pip install py_expression_eval`,
o el archivo `requirements.txt` al usar el comando `pip install -r requirements.txt`.

## Ejecución

Para ser ejecutada sólo es necesario utilizar el siguiente comando en una terminal (dentro de la carpeta src): 

```
python CAMEN.py
```

## Funcionalidad

### Búsqueda de raíces en funciones no lineales

Calcula aproximaciones a las raíces de una función no lineal por medio de:
- Bisección
- Regla falsa
- Punto fijo
- Newton-Raphson
- Secante

### Resolución de sistemas de ecuaciones lineales

Métodos con redondeo:
- Gauss simple
- Gauss-Jordan

Métodos sin redondeo:
- Gauss simple con pivoteo parcial
- Jacobi
- Gauss-Seidel
- Factorización en LU

### Ajuste de funciones con polinomios

Genera un polinomio interpolante con:
- Diferencias divididas de Newton
- Polinomio de Lagrange
- Regresión por medio de mínimos cuadrados

### Integración numérica

- Método de los trapecios
- Regla de Simpson
