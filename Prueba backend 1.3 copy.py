import re
import numbers

fila,columna = None,None

def separar_elementos(cadena):
    # Separar la cadena por los operadores (+, -, *, /)
    separador = "(\+|-|\*|/)"
    cadena = cadena.replace("=", "")
    elementos = re.split(separador, cadena)
    #Es para eliminar los elementos vacíos de la lista elementos
    elementos = list(filter(bool, elementos))
    # Comprobar el número de elementos en la lista
    if len(elementos) == 1:
        # Solo hay un valorc:\Users\cmanu\Downloads\Pruebas noritex\Prueba 1 - Back-end\spreadsheet.py
        return cadena
    elif len(elementos) == 2:
        # Hay dos elementos, puede ser que el primero sea un signo
        if elementos[0] in ["+", "-"]:
            # Concatenamos el signo con el operando
            elementos[0] = elementos[0] + elementos[1]
            # Eliminamos el segundo elemento de la lista
            elementos.pop()
            return list(elementos)
        else:
            raise ValueError("La función {} no es válida".format(cadena))
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
            # Comprobamos si la celda es una cadena de texto
            if isinstance(celda, str):
                # Comprobamos si la celda contiene una función
                if celda.strip().startswith("="):
                    # Llamamos a la función evaluate_cell para obtener el valor de la celda
                    resultado = evaluate_cell(m, i, j)
                    # Asignamos el resultado a la celda actual de la matriz m
                    m[i][j] = resultado

                elif celda.isnumeric(): # Comprobamos si la celda contiene solo números
                    numero = float(celda) # Convertimos la cadena a un número de tipo float
                    m[i][j] = numero # Asignamos el número a la celda actual

    return m


