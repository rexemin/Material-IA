#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Ivan Moreno'


import busquedas
from math import exp, log

class LightsOut(busquedas.ModeloBusqueda):
    # --------------------------------------------------------
    # Problema 2:  Completa la clase
    # para el modelo de lights out
    # --------------------------------------------------------
    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas
    adjacentes cambian (si estan prendidas se apagan y viceversa).

    El juego consiste en una matriz de 5 X 5, cuyo estado puede
    ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------

    Las acciones posibles son de elegir cambiar una luz y sus casillas
    adjacentes, por lo que la accion es un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self):
        """
        Se crea una única vez el generador de acciones legales.
        """
        self.acciones = range(25)

    def acciones_legales(self, estado):
        """
        Devuelve un generador de los números del 0 al 24 que 
        representan las 25 celdas que pueden ser presionadas.
        """
        return self.acciones

    def sucesor(self, estado, accion):
        """
        Actualiza el estado de las luces adyacentes a la acción.
        """

        s = list(estado)

        # Obtenemos las coordenadas de la casilla
        # que será presionada.
        r = (accion - (accion % 5)) // 5
        c = accion - 5 * (accion // 5)

        # Aprovechamos que los valores del estado viven en
        # Z2 para actualizarlos sin mucho problema.
        s[5*r + c] = (s[5*r + c] + 1) % 2

        # Volteamos los valores de todas las casillas
        # adyacentes.
        if r > 0:
            s[5*(r-1) + c] = (s[5*(r-1) + c] + 1) % 2
        if r < 4:
            s[5*(r+1) + c] = (s[5*(r+1) + c] + 1) % 2

        if c > 0:
            s[5*r + (c-1)] = (s[5*r + (c-1)] + 1) % 2
        if c < 4:
            s[5*r + (c+1)] = (s[5*r + (c+1)] + 1) % 2

        return tuple(s)

    def costo_local(self, estado, accion):
        """
        Devuelve el costo de realizar una acción en el tablero.
        1 porque solo se tiene que presionar una casilla.
        """
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = "---------------------\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n---------------------\n"
        return cadena


# ------------------------------------------------------------
#  Problema 3: Completa el problema de LightsOut
# ------------------------------------------------------------
class ProblemaLightsOut(busquedas.ProblemaBusqueda):
    def __init__(self, pos_ini):
        """
        Utiliza la superclase para hacer el problema

        """
        # Completa el código
        x0 = tuple(pos_ini)
        def meta(x):
            """
            Revisa si todas las luces del tablero están apagadas.
            Devuelve falso en cuanto encuentra una luz prendida, 
            verdadero en otro caso.
            """
            for casilla in x:
                if casilla == 1:
                    return False
            return True

        super().__init__(x0=x0, meta=meta, modelo=LightsOut())


# ------------------------------------------------------------
#  Problema 4: Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Esta heurística calcula una razón entre el número de casillas
    resueltas y las que faltan por resolver. Esta hecha de una manera
    que discrimina a los estados donde hay muchas luces encendidas.

    Creo que la heurística es admisible porque su valor no crece
    descontroladamente cuando el número de luces encendidas es grande.
    El valor que llega a tomar rara vez sobrepasa las dos decenas, y
    para este tablero, es razonable que se pueda tomar más de 10 pasos
    para resolver posiciones iniciales difíciles. Además, cuando el
    número de luces apagadas empieza a dominar el de luces encendidas
    los valores que toma son fraccionarios, con lo cual se vuelve muy
    optimista, debido a que no puedes resolver el juego en menos de
    1 paso.
    """

    ceros = sum([1 for casilla in range(25) if nodo.estado[casilla] == 0])
    unos = sum([1 for casilla in range(25) if nodo.estado[casilla] == 1])

    if ceros == 0:
        ceros = 1

    return unos/(ceros**2)

# ------------------------------------------------------------
#  Problema 5: Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    Esta heurística calcula el número de pasos necesarios para apagar
    todas las luces del tablero asumiendo que siempre se pueden apagar
    k luces distintas con una acción y utiliza el resultado para evaluar
    la función exponencial de manera que los estados con muchas luces
    son altamente penalizados.

    Creo que la heurística es admisible porque no toma en cuenta los
    pasos necesarios para apagar luces que se prendan colateralmente ni
    si dos luces prendidas no son adyacentes, siendo el número de pasos
    más optimista que la realidad. Aunque usa la función exponencial, el
    parámetro k = 9.5 que divide la suma de luces encendidas evita que en
    el peor caso (las 25 luces encendidas) se tenga una estimación pesimista.

    Al graficar las heurísticas propuestas en desmos (https://www.desmos.com/calculator)
    con el número de unos en el tablero como parámetro como sigue:
    h_1 = x / (25 - x)^2
    h_2 = e^(x / 9.5)
    h_3 = e^(x / 5) <- Ver h_3 más abajo

    Se puede ver que h_2 es mayor que h_1 para casi todos los valores
    aceptables (en el rango [0, 23]), en los últimos dos valores, sin embargo,
    h_1 es mayor. Estrictamente, ninguna heurística es dominante, pero si
    relajamos un poco nuestro formalismo, podemos decir que h_2 domina a h_1.

    Con respecto a h_3, esta si domina a h_2, y a h_1 (excepto por un intervalo
    muy pequeño).
    """
    return exp(sum(casilla for casilla in nodo.estado) / 9.5)

def h_3(nodo):
    """
    Es la mejor versión de h_2. Pero para algunos estados el valor que
    regresa ya no es optimista. Esta funciona mucho mejor que todas las
    demás heurísticas (propuestas en este módulo) porque permite buscar
    menos nodos y aún así encuentra el menor número de pasos.

    Cuenta el número de pasos ideal que se necesitan para apagar las luces
    del tablero (si asumimos que cada casilla apaga siempre 5 luces) y mete
    el resultado en una función exponencial.
    """
    return exp(sum(casilla for casilla in nodo.estado) / 5)

def prueba_modelo():
    """
    Prueba la clase LightsOut

    """

    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 = (1, 0, 0, 1, 0,
              1, 0, 1, 1, 0,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a4 = (1, 0, 0, 0, 1,
              1, 0, 1, 1, 1,
              0, 0, 0, 1, 1,
              0, 0, 1, 1, 1,
              0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)

    modelo = LightsOut()

    assert modelo.acciones_legales(pos_ini) == range(25)
    assert modelo.sucesor(pos_ini, 0) == pos_a0
    assert modelo.sucesor(pos_a0, 4) == pos_a4
    assert modelo.sucesor(pos_a4, 24) == pos_a24
    assert modelo.sucesor(pos_a24, 15) == pos_a15
    assert modelo.sucesor(pos_a15, 12) == pos_a12
    print("Paso la prueba de la clase LightsOut")


def compara_metodos(pos_inicial, heuristica_1, heuristica_2, heuristica_3):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla
    de la función

    """
    solucion1 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                             heuristica_1)
    solucion2 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_2)
    solucion3 = busquedas.busqueda_A_estrella(ProblemaLightsOut(pos_inicial),
                                              heuristica_3)

    print('-' * 50)
    print('Método'.center(10) + 'Costo'.center(20) + 'Nodos visitados')
    print('-' * 50 + '\n\n')
    print('A* con h1'.center(10) + str(solucion1.costo).center(20) +
          str(solucion1.nodos_visitados))
    print('A* con h2'.center(10) + str(solucion2.costo).center(20) +
          str(solucion2.nodos_visitados))
    print('A* con h3'.center(10) + str(solucion3.costo).center(20) +
          str(solucion3.nodos_visitados))
    print('-' * 50 + '\n\n')

if __name__ == "__main__":

    print("Antes de hacer otra cosa,")
    print("vamos a verificar medianamente la clase LightsOut")
    prueba_modelo()

    # Tres estados iniciales interesantes
    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    print("\n\nPara el problema en diagonal")
    print("\n{}".format(LightsOut.bonito(diagonal)))
    compara_metodos(diagonal, h_1, h_2, h_3)

    print("\n\nPara el problema simétrico")
    print("\n{}".format(LightsOut.bonito(simetria)))
    compara_metodos(simetria, h_1, h_2, h_3)

    print("\n\nPara el problema Bonito")
    print("\n{}".format(LightsOut.bonito(problemin)))
    compara_metodos(problemin, h_1, h_2, h_3)
