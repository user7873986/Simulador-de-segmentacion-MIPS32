class MemoriaDatos:
    def __init__(self):
        self.datos = {0: 5} #Solo inicializamos esto aunque haya 2 a la 32 direcciones

    def leer(self, direccion):
        if direccion % 4 != 0:
            raise ValueError(f"Excepción de Hardware: La dirección {direccion} no es múltiplo de 4.")

        # Si la direccion esta vacia devuelve 0
        return self.datos.get(direccion, 0)

    def escribir(self, direccion, valor):
        if direccion % 4 != 0:
            raise ValueError(f"Excepción de Hardware: La dirección {direccion} no es múltiplo de 4.")

        # Crea o sobreescribe
        self.datos[direccion] = valor