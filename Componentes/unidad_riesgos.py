class UnidadRiesgos:
    def __init__(self, unidad_proceso):
        self.uproceso = unidad_proceso

    def tiene_riesgo_raw(self,rs,rt):
        #solo cuando hay un lw antes (load use)
        if self.uproceso.ID_EX.inst not in [None, "NOP"]:
            ex_mem_read = self.uproceso.ID_EX.senales.get("mem_read")
            ex_rt = self.uproceso.ID_EX.rt
            if ex_mem_read == 1 and ex_rt in [rs, rt] and ex_rt not in ["", "$0", "$zero"]:
                return True
        return False

    def tiene_riesgo_salto(self,rs,rt):
        necesarios = [reg for reg in (rs, rt) if reg not in ("", "$0", "$zero")]

        if not necesarios:
            return False

        if self.uproceso.ID_EX.senales.get("reg_write") == 1:
            reg_dst = self.uproceso.ID_EX.senales.get("reg_dst")
            destino = self.uproceso.ID_EX.rd if reg_dst == 1 else self.uproceso.ID_EX.rt
            if destino in necesarios:
                return True

        if self.uproceso.EX_MEM.senales.get("reg_write") == 1 and self.uproceso.EX_MEM.reg_dest in necesarios:
            return True

        if self.uproceso.MEM_WB.senales.get("reg_write") == 1 and self.uproceso.MEM_WB.reg_dest in necesarios:
            return True

        return False

