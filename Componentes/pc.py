class PC:
    def __init__(self):
        self.contador = 0

    def set_pc(self, pc):
        self.contador = pc

    def actualizar_pc(self):
        self.contador = self.contador + 1