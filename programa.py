class Programa:
    """Clase encargada exclusivamente de gestionar el código a ejecutar."""
    def __init__(self):
        self.instrucciones = {} # Memoria de instrucciones (diccionario PC -> Instrucción)
        self.etiquetas = {}     # Diccionario para resolver saltos

    def cargar_instrucciones(self, ruta_instrucciones):
        pc_actual = 0
        try:
            with open(ruta_instrucciones, 'r') as archivo:
                for linea in archivo:
                    if '#' in linea:
                        linea = linea.split('#')[0]
                    linea = linea.strip()

                    if not linea:
                        continue

                    if linea.endswith(':'):
                        nombre_etiqueta = linea[:-1]
                        self.etiquetas[nombre_etiqueta] = pc_actual
                    else:
                        # Idealmente aquí parsearíamos el string a un objeto 'Instruccion'
                        self.instrucciones[pc_actual] = linea
                        pc_actual += 1
            print(f"Instrucciones cargadas correctamente desde {ruta_instrucciones}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_instrucciones}")