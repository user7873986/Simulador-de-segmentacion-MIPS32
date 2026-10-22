
class UnidadControl:
    def __init__(self):
        self.resetear_senales()

    #dada una instrucción saca las señales
    def decodificar(self, instruccion_str):
        self.resetear_senales()

        resultado_vacio = {
            "opcode": "NOP", "rs": "", "rt": "", "rd": "",
            "inmediato": 0, "etiqueta": "", "senales": {}
        }

        if not instruccion_str or instruccion_str == "NOP":
            return resultado_vacio

        partes = instruccion_str.replace(',', ' ').split()
        opcode = partes[0].lower()
        args = partes[1:]

        operaciones_alu = {
            "add": "ADD", "addi": "ADD", "lw": "ADD", "sw": "ADD",
            "sub": "SUB", "beq": "SUB", "bne": "SUB",
            "and": "AND", "andi": "AND",
            "or": "OR", "ori": "OR",
            "slt": "SLT",
            "sll": "SLL"
        }
        self.alu_op = operaciones_alu.get(opcode, "NOP")

        rs, rt, rd, etiqueta = "", "", "", ""
        inmediato = 0

        if opcode in ["add", "sub", "and", "or", "slt"]:
            self.reg_write = 1
            self.reg_dst = 1
            self.alu_src = 0
            self.mem_to_reg = 0

            rd = args[0].strip()
            rs = args[1].strip()
            rt = args[2].strip()

        elif opcode in ["addi", "andi"]:
            self.reg_write = 1
            self.reg_dst = 0
            self.alu_src = 1
            self.mem_to_reg = 0

            rt = args[0].strip()
            rs = args[1].strip()
            inmediato = int(args[2].strip())

        elif opcode == "sll":
            self.reg_write = 1
            self.reg_dst = 1
            self.alu_src = 1
            self.mem_to_reg = 0

            rs = args[1].strip()
            rd = args[0].strip()
            rt = "$zero"
            inmediato = int(args[2].strip())

        elif opcode in ["lw", "sw"]:
            rt = args[0].strip()
            partes_mem = args[1].replace(')', '').split('(')
            inmediato = int(partes_mem[0].strip())
            rs = partes_mem[1].strip()

            self.alu_src = 1
            if opcode == "lw":
                self.reg_write = 1
                self.reg_dst = 0
                self.mem_to_reg = 1
                self.mem_read = 1
            else:  # sw
                self.mem_write = 1

        elif opcode in ["beq", "bne"]:
            self.branch = 1

            rs = args[0].strip()
            rt = args[1].strip()
            etiqueta = args[2].strip()

        elif opcode == "j":
            self.jump = 1
            etiqueta = args[0].strip()

        senales_control = {
            "alu_src": self.alu_src,
            "alu_op": self.alu_op,
            "reg_dst": self.reg_dst,
            "reg_write": self.reg_write,
            "mem_read": self.mem_read,
            "mem_write": self.mem_write,
            "mem_to_reg": self.mem_to_reg,
            "branch": self.branch,
            "jump": self.jump
        }

        return {
            "opcode": opcode,
            "rs": rs,
            "rt": rt,
            "rd": rd,
            "inmediato": inmediato,
            "etiqueta": etiqueta,
            "senales": senales_control
        }


    def resetear_senales(self):
        self.reg_dst = 0
        self.pc_src = 0
        self.branch = 0
        self.mem_read = 0
        self.mem_to_reg = 0
        self.alu_op = "NOP"
        self.mem_write = 0
        self.alu_src = 0
        self.reg_write = 0
        self.jump = 0