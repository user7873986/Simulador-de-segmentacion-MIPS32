
class ForwardingUnit:
        def adelantar(self, ex_mem_reg_write, ex_mem_rd, rs, rt, resultado_alu, val_rs, val_rt):

            if ex_mem_reg_write == 1 and ex_mem_rd not in [None, ""]:
                if ex_mem_rd == rs:
                    val_rs = resultado_alu
                if ex_mem_rd == rt:
                    val_rt = resultado_alu

            return val_rs, val_rt