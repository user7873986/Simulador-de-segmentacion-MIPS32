class BancoRegistros:
    def __init__(self):
        # Un solo diccionario: Claves de texto y valores inicializados a 0
        self.registros = {
            "$0": 0, "$zero": 0,
            "$at": 0,
            "$v0": 0, "$v1": 0,
            "$a0": 0, "$a1": 0, "$a2": 0, "$a3": 0,
            "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0, "$t4": 0, "$t5": 0, "$t6": 0, "$t7": 0,
            "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0, "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,
            "$t8": 0, "$t9": 0,
            "$k0": 0, "$k1": 0,
            "$gp": 0,
            "$sp": 0,
            "$fp": 0,
            "$ra": 0
        }

    def leer(self, reg_str):
        # Devuelve el valor del registro o 0 si nos pasan un string inválido
        return self.registros.get(reg_str, 0)

    def escribir(self, reg_str, valor):
        # Regla de oro de MIPS: $0 y $zero están cableados a tierra y son inmutables
        if reg_str not in ["$0", "$zero"] and reg_str in self.registros:
            self.registros[reg_str] = valor

    def imprimir_registros(self):
        print("\n--- BANCO DE REGISTROS ---")

        # Filtramos para imprimir solo los registros que han sido modificados (distintos de 0)
        registros_modificados = {reg: val for reg, val in self.registros.items() if val != 0}

        if not registros_modificados:
            print("  (Todos los registros están a 0)")
        else:
            for reg, val in registros_modificados.items():
                # Formateamos para que quede alineado (ej. $t1 : 105)
                print(f"  {reg:<5} : {val}")

        print("-" * 26)