from memoria_instrucciones import MemoriaInstrucciones
from unidad_proceso import UnidadProceso
from unidad_control import UnidadControl


class CPU:
    def __init__(self):
        self.etiquetas = {}
        self.mem_instrucciones = MemoriaInstrucciones()
        self.unidad_proceso = UnidadProceso()
        self.unidad_control = UnidadControl()
        self.pc = 0

    def cargar_datos(self, ruta_archivo):
        """
        Lee el fichero de datos e instrucciones y
        puebla la mem_instrucciones y mem_datos.
        """
        try:
            with open(ruta_archivo, 'r') as archivo:
                # Aquí iría la lógica de lectura y parseo
                pass
            print(f"Datos cargados correctamente desde {ruta_archivo}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_archivo}")


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
                    self.mem_instrucciones.instrucciones[pc_actual] = linea
                    pc_actual += 1

    def ejecutar_ciclo(self):
        # Lógica para ejecutar un ciclo de reloj recuerda que el reloj es bucle while
        pass