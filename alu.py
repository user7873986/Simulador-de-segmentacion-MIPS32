class ALU:
    def __init__(self):
        self.entrada1 = 0
        self.entrada2 = 0
        self.resultado = 0

    # Define metodo para cada instrucción
    def add(self):
        self.resultado = self.entrada1 + self.entrada2

    def sub(self):
        self.resultado = self.entrada1 - self.entrada2