#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

#**************************************************************************************#

"""
Nombre: gestion_lineales.py.
Autor: Iván A. Moreno Soto.
Fecha: 08/Diciembre/2016

Este módulo contiene todas las funciones intermediarias entre los menús y los métodos numéricos de
solución de sistemas de ecuaciones lineales.
"""

#**************************************************************************************#

from tkinter import *

from metodos_numericos.sel.exacto import *
from metodos_numericos.sel.iterativo import *
from metodos_numericos.sel.operacion import verificarDominanciaDiagonal, redondearEntradasMatriz, escalarMatriz
from metodos_numericos.sel.operacion import escalarMatrizRedondeo, invertirMatrizRedondeo, multiplicarMatricesRedondeo
from metodos_numericos.sel.operacion import verificarErrorIdentidad, calcularDeterminanteTriangular
from metodos_numericos.excepcion.excepciones_metodos import NoHaySolucionUnicaExcepcion, MetodoFallidoExcepcion, DimensionNoCompatibleExcepcion
from metodos_numericos.excepcion.excepciones_metodos import IteracionesInvalidasExcepcion

from utilidades.impresion.matriz import imprimirMatriz
from utilidades.impresion.aviso import mostrarAviso

#**************************************************************************************#

"""
Gestiona la lectura del archivo de texto, el parseo de los parámetros introducidos por el usuario
y la realización de la eliminación gaussiana simple con sustitución hacia atrás.

Parámetros:
archivo -- Ruta del archivo de texto que contiene la matriz.
tolerancia -- Tolerancia para el error de las soluciones.
cifras -- Cifras con las que se aplicará redondeo.
iteraciones -- Número máximo de iteraciones que se realizará el proceso.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionGaussSimple (archivo, tolerancia, cifras, iteraciones, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        tolerancia_soluciones = abs((float)(tolerancia))
        cifras_redondeo = (int)(cifras)
        maximo_iteraciones = (int)(iteraciones)

        with open(archivo, 'r') as archivo_matriz:
            numero_ecuaciones = int(archivo_matriz.readline())

            if numero_ecuaciones >= 1:
                matriz = [list(map(float,line.split(' '))) for line in archivo_matriz if line.strip() != ""]

                area_texto.insert('end', '\n')
                area_texto.insert('end', "Sistema con ", str(numero_ecuaciones), " ecuaciones. \nMatriz capturada.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                redondearEntradasMatriz(matriz, cifras_redondeo)
                area_texto.insert('end', "Matriz capturada con redondeo aplicado a cada entrada.\n")
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                #Separa la matriz aumentada en la matriz asociada al SEL y el vector b de términos independientes.
                vector_b = [[matriz[i][numero_ecuaciones]] for i in range(0, numero_ecuaciones)]
                for i in range(0, len(matriz)):
                    del matriz[i][numero_ecuaciones]

                solucion = eliminacionGaussianaSimple(matriz, vector_b, tolerancia_soluciones, cifras_redondeo, maximo_iteraciones, area_texto)
                area_texto.insert('end', "\nSoluciones del sistema:\n")
                imprimirMatriz(solucion, area_texto)
            else:
                area_texto.insert('end', "El número de ecuaciones capturado es menor a 1, por favor revise su archivo de texto.")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt. ")
        area_texto.insert('end', "Por favor revise el campo de texto.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de las entradas de la matriz o alguno de los datos de los campos. Se detectó un valor no numérico.")
        area_texto.insert('end', "Por favor revise el archivo de texto.")
    except NoHaySolucionUnicaExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except DimensionNoCompatibleExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except NumeroCifrasRedondeoExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje)
    except IteracionesInvalidasExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje)
    except MetodoFallidoExcepcion as exc5:
        area_texto.insert('end', exc5.mensaje)
    except Exception as exc6:
        area_texto.insert('end', "Ha ocurrido un error: " + exc6.message)

#**************************************************************************************#

"""
Gestiona la lectura del archivo que contiene la matriz, el parseo de la tolerancia para
la cercanía a 0 del determinante y la verificación de la dominancia diagonal de una matriz.

