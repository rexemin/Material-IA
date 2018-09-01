# Aprendizaje no supervisado

En esta tarea vamos a incluir un ejemplo, en forma de libreta de
*Jupyter* sobre el uso de el análisis en componentes principales (PCA)
combinado con las K-medias como una forma de analizar datos y buscar
relaciones entre ellos (algo que se sule llamar KDD por *Knowledge
Discovery in Datasets*).

Como ejemplo se deja una libreta para hacer un análisis estandar con
datos muy manoseados en diferente tutoriales (prevalencia de
tuberculosos en distintos paises de 1990 al 2007). Para este ejemplo
vamos a considerar solamente 30 paises seleccionados al azar (para
ponerlo más divertido). En la libreta se agregaron algunas preguntas
las cuales se espera sean contestadas (no hay nada que programar, solo
ejecutar la libreta paso a paso y analizar los resultados que se van
obteniendo.

A partir de esta libreta, se pide hacer una nueva libreta nueva donde
se analicen los estados de la república mexicana a partir de los
indicadores de bienestar definidos por la OCDE y que el INEGI ha
publicado para el 2014. Los datos se obtuvieron de la [página del
INEGI](http://www.inegi.org.mx). Para este problema se tienen 37
indicadores, los cuales se pueden regrupar en 12 macro indicadores
(establecidos todos por la OCDE para comparar los niveles de bienestar
de la población en diferentes paises). Los indicadores se encuentran
en los archivos `ndicadores bienestar 2014.xlsx` e
`indicadores_bienestar_2014.csv` cada uno en su formato
correspondiente (se anexa el archivo de Excel para el que le guste
usar hojas de calculo, y revisar los macroindicadores). Se espera que
se realice un análisis similar y que se discutan los resultados.

Como para esta tarea se requiere el uso de `DataFrames` de la
biblioteca *Pandas*, se anexa una libreta tutorial de introducción a
Pandas, la cual es opcional.
