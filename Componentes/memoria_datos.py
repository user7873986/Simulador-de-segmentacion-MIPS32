
class MemoriaDatos:
    def __init__(self):
        self.datos = {0: 5} #Solo inicializamos esto aunque haya 2 a la 32 direcciones

    def leer(self, direccion):
        if direccion % 4 != 0:
            raise ValueError(f"Excepción de Hardware: La dirección {direccion} no es múltiplo de 4.")
        return self.datos.get(direccion, 0)

    def escribir(self, direccion, valor):
        if direccion % 4 != 0:
            raise ValueError(f"Excepción de Hardware: La dirección {direccion} no es múltiplo de 4.")

        self.datos[direccion] = valor

    #Como tal esto no lo debería de tener un HW pero por términos de POO lo hago aquí
    def imprimir_memoria(self):
        print("--- MEMORIA ---")
        for direccion, valor in self.datos.items():
            print(f" Direccion {direccion}: Valor : {valor}")
        print("")