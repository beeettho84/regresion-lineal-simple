pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]
def getB0(x,y): #funcion de regresion lineal simple, solicita como entrada dos arreglos
    Sx = sum(x) #obtenemos los valores parciales de las ecuaciones para facilitar el calculo
    Sy = sum(y)
    Sxy = 0
    Sx2 = 0
    n = len(x)
    i=0
    for i in range(n): #realizamos las sumatorias de los campos complejos
        Sxy = Sxy + (x[i] * y[i])
        Sx2 = Sx2 + (x[i] * x[i])
    B1 = (n * Sxy - (Sx * Sy)) / (n * Sx2 - (Sx * Sx)) #calculamos el valor de B1, necesario para obtener B0
    B0 = (Sy - (B1 * Sx)) / n #calculamos B0
    print("Dataset:")
    print("X: "+str(x))
    print("Y: "+str(y))
    print("B0 es igual a ", B0) #imprimimos los valores en consola, para implementaciones sin interfaz grafica
    print("B1 es igual a ", B1)
    Bs = [B0,B1]
    return Bs #retornamos ambos valores

def predict(x):
    #B = getB0(pruebax, pruebay)
    y = B[0]+(x*B[1])
    print("Dado X = "+str(x)+", Y = "+str(y))
    return y

B = getB0(pruebax, pruebay)#obtencion hardcodeada de valores en base al conjunto de prueba
predict(24)
predict(25)
predict(27)
predict(28)
predict(29)
