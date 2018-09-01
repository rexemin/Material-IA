#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Otello implementado por ustedes mismos, con jugador 'inteligente.'

"""

# -------------------------------------------------------------------------

__author__ = 'Ivan Moreno'

from collections import deque
from copy import deepcopy
import tkinter as tk
import numpy as np

import busquedas_adversarios as ba

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
# -------------------------------------------------------------------------

class Othello(ba.JuegoSumaCeros2T):
    """
    Clase que implementa una representacion computacional del Othello.

    La tupla del estado es así:
    0   1   2   3   4   5   6   7
    8   9   10  11  12  13  14  15
    16  17  18  19  20  21  22  23
    24  25  26  27  28  29  30  31
    32  33  34  35  36  37  38  39
    40  41  42  43  44  45  46  47
    48  49  50  51  52  53  54  55
    56  57  58  59  60  61  62  63
    """

    def __init__(self):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza.
        """
        x0 = (0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 1,-1, 0, 0, 0,
              0, 0, 0,-1, 1, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0)
        super().__init__(x0 = x0)

        # Iba a guardar las fichas cambiadas dentro del historial
        # de jugadas, pero luego me puse a ver como los del semestre
        # pasado habían hecho sus interfaces, y cuando vi lo que hizo
        # Belén para el historial de jugadas dije: "ah, eso esta mejor."
        # Por lo que hago lo que ella hizo y prefiero usar mucha más
        # memoria para que la búsqueda pueda ser más rápida.
        self.historial = deque()
        self.estados_anteriores = deque()

        self.orilla = set() # Guarda las casillas donde podrían haber jugadas legales.
        self.orillas_pasadas = deque()
        for casilla in (18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45):
            self.orilla.add(casilla)

        self.jugador = 1
        self.x = np.array(x0)

    def jugadas_legales(self):
        """
        Calcula las jugadas en las que el jugador actual obtiene fichas
        del oponente.
        """
        jugadas = []

        for casilla in list(self.orilla):
        #for casilla in range(64):
            # Se calculan las coordenadas de la casilla actual.
            x = casilla % 8
            y = casilla // 8
            captura = self.revisarCapturas((x, y))
            # Si hay al menos una captura, es jugada legal.
            if True in captura:
                jugadas.append((x, y))

        return jugadas

    def terminal(self):
        """
        Revisa si ambos oponentes tendrán que pasar en el próximo turno.
        Regresa la utilidad en base al jugador de fichas negras.
        """
        jugador_actual = self.jugador

        if len(self.jugadas_legales()) == 0:
            self.jugador *= -1

            if len(self.jugadas_legales()) == 0:
                self.jugador *= -1

                tablero = self.x.tolist()

                negras = tablero.count(1)
                blancas = tablero.count(-1)
                return (1 if negras > blancas else
                       -1 if blancas > negras else 0)
            else:
                self.jugador = jugador_actual

        return None

    def revisarCapturas(self, jugada):
        """
        Revisa que hileras de fichas se capturan con una jugada
        dada. Devuelve una lista indicando que filas fueron
        capturadas.

        @param jugada: Tupla con las coordenadas de la jugada.
        """
        x, y = jugada
        casilla = x + 8*y
        estado = self.x
        filas = [False for i in range(8)]

        if estado[casilla] != 0:
            return filas

        # Horizontal <-
        if x > 1:
            sig_capturada = estado[casilla - 1] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla-2, casilla-x-1, -1)]
                fila_capturada = False
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[0] = True

        # Horizontal ->
        if x < 6:
            sig_capturada = estado[casilla + 1] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla+2, casilla+8-x)]
                fila_capturada = False
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[1] = True

        # Vertical hacia abajo.
        if y < 6:
            sig_capturada = estado[casilla + 8] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla+16, casilla+((8-y)*8), 8)]
                fila_capturada = False
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[2] = True

        # Vertical hacia arriba.
        if y > 1:
            sig_capturada = estado[casilla - 8] == -1*self.jugador
            if sig_capturada:
                hilera = [estado[i] for i in range(casilla-16, casilla-(8*y)-1, -8)]
                fila_capturada = False
                for c in hilera:
                    if c == self.jugador:
                        fila_capturada = True
                        break
                    elif c == 0:
                        fila_capturada = False
                        break
                if fila_capturada:
                    filas[3] = True

        # Diagonal hacia abajo e izquierda.
        if x > 1 and y < 6:
            sig_capturada = estado[casilla + 7] == -1*self.jugador
            x_sig = x - 1
            y_sig = y + 1

            if sig_capturada:
                c = casilla + 14
                fila_capturada = False

                while (x_sig > -1 and y_sig < 7):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig -= 1
                    y_sig += 1
                    c += 7

                if fila_capturada:
                    filas[4] = True

        # Diagonal hacia abajo y derecha.
        if x < 6 and y < 6:
            sig_capturada = estado[casilla + 9] == -1*self.jugador
            x_sig = x + 1
            y_sig = y + 1

            if sig_capturada:
                c = casilla + 18
                fila_capturada = False

                while (x_sig < 7 and y_sig < 7):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig += 1
                    y_sig += 1
                    c += 9

                if fila_capturada:
                    filas[5] = True

        # Diagonal hacia arriba e izquierda.
        if x > 1 and y > 1:
            sig_capturada = estado[casilla - 9] == -1*self.jugador
            x_sig = x - 1
            y_sig = y - 1

            if sig_capturada:
                c = casilla - 18
                fila_capturada = False

                while (x_sig > -1 and y_sig > -1):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig -= 1
                    y_sig -= 1
                    c -= 9

                if fila_capturada:
                    filas[6] = True

        # Diagonal hacia arriba y derecha.
        if x < 6 and y > 1:
            sig_capturada = estado[casilla - 7] == -1*self.jugador
            x_sig = x + 1
            y_sig = y - 1

            if sig_capturada:
                c = casilla - 14
                fila_capturada = False

                while (x_sig < 7 and y_sig > -1):
                    if estado[c] == self.jugador:
                        fila_capturada = True
                        break
                    elif estado[c] == 0:
                        fila_capturada = False
                        break
                    x_sig += 1
                    y_sig -= 1
                    c -= 7

                if fila_capturada:
                    filas[7] = True

        return filas

    def hacer_jugada(self, jugada):
        """
        Actualiza el tablero de juego y guarda el estado anterior.

        @param jugada: Tupla que contiene la coordenada donde se agrega una ficha.
        """
        # Por si el jugador pasa su turno.
        if jugada is None:
            self.historial.append(jugada)
            self.jugador *= -1
            return None

        # Antes de modificar, guardamos el estado actual.
        self.estados_anteriores.append(self.x)
        self.orillas_pasadas.append(deepcopy(self.orilla))
        estado = self.x.copy()

        x, y = jugada
        casilla = x + 8*y
        estado[casilla] = self.jugador # Actualizamos la casilla donde se jugó.
        filas_capturadas = self.revisarCapturas(jugada) # Obtenemos donde capturó la jugada.

        # Revisa en el orden: <-, ->, arriba, abajo, diagonal superior izquierdo,
        # diagonal superior derecho, diagonal inferior izquierdo, diagonal
        # inferior derecho.
        for (f, d) in zip(filas_capturadas, (-1, 1, 8, -8, 7, 9, -9, -7)):
            # Si una fila fue capturada, voltea todas las fichas del oponente
            # que estén entre dos fichas del jugador actual.
            if f:
                cas_capturada = casilla + d
                while(estado[cas_capturada] != self.jugador):
                    estado[cas_capturada] = self.jugador
                    cas_capturada += d

        # Actualizamos la orilla de las fichas en el tablero.
        vecinos = []
        if x > 0:
            vecinos.append(-1)
            if y > 0:
                vecinos.append(-9)
            if y < 7:
                vecinos.append(7)
        if x < 7 :
            vecinos.append(1)
            if y > 0:
                vecinos.append(-7)
            if y < 7:
                vecinos.append(9)
        if y > 0:
            vecinos.append(-8)
        if y < 7:
            vecinos.append(8)

        for vecino in vecinos:
            if estado[casilla + vecino] == 0:
                self.orilla.add(casilla+vecino)

        # Formalizamos los cambios.
        self.x = estado
        self.jugador *= -1
        self.orilla.remove(casilla)
        self.historial.append(jugada)
        return None

    def deshacer_jugada(self):
        """
        Viaja en el tiempo y restaura el estado anterior del juego, mientras
        al estado actual lo manda a volar y actualiza la orilla de las fichas.
        """
        jugada = self.historial.pop()

        if jugada is None:
            self.jugador *= -1
        else:
            x, y = jugada
            casilla_pasada = x + 8*y
            if self.x[casilla_pasada] == -1*self.jugador:
                self.jugador *= -1

            self.x = self.estados_anteriores.pop()
            self.orilla = self.orillas_pasadas.pop()
        return None

    def contar_puntos(self, jugador):
        """
        Cuenta los puntos que tiene un jugador en el tablero.

        @param jugador: 1 o -1, para indicar a qué jugador le estamos contando
        los puntos.
        """
        puntos = 0

        for i in range(64):
            if self.x[i] == jugador:
                puntos += 1
        return puntos

