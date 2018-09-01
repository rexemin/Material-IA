#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.

   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán

   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ```

   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos,
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente,
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""

##############################################################

__author__ = 'IvanAlejandroMorenoSoto'

##############################################################

import entornos_o
from random import random, choice
from doscuartos_o import DosCuartos, AgenteReactivoModeloDosCuartos, AgenteAleatorio

##############################################################

# Ejercicio 1.

class SeisCuartos(entornos_o.Entorno):
    """
    Entorno de una casa con seis cuartos: tres en la planta inferior y
    tres en la superior.

    Análogamente a DosCuartos, el estado se define como:
    estado := [posición, A, B, C, D, E, F]

    D E F
    A B C

    Donde A, B, C, son los cuartos inferiores, D, E, F, los superiores,
    y posición puede tomar como valor cualquiera de ellos. Cada cuarto
    puede estar "limpio" o "sucio."

    Las acciones válidas son:
    acciones = {"ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"}
    Todas son legales en todos los cuartos excepto por "subir" que únicamente es
    legal en A y C, y "bajar" que sólo se puede realizar en E.

    Los sensores son una tupla que contiene la posición del robot y el estado de
    limpieza del cuarto.
    """

    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Define el estado inicial de este entorno.
        De forma predeterminada el robot se encuentra en el cuarto inferior izquierdo
        y toda la casa está sucia.

        @param x0: Vector con el estado inicial del entorno de la forma
        [posiciónInicial, limpieza_A, limpieza_B, limpieza_C, limpieza_D, limpieza_E, limpieza_F].
        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        """
        Determina si una acción es legal en el estado actual.

        @param acción: Acción que será revisada.

        @return True si la acción es legal, False en caso contrario.
        """
        # Se separan los casos en: el robot quiere subir o quiere bajar o quiere hacer
        # cualquier otra cosa.
        if acción == "subir" and (self.x[0] == "A" or self.x[0] == "C"):
            return True
        if acción == "bajar" and self.x[0] == "E":
            return True

        return acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")

    def transición(self, acción):
        """
        Transforma al entorno según la acción recibida.

        @param acción: Acción de entrada al entorno.
        """
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        posición = self.x[0]

        # Se determina el desempeño local.
        if "sucio" in self.x or acción == "limpiar":
            self.desempeño -= 1
        if acción == "ir_Derecha" or acción == "ir_Izquierda":
            self.desempeño -= 2
        elif acción == "subir" or acción == "bajar":
            self.desempeño -= 3

        # Se modifica al entorno.
        if acción == "limpiar":
            self.x[" ABCDEF".find(posición)] = "limpio"
        elif acción == "ir_Derecha":
            if posición == "A":
                self.x[0] = "B"
            elif posición == "B":
                self.x[0] = "C"
            elif posición == "D":
                self.x[0] = "E"
            elif posición == "E":
                self.x[0] = "F"
        elif acción == "ir_Izquierda":
            if posición == "B":
                self.x[0] = "A"
            elif posición == "C":
                self.x[0] = "B"
            elif posición == "E":
                self.x[0] = "D"
            elif posición == "F":
                self.x[0] = "E"
        elif acción == "subir":
            if posición == "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        elif acción == "bajar":
            self.x[0] = "B"

    def percepción(self):
        """
        Regresa la percepción del entorno en el estado actual.

        @return Una tupla (posición, limpio?)
        """
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

##############################################################

# Ejercicio 2

class AgenteAleatorioSeisCuartos(AgenteAleatorio):
    """
    Define un agente aleatorio que cambia su conjunto de
    posibles acciones dependiendo de lo que sea legal.
    """

    def programa(self, percepción):
        """
        Escoge una acción legal al azar.

        @param percepción: Percepción del entorno SeisCuartos.

        @return Acción del agente.
        """
        return choice(self.calcular_acciones_legales(percepción[0]))

    def calcular_acciones_legales(self, posición):
        """
        Devuelve una lista de acciones legales en la posición dada.

        @param posición: Posición actual del agente.

        @return Lista con acciones legales en la posición indicada.
        """
        acciones_legales = self.acciones[:]

        # Se remueven las acciones ilegales.
        if posición != "A" and posición != "C":
            acciones_legales.remove("subir")
        if posición != "E":
            acciones_legales.remove("bajar")

        return acciones_legales

class AgenteRacionalSeisCuartos:
    """
    Agente reactivo basado en modelo para el entorno SeisCuartos.
    Intenta minimizar el costo de sus acciones evitando subir y
    bajar, y prefiriendo moverse a los lados.
    """

    def __init__(self):
        """
        Inicializa el modelo interno del agente.
        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        """
        @param percepción: Percepción del entorno SeisCuartos.

        @return Acción del agente.
        """
        posición, situación = percepción

        # Se actualiza el modelo del agente.
        self.modelo[0] = posición
        self.modelo[' ABCDEF'.find(posición)] = situación

        if not 'sucio' in self.modelo:
            return 'nada'
        if situación == 'sucio':
            return 'limpiar'

        if posición in ('A', 'B', 'C'):
            if not 'sucio' in self.modelo[1:4]:
                return ('ir_Izquierda' if posición == 'B' else 'subir')
            else:
                return ('ir_Derecha' if posición == 'A' or (posición == 'B' and self.modelo[1] == 'limpio') else
                        'ir_Izquierda')
        else:
            if not 'sucio' in self.modelo[4:]:
                return ('ir_Izquierda' if posición == 'F' else
                        'ir_Derecha' if posición == 'D' else
                        'bajar')
            else:
                return ('ir_Derecha' if posición == 'D' or (posición == 'E' and self.modelo[4] == 'limpio') else
                        'ir_Izquierda')

def hacerPruebaEjercicio1_2(pasos):
    """
    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en SeisCuartos con un agente aleatorio.")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorioSeisCuartos(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']), pasos)

    print("Prueba en SeisCuartos con un agente reactivo basado en modelo.")
    entornos_o.simulador(SeisCuartos(), AgenteRacionalSeisCuartos(), pasos)

##############################################################

# Ejercicio 3.

class DosCuartosCiego(DosCuartos):
    """
    Entorno basado en DosCuartos donde el robot solo tiene
    acceso a su posición actual.
    """

    def percepción(self):
        """
        @return Únicamente la posición actual del robot.
        """
        return self.x[0]

class AgenteDosCuartosCiego(AgenteReactivoModeloDosCuartos):
    """
    Agente para el entorno DosCuartosCiego.
    """

    def programa(self, percepción):
        """
        Aquí, el robot decide que acción realizará según su memoria de la
        situación del cuarto donde está.

        @param percepción Percepción del entorno en el estado actual.

        @return Una de cuatro acciones de ['ir_A', 'ir_B', 'limpiar', 'nada'].
        """

        # Se actualiza el lugar actual del robot.
        self.modelo[0] = percepción

        # Revisa lo que recuerda sobre el cuarto en el que se encuentra.
        situación = self.modelo[' AB'.find(percepción)]

        a, b = self.modelo[1], self.modelo[2]

        if situación == 'sucio':
            # Antes de regresar la acción, se actualiza la memoria sobre
            # el cuarto actual.
            self.modelo[' AB'.find(percepción)] = 'limpio'
            return 'limpiar'
        else:
            return ('nada' if a == b == 'limpio' else
                   'ir_A' if percepción == 'B' else 'ir_B')

def hacerPruebaEjercicio3(pasos):
    """
    Prueba el AgenteDosCuartosCiego y el AgenteAleatorio (de doscuartos_o)
    en el entorno DosCuartosCiego.

    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en DosCuartosCiego con un agente aleatorio.")
    entornos_o.simulador(DosCuartosCiego(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), pasos)

    print("Prueba en DosCuartosCiego con un agente racional.")
    entornos_o.simulador(DosCuartosCiego(), AgenteDosCuartosCiego(), pasos)

##############################################################

# Ejercicio 4.

class DosCuartosEstocástico(DosCuartos):
    """
    Entorno en el cual el agente tiene un 80% de éxito al limpiar un
    cuarto y un 90% al cambiarse de cuarto.
    """

    def transición(self, acción):
        """
        Implementa una transición estocástica del entorno.

        @param acción Acción del agente.
        """
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado.")

        robot, a, b = self.x

        if acción != "nada" or a == "sucio" or b == "sucio":
            self.desempeño -= 1

        if acción == "limpiar" and random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción == "ir_A" and random() <= 0.9:
            self.x[0] = "A"
        elif acción == "ir_B" and random() <= 0.9:
            self.x[0] = "B"

class AgenteDosCuartosEstocástico(AgenteReactivoModeloDosCuartos):
    """
    Agente racional para el entorno DosCuartosEstocástico. Está
    basado en un modelo.
    """

    def programa(self, percepción):
        """
        Funciona igual que el agente reactivo basado en modelo usado
        en DosCuartos, pero al momento de escoger una acción tiene en
        cuenta que puede fallar.

        @param percepción: Percepción de DosCuartosEstocástico.
        """
        posición, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = posición
        self.modelo[' AB'.find(posición)] = situación

        # Decide sobre el modelo interno y la posibilidad de fallo.
        a, b = self.modelo[1], self.modelo[2]
        éxito = random()

        # Si el robot 'siente' que puede fallar, mejor hace nada.
        return ('nada' if a == b == 'limpio' or éxito < 0.2 else
                'limpiar' if situación == 'sucio' else
                'ir_B' if posición == 'A' else 'ir_A')

def hacerPruebaEjercicio4(pasos):
    """
    Realiza pruebas con un agente aleatorio y uno reactivo basado en
    modelo en el entorno DosCuartosEstocástico.

    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en DosCuartosEstocástico con un agente aleatorio.")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), pasos)

    print("Prueba en DosCuartosEstocástico con un agente racional.")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteDosCuartosEstocástico(), pasos)

##############################################################

if __name__ == "__main__":
    hacerPruebaEjercicio1_2(100)
    hacerPruebaEjercicio3(100)
    hacerPruebaEjercicio4(100)
