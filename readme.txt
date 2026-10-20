Simulación de segmentación

estructuras de datos ->

el reloj va a ser un bucle while

fichero de texto que incluye las instrucciones de nuestro programa

explicarlo empezando por lo mas global a lo especifico. Primero con un diagrama de clases . EXplicar luego elementos relevantes mediante capturas de codigo y luego explicar la salida

etiquetas, 15 instrucciones al menos, meter riesgos de datos RAWs solo, 1 o 2


DECISIONES DE DISEÑO
El pc se suma de uno en uno; Mientras que las direcciones van de 4 en 4

RIESGOS DE DATOS
Entre los riesgos de datos RAW distinguimos dos tipos; LOAD-USE y RAW entre aritméticas.
El riesgo LOAD-USE se da cuando una instrucción lw precede a una aritmética que necesita el dato que recupera de memoria lw, para solucionar este problema
congelamos la instrucción siguiente varios ciclos.

Para resolver la segunda problemática, trazaremos cables entre distintos componentes asegurándonos que los datos son capaces de viajar al sitio necesario
antes de ser usados otra vez. Esto se llama Unidad de adelantamiento

Si hay una burbuja, la fase if de la siguiente instrucción a tratar no empieza

FORWARDING
ifs de los registros origen igualando al de destino y luego el valor del registro de origen lo igualas al resultado final con ambos registros origen el 1 y el 2

Si hay un registro que no se reconoce se planta un 0

RIESGOS DE CONTROL


HAY QUE HACER DIAGRAMAS DE CÓMO LA INFORMACIÓN PASA DE UN REGISTRO A OTRO


UNIDADES DE ADELANTAMIENTO
Están en la fase_Ex, conectan a la alu si hay que meter un dato antes que otro

UNIDAD DE DETECCIÓN DE RIESGOS
Está en la fase_id para saber si se tiene que congelar

FLUJO DE INFORMACIÓN
fase_if  -> Lee: PC físico y Memoria Instrucciones | Escribe en: IF_ID

fase_id  -> Lee: IF_ID y Banco de Registros | Escribe en: ID_EX

fase_ex  -> Lee: ID_EX | Escribe en: EX_MEM ojo aquí espía los contenidos de ex_mem y mem_wb para saber si hay adelantamiento

fase_mem -> Lee: EX_MEM y Memoria de Datos | Escribe en: MEM_WB

fase_wb  -> Lee: MEM_WB | Escribe en: Banco de Registros físico





