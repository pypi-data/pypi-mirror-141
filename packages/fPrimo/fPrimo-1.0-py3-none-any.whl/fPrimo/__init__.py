#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 03 23:10:20 2022
@author: carahyba
"""
def fPrimo(n):
    if type(n)==int and n < 2:
        return(print("Necesita poner un número mayor que dos."))
    elif type(n)!=int:
        return(print("Esta función acepta solamente números enteros."))
    i = 2
    vListaPrimo = []
    while i <= n:
        vEsPrimo = True
        for j in range(2,i):
            if(i%j == 0):
                vEsPrimo = False
        if(vEsPrimo):
            vListaPrimo.append(i)
        i += 1
    print('Lista de números primos:',vListaPrimo)
    if n in vListaPrimo:
        print('El número',n,'es primo.')
    else:
        print('El número',n,'no es primo.')