Parámetros:
archivo -- Ruta del archivo de texto que contiene la matriz.
tolerancia -- Tolerancia para la cercanía a 0 del determinante.
area_texto -- Área de texto donde el proceso será imprimido.

Valor devuelto: Matriz triangular superior que queda al aplicar eliminación gaussiana con
pivoteo parcial. None si el proceso falla.
"""
def gestionVerificacionDeterminante (archivo, tolerancia, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_matriz:
            numero_ecuaciones = int(archivo_matriz.readline())

            if numero_ecuaciones >= 1:
                matriz = [list(map(float,line.split(' '))) for line in archivo_matriz if line.strip() != ""]

                area_texto.insert('end', "Sistema con ", str(numero_ecuaciones), " ecuaciones.\nMatriz capturada.\n")
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                escalarMatriz(matriz)

                area_texto.insert('end', "\nMatriz escalada.\n")
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                tolerancia_determinante = (float)(tolerancia)

                """
                1. Devuelve la matriz triangular superior.
                2. Devuelve el numero de intercambios de renglon.
                """
                matriz_ts = eliminacionGaussianaPivoteoParcial(matriz)

                area_texto.insert('end', "\nMatriz triangular superior luego de ser aplicada eliminación gaussiana con pivoteo parcial.\n")
                imprimirMatriz(matriz_ts[0], area_texto)
                area_texto.insert('end', '\n')

                determinante = calcularDeterminanteTriangular(matriz_ts[0], matriz_ts[1])

                area_texto.insert('end', "\nEl determinante de la matriz triangular superior es: " + str(determinante) + "\n")

                if abs(determinante) < tolerancia_determinante:
                    mostrarAviso("El sistema está mal condicionado. Si de todos modos quiere continuar con el proceso, oprima el botón Calcular.")

                return matriz_ts[0]
            else:
                area_texto.insert('end', "El número de ecuaciones capturado es menor a 1, por favor revise su archivo de texto.")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt. ")
        area_texto.insert('end', "Por favor revise el campo de texto.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de las entradas de la matriz o alguno de los datos de los campos. Se detectó un valor no numérico. ")
        area_texto.insert('end', "Por favor revise el archivo de texto.")
    except NoHaySolucionUnicaExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except Exception as exc2:
        area_texto.insert('end', "Ha ocurrido un error: " + exc2.message)

#**************************************************************************************#

"""
Gestiona la sustitución hacia atrás de una matriz triangular superior donde fue realizada
eliminación gaussiana con pivoteo parcial.

Parámetros:
matriz -- Matriz triangular superior.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionGaussPivoteo (matriz, area_texto):
    try:
        area_texto.insert('end', "\nSe continuará con el proceso.\n")

        #Separa la matriz aumentada en la matriz asociada al SEL y el vector b de términos independientes.
        vector_b = [[matriz[i][len(matriz)]] for i in range(0, len(matriz))]
        for i in range(0, len(matriz)):
            del matriz[i][len(matriz)]

        area_texto.insert('end', '\n')
        soluciones = sustitucionHaciaAtras(matriz, vector_b)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "Soluciones del sistema original.")
        area_texto.insert('end', '\n')
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', '\n')
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguno de los datos. Por favor revise los campos de texto.")
    except Exception as exc:
        area_texto.insert('end', "Ha ocurrido un error: " + exc.message)

#**************************************************************************************#

