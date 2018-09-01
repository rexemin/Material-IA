Tarea 2: Algoritmos de búsquedas directas
=========================================


Descripción
------------

Para esta tarea, vamos a entrenarnos primero en el uso y análisis del
algoritmo de temple simulado, en un problema de juguete como es el
clásico problema de las $n$ reinas.

Una vez entendido, vamos a usar el algoritmo para generar una
representación visual de un grafo no dirigido, a partir de su
definición por vértices y aristas. Lo más fácil es generar un dibujo
de forma aleatoria, pero lo que queremos es un dibujo del gráfo que
sea *estético*.


Esta tarea tiene como objetivo el entrenamiento para establecer con
claridad una función de costo de una apreciación subjetiva, así como
probar y ajustar un algoritmo de temple (recocido) simulado.

El problema no es tan complicado pero requiere de un análisis con
calma del código ya presentado.

Los puntos importantes a desarrollar en la tarea son:

1. Probar y ajustar los métodos de reinicios aleatorios y recocido
   simulado con el problema de las N-reinas.

2. Desarrollar una forma eficiente de generar un vecino aleatorio bien
   adaptado para ser usado con el algoritmo de temple simulado.

3. Establecer criterios para la medición de algo tan subjetivo como es
   la apreciación estética.

4. Implementar dichos criterios para ser usados dentro del algortimo
   de temple simulado.

5. Probar y ajustar el temple simulado con diferentes funciones de
   calendarización.


La tarea consta de 3 archivos:

1. El archivo ´blocales.py´ contiene la clase Problema y los métodos
   de busqueda local vistos en clase.

2. El archivo ¨nreinas.py´ contiene el ejemplo de las n-reinas, a
   desarrollar.

3. El archivo ´dibuja_grafo.py´ contiene el problema de dibujar un
   grafo, a desarrollar.

En principio todos los cambios se deben de realizar en los archivos
´nreinas.py´ y ´dibuja_grafo.py´.

Para la calificación de la tarea es **muy importante** explicar bien
las conclusiones que se obtienen del uso de los algoritmos, así como
la justificación de los criterios de coto seleccionados.
