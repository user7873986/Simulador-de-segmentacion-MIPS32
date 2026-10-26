from Componentes.cpu import CPU
from segmentacion import Segmentacion


def main():
    print("Iniciando simulación MIPS32...")
    procesador = CPU()

    #procesador.cargar_instrucciones("Entrada/Instrucciones.txt")
    procesador.cargar_datos("Entrada/Datos.txt")
    procesador.cargar_instrucciones("Entrada/ejemplo1.txt")
    ejemplo = Segmentacion(procesador)
    ejemplo.simular()

    print("Simulación finalizada.")
    return 0


if __name__ == "__main__":
    main()
