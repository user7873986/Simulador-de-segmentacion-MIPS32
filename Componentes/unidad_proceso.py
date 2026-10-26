from Componentes.alu import ALU
from Componentes.banco_registros import BancoRegistros
from Componentes.unidad_forwarding import ForwardingUnit
from Componentes.memoria_instrucciones import MemoriaInstrucciones
from Componentes.pc import PC
from Componentes.memoria_datos import MemoriaDatos
from Componentes.registros_acoplamiento import ID_EX, IF_ID, EX_MEM, MEM_WB, WB_OUT


class UnidadProceso:
    def __init__(self):
        self.pc = PC()
        self.banco_registros = BancoRegistros()
        self.alu = ALU()
        self.unidad_forwarding = ForwardingUnit()

        self.mem_instrucciones = MemoriaInstrucciones()
        self.mem_datos = MemoriaDatos()

        self.ID_EX = ID_EX()
        self.IF_ID = IF_ID()
        self.EX_MEM = EX_MEM()
        self.MEM_WB = MEM_WB()

        self.WB_OUT = WB_OUT()

