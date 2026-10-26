Simulación de segmentación

estructuras de datos -> diccionarios para las memorias tanto de instrucción como de datos
la unidad de control utiliza también un diccionario para controlar sus señales
los registros de acoplamiento utilizan solo las señales y atributos que necesitan saber las fases que se usan

el reloj va a ser un bucle while, cada ejecución del bucle es un ciclo de reloj


explicarlo empezando por lo mas global a lo especifico. Primero con un diagrama de clases . EXplicar luego elementos relevantes mediante capturas de codigo y luego explicar la salida

DECISIONES DE DISEÑO
El pc se suma de uno en uno; Mientras que las direcciones en memoria van de 4 en 4
se ha implementado una clase llamada forwarding que evalúa si se necesita hacer y adelanta el dato



RIESGOS DE DATOS
Entre los riesgos de datos RAW distinguimos dos tipos; LOAD-USE  y RAW entre aritméticas.
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

Están en la fase_Ex, conectan a la alu si hay que meter un dato antes que otro

UNIDAD DE DETECCIÓN DE RIESGOS
Está en la fase_id para saber si se tiene que congelar

FLUJO DE INFORMACIÓN
fase_if  -> Lee: PC físico y Memoria Instrucciones | Escribe en: IF_ID

fase_id  -> Lee: IF_ID y Banco de Registros | Escribe en: ID_EX

fase_ex  -> Lee: ID_EX | Escribe en: EX_MEM ojo aquí espía los contenidos de ex_mem y mem_wb para saber si hay adelantamiento

fase_mem -> Lee: EX_MEM y Memoria de Datos | Escribe en: MEM_WB

fase_wb  -> Lee: MEM_WB | Escribe en: Banco de Registros físico


PARA LA MEMORIA
•	La memoria debe relacionar explícitamente la salida del simulador con los elementos del MIPS de 32 bits y las cinco etapas;
incluirá diagrama de clases y capturas de código.
Se deben de comentar los tres casos de cortocircuito

Para saltos, se deben de resolver en ID indicar qué sucede con los

Elementos mínimos de una solución completa
Clases para instrucción/programa/cauce; estado IF/ID, ID/EX, EX/MEM y MEM/WB; banco de registros; memoria; unidad de detección de riesgos; unidad de forwarding; tratamiento del load-use; decisión de salto en ID; traza de cada ciclo; pruebas que demuestren al menos tres RAW.



ANTES DE ENTREGAR
Verificar el código sobretodo de segmentacion y de la última función para comprobar que es legible y no hay cosas raras
Se siguen patrones tanto en la nombración de variables como en orden de las funciones (tdo en ingles o en español)
Se actualiza el diagrama de clases correspondiente con la versión final



