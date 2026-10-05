class RegistroAcoplamiento:
    """Estructura de estado para los registros intermedios del cauce."""
    def __init__(self):
        self.inst = None      # Objeto Instruccion o string
        self.pc = 0
        self.op1 = 0
        self.op2 = 0
        self.resultado_alu = 0
        self.dato_mem = 0
        self.reg_dest = ""    # Registro destino para el WB

    def clonar(self):
        nuevo = RegistroAcoplamiento()
        nuevo.__dict__.update(self.__dict__)
        return nuevo