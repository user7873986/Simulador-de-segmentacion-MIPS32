from Componentes.cpu import CPU
from segmentacion import Segmentacion


def main():
    print("Iniciando simulación MIPS32...")
    procesador = CPU()

    #procesador.cargar_instrucciones("Instrucciones.txt")
    procesador.cargar_instrucciones("Entrada/ejemploInstruccion.txt")
    # procesador.ejecutar_ciclo()
    ejemplo = Segmentacion(procesador)
    ejemplo.simular()

    print("Simulación finalizada.")
    return 0


if __name__ == "__main__":
    main()





#REGISTROS de acoplamiento; controlan la segmentación


