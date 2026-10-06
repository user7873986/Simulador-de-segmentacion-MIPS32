class Segmentacion:
    def __init__(self, cpu):
        # Recibimos la CPU ya cargada con las instrucciones
        self.cpu = cpu
        self.fin = False
        self.ciclo_actual = 0

        # inicialmente comprobamos que están limpio


    def simular(self):
        while not self.fin:
            self.ciclo_actual += 1

            # Ejecutamos en orden inverso para no pisar los registros de acoplamiento
            self.fase_wb() #parametros de entrada son el contenido de ex/mem o si el flag de operacion nula. NO devuelve nada
            self.fase_ev() #aqui tocamos cosas fisicas y la funcion ex guarda algo en el registro de acoplamiento ex/mem, pero no puede hacerlo ahora asiq lo guarda en un ax
            self.fase_mem() #utiliza el ex/mem
            # aqui ya podemos guardar en ex/mem
            self.fase_id()  #devuelve informacion que se guarda en el id
            self.fase_if() #dado el pc devuelve la instruccion que guarda en id/if

            self.imprimir_estado()

            # TODO: Definir cuándo self.fin = True (ej. cuando WB procese un NOP final)

    def fase_wb(self):
        # Usa la información de self.cpu.MEM_WB
        pass

    def fase_mem(self):
        # Usa la información de self.cpu.EX_MEM y escribe en MEM_WB
        pass

    def fase_ex(self):
        # Usa self.cpu.ID_EX, calcula en la ALU y escribe en EX_MEM
        pass

    def fase_id(self):
        # Decodifica self.cpu.IF_ID y pasa datos a ID_EX
        pass

    def fase_if(self):
        # Lee la Memoria de Instrucciones y escribe en IF_ID
        pass

    def imprimir_estado(self):
        print(f"\n--- Ciclo {self.ciclo_actual} ---")
        # Aquí puedes imprimir qué hay en IF_ID, ID_EX, etc.

            
            
            
    #REGISTROS DE ACOPLAMIENTO
            #IF/ID guarda la ultima instruccion y el pc actual
            
            #ID/EX guarda tipoins reg1, reg2, regcode1, regcode2, etiqueta, offset, regdest; es decir la información troceada
            
            #EX/MEM guarda regcode1, regcode2, offset, regDest y valor de la alu
            
            #MEM/WB guardamos seguro el tipo con regDest, 
