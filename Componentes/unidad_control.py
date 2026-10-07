class UnidadControl:
    def __init__(self, unidad_procesamiento):

        self.unidad_procesamiento = unidad_procesamiento
        
        # Aquí irán las señales de control: RegDst, Branch, MemRead, etc.
        self.reg_dst = 0
        self.pc_src = 0
        self.branch = 0
        self.mem_read = 0
        self.mem_to_reg = 0
        self.alu_op = 0
        self.mem_write = 0
        self.alu_src = 0
        self.reg_write = 0

    def decodificar(self, instruccion_str):

        self.resetear_senales()

        if not instruccion_str or instruccion_str == "NOP":
            return {"opcode": "NOP", "args": []}

        # Limpiamos comas y separamos por espacios
        # 'addi $s0, $0, 1' -> partes = ['addi', '$s0', '$0', '1']
        partes = instruccion_str.replace(',', '').split()
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

        # 2. ENRUTAMIENTO DE SEÑALES DE CONTROL (Multiplexores y Memoria)
        if opcode in ["add", "sub", "and", "or", "slt"]:
            # Formato R puro (ej. add $t1, $t2, $t3)
            self.reg_write = 1
            self.reg_dst = 1  # Guarda en 'rd'
            self.alu_src = 0  # Operando 2 es un registro
            self.mem_to_reg = 0  # El dato viene de la ALU

        elif opcode in ["addi", "andi"]:
            # Formato I aritmético/lógico (ej. addi $t1, $t2, 100)
            self.reg_write = 1
            self.reg_dst = 0  # Guarda en 'rt'
            self.alu_src = 1  # Operando 2 es el inmediato
            self.mem_to_reg = 0  # El dato viene de la ALU

        elif opcode == "sll":
            # Desplazamientos (Shift)
            self.reg_write = 1
            self.reg_dst = 1
            self.alu_src = 1  # El amount (shamt) actúa como inmediato
            self.mem_to_reg = 0

        elif opcode == "lw":
            # Carga de memoria
            self.reg_write = 1
            self.reg_dst = 0  # Guarda en 'rt'
            self.alu_src = 1  # Suma el offset a la dirección
            self.mem_to_reg = 1  # El dato viene de la Memoria
            self.mem_read = 1

        elif opcode == "sw":
            # Almacenamiento en memoria
            self.alu_src = 1  # Suma el offset a la dirección
            self.mem_write = 1

        elif opcode in ["beq", "bne"]:
            # Saltos condicionales
            self.branch = 1
            # (alu_src = 0 por defecto, compara dos registros)

        elif opcode == "j":
            # Salto incondicional
            self.jump = 1

        return {"opcode": opcode, "args": args}

    def resetear_senales(self):
        self.reg_dst = 0
        self.pc_src = 0
        self.branch = 0
        self.mem_read = 0
        self.mem_to_reg = 0
        self.alu_op = 0
        self.mem_write = 0
        self.alu_src = 0
        self.reg_write = 0

#REGISTROS DE ACOPLAMIENTO POR ALGUN LADO DE AQUI
