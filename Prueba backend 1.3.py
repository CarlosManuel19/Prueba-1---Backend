import re


def separar_elementos(cadena):
    # Separar la cadena por los operadores (+, -, *, /)
    separador = "(\+|-|\*|/)"
    cadena = cadena.replace("=", "")
    elementos = re.split(separador, cadena)
    # Comprobar el número de elementos en la lista
    if len(elementos) == 1:
        # Solo hay un valor, devolverlo como una lista de un elemento
        return cadena
    elif len(elementos) == 3:
        return list(elementos)
    else:
        # Hay más o menos valores de los esperados, lanzar una excepción personalizada
        raise ValueError("La función {} no es válida".format(cadena))



# Definimos una función auxiliar para obtener los índices de fila y columna de una referencia de celda
def obtener_indices(cadena):
    # Convertir la cadena a mayúsculas
    cadena = cadena.upper()
    # Separar la cadena por la letra y el número
    letra, numero = cadena[0], cadena[1:]
    # Convertir la letra a un índice de columna (A=0, B=1, C=2, etc.)
    columna = ord(letra) - ord("A")
    # Convertir el número a un índice de fila (1=0, 2=1, 3=2, etc.)
    fila = int(numero) - 1
    # Devolver los índices de fila y columna como una tupla
    return (fila, columna)


def evaluate(m):
    # Recorremos la matriz por filas y columnas
    for i in range(len(m)):
        for j in range(len(m[i])):
            # Accedemos a la celda actual
            celda = m[i][j] 
            # Comprobamos si la celda contiene una función
        
            if isinstance(celda, str) and celda.strip().startswith("="):

                operando1,operando2,operador = None, None, None
                # Eliminamos los espacios dentro de la celda y la convertimos a mayúsculas
                celda = celda.replace(" ", "").upper()
                # Separamos los operandos y el operador de la función                
                elementos = separar_elementos(celda)
                if len(elementos) == 2:
                    # Solo hay un valor, devolverlo como una lista de un elemento
                    operando1 = elementos
                elif len(elementos) == 3:
                    operando1 = elementos[0]
                    operando2 = elementos[2]
                    operador = elementos[1]
                else:
                    # Hay más o menos valores de los esperados, lanzar una excepción personalizada
                    raise ValueError("La función {} no es válida".format(celda))
               
            
                # Comprobamos si el primer operando es una referencia a otra celda
                if not operando1.isnumeric():
                    # Obtenemos el índice de fila y el índice de columna de la referencia
                    fila, columna = obtener_indices(operando1)
                    
                    # Verificamos la condición fila == i and columna == j
                    if fila == i and columna == j: 
                        raise ValueError("Referencia circular detectada en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))
                    
                    # Accedemos al valor correspondiente en la matriz m
                    valor1 = m[fila][columna]
                else:
                    # Si el primer operando es un número, lo convertimos a flotante
                    valor1 = float(operando1)

                # Comprobamos si hay un segundo operando
                if operando2 is not None:
                    # Comprobamos si el segundo operando es una referencia a otra celda
                    if not operando2.isnumeric():
                        # Obtenemos el índice de fila y el índice de columna de la referencia
                        fila, columna = obtener_indices(operando2)
                        
                        # Verificamos la condición fila == i and columna == j
                        if fila == i and columna == j: 
                            raise ValueError("Referencia circular detectada en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))
                    
                        # Accedemos al valor correspondiente en la matriz m
                        valor2 = m[fila][columna]
                    else:
                        # Si el segundo operando es un número, lo convertimos a flotante
                        valor2 = float(operando2)
                        
                    # Definimos un diccionario con las funciones aritméticas
                    if operador == '+':
                        resultado = valor1 + valor2
                    elif operador == '-':
                        resultado = valor1 - valor2
                    elif operador == '*':
                        resultado = valor1 * valor2
                    elif operador == '/':
                        # Verificamos la división entre cero
                        if valor2 == 0:
                            raise ValueError("División entre cero en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))
                        resultado = valor1 / valor2
                    else:
                        raise ValueError("Operador no válido.")
                else:
                    # Si no hay un segundo operando, el resultado es el valor del primer operando
                    resultado = valor1

                # Asignamos el resultado a la celda actual
                m[i][j] = resultado
    # Devolvemos la matriz actualizada
    return m


# Supongamos que tenemos una matriz como esta:
m =  [
    [1, " =A1"],
    ["=B1+1", "=A2+1"]
    ]

# Llamamos a la función con la matriz m como argumento
m_actualizada = evaluate(m)

# Imprimimos la matriz m actualizada
print(m_actualizada)