"""
Gestiona la lectura del archivo que contiene la matriz, el parseo de parámetros introducidos por
el usuario y la verificación del error de la matriz identidad.

Parámetros:
archivo -- Ruta del archivo que contiene la matriz.
cifras -- Cifras con las que se aplicará redondeo.
tolerancia -- Tolerancia para el error de las entradas de la matriz identidad.
area_texto -- Área de texto donde el proceso será imprimido.

Valor devuelto: Tupla que contiene la matriz, su inversa y el vector de términos
independientes, en ese orden. None si el proceso falla.
"""
def gestionVerificacionIdentidad (archivo, cifras, tolerancia, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_matriz:
            numero_ecuaciones = int(archivo_matriz.readline())

            if numero_ecuaciones >= 1:
                matriz = [list(map(float,line.split(' '))) for line in archivo_matriz if line.strip() != ""]

                cifras_redondeo = (int)(cifras)

                redondearEntradasMatriz(matriz, cifras_redondeo)

                area_texto.insert('end', "Sistema con ", str(numero_ecuaciones), " ecuaciones.")
                area_texto.insert('end', "Matriz capturada con redondeo aplicado a cada entrada.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                escalarMatrizRedondeo(matriz, cifras_redondeo)

                area_texto.insert('end', "Matriz escalada.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                #Separa la matriz aumentada en la matriz asociada al SEL y el vector b de términos independientes.
                vector_b = [[matriz[i][numero_ecuaciones]] for i in range(0, numero_ecuaciones)]
                for i in range(0, len(matriz)):
                    del matriz[i][numero_ecuaciones]

                matriz_inversa = invertirMatrizRedondeo(matriz, cifras_redondeo)

                area_texto.insert('end', "Matriz inversa.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz_inversa, area_texto)
                area_texto.insert('end', '\n')

                tolerancia_acondicionamiento = (float)(tolerancia)

                identidad = multiplicarMatricesRedondeo(matriz_inversa, matriz, cifras_redondeo)

                area_texto.insert('end', "Matriz identidad.")
                area_texto.insert('end', '\n')
                imprimirMatriz(identidad, area_texto)
                area_texto.insert('end', '\n')

                if verificarErrorIdentidad(identidad, tolerancia_acondicionamiento, cifras_redondeo):
                    area_texto.insert('end', "La matriz está bien condicionada.\n")
                else:
                    mostrarAviso("La matriz está mal condicionada.\nSi quiere continuar, introduzca el máximo de iteraciones y la tolerancia del error en las soluciones,  y oprima el botón Calcular.")

                return matriz, matriz_inversa, vector_b
            else:
                area_texto.insert('end', "El número de ecuaciones capturado es menor a 1, por favor revise su archivo de texto.")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt. ")
        area_texto.insert('end', "Por favor revise el campo de texto.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de las entradas de la matriz o alguno de los datos de los campos. Se detectó un valor no numérico. ")
        area_texto.insert('end', "Por favor revise el archivo de texto.")
    except NumeroCifrasRedondeoExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except NoHaySolucionUnicaExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except Exception as exc4:
        area_texto.insert('end', "Ha ocurrido un error: " + exc4.message)

#**************************************************************************************#

"""
Gestiona el parseo de parámetros introducidos por el usuario y la realización de la última
parte del método de Gauss-Jordan.

Parámetros:
matriz -- Matriz asociada al SEL.
matriz_inversa -- Matriz inversa de la anterior.
vector_b -- Vector de términos independientes.
tolerancia -- Tolerancia para el error en las soluciones.
cifras -- Cifras con las que se aplicará redondeo.
iteraciones -- Número máximo de iteraciones que se realizará el proceso.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionGaussJordan (matriz, matriz_inversa, vector_b, tolerancia, cifras, iteraciones, area_texto):
    try:
        maximo_iteraciones = (int)(iteraciones)
        tolerancia_soluciones = abs((float)(tolerancia))
        cifras_redondeo = (int)(cifras)

        area_texto.insert('end', "\nSe continuará con el proceso.\n")

        area_texto.insert('end', '\n')
        soluciones = calcularSolucionesGJ(matriz, matriz_inversa, vector_b, tolerancia_soluciones, cifras_redondeo, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "Soluciones del sistema.")
        area_texto.insert('end', '\n')
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', '\n')
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguno de los datos. Por favor revise los campos de texto.")
    except NumeroCifrasRedondeoExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except NoHaySolucionUnicaExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except DimensionNoCompatibleExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje)
    except IteracionesInvalidasExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje)
    except MetodoFallidoExcepcion as exc5:
        area_texto.insert('end', exc5.mensaje)
    except Exception as exc6:
        area_texto.insert('end', "Ha ocurrido un error: " + exc6.message)

#**************************************************************************************#

"""
Gestiona la lectura del archivo que contiene la matriz y la verificación de que sea
diagonalmente dominante.

Parámetros:
archivo -- Ruta del archivo que contiene la matriz.
area_texto -- Área de texto donde el proceso será imprimido.

Valor devuelto: Tupla que contiene la matriz en una configuración diagonalmente dominante
y el vector de términos independientes, en ese orden. None si el proceso falla.
"""
def gestionVerificacionDominanciaDiagonal (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_matriz:
            numero_ecuaciones = int(archivo_matriz.readline())

            if numero_ecuaciones >= 1:
                matriz = [list(map(float,line.split(' '))) for line in archivo_matriz if line.strip() != ""]

                area_texto.insert('end', "Sistema con ", str(numero_ecuaciones), " ecuaciones.")
                area_texto.insert('end', "Matriz capturada.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                #Separa la matriz aumentada en la matriz asociada al SEL y el vector b de términos independientes.
                vector_b = [[matriz[i][numero_ecuaciones]] for i in range(0, numero_ecuaciones)]
                for i in range(0, len(matriz)):
                    del matriz[i][numero_ecuaciones]

                if verificarDominanciaDiagonal(matriz, vector_b):
                    area_texto.insert('end', "La matriz está bien condicionada.\n")
                    area_texto.insert('end', "Matriz luego de la verificación:\n")
                    imprimirMatriz(matriz, area_texto)
                else:
                    mostrarAviso("La matriz no es diagonalmente dominante.\nSi quiere continuar, introduzca el máximo de iteraciones y oprima el botón.")

                return matriz, vector_b
            else:
                area_texto.insert('end', "El número de ecuaciones capturado es menor a 1, por favor revise su archivo de texto.")
    except IOError:
        area_texto.insert('end', "Ha ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt. ")
        area_texto.insert('end', "Por favor revise el campo de texto.")
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguna de las entradas de la matriz o alguno de los datos de los campos. Se detectó un valor no numérico. ")
        area_texto.insert('end', "Por favor revise el archivo de texto.")
    except Exception as exc4:
        area_texto.insert('end', "Ha ocurrido un error: " + exc4.message)

#**************************************************************************************#

"""
Gestiona el parseo de las iteraciones máximas y la tolerancia, y la realización de Jacobi.

Parámetros:
matriz -- Matriz diagonalmente dominante.
vector_b -- Vector de términos independientes.
iteraciones -- Máximo de iteraciones del proceso.
tolerancia -- Tolerancia para el error en las soluciones del sistema.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionJacobi (matriz, vector_b, iteraciones, tolerancia, area_texto):
    try:
        maximo_iteraciones = (int)(iteraciones)
        tolerancia_soluciones = abs((float)(tolerancia))

        area_texto.insert('end', "\nSe continuará con el proceso.\n")

        area_texto.insert('end', '\n')
        soluciones = jacobi(matriz, vector_b, tolerancia_soluciones, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "Soluciones del sistema original.")
        area_texto.insert('end', '\n')
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', '\n')
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguno de los datos. Por favor revise los campos de texto.")
    except NoHaySolucionUnicaExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except DimensionNoCompatibleExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except IteracionesInvalidasExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje)
    except MetodoFallidoExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje)
    except Exception as exc5:
        area_texto.insert('end', "Ha ocurrido un error: " + exc5.message)

#**************************************************************************************#

"""
Gestiona el parseo de las iteraciones máximas, la tolerancia y la realización de Gauss-Seidel.

Parámetros:
matriz -- Matriz diagonalmente dominante.
vector_b -- Vector de términos independientes.
iteraciones -- Máximo de iteraciones del proceso.
tolerancia -- Tolerancia para el error en las soluciones del sistema.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionGaussSeidel (matriz, vector_b, iteraciones, tolerancia, area_texto):
    try:
        maximo_iteraciones = (int)(iteraciones)
        tolerancia_soluciones = abs((float)(tolerancia))

        area_texto.insert('end', "\nSe continuará con el proceso.\n")

        area_texto.insert('end', '\n')
        soluciones = gaussSeidel(matriz, vector_b, tolerancia_soluciones, maximo_iteraciones, area_texto)

        area_texto.insert('end', '\n')
        area_texto.insert('end', "Soluciones del sistema original.")
        area_texto.insert('end', '\n')
        imprimirMatriz(soluciones, area_texto)
        area_texto.insert('end', '\n')
    except ValueError:
        area_texto.insert('end', "Ha ocurrido un error al leer alguno de los datos. Por favor revise los campos de texto.")
    except NoHaySolucionUnicaExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except DimensionNoCompatibleExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except IteracionesInvalidasExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje)
    except MetodoFallidoExcepcion as exc4:
        area_texto.insert('end', exc4.mensaje)
    except Exception as exc5:
        area_texto.insert('end', "Ha ocurrido un error: " + exc5.message)

#**************************************************************************************#

"""
Gestiona la lectura del archivo de texto y la realización de la factorización en LU.

Parámetros:
archivo -- Ruta del archivo de texto que contiene la matriz.
area_texto -- Área de texto donde el proceso será imprimido.
"""
def gestionFactorizacion (archivo, area_texto):
    area_texto.delete('1.0', 'end')

    #El bloque se encarga de cerrar automáticamente el archivo pase lo que pase.
    try:
        with open(archivo, 'r') as archivo_matriz:
            numero_ecuaciones = int(archivo_matriz.readline())

            if numero_ecuaciones >= 1:
                matriz = [list(map(float,line.split(' '))) for line in archivo_matriz if line.strip() != ""]

                tolerancia_cercania_cero = 0.0001

                area_texto.insert('end', "Sistema con ", str(numero_ecuaciones), " ecuaciones.")
                area_texto.insert('end', "\nMatriz capturada.")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz, area_texto)
                area_texto.insert('end', '\n')

                #Separa la matriz aumentada en la matriz asociada al SEL y el vector b de términos independientes.
                vector_b = [[matriz[i][numero_ecuaciones]] for i in range(0, numero_ecuaciones)]
                for i in range(0, len(matriz)):
                    del matriz[i][numero_ecuaciones]

                factorizacion = doolittle(matriz, vector_b, tolerancia_cercania_cero)
                matriz_l = factorizacion[0]
                matriz_u = factorizacion[1]

                area_texto.insert('end', '\n')
                area_texto.insert('end', "Matriz triangular inferior (L)")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz_l, area_texto)
                area_texto.insert('end', '\n')

                area_texto.insert('end', '\n')
                area_texto.insert('end', "Matriz triangular superior (U)")
                area_texto.insert('end', '\n')
                imprimirMatriz(matriz_u, area_texto)
                area_texto.insert('end', '\n')

                vector_y = sustitucionHaciaAdelante(matriz_l, vector_b)

                area_texto.insert('end', '\n')
                area_texto.insert('end', "Soluciones del sistema LY = b.")
                area_texto.insert('end', '\n')
                imprimirMatriz(vector_y, area_texto)
                area_texto.insert('end', '\n')

                soluciones = sustitucionHaciaAtras(matriz_u, vector_y)

                area_texto.insert('end', '\n')
                area_texto.insert('end', "Soluciones del sistema original.")
                area_texto.insert('end', '\n')
                imprimirMatriz(soluciones, area_texto)
                area_texto.insert('end', '\n')
            else:
                area_texto.insert('end', "El número de ecuaciones capturado es menor a 1, por favor revise su archivo de texto.")
    except IOError:
        area_texto.insert('end', "\nHa ocurrido un error al manejar el archivo de texto. Puede ser que el archivo no exista o haya faltado la extensión .txt. ")
        area_texto.insert('end', "Por favor revise el campo de texto.")
    except ValueError:
        area_texto.insert('end', "\nHa ocurrido un error al leer alguna de las entradas de la matriz o alguno de los datos de los campos. Se detectó un valor no numérico.")
        area_texto.insert('end', "Por favor revise el archivo de texto.")
    except NoHaySolucionUnicaExcepcion as exc:
        area_texto.insert('end', exc.mensaje)
    except DimensionNoCompatibleExcepcion as exc2:
        area_texto.insert('end', exc2.mensaje)
    except MetodoFallidoExcepcion as exc3:
        area_texto.insert('end', exc3.mensaje)
    except Exception as exc4:
        area_texto.insert('end', "\nHa ocurrido un error: " + exc4.message)

#**************************************************************************************#
