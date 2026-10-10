from Componentes.registro_acoplamiento import RegistroAcoplamiento


class Segmentacion:
    def __init__(self, cpu):
        # Recibimos la CPU ya cargada con las instrucciones
        self.cpu = cpu
        self.fin = False
        self.ciclo_actual = 0

        # inicialmente comprobamos que están limpio
        self.ID_EX = RegistroAcoplamiento()
        self.IF_ID = RegistroAcoplamiento()
        self.EX_MEM = RegistroAcoplamiento()
        self.MEM_WB = RegistroAcoplamiento()

        self.WB_OUT = RegistroAcoplamiento()

    def simular(self):
        while not self.fin:
            self.ciclo_actual += 1

            # Ejecutamos en orden inverso para no pisar los registros de acoplamiento
            self.fase_wb() #parametros de entrada son el contenido de ex/mem o si el flag de operacion nula. NO devuelve nada
            self.fase_mem() #utiliza el ex/mem
            self.fase_ex() #aqui tocamos cosas fisicas y la funcion ex guarda algo en el registro de acoplamiento ex/mem, pero no puede hacerlo ahora asiq lo guarda en un ax





            # aqui ya podemos guardar en ex/mem
            self.fase_id()  #devuelve informacion que se guarda en el id
            self.fase_if() #dado el pc devuelve la instruccion que guarda en if/id

            self.imprimir_estado()

            self.imprimir_registros()

            if (self.IF_ID.inst in [None, "NOP"] and
                    self.ID_EX.inst in [None, "NOP"] and
                    self.EX_MEM.inst in [None, "NOP"] and
                    self.MEM_WB.inst in [None, "NOP"]):
                self.fin = True

    # Usa la información de self.cpu.MEM_WB
    def fase_wb(self):
        # 1. Leer el buffer de entrada (MEM_WB)
        inst_str = self.MEM_WB.inst

        if not inst_str or inst_str == "NOP":
            # Usamos WB_OUT para decirle al bucle principal que ha salido un NOP o una burbuja
            self.WB_OUT.inst = inst_str
            return

        senales = self.MEM_WB.senales_control
        reg_destino = self.MEM_WB.reg_dest

        # 2. Simular el Multiplexor MEM_TO_REG
        if senales["mem_to_reg"] == 1:
            # Instrucción 'lw': el dato válido viene de la Memoria de Datos
            dato_a_escribir = self.MEM_WB.dato_mem
        else:
            # Instrucción aritmética (add, addi...): el dato válido viene de la ALU
            dato_a_escribir = self.MEM_WB.resultado_alu

        # 3. Interactuar con el hardware físico (Banco de Registros)
        if senales["reg_write"] == 1:
            # Regla de oro de MIPS: el registro $0 es inmutable
            if reg_destino not in ["$0", "$zero"]:
                self.cpu.unidad_proceso.banco_registros.escribir(reg_destino, dato_a_escribir)

        # 4. Guardar en el registro de salida para contabilizar la instrucción completada
        self.WB_OUT.inst = inst_str

    # Usa la información de self.cpu.EX_MEM y escribe en MEM_WB
    def fase_mem(self):
        # 1. Leer el buffer de entrada (EX_MEM)
        inst_str = self.EX_MEM.inst
        pc_actual = self.EX_MEM.pc

        if not inst_str or inst_str == "NOP":
            self.MEM_WB.inst = "NOP"
            self.MEM_WB.pc = pc_actual
            return

        senales = self.EX_MEM.senales_control

        # En instrucciones de memoria, el resultado de la ALU es la dirección exacta a la que queremos acceder
        direccion_memoria = self.EX_MEM.resultado_alu
        dato_leido = 0

        # 2. Interactuar con el hardware físico (Memoria de Datos)
        if senales["mem_read"] == 1:
            # Instrucción 'lw': Leemos el dato de la memoria
            dato_leido = self.cpu.unidad_proceso.mem_datos.leer(direccion_memoria)

        if senales["mem_write"] == 1:
            # Instrucción 'sw': Escribimos el dato arrastrado desde ID_EX en la memoria
            dato_a_escribir = self.EX_MEM.dato_sw
            self.cpu.unidad_proceso.mem_datos.escribir(direccion_memoria, dato_a_escribir)

        # 3. Guardar todo en la última cinta transportadora (MEM_WB)
        self.MEM_WB.inst = inst_str
        self.MEM_WB.pc = pc_actual

        # Pasamos el resultado de la ALU intacto (vital para instrucciones como 'add' que no usan memoria)
        self.MEM_WB.resultado_alu = direccion_memoria

        self.MEM_WB.dato_mem = dato_leido
        self.MEM_WB.reg_dest = self.EX_MEM.reg_dest

        # Solo pasamos a la última fase las dos señales de control que aún necesita
        self.MEM_WB.senales_control = {
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }

    def fase_ex(self):
        # 1. Leer el buffer de entrada
        inst_str = self.ID_EX.inst
        pc_actual = self.ID_EX.pc

        if not inst_str or inst_str == "NOP":
            self.EX_MEM.inst = "NOP"
            self.EX_MEM.pc = pc_actual
            return

        senales = self.ID_EX.senales_control


        val_rs = self.ID_EX.op1
        val_rt = self.ID_EX.op2

        #RIEGOS DE TIPO 1 (el dato está a un ciclo)
        ex_mem_reg_write = self.EX_MEM.senales_control.get("reg_write", 0)
        ex_mem_rd = self.EX_MEM.reg_dest

        if ex_mem_reg_write == 1 and ex_mem_rd not in ["", "$0", "$zero"]:
            if ex_mem_rd == self.ID_EX.rs:
                val_rs = self.EX_MEM.resultado_alu
            if ex_mem_rd == self.ID_EX.rt:
                val_rt = self.EX_MEM.resultado_alu


        #RIESGOS DE TIPO 2 (el dato está a dos ciclos)
        mem_wb_reg_write = self.MEM_WB.senales_control.get("reg_write", 0)
        mem_wb_rd = self.MEM_WB.reg_dest

        # El dato adelantado desde WB depende de si fue un 'lw' o una operación de ALU
        if self.MEM_WB.senales_control.get("mem_to_reg", 0) == 1:
            dato_wb = self.MEM_WB.dato_mem
        else:
            dato_wb = self.MEM_WB.resultado_alu

        if mem_wb_reg_write == 1 and mem_wb_rd not in ["", "$0", "$zero"]:
            # Solo adelantamos desde WB si la etapa MEM no ha adelantado ya ese mismo registro (tiene prioridad el más reciente)
            if mem_wb_rd == self.ID_EX.rs and not (ex_mem_reg_write == 1 and ex_mem_rd == self.ID_EX.rs):
                val_rs = dato_wb
            if mem_wb_rd == self.ID_EX.rt and not (ex_mem_reg_write == 1 and ex_mem_rd == self.ID_EX.rt):
                val_rt = dato_wb

        # 2. Simular el Multiplexor ALU_SRC
        op1 = val_rs

        if senales["alu_src"] == 1:
            op2 = self.ID_EX.inmediato
        else:
            op2 = val_rt

        # 3. Usar el hardware físico (ALU) para el cálculo
        self.cpu.unidad_proceso.alu.entrada1 = op1
        self.cpu.unidad_proceso.alu.entrada2 = op2
        self.cpu.unidad_proceso.alu.ejecutar(senales["alu_op"])

        resultado = self.cpu.unidad_proceso.alu.resultado

        # 4. Simular el Multiplexor REG_DST
        # Si es formato R (ej. add), va a rd. Si es formato I (ej. lw, addi), va a rt.
        if senales["reg_dst"] == 1:
            reg_destino = self.ID_EX.rd
        else:
            reg_destino = self.ID_EX.rt

        # 5. Guardar todo en la cinta transportadora de salida (EX_MEM)
        self.EX_MEM.inst = inst_str
        self.EX_MEM.pc = pc_actual
        self.EX_MEM.resultado_alu = resultado

        # En una instrucción 'sw', necesitamos el valor original leído del registro origen
        # para guardarlo en memoria. Lo arrastramos aquí.
        self.EX_MEM.dato_sw = self.ID_EX.op2

        self.EX_MEM.reg_dest = reg_destino

        # Pasamos a la siguiente fase solo las señales de control que aún hacen falta
        self.EX_MEM.senales_control = {
            "mem_read": senales["mem_read"],
            "mem_write": senales["mem_write"],
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }

    # Decodifica self.cpu.IF_ID y pasa datos a ID_EX
    def fase_id(self):
        # 1. Leer el buffer de entrada
        inst_str = self.IF_ID.inst
        pc_actual = self.IF_ID.pc

        if not inst_str or inst_str == "NOP":
            self.ID_EX.inst = "NOP"
            self.ID_EX.pc = pc_actual
            return

        # 2. Usar el hardware de la CPU para decodificar
        # Esto configura las señales internas de self.cpu.unidad_control
        datos = self.cpu.unidad_control.decodificar(inst_str)
        opcode = datos["opcode"]
        args = datos["args"]

        op1_val = 0
        op2_val = 0
        inmediato = 0
        rs = ""
        rt = ""
        rd = ""

        # 3. Extraer operandos y leer del hardware (Banco de Registros)
        if opcode == "addi":
            # Formato I (Ej: addi $t1, $t2, 100 -> args = ['$t1', '$t2', '100'])
            rt = args[0]
            rs = args[1]
            inmediato = int(args[2])

            op1_val = self.cpu.unidad_proceso.banco_registros.leer(rs)
            op2_val = self.cpu.unidad_proceso.banco_registros.leer(rt)

        elif opcode in ["lw","sw"]:
            # args llega como ['$s1', '0($0)']
            rt = args[0]

            # Limpiamos el paréntesis de cierre y partimos por el de apertura
            # '0($0)' -> replace -> '0($0' -> split -> ['0', '$0']
            partes_mem = args[1].replace(')', '').split('(')

            inmediato = int(partes_mem[0])  # El offset numérico (0)
            rs = partes_mem[1]  # El registro base ('$0')

            # Leemos físicamente los valores
            op1_val = self.cpu.unidad_proceso.banco_registros.leer(rs)
            op2_val = self.cpu.unidad_proceso.banco_registros.leer(rt)

        elif opcode in ["add", "sub", "and", "or", "slt"]:
            # Formato R (Ej: add $t1, $t2, $t3 -> args = ['$t1', '$t2', '$t3'])
            rd = args[0]
            rs = args[1]
            rt = args[2]

            op1_val = self.cpu.unidad_proceso.banco_registros.leer(rs)
            op2_val = self.cpu.unidad_proceso.banco_registros.leer(rt)

        elif opcode == "beq":
            # SALTO RESUELTO EN ID
            rs = args[0]
            rt = args[1]
            etiqueta = args[2]

            val1 = self.cpu.unidad_proceso.banco_registros.leer(rs)
            val2 = self.cpu.unidad_proceso.banco_registros.leer(rt)

            if val1 == val2:
                # Modificamos directamente el PC de la máquina física
                self.cpu.unidad_proceso.pc.contador = self.cpu.etiquetas.get(etiqueta, 0)
                # Al saltar, lo que hay en IF_ID (instrucción siguiente) no sirve, hay que vaciarlo
                self.IF_ID.inst = "NOP"

        # 4. DETECCIÓN DE RIESGOS (LOAD-USE)
        # Miramos si la instrucción anterior (que ahora está en ID_EX) es un 'lw'
        # y si su destino coincide con nuestro rs o rt.
        if self.ID_EX.inst not in [None, "NOP"]:
            ex_mem_read = self.ID_EX.senales_control.get("mem_read", 0)
            ex_rt = self.ID_EX.rt

            if ex_mem_read == 1 and ex_rt in [rs, rt] and ex_rt not in ["", "$0", "$zero"]:
                # ¡Riesgo detectado! Levantamos bandera, inyectamos NOP y salimos
                self.hazard_stall = True
                self.ID_EX.inst = "NOP"
                return

        # 5. Guardar todo en el registro de salida ID_EX para el siguiente ciclo
        self.ID_EX.inst = inst_str
        self.ID_EX.pc = pc_actual
        self.ID_EX.op1 = op1_val
        self.ID_EX.op2 = op2_val
        self.ID_EX.inmediato = inmediato
        self.ID_EX.rs = rs
        self.ID_EX.rt = rt
        self.ID_EX.rd = rd

        # "Fotografiamos" las señales de control para que viajen con la instrucción
        self.ID_EX.senales_control = {
            "alu_src": self.cpu.unidad_control.alu_src,
            "alu_op": self.cpu.unidad_control.alu_op,
            "reg_dst": self.cpu.unidad_control.reg_dst,
            "reg_write": self.cpu.unidad_control.reg_write,
            "mem_read": self.cpu.unidad_control.mem_read,
            "mem_write": self.cpu.unidad_control.mem_write,
            "mem_to_reg": self.cpu.unidad_control.mem_to_reg
        }

    # Lee la Memoria de Instrucciones y escribe en IF_ID
    def fase_if(self):
        # 1. Leer el valor actual del Program Counter (PC) físico
        pc_actual = self.cpu.unidad_proceso.pc.contador

        # 2. Leer la instrucción de la Memoria de Instrucciones física
        # Si el PC apunta a una dirección sin código, inyectamos una burbuja ("NOP")
        inst_str = self.cpu.unidad_proceso.mem_instrucciones.instrucciones.get(pc_actual, "NOP")

        # 3. Escribir los datos en la primera cinta transportadora (Registro IF_ID)
        self.IF_ID.inst = inst_str
        self.IF_ID.pc = pc_actual

        # 4. Avanzar el PC para el próximo ciclo
        # Nota: En MIPS real se suma 4 porque la memoria va por bytes.
        # Si tu diccionario usa índices 0, 1, 2..., sumamos 1.
        if inst_str != "NOP":
            self.cpu.unidad_proceso.pc.contador += 1

    def imprimir_estado(self):
        print(f"\n--- Ciclo {self.ciclo_actual} ---")
        # Aquí puedes imprimir qué hay en IF_ID, ID_EX, etc.
        print(self.IF_ID.inst )
            

    def imprimir_registros(self):
        self.cpu.unidad_proceso.banco_registros.imprimir_registros()
            
    #REGISTROS DE ACOPLAMIENTO
            #IF/ID guarda la ultima instruccion y el pc actual
            
            #ID/EX guarda tipoins reg1, reg2, regcode1, regcode2, etiqueta, offset, regdest; es decir la información troceada
            
            #EX/MEM guarda regcode1, regcode2, offset, regDest y valor de la alu
            
            #MEM/WB guardamos seguro el tipo con regDest, 
