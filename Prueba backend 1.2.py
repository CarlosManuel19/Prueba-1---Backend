# Definimos una función auxiliar para separar los operandos y el operador de una cadena
import re

# Definimos una excepción personalizada para las funciones no válidas
class FuncionInvalida(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje

# Definimos una función auxiliar para separar los operandos y el operador de una cadena
def separar_elementos(cadena):
    # Separar la cadena por los operadores (+, -, *, /)
    separador = "(\+|-|\*|/)"
    cadena = cadena.replace("=", "")
    elementos = re.split(separador, cadena)
    # Comprobar si hay más de 4 elementos en la lista
    if len(elementos) >4:
        # Lanzar una excepción personalizada
        raise FuncionInvalida(f"La función {cadena} no es válida")
    # Obtener el operador
    operador = elementos[1]
    # Obtener los operandos
    operando1 = elementos[0]
    operando2 = elementos[2]
    # Devolver los operandos y el operador como una tupla
    return (operando1, operando2, operador)

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

                # Usamos un bloque try-except para capturar la excepción personalizada
                try:
                    # Eliminamos los espacios dentro de la celda
                    celda = celda.replace(" ", "")
                    # Separamos los operandos y el operador de la función                
                    operando1, operando2, operador = separar_elementos(celda)
                except FuncionInvalida as e:
                    # Mostramos el mensaje de la excepción y salimos del programa con un código de error
                    print(e.mensaje)
                    exit(1)
        
                # Comprobamos si el primer operando es una referencia a otra celda
                if operando1[0].isalpha():
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
                        # Accedemos al valor correspondiente en la matriz m
                        valor2 = m[fila][columna]
                    else:
                        # Si el segundo operando es un número, lo convertimos a flotante
                        valor2 = float(operando2)
                    
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
    [1, " =A1/0"],
    ["=B1+1", "=A2+1"]
    ]

# Llamamos a la función con la matriz m como argumento
m_actualizada = evaluate(m)

# Imprimimos la matriz m actualizada
print(m_actualizada)





