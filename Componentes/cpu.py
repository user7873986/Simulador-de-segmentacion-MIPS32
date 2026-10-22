from Componentes.unidad_proceso import UnidadProceso
from Componentes.unidad_control  import UnidadControl

class CPU:
    def __init__(self):
        self.etiquetas = {}
        self.unidad_proceso = UnidadProceso()
        self.unidad_control = UnidadControl()

    def cargar_datos(self, ruta_datos):
            with open(ruta_datos, 'r') as archivo:
                for linea in archivo:
                    linea = linea.strip()

                    if not linea:
                        continue

                    partes = linea.split()

                    if len(partes) == 2:
                        direccion = int(partes[0])
                        valor = int(partes[1])

                        self.unidad_proceso.mem_datos.escribir(direccion, valor)

    def cargar_instrucciones(self, ruta_instrucciones):
        pc_actual = 0

        with open(ruta_instrucciones, 'r') as archivo:
            for linea in archivo:
                linea = linea.split('#')[0].split(';')[0].strip()

                if not linea:
                    continue

                if linea.endswith(':'):
                    etiqueta = linea[:-1]
                    self.etiquetas[etiqueta] = pc_actual

                else:
                    self.unidad_proceso.mem_instrucciones.instrucciones[pc_actual] = linea
                    pc_actual += 1

