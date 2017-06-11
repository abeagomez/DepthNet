# Aplicación de filtros sobre imágenes

En muchas ocasiones, las imágenes obtenidas para procesamiento contienen algunas características o estructuras que se desean extraer; junto con carcaterísticas y estructuras que no resultan de interés y se desean suprimir.

## Reducción de ruido

### Qué es el ruido?

En Visión por computadoras, el ruido hace referencia a cualquier entidad en una imagen o un conjunto de datos, que carece de interés para el objetivo principal a computar. Podemos hablar de ruido en disímiles casos. Para algoritmos de procesamiento de imágenes, como detección de esquinas o de líneas, se considera ruido cualquier fluctuación falsa del valor de un pixel introducida por el dispositivo de captura.

### Caracterización del ruido

Se asumirá que el ruido en una imagen es **aditivo** y **aleatorio**; esto significa que está compuesta por una señal aleatoria, de valor erróneo, n(i,j), sumada al valor verdadero del pixel I(i,j): 

FORMULA AQUI

La **cantidad de ruido** en una imagen puede ser estimada por medio de (sigma sub n), la desviación estándar de la señal aleatoria n(i,j). Es importante saber la intensidad del ruido con respecto a la señal de interés. Esto es especificado por el **signal-to-noise ratio** o **SNR**:

FORMULA AQUI

Donde (sigma sub s) no es más que la desviación estándar de la señal (el valor del pixel I(i,j))

### Ruido Gaussiano

El modelo Gaussiano para predicción de ruido es un modelo simple. Se basa en la asunción de que los valores de ruidos están distribuidos simétricamente alrededor del cero, y, consecuentemente, los valores (I ñañarita (i,j)) están distribuidos simétricamente alrededor de los valores I(i,j). Esto es lo que se esperaría de buenos sistemas de captura de imágenes, que, además, deberían garantizar bajos niveles de ruido.

### Eliminación de ruido

Como se reflejó anteriormente, es una práctica general asumir como aditivo el ruido en una imagen. La eliminación de ruido puede ser descrita como el proceso mediante el cual, dada una imagen (I ñañarita), donde el valor de cada pixel (i,j) puede definirse como la suma del valor original de pixel I(i,j) más un valor erróneo que definimos como ruido n(i,j):

    I(ñañarita)(i,j) = I(i,j) + n(i,j)

Se intenta reducir a cero el valor de n(i,j).

-------------------------------------------------

Dado un conjunto I de n imágenes de la misma escena, tomadas en las mismas condiciones, es posible calcular una secuencia de valores que nos permitan caracterizar el ruido. Tras aplicar a cada una de las n imágenes una transformación a escala de grises, se obtiene un nuevo conjunto P de n imágenes donde cada pixel tiene asociado un único valor: el de su intensidad en la escena. Al haber sido tomadas estas imágenes, originalmente, en las mismas condiciones, se puede afirmar que cualquier diferencia entre ellas se debe al ruido asociado al dispositivo de captura.

Se estlabece entonces el valor de intensidad de cada pixel en una imagen sin ruido Im(i,j) como el promedio de intensidad de dicho pixel en las n imágenes del conjunto P.

Im(i,j) = sumatoria desde l = 0 hasta n de Psub n en (i,j)

Luego de aplicar esta transformación ParaTodo (i,j) QuePertenece a Im, se obtiene una imagen C en escala de grises donde cada uno de los pixeles posee el valor esperado de intensidad para una imagen sin ruido.

Finalmente, se halla el módulo de la diferencia de C con cada una de las n imágenes que pertenecen al conjunto P. Si se asume C como una imagen libre de ruido, la diferencia con cada uno de los n-sub-i elementos de P representa el ruido asociado a n-sub-i. Al hallar el promedio de estas n diferencias, estamos caracterizando el ruido asociado 