# Detección de Luz

Para la detección de luz se decidió realizar dos tipos de prueba: detección de una luz blanca y detección de una luz infrarroja. Esto permitió evaluar ambos resultados y elegir el de mejor desempeño. (imágenes con luz blanca y con luz infrarroja)

En ambos casos, se utilizó la cámara RGB del Kinect para el procesamiento de la imagen descrito a continuación.

Para comenzar, se aplicó a cada cuadro (frame) un "Desenfoque Gaussiano" (Gaussian Blur) AGREGAR REFERENCIA. Esta técnica es ampliamente utilizada en la visión por computadoras para reducir el ruido y el nivel de detalle de una imagen. AQUI IMAGENES DE GAUSSIAN BLUR.

La elección del "Gaussian Blur" como técnica para reducir el ruido de la imagen estuvo basada en un estudio de ruido[2.6.3 de Computer Vision Fundamentals] de la cámara del Kinect. El ruido fue medido a partir de una porción de la imagen con una distribución de color uniforme. Al analizar el histograma de distribución de intensidad de los pixeles en dicha porción de imagen, se puede ver (IMAGEN DEBAJO) que la distribución resultante es muy similar a la gaussiana, es por esto que para eliminarlo se utilizó un filtro lineal gaussiano.

Luego, se aplicó un umbral binario (binary threshold) [Referencia al libro] a la imagen resultante, previamente transformada a escala de grises. Aplicar un umbral binario a partir de determinado valor de intensidad permite filtrar aquellas partes y objetos en la imagen que no serán de utilidad. En el presente trabajo, se deseaba filtrar todo elemento de la imagen que no se correspondiera con una zona de emisión de luz. Luego de transformar la imagen a escala de grises, se pudo comprobar que los emisores de luz son puntos de alta intensidad, cercanos al blanco; esto permitió establecer un umbral bastante alto y filtrar la mayor parte de los elementos de la imagen que no eran de interés. El proceso de filtrado consistió en disminuir a 0 la intensidad de todos aquellos pixeles que estuvieran por debajo del umbral establecido y aumentar a 255 la intensidad de los pixeles que superaran dicho umbral.

IMAGENES DE BINARY THRESHOLD [10.3]

Al aplicar el proceso anterior utilizando un dioso emisor de luz (LED) blanca, surgió el problema de las superficies reflexivas: con frecuencia, el ambiente de trabajo contiene un número elevado de superficies reflexivas, que trae como resultado la detección de varios puntos de emisión de luz en la imagen. Así, por ejemplo, una mesa de madera o metal puede reflejar la luz del emisor con la intensidad suficiente para ser detectada como otro emisor en la escena.

Como posible solución se intentó probar con emisores LED de menor intensidad, esto implicó disminuir el umbral de intensidad establecido previamente como parámetro de filtrado. Como resultado, se detectaron múltiples objetos en la escena que no resultaban de interés.

Otro de los problemas enfrentados fue la existencia de emisores de luz blanca secundarios, que pueden ser fácilmente confundidos con el emisor principal, como, por ejemplo, lámparas existentes en la habitación.

Se decidió entonces descartar un emisor LED de luz blanca como posible solución, teniendo en cuenta que no fue posible obtener lecturas con él que excluyeran, si no de forma absoluta, al menos para la mayoría de los casos controlables, elementos adicionales como posibles focos de emisión de luz. Resultaba extremadamente complejo distinguir en una lectura de intensidad de la escena el emisor deseado de un emisor de luz secundario. Incluso, en algunos casos, ambos emisores se superponían originando una supuesta "lectura única" errónea.

IMAGENES DEL EMISOR CON REFLEXION Y CON BOMBILLO DETRAS

Fue utilizado entonces un diodo emisor de luz infrarroja (IRLED), teniendo en cuenta que un ambiente de trabajo regular se hace menos frecuente la existencia de múltiples emisores de luz infrarroja. Utilizar este tipo de luz nos permitió fijar el umbral de filtrado lo suficientemente bajo, dado que que la detección de luz infrarroja no puede confundirse con un emisor de luz en el espectro visible.

Se construyó un filtro infrarrojo A BASE DE NEGATIVOS para la cámara del kinect, esto nos permitió filtrar aquellos elementos de la imagen que no fueran emisores de luz infrarroja. Para todos los casos probados, obtuvimos como resultado únicamente nuestro emisor.

IMAGENES CON FILTRO INFRARROJO

Al aplicar un umbral binario en el rango de 0 a 255, en el caso de la luz blanca, debimos filtrar elementos con valores de intensidad por debajo de 210, mientras que para la luz infrarroja, bastó con filtrar aquellos elementos con intensidad menor que 20.

Finalmente, se seleccionó el emisor de luz infrarroja como la mejor alternativa de solución para la detección de un punto único de emisión de luz. Como consecuencia, la solución presentada es válida solo en aquellos ambientes donde existe un único emisor de luz infrarroja.
