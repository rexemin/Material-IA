#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
spam_filter.py
------------

Archivo para poder generar un filtro de spam utilizando el método de
Naïve Bayes, en forma laplaciana. Esto es, cada palabra se considera
un atributo, el cual puede tener valores binarios (1 si se encuentra
en el mail y 0 si no se encuentra en el mail.)

Las clases tambien son binarias, 1 si son spam y 0 si no son spam.

Los datos ya vienen preprocesados.
"""

__author__ = 'Ivan Moreno'

from random import randint

import nb
from naive_bayes import error_clasif


def carga_datos(file_datos, file_clases):

    datos = []
    lineas = open(file_datos, 'r').readlines()
    for linea in lineas:
        datos.append([int(val) for val in linea.strip().strip(',').split(',')])

    clinea = open(file_clases).readline()
    clases = [int(cl) for cl in clinea.split()]

    return datos, clases


def carga_vocabulario():
    palabras = open('vocab.txt', 'r').readlines()
    return [palabra.strip().split()[1] for palabra in palabras]


def ejemplo_datos():
    datos, clases = carga_datos('mails.data', 'mails.class')
    vocabulario = carga_vocabulario()

    print("Datos: {} con dimensión {}".format(len(datos), len(datos[0])))
    print("Clases: {}".format(len(clases)))
    print("Vocabulario: {}".format(len(vocabulario)))

    print("Ejemplos de correos en los datos")
    print("--------------------------------\n")

    for _ in range(10):
        mail = randint(0, len(clases) - 1)
        print("\nPara el mail {} tenemos las palabras:\n\n".format(mail))
        print([vocabulario[i] for i in range(len(vocabulario))
               if datos[mail][i] == 1])
        print("\ny el mail {}".format("es spam" if clases[mail] == 1
                                      else "no es spam"))
        print("\n" + 20*'-')


def spam_filter():
    """
    Filtro spam a desarrollar para reconocer si un correo es spam o no.

    Para obtener los datos de aprendizaje se puede utilizar
        datos, clases = carga_datos('mails.data','mails.class')

    Mientras que para obtener los datos de prueba se puede utilizar
        datos, clases = carga_datos('mails_test.data','mails_test.class')

    En la función ejemplo_datos viene una manera de mostrar los resultados
    mostrando el valor de las palabras.

    La función debe de devolver el error de predicción tanto con los datos
    de entrenamiento como con los datos de prueba
    """
    #  ---------------------------------------------------
    #   Agregar aquí el código.
    #  ---------------------------------------------------
    datos, clases = carga_datos('mails.data','mails.class')

    # Entrenamos a la red bayesiana.
    filtro = nb.NaiveBayes([0, 1]) # No es spam, o si lo es.
    filtro.aprende(datos, clases)

    # Probamos con los datos de entrenamiento.
    c_e_entrenamiento = filtro.reconoce(datos)
    error_entrenamiento = error_clasif(clases, c_e_entrenamiento)

    # Probamos con los datos de prueba al mismo filtro.
    datos_prueba, clases_prueba = carga_datos('mails_test.data','mails_test.class')
    c_e_prueba = filtro.reconoce(datos_prueba)
    error_prueba = error_clasif(clases_prueba, c_e_prueba)

    return error_entrenamiento*100, error_prueba*100


if __name__ == "__main__":
    #ejemplo_datos()
    ee, ep = spam_filter()
    print("El error de entrenamiento es {}%".format(ee))
    print("El error de predicción es {}%".format(ep))
    """
    Como vimos en clase, este enfoque para clasificar información automáticamente
    da buenos resultados aunque sencillo.
    """

    """
    Debería ser posible detectar las palabras que más influyen en decidir si un correo
    es spam o no, debido a que la red bayesiana ingenua clasifica de acuerdo a las
    ocurrencias de cada valor para cada clase para cada variable en las muestras de
    entrenamiento. Por tanto, las variables más frecuentes en correos spam de los datos
    de entrenamiento tendrán un mayor peso al momento de calcular la probabilidad de que
    un nuevo correo sea spam efectivamente.
    Pareciera que las palabras que más determinan si un correo no es spam son sustantivos
    y pronombres, aparecen en grandes cantidades en correos que no son spam, y los
    pronombres son raros en correos spam.
    """
