from Componentes.memoria_instrucciones import MemoriaInstrucciones
from Componentes.unidad_proceso import UnidadProceso
from Componentes.unidad_control  import UnidadControl


class CPU:
    def __init__(self):
        self.etiquetas = {}
        self.unidad_proceso = UnidadProceso()
        self.unidad_control = UnidadControl()

    def cargar_datos(self, ruta_archivo):
        pass

    def cargar_instrucciones(self, ruta_instrucciones):
        pc_actual = 0

        with open(ruta_instrucciones, 'r') as archivo:
            for linea in archivo:
                # 1. Limpiar comentarios y espacios en blanco
                if '#' in linea:
                    linea = linea.split('#')[0]
                linea = linea.strip()

                # Ignorar líneas vacías
                if not linea:
                    continue

                # 2. Detectar si es una etiqueta (ej. "for:")
                if linea.endswith(':'):
                    nombre_etiqueta = linea[:-1]
                    # Guardamos a qué PC corresponderá la siguiente instrucción
                    self.etiquetas[nombre_etiqueta] = pc_actual

                # 3. Es una instrucción real
                else:
                    self.unidad_proceso.mem_instrucciones.instrucciones[pc_actual] = linea
                    pc_actual += 1

