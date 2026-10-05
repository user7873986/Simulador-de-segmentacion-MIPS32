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

    def ejecutar(self, alu_op):
        """
        Realiza la operación indicada por alu_op entre operando1 y operando2.
        """
        # Convertimos a enteros por seguridad, ya que los datos de memoria/registros deben ser números
        op1 = self.entrada1
        op2 = self.entrada2

        if alu_op == "ADD":
            # Usado por add, addi, lw, sw
            self.resultado = op1 + op2

        elif alu_op == "SUB":
            # Usado por sub, beq, bne
            self.resultado = op1 - op2

        elif alu_op == "AND":
            # Usado por and, andi
            self.resultado = op1 & op2

        elif alu_op == "OR":
            # Usado por or
            self.resultado = op1 | op2

        elif alu_op == "SLT":
            # Set on Less Than: 1 si op1 < op2, 0 si no
            self.resultado = 1 if op1 < op2 else 0

        elif alu_op == "SLL":
            # Shift Left Logical: Desplaza op2 a la izquierda op1 veces
            # Ojo al parsear en la etapa ID: asegúrate de pasar el 'shamt' como op1
            self.resultado = op2 << op1

        else:
            # Para operaciones no reconocidas o NOPs
            self.resultado = 0

        # El flag Zero es vital para los saltos.
        # Por ejemplo, en un 'beq', si restamos ambos operandos y dan 0, son iguales.
        if self.resultado == 0:
            self.zero = 1
        else:
            self.zero = 0