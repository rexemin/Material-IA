#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conecta4.py.py
------------

El juego de conecta 4

Este juego contiene una parte de la tarea 5, y otra parte
es la implementación desde 0 del juego de Otello.

"""
from busquedas_adversarios import JuegoSumaCeros2T
from busquedas_adversarios import minimax_t
from busquedas_adversarios import minimax
from random import shuffle
import tkinter as tk

__author__ = 'juliowaissman'


class ConectaCuatro(JuegoSumaCeros2T):
    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y
        renglones y el estado inicial del juego. Cuyas posiciones
        estan dadas como:

                        35  36  37  38  39  40  41
                        28  29  30  31  32  33  34
                        21  22  23  24  25  26  27
                        14  15  16  17  18  19  20
                         7   8   9  10  11  12  13
                         0   1   2   3   4   5   6
        """
        super().__init__(tuple([0 for _ in range(6 * 7)]))

    def jugadas_legales(self):
        """
        Las jugadas legales son las columnas donde se puede
        poner una ficha (0, ..., 6), si no está llena.
        """
        return (j for j in range(7) if self.x[35 + j] == 0)

    def terminal(self):
        x = self.x
        # Primero checamos filas y diagonales
        if any((xj != 0 for xj in x[21:28])):
            # Filas
            for i in range(7):
                if x[i + 21] == 0 or x[i + 14] != x[i + 21]:
                    continue
                if ((x[i] == x[i + 7] == x[i + 14]) or
                    (x[i + 7] == x[i + 14] == x[i + 28]) or
                    (x[i + 14] == x[i + 28] == x[i + 35])):
                    return x[i + 14]
            # Diagonales
            for j in (0, 7, 14):
                for i in (0, 1, 2, 3):
                    # Hacia arriba
                    if (x[i + j + 24] != 0 and
                        x[i + j + 24] == x[i + j + 16] and
                        x[i + j + 16] == x[i + j + 8] and
                        x[i + j + 8] == x[i + j]):
                        return x[i + j]
                    # Hacia abajo
                    if (x[i + j + 21] != 0 and
                        x[i + j + 21] == x[i + j + 15] and
                        x[i + j + 15] == x[i + j + 9] and
                        x[i + j + 9] == x[i + j + 3]):
                        return x[i + j + 3]
        # Ahora checamos renglones
        for i in range(0, 41, 7):
            if x[i + 3] == 0:
                break
            for j in range(4):
                if (x[i + j] == x[i + j + 1] == x[i + j + 2] == x[i + j + 3]):
                    return x[i + 3]
        # Ahora checamos si no se lleno el tabero
        if 0 not in x:
            return 0
        return None

    def hacer_jugada(self, jugada):
        for i in range(0, 41, 7):
            if self.x[i + jugada] == 0:
                self.x[i + jugada] = self.jugador
                self.historial.append(jugada)
                self.jugador *= -1
                return None

    def deshacer_jugada(self):
        pos = self.historial.pop()
        for i in (35, 28, 21, 14, 7, 0):
            if self.x[i + pos] != 0:
                self.x[i + pos] = 0
                self.jugador *= -1
                return None


def utilidad_c4(juego):
    """
    Calcula la utilidad de una posición del juego conecta 4
    para el jugador max (las fichas rojas, o el que empieza)

    @param x: Una lista con el estado del tablero

    @return: Un número entre -1 y 1 con la ganancia esperada

    Para probar solo busque el número de conecciones de las
    bolitas de mas arriba con su alrededor
    """
    x = juego.x
    utilidad = 0

    # Revisamos cuantas secuencias verticales de 3 fichas hay.
    for c in range(7):
        for r in (c, c+7, c+14, c+21, c+28):
            tres_seguidos = x[r] == x[r+7] #and x[r] == x[r+14]
            hay_pos = r + 21 < 42

            if tres_seguidos and x[r] == 1:
                utilidad += 1
            elif tres_seguidos and hay_pos:
                if x[r + 14] == 1:
                    utilidad += 10
                else:
                    utilidad -= 10

    # Revisamos cuantas secuencias horizontales de 3 fichas hay.
    for r in (0, 7, 14, 21, 28, 35):
        for c in (r, r+1, r+2, r+3):
            tres_seguidos = x[c] == x[c+1] and x[c] == x[c+2]
            hay_pos = c > r

            if tres_seguidos:
                if x[c] == 1: utilidad += 1
                if hay_pos:
                    if x[c - 1] == 1: utilidad += 3
                    else: utilidad -= 10
                if x[c + 3] == 1: utilidad += 3
                else: utilidad -= 10

    # Revisamos cuantas secuencias diagonales de 3 fichas hay.
    for r in (0, 7, 14):
        for c in (r, r+1, r+2, r+3):
            tres_seguidos = x[c] == x[c+8] and x[c] == x[c+16]
            hay_pos = c > 6 and c != r

            if tres_seguidos:
                if x[c] == 1: utilidad += 1
                if hay_pos:
                    if x[c - 8] == 1: utilidad += 3
                    else: utilidad -= 10
                if x[c + 24] == 1: utilidad += 3
                else: utilidad -= 10

    # Revisamos la otra direccion de las diagonales.
    for r in (0, 7, 14):
        for c in (r+3, r+4, r+5, r+6):
            tres_seguidos = x[c] == x[c+6] and x[c] == x[c+12]
            hay_pos = c > 6 and c != r+6

            if tres_seguidos:
                if x[c] == 1: utilidad += 1
                if hay_pos:
                    if x[c - 6] == 1: utilidad += 3
                    else: utilidad -= 10
                if x[c + 18] == 1: utilidad += 3
                else: utilidad -= 10

    return utilidad


