![](ia.png)
# Tarea 1
## Desarrollo de entornos y agentes
**Julio Waissman Vilanova**, 24 de enero de 2018

### Objetivo de la tarea

Esta tarea tiene como objetivo revisar y dejar claro el desarrollo de las técnicas que se 
estudiarán en el curso como el desarrollo de programas de agentes racionales, y se revisará
en forma superficial el desarrollo de agentes *reactivos* y *reactivos basados en modelo*, así
como las peculiaridades de diferentes tipos de entornos. 

Igualmente, esta tarea es un primer acercamiento a `python` y a la forma en la que vamos a
trabajar el resto del curso. Es por esta razón que la mayoría del código ya viene programado.


### Trabajo a realizar

**Importante:** Todo el desarrollo que se realice para la tarea debe de ser
incluido en el archivo `tarea_1.py`. Recuerda que los commits que hagas de tus
avances son importantes para que como profesor pueda medir lo que vas haciendo.

En esta tarea realiza las siguiente acciones:

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

La fecha límite para entrega de la tarea es el **lunes 5 de febrero de 2018**.

