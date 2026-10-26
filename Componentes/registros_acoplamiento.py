
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
        self.reg_dest = "" #señal de control
        self.senales_control = {}

class MEM_WB:
    def __init__(self):
        self.inst = "NOP"
        self.pc = 0
        self.resultado_alu = 0
        self.dato_mem = 0
        self.reg_dest = ""
        self.senales_control = {}

class WB_OUT:
    def __init__(self):
        self.inst = ""
