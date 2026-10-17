from Componentes.pc import PC
from Componentes.registro_acoplamiento import RegistroAcoplamiento


class Segmentacion:
    def __init__(self, cpu):
        # Recibimos la CPU ya cargada con las instrucciones
        self.cpu = cpu
        self.fin = False
        self.ciclo_actual = 0


    def simular(self):
        while not self.fin:
            self.ciclo_actual += 1

            # Ejecutamos en orden inverso para no pisar los registros de acoplamiento
            self.fase_wb()  # parametros de entrada son el contenido de ex/mem o si el flag de operacion nula. NO devuelve nada
            self.fase_mem()  # utiliza el ex/mem
            self.fase_ex()  # aqui tocamos cosas fisicas y la funcion ex guarda algo en el registro de acoplamiento ex/mem, pero no puede hacerlo ahora asiq lo guarda en un ax

            # aqui ya podemos guardar en ex/mem
            self.fase_id()  # devuelve informacion que se guarda en el id
            self.fase_if()  # dado el pc devuelve la instruccion que guarda en if/id

            self.imprimir_estado()

            # Comprobación de fin de programa leyendo los registros físicos
            if (self.cpu.unidad_proceso.IF_ID.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.ID_EX.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.EX_MEM.inst in [None, "NOP"] and
                    self.cpu.unidad_proceso.MEM_WB.inst in [None, "NOP"]):
                self.fin = True

    # Usa la información de self.cpu.MEM_WB
    def fase_wb(self):
        # 1. Leer el buffer de entrada (MEM_WB)
        inst_str = self.cpu.unidad_proceso.MEM_WB.inst

        if not inst_str or inst_str == "NOP":
            # Usamos WB_OUT para decirle al bucle principal que ha salido un NOP o una burbuja
            self.cpu.unidad_proceso.WB_OUT.inst = inst_str
            return

        senales = self.cpu.unidad_proceso.MEM_WB.senales_control
        reg_destino = self.cpu.unidad_proceso.MEM_WB.reg_dest

        # 2. Simular el Multiplexor MEM_TO_REG
        if senales["mem_to_reg"] == 1:
            # Instrucción 'lw': el dato válido viene de la Memoria de Datos
            dato_a_escribir = self.cpu.unidad_proceso.MEM_WB.dato_mem
        else:
            # Instrucción aritmética (add, addi...): el dato válido viene de la ALU
            dato_a_escribir = self.cpu.unidad_proceso.MEM_WB.resultado_alu

        # 3. Interactuar con el hardware físico (Banco de Registros)
        if senales["reg_write"] == 1:
            # Regla de oro de MIPS: el registro $0 es inmutable
            if reg_destino not in ["$0", "$zero"]:
                self.cpu.unidad_proceso.banco_registros.escribir(reg_destino, dato_a_escribir)

        # 4. Guardar en el registro de salida para contabilizar la instrucción completada
        self.cpu.unidad_proceso.WB_OUT.inst = inst_str
        self.cpu.unidad_proceso.WB_OUT.reg_dest = reg_destino
        self.cpu.unidad_proceso.WB_OUT.dato_wb = dato_a_escribir
        self.cpu.unidad_proceso.WB_OUT.reg_write = senales.get("reg_write", 0)

    # Usa la información de self.cpu.unidad_proceso.EX_MEM y escribe en MEM_WB
    def fase_mem(self):
        # 1. Leer el buffer de entrada (EX_MEM)
        inst_str = self.cpu.unidad_proceso.EX_MEM.inst
        pc_actual = self.cpu.unidad_proceso.EX_MEM.pc

        if not inst_str or inst_str == "NOP":
            self.cpu.unidad_proceso.MEM_WB.inst = "NOP"
            self.cpu.unidad_proceso.MEM_WB.pc = pc_actual
            self.cpu.unidad_proceso.MEM_WB.reg_dest = ""
            self.cpu.unidad_proceso.MEM_WB.senales_control = {
                "reg_write": 0,
                "mem_to_reg": 0
            }
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
        self.cpu.unidad_proceso.MEM_WB.inst = inst_str
        self.cpu.unidad_proceso.MEM_WB.pc = pc_actual

        # Pasamos el resultado de la ALU intacto (vital para instrucciones como 'add' que no usan memoria)
        self.cpu.unidad_proceso.MEM_WB.resultado_alu = direccion_memoria
        self.cpu.unidad_proceso.MEM_WB.dato_mem = dato_leido
        self.cpu.unidad_proceso.MEM_WB.reg_dest = self.cpu.unidad_proceso.EX_MEM.reg_dest

        # Solo pasamos a la última fase las dos señales de control que aún necesita
        self.cpu.unidad_proceso.MEM_WB.senales_control = {
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }

    def fase_ex(self):
        inst_str = self.cpu.unidad_proceso.ID_EX.inst
        pc_actual = self.cpu.unidad_proceso.ID_EX.pc

        if not inst_str or inst_str == "NOP":
            self.cpu.unidad_proceso.EX_MEM.inst = "NOP"
            self.cpu.unidad_proceso.EX_MEM.pc = pc_actual
            self.cpu.unidad_proceso.EX_MEM.reg_dest = ""
            self.cpu.unidad_proceso.EX_MEM.senales_control = {
                "mem_read": 0, "mem_write": 0, "reg_write": 0, "mem_to_reg": 0
            }
            return

        senales = self.cpu.unidad_proceso.ID_EX.senales_control

        # Limpiamos espacios y basura de los nombres (el fallo más común en Python)
        rs_limpio = self.cpu.unidad_proceso.ID_EX.rs.strip() if self.cpu.unidad_proceso.ID_EX.rs else ""
        rt_limpio = self.cpu.unidad_proceso.ID_EX.rt.strip() if self.cpu.unidad_proceso.ID_EX.rt else ""

        val_rs = self.cpu.unidad_proceso.ID_EX.op1
        val_rt = self.cpu.unidad_proceso.ID_EX.op2

        # REFRESCO SEGURO DEL BANCO DE REGISTROS
        if rs_limpio not in ["", "$0", "$zero"]:
            val_rs = self.cpu.unidad_proceso.banco_registros.leer(rs_limpio)
        if rt_limpio not in ["", "$0", "$zero"]:
            val_rt = self.cpu.unidad_proceso.banco_registros.leer(rt_limpio)

        # FORWARDING TIPO 1: EX/MEM
        ex_mem_reg_write = self.cpu.unidad_proceso.EX_MEM.senales_control.get("reg_write", 0)
        ex_mem_rd = self.cpu.unidad_proceso.EX_MEM.reg_dest.strip() if self.cpu.unidad_proceso.EX_MEM.reg_dest else ""

        if ex_mem_reg_write == 1 and ex_mem_rd not in ["", "$0", "$zero"]:
            if ex_mem_rd == rs_limpio:
                val_rs = self.cpu.unidad_proceso.EX_MEM.resultado_alu
            if ex_mem_rd == rt_limpio:
                val_rt = self.cpu.unidad_proceso.EX_MEM.resultado_alu

        # --- CHIVATO PARA LA CONSOLA ---
        print(f"[DEBUG ALU] {inst_str:^18} | rs({rs_limpio})={val_rs} | rt({rt_limpio})={val_rt}")
        # -------------------------------

        # EJECUCIÓN
        op1 = val_rs
        if senales["alu_src"] == 1:
            op2 = self.cpu.unidad_proceso.ID_EX.inmediato
        else:
            op2 = val_rt

        self.cpu.unidad_proceso.alu.entrada1 = op1
        self.cpu.unidad_proceso.alu.entrada2 = op2
        self.cpu.unidad_proceso.alu.ejecutar(senales["alu_op"])
        resultado = self.cpu.unidad_proceso.alu.resultado

        # MULTIPLEXOR DESTINO
        if senales["reg_dst"] == 1:
            reg_destino = self.cpu.unidad_proceso.ID_EX.rd.strip() if self.cpu.unidad_proceso.ID_EX.rd else ""
        else:
            reg_destino = rt_limpio

        # GUARDAR EN EX_MEM
        self.cpu.unidad_proceso.EX_MEM.inst = inst_str
        self.cpu.unidad_proceso.EX_MEM.pc = pc_actual
        self.cpu.unidad_proceso.EX_MEM.resultado_alu = resultado
        self.cpu.unidad_proceso.EX_MEM.dato_sw = val_rt
        self.cpu.unidad_proceso.EX_MEM.reg_dest = reg_destino
        self.cpu.unidad_proceso.EX_MEM.senales_control = {
            "mem_read": senales["mem_read"],
            "mem_write": senales["mem_write"],
            "reg_write": senales["reg_write"],
            "mem_to_reg": senales["mem_to_reg"]
        }

    # Decodifica self.cpu.unidad_proceso.IF_ID y pasa datos a ID_EX
    def fase_id(self):
        inst_str = self.cpu.unidad_proceso.IF_ID.inst
        pc_actual = self.cpu.unidad_proceso.IF_ID.pc

        decodificado = self.cpu.unidad_control.decodificar(inst_str)
        if not inst_str or inst_str == "NOP":
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

            # --- RADAR DE RIESGOS PARA SALTOS (Branch Interlock) ---
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
                self.hazard_stall = True
                self.mensaje_stall = "STALL(branch-hazard)"
                self.inyectar_burbuja()
                return

            val1 = self.cpu.unidad_proceso.banco_registros.leer(rs)
            val2 = self.cpu.unidad_proceso.banco_registros.leer(rt)

            if val1 != val2:
                nuevo_pc = self.cpu.etiquetas.get(etiqueta, 0)
                self.cpu.unidad_proceso.pc.set_pc(nuevo_pc)
                self.mensaje_salto = f"    [salto resuelto en ID: condición CUMPLIDA -> objetivo PC {nuevo_pc}]"
                self.cpu.unidad_proceso.IF_ID.inst = "NOP"
            else:
                self.mensaje_salto = f"    [salto resuelto en ID: condición FALLIDA -> no salta]"

            self.inyectar_burbuja()
            return

        if opcode == "j":
            etiqueta = decodificado["etiqueta"]
            nuevo_pc = self.cpu.etiquetas.get(etiqueta, 0)
            self.cpu.unidad_proceso.pc.set_pc(nuevo_pc)
            self.mensaje_salto = f"    [salto resuelto en ID: incondicional -> objetivo PC {nuevo_pc}]"
            self.inyectar_burbuja()
            return

        # 4. DETECCIÓN DE RIESGOS (LOAD-USE)
        if self.cpu.unidad_proceso.ID_EX.inst not in [None, "NOP"]:
            ex_mem_read = self.cpu.unidad_proceso.ID_EX.senales_control.get("mem_read", 0)
            ex_rt = self.cpu.unidad_proceso.ID_EX.rt

            if ex_mem_read == 1 and ex_rt in [rs, rt] and ex_rt not in ["", "$0", "$zero"]:
                self.hazard_stall = True
                self.mensaje_stall = "STALL(load-use)"
                self.inyectar_burbuja()
                return

        # 5. GUARDAR EN ID_EX (Paso a la cinta transportadora)
        self.cpu.unidad_proceso.ID_EX.inst = inst_str
        self.cpu.unidad_proceso.ID_EX.pc = pc_actual
        self.cpu.unidad_proceso.ID_EX.op1 = val_rs
        self.cpu.unidad_proceso.ID_EX.op2 = val_rt
        self.cpu.unidad_proceso.ID_EX.inmediato = inmediato
        self.cpu.unidad_proceso.ID_EX.rs = rs
        self.cpu.unidad_proceso.ID_EX.rt = rt
        self.cpu.unidad_proceso.ID_EX.rd = rd
        self.cpu.unidad_proceso.ID_EX.senales_control = decodificado["senales_control"]


    # Lee la Memoria de Instrucciones y escribe en IF_ID
    def fase_if(self):
        if getattr(self, "hazard_stall", False) == True:
            self.hazard_stall = False
            return  # Cortamos aquí. Ni avanzamos el PC, ni leemos memoria, ni sobrescribimos IF_ID.

        pc_actual = self.cpu.unidad_proceso.pc.contador
        inst_str = self.cpu.unidad_proceso.mem_instrucciones.instrucciones.get(pc_actual, "NOP")

        self.cpu.unidad_proceso.IF_ID.inst = inst_str
        self.cpu.unidad_proceso.IF_ID.pc = pc_actual

        if inst_str != "NOP":
            self.cpu.unidad_proceso.pc.contador += 1

    def imprimir_registros(self):
        self.cpu.unidad_proceso.banco_registros.imprimir_registros()

    def inyectar_burbuja(self):
        self.cpu.unidad_proceso.ID_EX.inst = "NOP"
        self.cpu.unidad_proceso.ID_EX.rs = ""
        self.cpu.unidad_proceso.ID_EX.rt = ""
        self.cpu.unidad_proceso.ID_EX.rd = ""
        self.cpu.unidad_proceso.ID_EX.senales_control = {}

    def imprimir_estado(self):
        stall_str = ""
        if getattr(self, "mensaje_stall", "") != "":
            stall_str = f"  STALL({self.mensaje_stall})"
            self.mensaje_stall = ""

        print(f"\nCiclo {self.ciclo_actual:02d}{stall_str}")

        def formato(inst):
            return inst if inst and inst != "NOP" else "--"

        _if = formato(self.cpu.unidad_proceso.IF_ID.inst)
        _id = formato(self.cpu.unidad_proceso.ID_EX.inst)
        _ex = formato(self.cpu.unidad_proceso.EX_MEM.inst)
        _mem = formato(self.cpu.unidad_proceso.MEM_WB.inst)
        _wb = formato(self.cpu.unidad_proceso.WB_OUT.inst)

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