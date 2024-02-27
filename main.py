import math

pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]

class pls:
    x = list()
    y = list()
    B0 = float()
    B1 = float()
    n = 0
    r = 0
    r2 = 0

    def __init__(self, inx, iny):
        if(len(inx) == len(iny)):
            self.n = len(inx)
            self.x = inx
            self.y = iny
            self.calculaBs()

    def calculaBs(self):
        Sx = sum(self.x)  # obtenemos los valores parciales de las ecuaciones para facilitar el calculo
        Sy = sum(self.y)
        Sxy = 0
        Sx2 = 0
        Sy2 = 0
        i = 0
        for i in range(self.n):  # realizamos las sumatorias de los campos complejos
            Sxy = Sxy + (self.x[i] * self.y[i])
            Sx2 = Sx2 + (self.x[i] * self.x[i])
            Sy2 = Sy2 + (self.y[i] * self.y[i])
        self.B1 = (self.n * Sxy - (Sx * Sy)) / (self.n * Sx2 - (Sx * Sx))  # calculamos el valor de B1, necesario para obtener B0
        self.B0 = (Sy - (self.B1 * Sx)) / self.n  # calculamos B0
        Ssr = sum((yi - (self.B0 + self.B1 * xi)) ** 2 for xi, yi in zip(self.x, self.y))
        y_mean = Sy / self.n
        Sst = sum((yi - y_mean) ** 2 for yi in self.y)
        self.r = ((self.n*Sxy)-(Sx*Sy))/math.sqrt((self.n*Sx2-(Sx*Sx))*(self.n*Sy2-(Sy*Sy)))
        self.r2 = 1 - (Ssr / Sst)
        print("B0 es igual a ", self.B0)  # imprimimos los valores en consola, para implementaciones sin interfaz grafica
        print("B1 es igual a ", self.B1)

    def getB0(self): #funcion de regresion lineal simple, solicita como entrada dos arreglos
        return self.B0

    def getB1(self):
        return self.B1

    def null(self):
        self.n = 0
        self.x = list()
        self.y = list()
        self.B0 = 0.0
        self.B1 = 0.0

    def pop(self, pos):
        if pos <= self.n:
            self.x.pop(pos)
            self.y.pop(pos)
            self.n = len(self.x)
            self.calculaBs()

    def input(self, inx, iny):
        self.x.append(inx)
        self.y.append(iny)
        self.n = len(self.x)
        self.calculaBs()

    def predict(self, ox):
        oy = self.B0 + (ox * self.B1)
        print("Dado X = "+str(ox)+", Y = "+str(self.B0)+" + ("+str(self.B1)+" * "+str(ox)+") = "+str(oy))
        return oy

    def getR2(self):
        return self.r2

    def getR(self):
        return self.r

exam = pls(pruebax,pruebay)
exam.predict(24)
exam.predict(25)
exam.predict(27)
exam.predict(28)
exam.predict(29)
print("R squared = "+str(exam.getR2()))
print("R = "+str(exam.getR()))