# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:59:56 2022

@author: Macarena Coloma
"""
#Definimos la funcion y el valor que vamos a introducir

def nprimos(n):

    #El uno no es primo ya que no cumple con la condicion de ser primo
    #Un nº primo solo es divisible por si mismo y por la unidad
    print ('el 1 no es primo')   
 
#Hacemos un bucle que recorra desde el 2 hasta el número + 1 para que también tenga en cuenta
#el numero que hemos introducido
    for a in range (2,n+1):        
        c= True
    
        for b in range (2, a):
#Añadimos esta condicion porque todos los numeros son divisibles por si mismos
#cuando el numero del primer bucle es igual al numero del segundo salimos del buble
            if a == b:
                break
#Al tener asegurado que a != b, ya podemos añadir la condicion de que si el resto entre el numero del primer bucle y
#el segundo son iguales a 0 entonces no será primo porque será un divisor
#Ejemplo, si a=4 y b = 2, entonces el resto será 0, no nos interesa el 4 ya que no es primo, por tanto, saldra del segundo
#bucle y continuará con el primer bucle, según el ejemplo anterior seguirá con el 5.
            if a%b ==0:
                c=False
#Finalmente, ya tenemos las condiciones que no queremos que se cumplan por tanto, salimos del bucle para empezar
#con el siguiente if que imprimirá por pantalla los numeros primos hasta el valor indicado
            else :
                continue
        
        if c == True :
            return a
       
            
