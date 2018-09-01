# Tarea 6: Red bayesiana simple: Bayes inocente

## Objetivos

1. Reforzar los conocimientos básicos sobre redes bayesianas, desarrollando la red 
   bayesiana más simple de todas: El método de bayes inocente.
   
2. Desarrollar los métodos basados en frecuencias y el criterio MAP en un método de clasificación sencillo y 
   probarlo con una base de datos real (cadenas de ADN).
   
3. Conocer los conceptos básicos de *Procesamiento de Lenguaje Natural*, en particular el uso de la técnica de Bolsa de 
   Palabras e implementar un filtro *anti-spam* simple.
   
   
## Instrucciones:

1. En el archivo `nb.py` complete el método `aprende` y el método `reconoce` de la clase `NaiveBayes` de acuerdo
   a las técnicas vistas en clase. Recuerde utilizar siempre el modificador de LaPlace para la estimación de verosimilitudes.
   Verifique con la función `test` incluida en el mismo archivo que el código funciona correctamente.
   
2. Revise, comprenda y ejecute el codigo contenido en el archivo `naive_bayes.py`. Revise los resultados y de ser necesario, 
   modifique de nuevo la clase `NaiveBayes` del modupo `nb.py`. Se espera una estimacion con un error de precisión menor al 10% con los datos sin ruido. 
   Compare los resultados de datos con ruido y sin ruido y explique el porqué de los resultados obtenidos en forma de comentario en el 
   archivo.

3. Abre el archivo `spam_filter.py` y complete el código de la función `spam_filter`. Revise y comprenda el código, y ejecutelo, 
   revisando cual es el resultado de aplicar Naive Bayes para la detección de spam.
   
4. ¿Es posible detectar con Naive Bayes cuales son las palabras que más influyen para decidir que un correo es Spam? 
   ¿Cuañes palabras son las que determinan más claramente que un correo no es Spam? Anexe su respuesta con justificación 
   al final del archivo `spam_filter.py` en forma de comentario.

