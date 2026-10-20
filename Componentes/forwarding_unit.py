
class ForwardingUnit:

    def adelantar(self,regwrite, rd,rt,rs,resultado_alu,val_rs,val_rt):
        if regwrite == 1:
            if rd == rs:
                val_rs = resultado_alu
            if rd == rt:
                val_rt = resultado_alu

        return val_rs,val_rt