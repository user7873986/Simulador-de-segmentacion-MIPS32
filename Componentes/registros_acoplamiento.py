
class RegistroAcoplamiento:
    def __init__(self):
        self.senales_control = {}
        self.inst = ""
        self.pc = 0
        self.op1 = 0
        self.op2 = 0
        self.inmediato = 0
        self.resultado_alu = 0
        self.dato_mem = 0
        self.dato_wb = 0

        self.reg_dest = 0 #señal de control
        self.reg_write = 0
        self.dato_sw = 0

        self.rd = ""
        self.rt = ""
        self.rs = ""

class IF_ID:
    def __init__(self):
        self.inst = "NOP"
        self.pc = 0

class ID_EX:
    def __init__(self):
        self.inst = "NOP"
        self.pc = 0
        self.op1 = 0
        self.op2 = 0
        self.inmediato = 0
        self.rs = ""
        self.rt = ""
        self.rd = ""
        self.senales_control = {}

class EX_MEM:
    def __init__(self):
        self.inst = "NOP"
        self.pc = 0
        self.resultado_alu = 0
        self.dato_sw = 0
        self.reg_dest = ""
        self.senales_control = {}

class MEM_WB:
    def __init__(self):
        self.inst = "NOP"
        self.pc = 0
        self.resultado_alu = 0
        self.dato_mem = 0
        self.reg_dest = ""
        self.senales_control = {}