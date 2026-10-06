from alu import ALU
from Componentes.banco_registros import BancoRegistros
from Componentes.pc import PC
from Componentes.memoria_datos import MemoriaDatos


class UnidadProceso:
    def __init__(self):
        # Instanciamos los componentes de hardware
        self.pc = PC()
        self.banco_registros = BancoRegistros()
        self.alu = ALU()

        # Memorias
        self.mem_instrucciones = {}
        self.mem_datos = MemoriaDatos()

        """# Registros de acoplamiento (para controlar la segmentación/pipeline)
        self.IF_ID = {}
        self.ID_EX = {}
        self.EX_MEM = {}
        self.MEM_WB = {}"""