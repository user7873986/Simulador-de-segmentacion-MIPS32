
class Segmentacion:
    def __init__(self, cpu):
        # Recibimos la CPU ya cargada con las instrucciones
        self.cpu = cpu
        self.fin = False
        self.ciclo_actual = 0
        self.burbuja = False
        self.mensaje_burbuja = ""
        self.mensaje_salto = ""

    def simular(self):
        while not self.fin:
            self.ciclo_actual += 1

            # Ejecutamos en orden inverso para no pisar los registros de acoplamiento
            self.wb()  # parametros de entrada son el contenido de ex/mem o si el flag de operacion nula. NO devuelve nada
            self.mem()  # utiliza el ex/mem
            self.ex()  # aqui tocamos cosas fisicas y la funcion ex guarda algo en el registro de acoplamiento ex/mem, pero no puede hacerlo ahora asiq lo guarda en un ax

            # aqui ya podemos guardar en ex/mem
            self.id()  # devuelve informacion que se guarda en el id
            self.iff()  # dado el pc devuelve la instruccion que guarda en if/id

            self.imprimir_estado()

            if (self.cpu.unidad_proceso.IF_ID.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.ID_EX.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.EX_MEM.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.MEM_WB.inst in [None, "NOP"]):
                self.fin = True


    def iff(self):
        if self.burbuja:
            self.burbuja = False
            return

        pc = self.cpu.unidad_proceso.pc.contador
        inst = self.cpu.unidad_proceso.mem_instrucciones.instrucciones.get(pc)

        self.cpu.unidad_proceso.IF_ID.inst = inst
        self.cpu.unidad_proceso.IF_ID.pc = pc

        if inst != "NOP":
            self.cpu.unidad_proceso.pc.contador += 1


    # Decodifica self.cpu.unidad_proceso.IF_ID y pasa datos a ID_EX
    def id(self):
        inst = self.cpu.unidad_proceso.IF_ID.inst
        pc = self.cpu.unidad_proceso.IF_ID.pc

        decodificado = self.cpu.unidad_control.decodificar(inst)
        if not inst or inst == "NOP":
            self.inyectar_burbuja()
            return

        rs = decodificado["rs"]
        rt = decodificado["rt"]
        rd = decodificado["rd"]
        inmediato = decodificado["inmediato"]
        opcode = decodificado["opcode"]

        val_rs = self.cpu.unidad_proceso.banco_registros.leer(rs)
        val_rt = self.cpu.unidad_proceso.banco_registros.leer(rt)

        if opcode == "bne":
            etiqueta = decodificado["etiqueta"]

            # OJO TODDO ESTE BLOQUE
            id_ex_reg_write = self.cpu.unidad_proceso.ID_EX.senales_control.get("reg_write", 0)
            id_ex_dest = self.cpu.unidad_proceso.ID_EX.rd if self.cpu.unidad_proceso.ID_EX.senales_control.get(
                "reg_dst", 0) == 1 else self.cpu.unidad_proceso.ID_EX.rt
            id_ex_dest = id_ex_dest.strip() if id_ex_dest else ""
            riesgo_ex = id_ex_reg_write == 1 and id_ex_dest in [rs, rt] and id_ex_dest not in ["", "$0", "$zero"]

            ex_mem_reg_write = self.cpu.unidad_proceso.EX_MEM.senales_control.get("reg_write", 0)
            ex_mem_dest = self.cpu.unidad_proceso.EX_MEM.reg_dest.strip() if self.cpu.unidad_proceso.EX_MEM.reg_dest else ""
            riesgo_mem = ex_mem_reg_write == 1 and ex_mem_dest in [rs, rt] and ex_mem_dest not in ["", "$0", "$zero"]

            mem_wb_reg_write = self.cpu.unidad_proceso.MEM_WB.senales_control.get("reg_write", 0)
            mem_wb_dest = self.cpu.unidad_proceso.MEM_WB.reg_dest.strip() if self.cpu.unidad_proceso.MEM_WB.reg_dest else ""
            riesgo_wb = mem_wb_reg_write == 1 and mem_wb_dest in [rs, rt] and mem_wb_dest not in ["", "$0", "$zero"]

            if riesgo_ex or riesgo_mem or riesgo_wb:
                self.burbuja = True
                self.mensaje_burbuja = "BURBUJA"
                self.inyectar_burbuja()
                return

            val1 = self.cpu.unidad_proceso.banco_registros.leer(rs)
            val2 = self.cpu.unidad_proceso.banco_registros.leer(rt)

            if val1 != val2:
                nuevo_pc = self.cpu.etiquetas.get(etiqueta)
                self.cpu.unidad_proceso.pc.set_pc(nuevo_pc)
                self.mensaje_salto = f"[salto resuelto en ID: condición cumplida -> nuevo PC {nuevo_pc}]"
                self.cpu.unidad_proceso.IF_ID.inst = "NOP"
            else:
                self.mensaje_salto = f"[salto resuelto en ID: condición fallida -> no salta]"

            self.inyectar_burbuja()
            return

        if opcode == "j":
            etiqueta = decodificado["etiqueta"]
            nuevo_pc = self.cpu.etiquetas.get(etiqueta, 0)
            self.cpu.unidad_proceso.pc.set_pc(nuevo_pc)
            self.mensaje_salto = f"[salto incondicional -> nuevo PC {nuevo_pc}]"
            self.inyectar_burbuja()
            return

        #OJO MIRAR AQUI
        if self.cpu.unidad_proceso.ID_EX.inst not in [None, "NOP"]:
            ex_mem_read = self.cpu.unidad_proceso.ID_EX.senales_control.get("mem_read", 0)
            ex_rt = self.cpu.unidad_proceso.ID_EX.rt

            if ex_mem_read == 1 and ex_rt in [rs, rt] and ex_rt not in ["", "$0", "$zero"]:
                self.burbuja = True
                self.mensaje_burbuja = "STALL(load-use)"
                self.inyectar_burbuja()
                return

        self.cpu.unidad_proceso.ID_EX.inst = inst
        self.cpu.unidad_proceso.ID_EX.pc = pc
        self.cpu.unidad_proceso.ID_EX.op1 = val_rs
        self.cpu.unidad_proceso.ID_EX.op2 = val_rt
        self.cpu.unidad_proceso.ID_EX.inmediato = inmediato
        self.cpu.unidad_proceso.ID_EX.rs = rs
        self.cpu.unidad_proceso.ID_EX.rt = rt
        self.cpu.unidad_proceso.ID_EX.rd = rd
        self.cpu.unidad_proceso.ID_EX.senales_control = decodificado["senales"]

    def ex(self):
        inst = self.cpu.unidad_proceso.ID_EX.inst
        pc = self.cpu.unidad_proceso.ID_EX.pc

        if not inst or inst == "NOP":
            self.cpu.unidad_proceso.EX_MEM.inst = "NOP"
            self.cpu.unidad_proceso.EX_MEM.pc = pc
            self.cpu.unidad_proceso.EX_MEM.reg_dest = ""
            self.cpu.unidad_proceso.EX_MEM.senales_control = {
                "mem_read": 0, "mem_write": 0, "reg_write": 0, "mem_to_reg": 0
            }
            return

        senales = self.cpu.unidad_proceso.ID_EX.senales_control #solo las necesarias

        rs = self.cpu.unidad_proceso.ID_EX.rs
        rt = self.cpu.unidad_proceso.ID_EX.rt

        val_rs = self.cpu.unidad_proceso.banco_registros.leer(rs)
        val_rt = self.cpu.unidad_proceso.banco_registros.leer(rt)

        # Unidad de forwarding
        ex_mem_reg_write = self.cpu.unidad_proceso.EX_MEM.senales_control.get("reg_write") #espío si la instrucción de antes va a escribir en un registro
        ex_mem_rd = self.cpu.unidad_proceso.EX_MEM.reg_dest

        if ex_mem_reg_write == 1:
            if ex_mem_rd == rs:
                val_rs = self.cpu.unidad_proceso.EX_MEM.resultado_alu
            if ex_mem_rd == rt:
                val_rt = self.cpu.unidad_proceso.EX_MEM.resultado_alu

        op1 = val_rs
        if senales["alu_src"] == 1:
            op2 = self.cpu.unidad_proceso.ID_EX.inmediato
        else:
            op2 = val_rt

        self.cpu.unidad_proceso.alu.entrada1 = op1
        self.cpu.unidad_proceso.alu.entrada2 = op2
        self.cpu.unidad_proceso.alu.ejecutar(senales["alu_op"])
        resultado = self.cpu.unidad_proceso.alu.resultado

        # multiplexor
        if senales["reg_dst"] == 1:
            reg_destino = self.cpu.unidad_proceso.ID_EX.rd
        else:
            reg_destino = rt

        self.cpu.unidad_proceso.EX_MEM.inst = inst
        self.cpu.unidad_proceso.EX_MEM.pc = pc
        self.cpu.unidad_proceso.EX_MEM.resultado_alu = resultado
        self.cpu.unidad_proceso.EX_MEM.dato_sw = val_rt
        self.cpu.unidad_proceso.EX_MEM.reg_dest = reg_destino
        self.cpu.unidad_proceso.EX_MEM.senales_control = {
            "mem_read": senales["mem_read"],
            "mem_write": senales["mem_write"],
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }

    def mem(self):
        inst = self.cpu.unidad_proceso.EX_MEM.inst
        pc = self.cpu.unidad_proceso.EX_MEM.pc

        if not inst or inst == "NOP":
            self.burbuja_mem(pc)
            return

        senales = self.cpu.unidad_proceso.EX_MEM.senales_control

        # En instrucciones de memoria, el resultado de la ALU es la dirección exacta a la que queremos acceder
        direccion_memoria = self.cpu.unidad_proceso.EX_MEM.resultado_alu
        dato_leido = 0

        # 2. Interactuar con el hardware físico (Memoria de Datos)
        if senales["mem_read"] == 1:
            # Instrucción 'lw': Leemos el dato de la memoria
            dato_leido = self.cpu.unidad_proceso.mem_datos.leer(direccion_memoria)

        if senales["mem_write"] == 1:
            # Instrucción 'sw': Escribimos el dato arrastrado desde ID_EX en la memoria
            dato_a_escribir = self.cpu.unidad_proceso.EX_MEM.dato_sw
            self.cpu.unidad_proceso.mem_datos.escribir(direccion_memoria, dato_a_escribir)

        # 3. Guardar todo en la última cinta transportadora (MEM_WB)
        self.cpu.unidad_proceso.MEM_WB.inst = inst
        self.cpu.unidad_proceso.MEM_WB.pc = pc

        # Pasamos el resultado de la ALU intacto (vital para instrucciones como 'add' que no usan memoria)
        self.cpu.unidad_proceso.MEM_WB.resultado_alu = direccion_memoria
        self.cpu.unidad_proceso.MEM_WB.dato_mem = dato_leido
        self.cpu.unidad_proceso.MEM_WB.reg_dest = self.cpu.unidad_proceso.EX_MEM.reg_dest

        # Solo pasamos a la última fase las dos señales de control que aún necesita
        self.cpu.unidad_proceso.MEM_WB.senales_control = {
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }


    # Usa la información de self.cpu.MEM_WB
    def wb(self):
        inst = self.cpu.unidad_proceso.MEM_WB.inst

        if not inst or inst == "NOP": #ie hemos metido una burbuja
            self.cpu.unidad_proceso.WB_OUT.inst = inst
            return

        senales = self.cpu.unidad_proceso.MEM_WB.senales_control
        reg_destino = self.cpu.unidad_proceso.MEM_WB.reg_dest

        if senales["mem_to_reg"] == 1:
            valor = self.cpu.unidad_proceso.MEM_WB.dato_mem
        else:
            valor = self.cpu.unidad_proceso.MEM_WB.resultado_alu

        # 3. Interactuar con el hardware físico (Banco de Registros)
        if senales["reg_write"] == 1:
            # Regla de oro de MIPS: el registro $0 es inmutable
            if reg_destino not in ["$0", "$zero"]:
                self.cpu.unidad_proceso.banco_registros.escribir(reg_destino, valor)

        # 4. Guardar en el registro de salida para contabilizar la instrucción completada
        self.cpu.unidad_proceso.WB_OUT.inst = inst
        self.cpu.unidad_proceso.WB_OUT.reg_dest = reg_destino
        self.cpu.unidad_proceso.WB_OUT.dato_wb = valor
        self.cpu.unidad_proceso.WB_OUT.reg_write = senales.get("reg_write", 0)


    def burbuja_id(self):
        self.cpu.unidad_proceso.ID_EX.inst = "NOP"
        self.cpu.unidad_proceso.ID_EX.rs = ""
        self.cpu.unidad_proceso.ID_EX.rt = ""
        self.cpu.unidad_proceso.ID_EX.rd = ""
        self.cpu.unidad_proceso.ID_EX.senales_control = {}


    def burbuja_ex(self, pc):
        self.cpu.unidad_proceso.EX_MEM.inst = "NOP"
        self.cpu.unidad_proceso.EX_MEM.pc = pc
        self.cpu.unidad_proceso.EX_MEM.reg_dest = ""
        self.cpu.unidad_proceso.EX_MEM.senales_control = {"mem_read": 0, "mem_write": 0, "reg_write": 0, "mem_to_reg": 0}

    def burbuja_mem(self, pc):
        self.cpu.unidad_proceso.MEM_WB.inst = "NOP"
        self.cpu.unidad_proceso.MEM_WB.pc = pc
        self.cpu.unidad_proceso.MEM_WB.reg_dest = ""
        self.cpu.unidad_proceso.MEM_WB.senales_control = {"reg_write": 0, "mem_to_reg": 0}

    def imprimir_estado(self):
        stall_str = ""
        if getattr(self, "mensaje_burbuja", "") != "":
            stall_str = f"  STALL({self.mensaje_burbuja})"
            self.mensaje_burbuja = ""

        print(f"\nCiclo {self.ciclo_actual:02d}{stall_str}")

        _if = self.cpu.unidad_proceso.IF_ID.inst if self.cpu.unidad_proceso.IF_ID.inst != "NOP" else "--"
        _id = self.cpu.unidad_proceso.ID_EX.inst if self.cpu.unidad_proceso.ID_EX.inst != "NOP" else "--"
        _ex = self.cpu.unidad_proceso.EX_MEM.inst if self.cpu.unidad_proceso.EX_MEM.inst != "NOP" else "--"
        _mem = self.cpu.unidad_proceso.MEM_WB.inst if self.cpu.unidad_proceso.MEM_WB.inst != "NOP" else "--"
        _wb = self.cpu.unidad_proceso.WB_OUT.inst if self.cpu.unidad_proceso.WB_OUT.inst != "NOP" else "--"

        print(f"IF: {_if} | ID: {_id} | EX: {_ex} | MEM: {_mem} | WB: {_wb}")

        if getattr(self, "mensaje_salto", "") != "":
            print(self.mensaje_salto)
            self.mensaje_salto = ""

        print("-" * 75)
        self.cpu.unidad_proceso.banco_registros.imprimir_registros()
        self.cpu.unidad_proceso.mem_datos.imprimir_memoria()

        etiquetas = self.cpu.etiquetas
        if etiquetas:
            str_etiquetas = " | ".join([f"{nombre}: PC {valor}" for nombre, valor in etiquetas.items()])
            print(f"ETIQUETAS: {str_etiquetas}")
        else:
            print("ETIQUETAS: (ninguna)")

        print("-" * 75)