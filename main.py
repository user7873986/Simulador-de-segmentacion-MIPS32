from cpu import CPU


def main():
    print("Iniciando simulación MIPS32...")
    procesador = CPU()

    #procesador.cargar_instrucciones("Instrucciones.txt")
    procesador.cargar_instrucciones("ejemploInstruccion.txt")
    # procesador.ejecutar_ciclo()


    print("Simulación finalizada.")
    return 0


if __name__ == "__main__":
    main()





#REGISTROS de acoplamiento; controlan la segmentación


