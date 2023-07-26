# Prueba-1--.Backend

# Función separar_elementos 

Esta función recibe una cadena que representa una operación aritmética simple (suma, resta, multiplicación o división) y la separa por los operadores (+, -, *, /), devolviendo una lista con los elementos separados.

separar_elementos("3+5")
['3', '+', '5']

## Excepciones
La función puede lanzar una excepción ValueError si la cadena no tiene un formato válido, es decir, si tiene más o menos elementos de los esperados, o si tiene signos donde no debería. Por ejemplo:

separar_elementos("3+5*2")
ValueError: La función 3+5*2 no es válida

# Función obtener_indices
Esta función recibe una cadena que representa una referencia de celda (por ejemplo, “A1”, “B3”, “C5”) y devuelve una tupla con los índices de fila y columna correspondientes (por ejemplo, (0, 0), (2, 1), (4, 2)).

>>> obtener_indices("A1")
(0, 0)

>>> obtener_indices("B3")
(2, 1)

>>> obtener_indices("C5")
(4, 2)

## Excepciones
La función puede lanzar una excepción ValueError si la cadena no tiene un formato válido, es decir, si no tiene una letra seguida de un número positivo. Por ejemplo:

>>> obtener_indices("A0")
ValueError: El número debe ser mayor que cero

>>> obtener_indices("D")
ValueError: La cadena debe tener una letra y un número

>>> obtener_indices("3A")
ValueError: La cadena debe tener una letra y un número

# Función evaluate
Esta función recibe una matriz que representa una hoja de cálculo y evalúa el valor de las celdas que contienen fórmulas. Una fórmula es una cadena que empieza por “=” y contiene una operación aritmética simple (suma, resta, multiplicación o división) entre dos valores numéricos o dos referencias de celda (por ejemplo, “=A1+B2”). La función devuelve la misma matriz con los valores calculados.

Ejemplos
>>> m = [["", 3, 5], ["=A1+B1", "=B1*C1", 7], [9, "=B2+C2", "=A3*B3"]]
>>> evaluate(m)
[[0.0, 3.0, 5.0], [3.0, 15.0, 7.0], [9.0, 22.0, 81.0]]

>>> m = [["=A2-B2", 4, 6], [8, "=C1*A2", 10], ["=B3+C3", "=A1+B1", "=C2/A3"]]
>>> evaluate(m)
[[-4.0, 4.0, 6.0], [8.0, 48.0, 10.0], [18.0, 0.0, 5.333333333333333]]

## Excepciones
La función puede lanzar una excepción ValueError si alguna de las celdas tiene un formato inválido, es decir, si es una cadena vacía, un valor None o una cadena de texto que no sea una fórmula válida. Por ejemplo:

>>> m = [["", None, "hola"], [3, 4, 5], [6, 7, 8]]
>>> evaluate(m)
ValueError: La celda A1 no puede estar vacía o ser None
ValueError: La celda B1 no puede estar vacía o ser None
ValueError: La celda C1 no puede ser una cadena de texto que no sea una fórmula

Para manejar estas excepciones, se puede usar un bloque try-except y mostrar un mensaje de error adecuado. Por ejemplo:

try:
    resultado = evaluate(m)
    print(resultado)
except ValueError as e:
    print(e)
    
# Función evaluate_cell

Esta función recibe una matriz que representa una hoja de cálculo, y los índices de fila y columna de una celda que contiene una fórmula. Una fórmula es una cadena que empieza por “=” y contiene una operación aritmética simple (suma, resta, multiplicación o división) entre dos valores numéricos o dos referencias de celda (por ejemplo, “=A1+B2”). La función evalúa recursivamente el valor de la fórmula y lo devuelve como un número.

### Ejemplos
>>> m = [["", 3, 5], ["=A1+B1", "=B1*C1", 7], [9, "=B2+C2", "=A3*B3"]]
>>> evaluate_cell(m, 0, 0)
0.0

>>> evaluate_cell(m, 1, 0)
3.0

>>> evaluate_cell(m, 2, 2)
81.0

## Excepciones
La función puede lanzar una excepción ValueError si la celda tiene un formato inválido, es decir, si es una cadena vacía, un valor None o una cadena de texto que no sea una fórmula válida. Por ejemplo:

>>> m = [["", None, "hola"], [3, 4, 5], [6, 7, 8]]
>>> evaluate_cell(m, 0, 0)
ValueError: La celda A1 no puede estar vacía o ser None

>>> evaluate_cell(m, 0, 1)
ValueError: La celda B1 no puede estar vacía o ser None

>>> evaluate_cell(m, 0, 2)
ValueError: La celda C1 no puede ser una cadena de texto que no sea una fórmula
Copiar
La función también puede lanzar una excepción ReferenceError si la fórmula contiene una referencia a una celda que está fuera de los límites de la matriz. Por ejemplo:

>>> m = [["=A2-B2", 4, 6], [8, "=C1*A2", 10], ["=B3+C3", "=A1+B1", "=C2/A3"]]
>>> evaluate_cell(m, 0, 0)
ReferenceError: Invalid cell reference: A2

>>> evaluate_cell(m, 1, 1)
ReferenceError: Invalid cell reference: C1
Copiar
Para manejar estas excepciones, se puede usar un bloque try-except y mostrar un mensaje de error adecuado. Por ejemplo:

try:
    resultado = evaluate_cell(m, i, j)
    
    print(resultado)
    
except ValueError as e:

    print(e)
    
except ReferenceError as e:

    print(e)
