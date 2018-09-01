#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

naive_bayes.py
---------------

Archivo general para realizar las pruebas del uso del método de bayes inocente.

Se prueba en un conjunto de prueba de dimensión fija sobre cadenas de ADN.
Para mayor información sobre la base de datos, se puede consultar en

http://archive.ics.uci.edu/ml/datasets/Molecular+Biology+(Splice-junction+Gene+Sequences)

La base ya se trató y se convirtieron los valores de genes a números enteros
con el fin de poder utilizar la base para varios métodos de clasificación (como
redes neuronales).

La base de datos ya se repartió en una base de entrenamiento (dna.data) y otra
base de prueba (dna.test.) Con el fin de probar la robustez de los algoritmos de
aprendizaje ante ruido, se agregó a la base otros atributos extra con valores
asignados al azar (como si tuviéramos atributos extra con información no
significativa.) Estos datos se encuentran en dna_noise.data y dna_noise.test
respectivamente.

Para estar seguro que el algoritmo funciona, tanto sin ruido como con
ruido el error de clasificación con los datos originales debe estar
por debajo del 5%, mientras que el error en el conjunto de prueba debe
de andar un poco por arriba del 5% pero claramente menor al 7%
"""

import nb


def carga_archivo(archivo):
    """
    Cargar el archivo de datos a clasificar, devuelve

    - datos = [dato1, dato2, ..., datoE], la lista de E datos a clasificar
      donde dato1 = [dato1(1), ..., dato1(n)] son los n valores de los
      atributos de dato1.

    - clases = [clase1, clase2, ..., claseE] la clase a la que pertenece
      cada dato
    """
    datos, clases = [], []

    enlistado = open(archivo, 'rU').readlines()
    for linea in enlistado:
        renglon = [int(d.strip().strip('\n')) for d in linea.split(',')]
        datos.append(renglon[0: -1])
        clases.append(renglon[-1])
    return datos, clases


def error_clasif(c1, c2):
    """
    Encuentra el porcentaje de valores diferentes entre la lista c1 y la c2
    """
    acc = len([1 for i in range(len(c1)) if c1[i] != c2[i]])
    return 1.0 * acc / len(c1)


def main():
    print("\nPrueba con la base de datos de DNA sin ruido")
    print("----------------------------------------------")

    datos, clases = carga_archivo("dna.data")
    clasificador = nb.NaiveBayes([1,2,3])

    clasificador.aprende(datos, clases)
    clases_estimadas = clasificador.reconoce(datos)
    error = error_clasif(clases, clases_estimadas)
    print("Error de estimación en los mismos datos: " +
          str(error*100)+" %")

    d_test, c_test = carga_archivo("dna.test")
    c_e_test = clasificador.reconoce(d_test)
    e_test = error_clasif(c_test, c_e_test)
    print("Error de estimación en los datos de prueba: " +
          str(e_test*100)+" %\n")

    print("\nPrueba con la base de datos de DNA con ruido")
    print("----------------------------------------------")

    datos, clases = carga_archivo("dna_noise.data")
    clasificador_ruido = nb.NaiveBayes([1,2,3])

    clasificador_ruido.aprende(datos, clases)
    clases_estimadas = clasificador_ruido.reconoce(datos)
    error = error_clasif(clases, clases_estimadas)
    print("Error de estimación en los mismos datos: "+str(error*100)+"%")

    d_test, c_test = carga_archivo("dna_noise.test")
    c_e_test = clasificador_ruido.reconoce(d_test)
    e_test = error_clasif(c_test, c_e_test)
    print("Error de estimación en los datos de prueba: "+str(e_test*100)+"%\n")

if __name__ == "__main__":
    main()

    """
    Los resultados son parecidos con y sin ruido, debido a que aunque exista ruido
    en la segunda base de datos, el resto de los valores de las variables son creíbles
    y siguen teniendo el mismo peso al momento de calcular la probabilidad de que
    un dato pertenezca a una clase en particular, es decir, el ruido llega a ser
    'ignorado' porque siguen siendo muchos más valores reales.
    """
