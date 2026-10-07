class RegistroAcoplamiento:
    """Estructura de estado para los registros intermedios del cauce."""
    def __init__(self):
        self.senales_control = {}
        self.inst = None      # Objeto Instruccion o string
        self.pc = 0
        self.op1 = 0
        self.op2 = 0
        self.inmediato = 0
        self.resultado_alu = 0
        self.dato_mem = 0

        self.reg_dest = 0 #señal de control
        self.dato_sw = 0

        self.rd = ""    # Registro destino para el WB
        self.rt = ""    # Nombres de los registros ej: $t1
        self.rs = ""