def evaluate_cell(m, i, j):
    # Esta función evalúa recursivamente el valor de una celda que contiene una fórmula

    # Accedemos a la celda actual
    celda = m[i][j] 
    valor1,valor2 = None, None
    operando1,operando2,operador=None,None,None

    # Comprobamos si la celda es una cadena de texto
    if isinstance(celda, str):
        # Comprobamos si la celda contiene una función
        if celda.strip().startswith("="):
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
                fila,columna = obtener_indices(operando1)
                # Verificamos la condición fila == i and columna == j
                if fila == i and columna == j: 
                    raise ValueError("Referencia circular detectada en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))
                
                # Verificamos si la referencia está dentro del rango de la matriz
                if fila < 0 or fila >= len(m) or columna < 0 or columna >= len(m[0]):
                    raise ReferenceError("Referencia fuera de rango en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))

                # Obtenemos el valor de la referencia usando la función recursiva
                valor1 = evaluate_cell(m, fila, columna)
            else:
                # Si el primer operando es un número, lo convertimos a flotante
                valor1 = float(operando1)

            # Comprobamos si hay un segundo operando
            if operando2 is not None:
                # Comprobamos si el segundo operando es una referencia a otra celda
                if operando2[0].isalpha():
                    # Verificamos la condición fila == i and columna == j
                    fila,columna = obtener_indices(operando2)
                    if fila == i and columna == j: 
                        raise ValueError("Referencia circular detectada en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))
                    
                    # Verificamos si la referencia está dentro del rango de la matriz
                    if fila < 0 or fila >= len(m) or columna < 0 or columna >= len(m[0]):
                        raise ReferenceError("Referencia fuera de rango en la celda {}: {}".format(chr(j + ord('A')) + str(i + 1), celda))

                    valor2 = evaluate_cell(m, fila, columna)
                else:
                    # Si el segundo operando es un número, lo convertimos a flotante
                    valor2 = float(operando2)
                    
                
                # Definimos un diccionario con las funciones aritméticas
                if operador == '+':
                    resultado = valor1 + float(valor2)
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
        
            # Devolvemos el resultado de la celda actual
            return resultado

        elif celda.isnumeric(): # Comprobamos si la celda contiene solo números
            numero = float(celda) # Convertimos la cadena a un número de tipo float
            return numero # Devolvemos el número

    else:
        # Si la celda no es una cadena de texto, devolvemos su valor tal cual
        return celda



# =============================================================================
#
# Some example inputs and solutions to test against
#
# =============================================================================

testcase = []
solution = []

# Case: simple spreadsheet with strings and ints
testcase.append(
    [
        [1, "2"],
        ["3", 4]
    ]
)
solution.append (
    [
        [1, 2],
        [3, 4]
    ]
)

# Case: simple (non-recursive) formulas
testcase.append(
    [
        [1, "=A1+1"],
        [3, "=A2+1"]
    ]
)
solution.append(
    [
        [1, 2],
        [3, 4]
    ]
)

testcase.append(
    [
        [1, "=1-1"],
        [3, "=A2+1"]
    ]
)
solution.append(
    [
        [1, 0],
        [3, 4]
    ]
)


# Case: formulas referencing two cells
testcase.append(
    [
        [1,     "=A1+1", "=A1 + B1"],
        ["=B1", "3",     "=C1 + B2"]
    ]
)
solution.append(
    [
        [1, 2, 3],
        [2, 3, 6]
    ]
)

# Cases: formula referencing cells out of range
testcase.append(
    [
        [1,         "=A5 + 2"],
        ["=B1 + 1", "=A2 + 1"]
    ]
)
solution.append(ReferenceError)

testcase.append([ [1, "=C1"] ])
solution.append(ReferenceError)

# Case: circular dependencies
testcase.append(
    [
        ["=B1 + 1", "=A1 + 1"]
    ]
)
solution.append(ValueError)

# Case: highly recursive spreadsheet, all operations represented
testcase.append(
    [
        [ "=C1+5", "=A3/2", "=c2-1" ],
        [ "=b3+7",       1, "=B1*4" ],
        [ "=B2+5", "=a1/5", "=A2-2" ]
    ]
)
solution.append(
    [
        [ 16,   3,   11   ],
        [ 10.2, 1,   12   ],
        [  6,   3.2,  8.2 ]
    ]
)

# Cases: malformed formulas
testcase.append([ [ 1, "=A1 +" ] ] )
solution.append(ValueError)

testcase.append([ [ 1, "=A1+5+6+7" ] ])
solution.append(ValueError)

testcase.append([ [ 1, "=A1 $ A1" ] ])
solution.append(ValueError)

# Case: division by zero
testcase.append([ [ 1, "=A1 - 1", "=A1 / B1" ] ])
solution.append(ZeroDivisionError)

# Case: negative numbers
testcase.append([ [ 1, "=A1 * -1" ] ])
solution.append([ [ 1, -1 ] ])

testcase.append([ [ -1, "=A1 * -5" ] ])
solution.append([ [ -1, 5 ] ])

testcase.append([ [ 1, "=-2 + a1" ] ])
solution.append([ [ 1, -1 ] ])

testcase.append([ [ 1, "=A1 + -5" ] ])
solution.append([ [ 1, -4 ] ])

testcase.append([ [ 1, "=A-1 + 1" ] ])
solution.append(ValueError)

testcase.append([ [ 1, "=-A1 + 1" ] ])
solution.append([ [ 1, 0 ] ])

# Case: Errors in input
testcase.append([ [ -1, "=A1 + - 5" ] ])
solution.append(ValueError)

testcase.append([ [ "" ] ])
solution.append(ValueError)

testcase.append([ [ None ] ])
solution.append(ValueError)

testcase.append([ [ None, "=A1" ] ])
solution.append(ValueError)

testcase.append([ [ "A1" ] ])
solution.append(ValueError)




def validate(proposed, actual):
    """Check if the proposed solution is the same as the actual solution.

    Feel free to modify this function as we will be testing your code with
    our copy of this function.

    :param proposed: The proposed solution
    :param actual: The actual solution
    :return: True if they are the same. Else, return False.
    """
    if proposed is None:
        print ("Oops! Looks like your proposed result is None")
        return False
    proposed_items = [item for sublist in proposed for item in sublist]
    actual_items = [item for sublist in actual for item in sublist]
    if len(proposed_items) != len(actual_items):
        print ("Oops! There don't seem to be the same number of elements")
        return False
    if proposed_items != actual_items:
        print ("Oops! Looks like your proposed solution is not right...")
        return False
    return True
        

def print_error(solution, result):
    """Helper to print the error string"""
    print ("    Expected {}({}), got {}({})".format(
        type(solution), solution, type(result), result))


if __name__ == '__main__':
    """The main entry point for this module.

    The main entry point for the function that runs a couple tests to validate
    the implementation of evaluate().
    """

    # The number of test cases that are correct
    correct = 0

    for i in range(len(testcase)):

        print ("Test {}.".format(i))
        
        try:
            result = evaluate(testcase[i])
        except Exception as exc:
            result = exc

        # If the result is a matrix, make sure we were expecting a matrix
        if isinstance(result, list):
            if isinstance(solution[i], list):
                if validate(result, solution[i]):
                    print ("    OK.")
                    correct += 1
                else:
                    print ("    Results don't match")
            else:
                print_error(solution[i], result)

        # If the result is an error, make sure we were expecting an error
        else:
            if isinstance(solution[i], list):
                print_error(solution[i], result)
            else:
                if result.__class__ == solution[i]:
                    print ("    OK.")
                    correct += 1
                else:
                    print_error(solution[i], result)

    print ("------------------------------------------------------")
    print ("You got {} out of {} correct.".format(correct, len(testcase)))



