import math

class ALU:

    #Cada flag se inicializa a 0
    def __init__(self):
        self.entrada1 = 0
        self.entrada2 = 0
        self.resultado = 0

    def ejecutar(self, alu_op):
        op1 = self.entrada1
        op2 = self.entrada2

        if alu_op == "ADD":
            self.resultado = op1 + op2

        elif alu_op == "SUB":
            self.resultado = op1 - op2

        elif alu_op == "AND":
            self.resultado = op1 & op2

        elif alu_op == "OR":
            self.resultado = op1 | op2

        elif alu_op == "SLT":
            self.resultado = 1 if op1 < op2 else 0

        elif alu_op == "SLL":
            self.resultado = op1 << op2
        else:
            self.resultado = 0
