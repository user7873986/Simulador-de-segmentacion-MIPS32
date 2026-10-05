from Componentes.memoria_instrucciones import MemoriaInstrucciones
from unidad_proceso import UnidadProceso
from unidad_control import UnidadControl
from registro_acoplamiento import RegistroAcoplamiento


class CPU:
    def __init__(self):
        self.etiquetas = {}
        self.mem_instrucciones = MemoriaInstrucciones()
        self.unidad_proceso = UnidadProceso()
        self.unidad_control = UnidadControl()
        self.pc = 0

        for pc, inst in self.programa.instrucciones.items():
            self.unidad_proceso.mem_instrucciones.escribir(pc, inst)

        self.IF_ID = RegistroAcoplamiento()
        self.ID_EX = RegistroAcoplamiento()
        self.EX_MEM = RegistroAcoplamiento()
        self.MEM_WB = RegistroAcoplamiento()

        self.ciclo_actual = 0
        self.instrucciones_completadas = 0

    def cargar_datos(self, ruta_archivo):
        """
        Lee el fichero de datos e instrucciones y
        puebla la mem_instrucciones y mem_datos.
        """
        try:
            with open(ruta_archivo, 'r') as archivo:
                # Aquí iría la lógica de lectura y parseo
                pass
            print(f"Datos cargados correctamente desde {ruta_archivo}")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_archivo}")


    def cargar_instrucciones(self, ruta_instrucciones):
        pc_actual = 0

        with open(ruta_instrucciones, 'r') as archivo:
            for linea in archivo:
                # 1. Limpiar comentarios y espacios en blanco
                if '#' in linea:
                    linea = linea.split('#')[0]
                linea = linea.strip()

                # Ignorar líneas vacías
                if not linea:
                    continue

                # 2. Detectar si es una etiqueta (ej. "for:")
                if linea.endswith(':'):
                    nombre_etiqueta = linea[:-1]
                    # Guardamos a qué PC corresponderá la siguiente instrucción
                    self.etiquetas[nombre_etiqueta] = pc_actual

                # 3. Es una instrucción real
                else:
                    self.mem_instrucciones.instrucciones[pc_actual] = linea
                    pc_actual += 1



    def simular_programa(self):
        total_instrucciones = len(self.programa.instrucciones)

        while self.instrucciones_completadas < total_instrucciones:
            self.ejecutar_ciclo()


    def ejecutar_ciclo(self):
        self.ciclo_actual += 1

        # Si hay una instrucción saliendo de la última etapa, sumamos una completada
        if self.WB_OUT.inst is not None:
            self.instrucciones_completadas += 1

        # Detectar riesgo load-use comparando lo que hay en IF/ID y ID/EX
        stall = self.unidad_riesgos.detectar_load_use(self.IF_ID, self.ID_EX)

        # Clonamos el estado exacto del ciclo anterior
        old_IF_ID = self.IF_ID.clonar()
        old_ID_EX = self.ID_EX.clonar()
        old_EX_MEM = self.EX_MEM.clonar()
        old_MEM_WB = self.MEM_WB.clonar()

        # --- FASE DE MOVIMIENTO DE DATOS ---
        if stall:
            # WB <- MEM, MEM <- EX; insertamos burbuja en EX; mantenemos ID e IF.
            self.WB_OUT = old_MEM_WB
            self.MEM_WB = old_EX_MEM
            self.EX_MEM = RegistroAcoplamiento()  # Burbuja vacía

            # IF_ID e ID_EX mantienen su estado actual, y el PC NO avanza
        else:
            # Avance normal de todo el cauce
            self.WB_OUT = old_MEM_WB
            self.MEM_WB = old_EX_MEM
            self.EX_MEM = old_ID_EX
            self.ID_EX = old_IF_ID

            # Fetch: Leemos nueva instrucción y la metemos en IF/ID
            inst_texto = self.programa.instrucciones.get(self.pc, None)

            self.IF_ID = RegistroAcoplamiento()
            self.IF_ID.inst = inst_texto
            self.IF_ID.pc = self.pc

            if inst_texto is not None:
                self.pc += 1

        # --- FASE DE TRABAJO DEL HARDWARE ---
        # Las unidades físicas procesan los registros ya actualizados
        self.fase_wb(self.WB_OUT)
        self.fase_mem(self.MEM_WB)
        self.fase_ex(self.EX_MEM)
        self.fase_id(self.ID_EX)

        self.imprimir_traza(stall)


    def imprimir_traza(self, stall):
        nota = "  [STALL por Load-Use]" if stall else ""
        print(f"\nCiclo {self.ciclo_actual:02d}{nota}")

        print(f"  IF/ID : {self.IF_ID.inst if self.IF_ID.inst else '--'}")
        print(f"  ID/EX : {self.ID_EX.inst if self.ID_EX.inst else '--'}")
        print(f"  EX/MEM: {self.EX_MEM.inst if self.EX_MEM.inst else '--'}")
        print(f"  MEM/WB: {self.MEM_WB.inst if self.MEM_WB.inst else '--'}")
        print(f"  SALIDA: {self.WB_OUT.inst if self.WB_OUT.inst else '--'}")