def ordena_jugadas(juego):
    """
    Ordena las jugadas de acuerdo al jugador actual, en función
    de las más prometedoras.

    Para que funcione le puse simplemente las jugadas aleatorias
    pero es un criterio bastante inaceptable

    """
    jugadas = list(juego.jugadas_legales())
    x = juego.x

    orden = sorted([(abs(sum([1 for i in range(jug, jug + 36, 7)
                              if x[i] != 0]) - 3.5),
                     jug) for jug in jugadas])

    return [j[1] for j in orden]

class Conecta4GUI:
    def __init__(self, tmax=10, escala=1):

        # La tabla de transposición
        self.tr_ta = {}

        # Máximo tiempo de búsqueda
        self.tmax = tmax

        self.app = app = tk.Tk()
        self.app.title("Conecta Cuatro")
        self.L = L = int(escala) * 50

        tmpstr = "Escoge color, rojas empiezan"
        self.anuncio = tk.Message(app, bg='white', borderwidth=1,
                                  justify=tk.CENTER, text=tmpstr,
                                  width=7*L)
        self.anuncio.pack()

        barra = tk.Frame(app)
        barra.pack()
        botonR = tk.Button(barra, command=lambda x=True: self.jugar(x),
                           text='(re)iniciar con rojas', width=22)
        botonR.grid(column=0, row=0)
        botonN = tk.Button(barra, command=lambda x=False: self.jugar(x),
                           text='(re)iniciar con negras', width=22)
        botonN.grid(column=1, row=0)

        ctn = tk.Frame(app, bg='black')
        ctn.pack()

        self.sel_j = tk.IntVar(self.anuncio.master, -1, 'sel_j')

        def boton_f(fila):
            self.sel_j.set(fila)

        self.flecha = tk.PhotoImage(file='flecha2.gif')
        self.botones = [None for _ in range(7)]
        for i in range(7):
            self.botones[i] = tk.Button(ctn, image=self.flecha,
                                        command=lambda fila=i: boton_f(fila),
                                        width=L, height=L,
                                        state=tk.DISABLED)
            self.botones[i].grid(column=i, row=0)

        self.can = [None for _ in range(6 * 7)]
        self.cuadritos = [None for _ in range(6 * 7)]
        for i in range(6 * 7):
            self.can[i] = tk.Canvas(ctn, height=L, width=L,
                                    bg='light grey', borderwidth=0)
            self.can[i].grid(row=((41 - i) // 7) + 1, column=i % 7)
            self.cuadritos[i] = self.can[i].create_oval(5, 5, L, L,
                                                        fill='white', width=2)
            self.can[i].val = 0

    def jugar(self, primero):

        juego = ConectaCuatro()

        for i in range(42):
            if self.can[i].val != 0:
                self.can[i].itemconfigure(self.cuadritos[i], fill='white')
                self.can[i].val = 0
        color, color_p = 'red', 'black'

        if not primero:
            color, color_p = 'black', 'red'
            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

        for _ in range(43):
            self.anuncio['text'] = "Te toca jugar"
            self.anuncio.update()
            for i in juego.jugadas_legales():
                self.botones[i]['state'] = tk.NORMAL

            self.anuncio.master.wait_variable('sel_j')
            jugada = self.sel_j.get()
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

            self.anuncio['text'] = "Ahora juega Python"
            self.anuncio.update()
            for i in range(7):
                self.botones[i]['state'] = tk.DISABLED
                self.botones[i].update()

            jugada = minimax(juego, dmax=6, utilidad=utilidad_c4,
                             ordena_jugadas=ordena_jugadas,
                             transp=self.tr_ta)
            juego.hacer_jugada(jugada)
            self.actualiza_tablero(jugada, color_p)

            ganancia = juego.terminal()
            if ganancia is not None:
                break

        for i in range(7):
            self.botones[i]['state'] = tk.DISABLED

        str_fin = ("Ganaron las rojas" if ganancia > 0 else
                   "Ganaron las negars" if ganancia < 0 else
                   "Un asqueroso empate")
        self.anuncio['text'] = str_fin

    def actualiza_tablero(self, fila, color):
        for i in range(0, 41, 7):
            if self.can[i + fila].val == 0:
                self.can[i + fila].itemconfigure(self.cuadritos[i + fila],
                                                 fill=color)
                self.can[i + fila].val = 1 if color is 'red' else -1
                self.can[i + fila].update()
                break

    def arranca(self):
        self.app.mainloop()


if __name__ == '__main__':
    Conecta4GUI(tmax=10).arranca()
