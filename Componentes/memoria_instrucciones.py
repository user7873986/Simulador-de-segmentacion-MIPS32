
class MemoriaInstrucciones:

    def __init__(self):
        # Cada entrada coincide con la instruccion en formato string, PC se suma de 1 en 1
        self.instrucciones = {}

    def leer(self, pc):
        return self.instrucciones.get(pc)