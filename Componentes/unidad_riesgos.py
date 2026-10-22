class UnidadRiesgos:
    def __init__(self, unidad_proceso):
        self.up = unidad_proceso

    def tiene_riesgo_raw(self,rs,rt):
        #solo cuando hay un lw antes
        if self.up.ID_EX.inst not in [None, "NOP"]:
            ex_mem_read = self.up.ID_EX.senales.get("mem_read", 0)
            ex_rt = self.up.ID_EX.rt
            if ex_mem_read == 1 and ex_rt in [rs, rt] and ex_rt not in ["", "$0", "$zero"]:
                return True
        return False

    def tiene_riesgo_salto(self,rs,rt):
        necesarios = [reg for reg in (rs, rt) if reg not in ("", "$0", "$zero")]

        if not necesarios:
            return False

        if self.up.ID_EX.senales.get("reg_write") == 1:
            reg_dst = self.up.ID_EX.senales.get("reg_dst")
            destino = self.up.ID_EX.rd if reg_dst == 1 else self.up.ID_EX.rt
            if destino in necesarios:
                return True

        if self.up.EX_MEM.senales.get("reg_write") == 1 and self.up.EX_MEM.reg_dest in necesarios:
            return True

        if self.up.MEM_WB.senales.get("reg_write") == 1 and self.up.MEM_WB.reg_dest in necesarios:
            return True

        return False

