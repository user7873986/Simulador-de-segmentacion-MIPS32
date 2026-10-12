Simulación de segmentación

estructuras de datos ->

el reloj va a ser un bucle while

fichero de texto que incluye las instrucciones de nuestro programa

explicarlo empezando por lo mas global a lo especifico. Primero con un diagrama de clases . EXplicar luego elementos relevantes mediante capturas de codigo y luego explicar la salida

etiquetas, 15 instrucciones al menos, meter riesgos de datos RAWs solo, 1 o 2


DECISIONES DE DISEÑO
El pc se suma de uno en uno; Mientras que las direcciones van de 4 en 4

Entre los riesgos de datos RAW distinguimos dos tipos; LOAD-USE y RAW entre aritméticas.
El riesgo LOAD-USE se da cuando una instrucción lw precede a una aritmética que necesita el dato que recupera de memoria lw, para solucionar este problema
congelamos la instrucción siguiente varios ciclos.

Para resolver la segunda problemática, trazaremos cables entre distintos componentes asegurándonos que los datos son capaces de viajar al sitio necesario
antes de ser usados otra vez. Esto se llama Unidad de adelantamiento

Si hay una burbuja, la fase if de la siguiente instrucción a tratar no empieza
