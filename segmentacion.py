class segmentacion:
    
    
    
    def __init__:
        
        self.if 
        self.id
        self.ex #inicialmente comprobamos que están limpio
        
        
        
    def simulate():
        
        while not fin:
            #ejecutamos las fases de la segmentacion
            wb() #parametros de entrada son el contenido de ex/mem o si el flag de operacion nula. NO devuelve nada
            ex() #aqui tocamos cosas fisicas y la funcion ex guarda algo en el registro de acoplamiento ex/mem, pero no puede hacerlo ahora asiq lo guarda en un ax
            mem() #utiliza el ex/mem
            #aqui ya podemos guardar en ex/mem
            id() #devuelve informacion que se guarda en el id
            if() #dado el pc devuelve la instruccion que guarda en id/if
            
            
            
            
    #REGISTROS DE ACOPLAMIENTO
            #IF/ID guarda la ultima instruccion y el pc actual
            
            #ID/EX guarda tipoins reg1, reg2, regcode1, regcode2, etiqueta, offset, regdest; es decir la información troceada
            
            #EX/MEM guarda regcode1, regcode2, offset, regDest y valor de la alu
            
            #MEM/WB guardamos seguro el tipo con regDest, 
