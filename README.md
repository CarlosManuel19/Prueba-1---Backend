#Prueba-1--.Backend

##Función separar_elementos 

Esta función recibe una cadena que representa una operación aritmética simple (suma, resta, multiplicación o división) y la separa por los operadores (+, -, *, /), devolviendo una lista con los elementos separados.

separar_elementos("3+5")
['3', '+', '5']

##Excepciones
La función puede lanzar una excepción ValueError si la cadena no tiene un formato válido, es decir, si tiene más o menos elementos de los esperados, o si tiene signos donde no debería. Por ejemplo:

[s](url)separar_elementos("3+5*2")
ValueError: La función 3+5*2 no es válida