# -------------------------------------------------------------------------

class OthelloGUI:
    """
    Clase que define el contenedor de Tkinter para desplegar una GUI
    con la cual jugar Othello.
    """

    def __init__(self, escala = 2):
        """
        Inicializa una nueva ventana para jugar Othello.

        @param escala: algo.
        """
        # Inicialización de todo el contenedor de Tk.
        self.app = app = tk.Tk()
        self.app.title('Othello V1.0')
        self.L = L = int(escala) * 30

        # Despliegue del aviso principal.
        aviso = 'Escoge con qué juegas. Las negras siempre empiezan.'
        self.anuncio = tk.Message(app, bg = 'white',
                                  borderwidth = 1,
                                  justify = tk.CENTER,
                                  text = aviso,
                                  width = 8 * L)
        self.anuncio.pack()

        # Desplegamos en pantalla la ventana de la aplicación.
        barra = tk.Frame(app)
        barra.pack()

        # Creamos la barra de puntos del usuario.
        self.puntos_usuario = tk.Label(barra,
                                       bg = 'light grey',
                                       text = 'Humano: ')
        self.puntos_usuario.grid(column = 0, row = 0)

        # Botones para iniciar el juego.
        btn_inicio_neg = tk.Button(barra,
                               command = lambda x = 1: self.jugar(x),
                               text = 'Volver a iniciar con negras')
        btn_inicio_neg.grid(column = 1, row = 0)

        btn_inicio_blancas = tk.Button(barra,
                                       command = lambda x = -1: self.jugar(x),
                               text = 'Volver a iniciar con blancas')
        btn_inicio_blancas.grid(column = 2, row = 0)

        # Creamos la barra de puntos de la computadora.
        self.puntos_cpu = tk.Label(barra,
                                   bg = 'light grey',
                                   text = 'CPU: ')
        self.puntos_cpu.grid(column = 3, row = 0)

        # Creamos un contenedor para el canvas sobre el que dibujaremos.
        ctn = tk.Frame(app, bg = 'black')
        ctn.pack()

        # Dibujamos un tablero vacío.
        self.tablero = [None for _ in range(64)]
        self.textos = [None for _ in range(64)]
        letra = ('Helvetica', -int(0.4 * L), 'bold') # Que bonito si tienes Helvetica.

        for i in range(64):
            self.tablero[i] = tk.Canvas(ctn,
                                        height = L,
                                        width = L,
                                        bg = 'light grey',
                                        borderwidth = 0)

            # Posicionamos a la casilla dentro del canvas.
            self.tablero[i].grid(row = i // 8,
                                 column = i % 8)
            self.textos[i] = self.tablero[i].create_text(L // 2,
                                                         L // 2,
                                                         font = letra,
                                                         text = ' ')
            # Inicializamos los atributos que después ocuparemos para
            # actualizar el tablero.
            self.tablero[i].val = 0
            self.tablero[i].pos = i

    def jugar(self, fichas_hum):
        """
        Inicia un nuevo juego de Othello.

        @param fichas_hum: Indica que color de fichas usará el usuario.
        1 es negras, -1 es blancas.
        """
        juego = Othello()

        # Cuando la computadora empieza.
        if fichas_hum == -1:
            jugada = ba.minimax_t(juego, 5, utilidad = utilidad_othello, ordena_jugadas=ordenar_jugadas)
            juego.hacer_jugada(jugada)

        # lmao
        self.anuncio['text'] = 'Si pierdes, te das de baja.'

        # Ahora si, repetimos el proceso de jugar hasta que alguien pierda.
        for _ in range(64):
            self.actualizar_tablero(juego.x)

            if juego.jugadas_legales():
                casilla = self.escoger_jugada(juego)
                jugada = (casilla % 8, casilla // 8)
                print('Jugada tuya: ' + str(jugada))
                juego.hacer_jugada(jugada)

                self.actualizar_puntos(juego, fichas_hum)
                self.actualizar_tablero(juego.x)
            else:
                print('Ya valiste, no hay jugadas para ti durante este turno.')
                juego.hacer_jugada(None)

            ganador = juego.terminal()
            if ganador is not None: break
            print('Jugador de la máquina: ' + str(juego.jugador))

            if juego.jugadas_legales():
                print('La máquina está viendo que hace')

                jugada = ba.minimax_t(juego, 15, utilidad = utilidad_othello, ordena_jugadas=ordenar_jugadas)
                print('Jugada: ' + str(jugada))
                juego.hacer_jugada(jugada)

                self.actualizar_puntos(juego, fichas_hum)
                self.actualizar_tablero(juego.x)
                print('La máquina ha elegido.')
            else:
                print('Oh, no, no hay jugadas para la máquina, se supone que ibas a perder.')
                juego.hacer_jugada(None)

            ganador = juego.terminal()
            if ganador is not None: break
            print('Jugador de la humano: ' + str(juego.jugador))

        self.actualizar_puntos(juego, fichas_hum)
        self.actualizar_tablero(juego.x)

        if ganador == fichas_hum:
            anuncio_final = 'Demonios, le ganaste a varios GB de RAM y a al menos 4 núcleos de procesamiento poderosos'
        elif ganador == -1*fichas_hum:
            anuncio_final = 'Y así, las computadoras vuelven a mostrar su superioridad'
        else:
            anuncio_final = 'lmao, un empate. Que anticlimático, si me preguntas'

        self.anuncio['text'] = anuncio_final
        self.anuncio.update()

    def escoger_jugada(self, juego):
        """
        Permite al usuario escoger en qué casilla jugar durante su turno.

        @param juego: Objeto Othello con el estado actual del juego.
        """
        jugadas_posibles = juego.jugadas_legales()

        seleccion = tk.IntVar(self.tablero[0].master, -1, 'seleccion')

        # Definimos los cambios que sufrirán las casillas cuando el usuario
        # mueva el ratón sobre ellas.
        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'blue'

        def salida(evento):
            evento.widget['bg'] = evento.widget.color_original

        def presionar_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        # Indicamos a las casillas de posibles jugadas sobre el comportamiento
        # que deben tener.
        for (x, y) in jugadas_posibles:
            casilla = x + 8*y

            self.tablero[casilla].bind('<Enter>', entrada)
            self.tablero[casilla].bind('<Leave>', salida)
            self.tablero[casilla].bind('<Button-1>', presionar_raton)

        self.tablero[0].master.wait_variable('seleccion')

        # Les quitamos el comportamiento para que no se vea raro.
        for (x, y) in jugadas_posibles:
            casilla = x + 8*y

            self.tablero[casilla].unbind('<Enter>')
            self.tablero[casilla].unbind('<Leave>')
            self.tablero[casilla].unbind('<Button-1>')

        return seleccion.get()

    def actualizar_tablero(self, estado_nuevo):
        """
        Actualiza las casillas de la ventana del juego.

        @param estado_nuevo: Tupla que describe el estado nuevo del tablero.
        """
        for i in range(64):
            if self.tablero[i].val != estado_nuevo[i]:
                self.tablero[i].itemconfigure(self.textos[i],
                                              text = ' xo'[estado_nuevo[i]])
                self.tablero[i].val = estado_nuevo[i]
                self.tablero[i].update()

    def actualizar_puntos(self, juego, fichas_hum):
        """
        Actualiza las etiquetas que despliegan los puntos de los
        jugadores.

        @param juego: Objeto Othello que contiene el estado actual del juego.
        @param fichas_hum: Indica las fichas que está usando el usuario.
        """
        self.puntos_usuario['text'] = 'Humano: {}'.format(juego.contar_puntos(fichas_hum))
        self.puntos_usuario.update()
        self.puntos_cpu['text'] = 'CPU: {}'.format(juego.contar_puntos(-1*fichas_hum))
        self.puntos_cpu.update()

    def iniciar(self):
        """
        Inicia el ciclo de actualización de la ventana del juego.
        """
        self.app.mainloop()

# -------------------------------------------------------------------------

def utilidad_othello(juego):
    """
    Devuelve una utilidad basada en las posibles jugadas del jugador 1,
    las fichas en las orillas y en las esquinas.

    @param juego: Objeto Othello.
    """
    estado = juego.x

    fichas = 0
    orilla = [0, 1, 2, 3, 4, 5, 6, 7,
              8, 16, 24, 32, 40, 48,
              15, 23, 31, 39, 47, 55,
              56, 57, 58, 59, 60, 61, 62, 63]

    for casilla in orilla:
        if estado[casilla] == 1:
            fichas += 1

    if juego.jugador == 1:
        jugadas_sig_turno = len(juego.jugadas_legales())
    else:
        juego.jugador *= -1
        jugadas_sig_turno = len(juego.jugadas_legales())
        juego.jugador *= -1

    esquinas = sum([1 for casilla in (0, 7, 56, 63)
                     if estado[casilla] == 1])

    return fichas + 10*jugadas_sig_turno + 10*esquinas

# -------------------------------------------------------------------------

def ordenar_jugadas(juego):
    """
    Ordena las jugadas respecto a qué tan cerca están de la parte superior
    del tablero.

    @param juego: Juego actual de Othello.
    """
    jugadas = list(juego.jugadas_legales())

    if jugadas is None:
        return None

    casillas = [x + 8*y for (x, y) in jugadas]

    return sorted(jugadas, key = lambda jugada: casillas[jugadas.index(jugada)])

# -------------------------------------------------------------------------

if __name__ == '__main__':
    """
    juego = Othello()
    jugadas = [(5, 4), (3, 5), (2, 6), (5, 3), (3, 2)]

    print(juego)
    print(juego.orilla)

    juego.hacer_jugada(jugadas[0])
    print(juego)
    print(juego.orilla)

    juego.deshacer_jugada()
    print(juego)
    print(juego.orilla)

    juego.hacer_jugada(jugadas[1])
    print(juego)

    juego.hacer_jugada(jugadas[2])
    print(juego)

    juego.hacer_jugada(jugadas[3])
    print(juego)

    juego.hacer_jugada(jugadas[4])
    print(juego)
    """
    juego = OthelloGUI()
    juego.iniciar()

