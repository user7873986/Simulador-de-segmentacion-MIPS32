from Componentes.alu import ALU
from Componentes.banco_registros import BancoRegistros
from Componentes.memoria_instrucciones import MemoriaInstrucciones
from Componentes.pc import PC
from Componentes.memoria_datos import MemoriaDatos
from Componentes.registro_acoplamiento import RegistroAcoplamiento


class UnidadProceso:
    def __init__(self):
        # Instanciamos los componentes de hardware
        self.pc = PC()
        self.banco_registros = BancoRegistros()
        self.alu = ALU()

        # Memorias
        self.mem_instrucciones = MemoriaInstrucciones()
        self.mem_datos = MemoriaDatos()

        # inicialmente comprobamos que están limpio
        self.ID_EX = RegistroAcoplamiento()
        self.IF_ID = RegistroAcoplamiento()
        self.EX_MEM = RegistroAcoplamiento()
        self.MEM_WB = RegistroAcoplamiento()

        self.WB_OUT = RegistroAcoplamiento()

        """# Registros de acoplamiento (para controlar la segmentación/pipeline)
        self.IF_ID = {}
        self.ID_EX = {}
        self.EX_MEM = {}
        self.MEM_WB = {}"""