#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

"""
Autor: Iván A. Moreno Soto.
Fecha: 07/Diciembre/2016.

Subpaquete: metodos_numericos.sel

Este subpaquete contiene funciones para operar matrices y resolver sistemas de
ecuaciones lineales.

Contenidos:
metodos_numericos.sel.exacto
    eliminacionGaussianaSimple
    eliminacionGaussianaPivoteoParcial
    calcularSolucionesGJ
    doolittle
    sustitucionHaciaAdelante
    sustitucionHaciaAtras
    sustitucionHaciaAtrasRedondeo

metodos_numericos.sel.iterativo
    jacobi
    gaussSeidel

metodos_numericos.sel.operacion
    repeticionLista
    encontrarRenglonMenor
    encontrarRenglonMayor
    encontrarNumeroMayorLista
    encontrarNumeroMayorMatriz
    sumatoriaRenglon
    verificarDominanciaDiagonal
    verificarErrorIdentidad
    calcularDeterminanteTriangular
    permutarRenglones
    operacionElementalRenglon
    operacionElementalRenglonRedondeo
    redondearEntradasMatriz
    escalarMatriz
    escalarMatrizRedondeo
    restarMatrices
    restarMatricesRedondeo
    multiplicarMatrices
    multiplicarMatricesRedondeo
    invertirMatrizRedondeo
    copiarMatriz
"""
