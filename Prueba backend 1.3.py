import re
from validate import validate

fila,columna= None,None

def separar_elementos(cadena):
    # Separar la cadena por los operadores (+, -, *, /)
    separador = "(\+|-|\*|/)"
    cadena = cadena.replace("=", "")
    elementos = re.split(separador, cadena)
    elementos = list(filter(bool, elementos))
    # Comprobar el número de elementos en la lista
    if len(elementos) == 1:
        # Solo hay un valor, devolverlo como una lista de un elemento
        return cadena
    elif len(elementos) == 3:
        return list(elementos)
    elif len(elementos) == 4 :
        # Hay cuatro elementos, puede ser que el primero o el tercero sean un signo
        if elementos[0] in ["+", "-"]:
            # Concatenamos el signo con el primer operando
            elementos[0] = elementos[0] + elementos[1]
            # Eliminamos el segundo elemento de la lista
            elementos.pop(1)
            return list(elementos)
        elif elementos[2] in ["+", "-"]:
            # Concatenamos el signo con el segundo operando
            elementos[2] = elementos[2] + elementos[3]
            # Eliminamos el cuarto elemento de la lista
            elementos.pop()
            return list(elementos)
        elif re.match("[A-Z]+\d+", elementos[0]):
            # El primer elemento es una referencia a una celda
            fila, columna = obtener_indices(elementos[0])
            return list(elementos)
        elif re.match("[A-Z]+\d+", elementos[2]):
            # El tercer elemento es una referencia a una celda
            fila, columna = obtener_indices(elementos[2])
            return list(elementos)
        else:
           raise ValueError("La función {} no es válida".format(cadena))
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
                if  operando1[0].isalpha():
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
                    if operando2[0].isalpha():
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

                # Asignamos el resultado a la celda actual de la matriz m
                m[i][j] = resultado

    return m



# Definimos una lista vacía para guardar los casos de prueba
testcase = []

# Definimos una lista vacía para guardar las soluciones esperadas
solution = []

# Añadimos el caso de prueba con números negativos
testcase.append([ [ 1, "=A1* -1" ] ])
solution.append([ [ 1, -1 ] ])

# Recorremos los casos de prueba y las soluciones
for i in range(len(testcase)):
    # Obtenemos el caso de prueba y la solución correspondiente
    caso = testcase[i]
    solucion = solution[i]
    # Llamamos a la función evaluate para obtener el resultado del caso de prueba
    resultado = evaluate(caso)
    # Llamamos a la función validate para comprobar si el resultado es igual a la solución
    valido = validate(resultado, solucion)
    # Imprimimos el resultado de la validación
    if valido:
        print ("El caso de prueba {} es correcto.".format(i + 1))
    else:
        print ("El caso de prueba {} no es correcto.".format(i + 1))




