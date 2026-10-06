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

        if opcode in ["addi", "add", "sub", "and", "or", "slt", "sll", "andi"]:
            self.reg_write = 1
            if opcode in ["addi", "andi"]:
                self.alu_src = 1
                self.reg_dst = 0
            elif opcode == "sll":
                self.alu_src = 1
                self.reg_dst = 1
            else:
                self.alu_src = 0
                self.reg_dst = 1

            # Pasamos la operación literal a la ALU
            self.alu_op = opcode.upper()

        elif opcode == "lw":
            self.alu_src = 1
            self.mem_to_reg = 1
            self.reg_write = 1
            self.mem_read = 1
            self.alu_op = "ADD"  # Suma la dirección base + offset

        elif opcode == "sw":
            self.alu_src = 1
            self.mem_write = 1
            self.alu_op = "ADD"  # Suma la dirección base + offset

        elif opcode in ["beq", "bne"]:
            self.branch = 1
            self.alu_op = "SUB"  # Resta para comparar si son iguales

        elif opcode == "j":
            self.jump = 1

        # Retornamos las partes para que la etapa ID (Decode) extraiga los registros
        return {"opcode": opcode, "args": args}



#REGISTROS DE ACOPLAMIENTO POR ALGUN LADO DE AQUI
