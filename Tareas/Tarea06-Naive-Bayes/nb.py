#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nb.py
------------

Clase genérica para realizar el método de clasificación de Naïve Bayes.
"""

__author__ = 'juliowaissman'

##-----------------------------------------------------------------------------

from math import log

##-----------------------------------------------------------------------------

class NaiveBayes:
    """
    Clase genérica del clasificador Naïve Bayes, para entradas con
    dominio discreto y finito.
    """

    def __init__(self, clases=None, variables=None, valores=None):
        """Inicializa el algoritmo de NB.

        @param clases: es un conjunto (o lista) [clase1, ..., clasek],
                       con el nombre de las k clases que nos
                       interesan.

        @param variables: Lista con los nombres de las variabes
                          que se usan, en el orden en que vienen
                          organizadas dentro de los datos con los que
                          se alimenta al método de aprendizaje.

        @param valores: Diccionario donde valores[var] es una lista
                        o un conjunto con los valores que puede tomar
                        la variable en cuestión.

        """
        self.clases = clases
        self.var_nom = variables
        self.vals = valores
        if (clases is not None and
            variables is not None and
            valores is not None):
            self.inicializa_cuentas()
        else:
            self.frec = None
            self.log_probs = None

    def inicializa_cuentas(self):
        """
        Para poder hacer un aprendizaje incremental, esto es, poder
        agregar nuevos ejemplos de aprendizaje en línea, en lugar de
        guardar las CPTs, vamos a utilizar un diccionario con
        frecuencias.

        self.frecuencias['clases'] es un diccionario, donde en cada
        nombre de clase guarda la frecuencia encontrada (esto permite
        inclusive agregar nuevas clases en línea). Así, por cada valor
        en la lista self.cls_nombre habrá una entrada del diccionario
        self.frecuencias['clases].

        Por cada variable habrá otros dicionarios, de manera que
        self.frecuencias[var][clase][val] es el número de ocurrencias
        del valor 'val', de la variable 'var', cuando los datos están
        asociados a la clase 'clase'.

        De la misma manera, para facilitar el reconocimiento se utiliza
        un diccionario llamado self.log_probs.

        """
        self.frec = {var: {clase: {val: 0 for val in self.vals[var]}
                           for clase in self.clases}
                     for var in self.var_nom}
        self.frec['clases'] = {clase: 0 for clase in self.clases}

        self.log_probs = {var: {clase: {val: 0 for val in self.vals[var]}
                                for clase in self.clases}
                          for var in self.var_nom}
        self.log_probs['clases'] = {clase: 0 for clase in self.clases}

    def aprende(self, datos, clases):
        """
        Aprende los valores de la CPT, es el trabajo a realizar.

        @param datos: Lista [dato_1, ..., dato_N],
                      donde dato_i es a su vez una lista
                      tal que dato_i = [d_i1, ..., d_in]
                      es el vector del i-ésimo dato.

        @param clases: Lista [clase_1, ..., clase_N] con
                       las clases correspondientes a cada dato
                       dato_i de la estructura anterior.
        """

        # Inicializa en cero todas las cuentas si no hay un valor previo
        # (en un futuro sería importante verificar si no hay algún valor nuevo
        # que no se hubiera agregado antes).
        inicializar = False
        if self.var_nom is None:
            self.var_nom = [str(i) for i in range(len(datos[0]))]
            inicializar = True
        if self.vals is None:
            self.vals = {var: set([datos[j][i] for j in range(len(datos))])
                         for (i, var) in enumerate(self.var_nom)}
            inicializar = True
        if self.clases is None:
            self.clases = set(clases)
            inicializar = True
        if inicializar:
            self.inicializa_cuentas()

        # Se actualizan los valores de las frecuencias para calcular la
        # probabilidad a priori.
        for clase in self.clases:
            #  ---------------------------------------------------
            #  Agregar aquí el código
            self.frec['clases'][clase] += clases.count(clase)
            #  raise NotImplementedError("Falta completar esto para la tarea.")
            #  ---------------------------------------------------

            # Ahora se actualiza el valor de las frecuencias por cada atributo y
            # para cada posible clase.
            for (i, var) in enumerate(self.var_nom):

                dato_var_clase = [datos[j][i] for j in range(len(datos))
                                  if clases[j] == clase]

                for val in self.vals[var]:
                    #  --------------------------------------------------
                    #  Agregar aquí el código
                    self.frec[var][clase][val] += dato_var_clase.count(val)
                    #  raise NotImplementedError("Falta completar esto para la tarea.")
                    #  --------------------------------------------------

        # Ahora hay que actualizar al final los logaritmos de las
        # probabilidades para hacer el reconocimiento muy rápido (Usar
        # únicamente la información de self.frec par hacer esto.)
        N = sum([self.frec['clases'][cls] for cls in self.frec['clases'].keys()])
        for clase in clases:
            #  ---------------------------------------------------
            #  Agregar aquí el código
            Nc = self.frec['clases'][clase]
            self.log_probs['clases'][clase] = log(Nc/N)
            #  raise NotImplementedError("Falta completar esto para la tarea.")
            #  ---------------------------------------------------

            # Ahora se actualiza la probabilidad por cada atributo y
            # para cada posible clase.
            for var in self.var_nom:
                for val in self.vals[var]:
                    #  --------------------------------------------------
                    #  Agregar aquí el código
                    Ncv = self.frec[var][clase][val]
                    K = len(self.vals[var])
                    self.log_probs[var][clase][val] = log((Ncv + 1)/(Nc + K))
                    #  raise NotImplementedError("Falta completar esto para la tarea.")
                    #  --------------------------------------------------

    def reconoce(self, datos):
        """
        Identifica la clase a la que pertenece cada uno de los datos que
        se solicite, de acuerdo al clasificador.

        @param datos = [dato_1, dato_2, ...] es una lista de datos
                       para clasificar, donde dato_i = [dato_i,1,
                       ..., dato_i,n] es el valor del dato en cada
                       atributo. Hay que recordar que se puede
                       utilizar el método de Naïve Bayes si no se
                       conocen todos los atributos. Si un atributo no
                       se conoce, entonces lo definimos dato(i,n) = None.

        """
        clases = []

        #  ---------------------------------------------------
        #  Agregar aquí el código.

        def log_prob(dato, clase):
            return (self.log_probs['clases'][clase] +
                    sum([self.log_probs[var][clase][dato[i]]
                         for (i, var) in enumerate(self.var_nom)]))

        clases = [max(self.clases, key=lambda clase: log_prob(dato, clase))
                  for dato in datos]
        #  ---------------------------------------------------
        return clases


def test():
    """
    Esta función sirve para poder ir probando y corrigiendo el programa.

    Hay 4 pruebas básicas: una para probar la inicialización, otras dos
    para probar el aprendizaje (o el llenado de cuentas), y la 4ta para
    probar si el reconocimiento se hace correctamente. Hasta que se pasen
    todas las pruebas no hay que pasar al problema que se encuentra en
    el archivo naive_bayes.py
    """

    clases = {'N', 'P'}
    variables = ['uno', 'dos']
    valores = {'uno': {1, 2, 3, 4}, 'dos': {10, 20}}
    nb = NaiveBayes(clases, variables, valores)

    assert nb.frec['clases'] == {'N': 0, 'P': 0}
    assert nb.frec['uno']['N'] == {1: 0, 2: 0, 3: 0, 4: 0}
    print("La primera prueba se completó con éxito.")

    data = [[1, 10], [2, 10], [3, 10], [4, 10],
            [1, 20], [2, 20], [3, 20], [4, 20]]
    clases = ['N', 'P', 'P', 'N', 'N', 'P', 'N', 'N']

    nb = NaiveBayes()
    assert nb.frec is None

    nb.aprende(data, clases)
    assert nb.frec['clases'] == {'N': 5, 'P': 3}
    assert nb.frec['0']['P'] == {1: 0, 2: 2, 3: 1, 4: 0}
    assert nb.frec['0']['N'] == {1: 2, 2: 0, 3: 1, 4: 2}
    assert nb.frec['1']['P'] == {10: 2, 20: 1}
    assert nb.frec['1']['N'] == {10: 2, 20: 3}
    print("La segunda prueba se completó con éxito.")

    assert nb.log_probs['clases']['N'] == log(5/8)
    assert nb.log_probs['0']['P'][1] == log(1/7)
    assert nb.log_probs['1']['N'][20] == log(4/7)
    print("La tercera prueba se completó con éxito.")

    data_test = [[2, 20], [4, 10]]
    clase_test = nb.reconoce(data_test)
    print(clase_test)
    assert clase_test == ['P', 'N']
    print("La cuarta prueba se completó con éxito.")


if __name__ == "__main__":
    test()
