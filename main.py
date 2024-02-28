from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import math

pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]
seleccion = None
indice = None
B = None

class Dataset:
    x = list()
    y = list()
    def __init__(self, inx, iny):
        self.x = inx
        self.y = iny

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def null(self):
        self.x = list()
        self.y = list()


class DiscreteMath:
    def SumX(x):
        return sum(x)

    def SumY(y):
        return sum(y)

    def SumXY(x, y):
        i=0
        out = 0.0
        if len(x) == len(y):
            for i in range(len(x)):
                out += x[i] * y[i]
            return out
        else:
            print("error, X y Y deben tener la misma longitud")

    def SumX2(x):
        i = 0
        out = 0.0
        for i in range(len(x)):
            out += x[i] * x[i]
        return out

    def SumY2(y):
        i = 0
        out = 0.0
        for i in range(len(y)):
            out += y[i] * y[i]
        return out

    def SumXSumX(x):
        return sum(x)*sum(x)

    def SumXSumY(x,y):
        return sum(x)*sum(y)


class pls:
    #x = list()
    #y = list()
    data = None
    B0 = float()
    B1 = float()
    n = 0
    r = 0
    r2 = 0

    def __init__(self, inx, iny):
        if(len(inx) == len(iny)):
            self.n = len(inx)
            #self.x = inx
            #self.y = iny
            self.data = Dataset(inx, iny)
            self.calculaBs()

    def calculaBs(self):
        Sx = DiscreteMath.SumX(self.data.getX())  # obtenemos los valores parciales de las ecuaciones para facilitar el calculo
        Sy = DiscreteMath.SumY(self.data.getY())
        Sxy = DiscreteMath.SumXY(self.data.getX(), self.data.getY())
        Sx2 = DiscreteMath.SumX2(self.data.getX())
        Sy2 = DiscreteMath.SumY2(self.data.getY())
        self.B1 = (self.n * Sxy - (DiscreteMath.SumXSumY(self.data.getX(), self.data.getY()))) / (self.n * Sx2 - (DiscreteMath.SumXSumX(self.data.getX())))  # calculamos el valor de B1, necesario para obtener B0
        self.B0 = (Sy - (self.B1 * Sx)) / self.n  # calculamos B0
        Ssr = sum((yi - (self.B0 + self.B1 * xi)) ** 2 for xi, yi in zip(self.data.getX(), self.data.getY()))
        y_mean = Sy / self.n
        Sst = sum((yi - y_mean) ** 2 for yi in self.data.getY())
        self.r = ((self.n*Sxy)-(DiscreteMath.SumXSumY(self.data.getX(), self.data.getY())))/math.sqrt((self.n*Sx2-(DiscreteMath.SumXSumX(self.data.getX())))*(self.n*Sy2-(DiscreteMath.SumXSumX(self.data.getY()))))
        self.r2 = 1 - (Ssr / Sst)

        print("B0 es igual a ", self.B0)  # imprimimos los valores en consola, para implementaciones sin interfaz grafica
        print("B1 es igual a ", self.B1)

    def getB0(self): #funcion de regresion lineal simple, solicita como entrada dos arreglos
        return self.B0

    def getB1(self):
        return self.B1

    def null(self):
        self.n = 0
        self.data.null()
        self.B0 = 0.0
        self.B1 = 0.0

    def pop(self, pos):
        if pos <= self.n:
            self.data.getX().pop(pos)
            self.data.getY().pop(pos)
            self.n = len(self.data.getX())
            self.calculaBs()

    def input(self, inx, iny):
        self.data.getX().append(inx)
        self.data.getY().append(iny)
        self.n = len(self.data.getX())
        self.calculaBs()

    def predict(self, ox):
        oy = self.B0 + (ox * self.B1)
        print("Dado X = "+str(ox)+", Y = "+str(self.B0)+" + ("+str(self.B1)+" * "+str(ox)+") = "+str(oy))
        return oy


    def getR2(self):
        return self.r2

    def getR(self):
        return self.r


def nullDataset(obj): #vacia la tabla y los conjuntos
    global pruebax, pruebay
    tabla.delete(*tabla.get_children())
    obj.null()
    nullScatter()
    #print("Hecho")

def nullScatter(): #vacia el scatter plot
    subplot.clear()
    canvas.draw()

def inputData(obj): #permite entrada de valores por pares
    Ix = IntVar()
    Iy = IntVar()
    InX = Entry(ventana, textvariable=Ix, width=5)
    InY = Entry(ventana, textvariable=Iy, width=5)
    lblX = Label(ventana, text="X:", anchor=W, background='white')
    lblY = Label(ventana, text="Y:", anchor=W, background='white')
    btnGuardar = Button(ventana, text="Guardar", command=lambda:insertData(obj, Ix.get(), Iy.get()))
    lblX.place(anchor=N, x=560, y=450)
    InX.place(anchor=N, x=600, y=450)
    lblY.place(anchor=N, x=660, y=450)
    InY.place(anchor=N, x=700, y=450)
    btnGuardar.place(anchor=N, x=800, y=450)
    def insertData(obj, x,y): #introduce los valores en las listas y vacia las variables auxiliares
        b=True
        #global pruebax, pruebay
        if x == 0 and y == 0: #en caso de que ambos valores sean 0 se pide una confirmacion de inserte
            b=messagebox.askyesno("Error","Introduciendo datos vacios ¿Desea continuar?")
        if b: #si los valores no son 0 o son 0 pero se autoriza la entrada
            Ix.set(None) #se vacian las variables auxiliares
            Iy.set(None)
            lblX.destroy()
            InX.destroy()
            lblY.destroy()
            InY.destroy()
            btnGuardar.destroy()
            obj.input(x,y)
            tabla.insert("","end", values=(x,y))
            nullScatter()#borramos el plot anterior
            graficar(obj)#y dibujamos uno nuevo

def graficar(obj):#funcion para dibujar la grafica de puntos en base a las listas
    global pruebax, pruebay, lblB0, lblB1
    lblB0.destroy()
    lblB1.destroy()
    subplot.scatter(pruebax,pruebay)
    canvas.draw()
    lblB0 = Label(ventana, text="B0 = " + str(obj.getB0()), font="Arial 20 bold", background='white', anchor=W, width=20)
    lblB1 = Label(ventana, text="B1 = " + str(obj.getB1()), font="Arial 20 bold", background='white', anchor=W, width=20)
    lblB0.place(anchor=N, x=200, y=400)
    lblB1.place(anchor=N, x=200, y=450)
    lblR = Label(ventana, text="R = " + str(exam.getR()), font="Arial 20 bold", background='white', anchor=W, width=20)
    lblR2 = Label(ventana, text="R2 = " + str(exam.getR2()), font="Arial 20 bold", background='white', anchor=W, width=20)
    lblR.place(anchor=N, x=200, y=500)
    lblR2.place(anchor=N, x=200, y=550)
    #print("Graficado")#impresion de control

def grafPredict(obj,x):
    lblY.configure(text="Y = "+str(obj.predict(x)))

def deleteData(obj):#borra un par de elementos de tabla, grafica y listas
    global seleccion,indice
    #print(seleccion, indice)
    tabla.delete(seleccion)
    btnEliminar.configure(state=DISABLED)
    obj.pop(indice)
    nullScatter()
    graficar(obj)
    indice = None
    seleccion = None

ventana = Tk() #configuracion de ventana
ventana.title("Regresion lineal simple")
ventana.geometry("900x600")
ventana.configure(background='white')
exam = pls(pruebax,pruebay)
figura = Figure(figsize=(5,4), dpi=100)#configuracion de grafica
subplot = figura.add_subplot(1,1,1)
subplot.scatter(exam.data.getX(),exam.data.getY())
grafica = Frame(ventana, width=600, height=600)
grafica.place(anchor=N, x=250, y=0)
canvas = FigureCanvasTkAgg(figura, master=grafica)
canvas.draw()
canvas.get_tk_widget().pack()
tabla = ttk.Treeview(ventana, columns=("X", "Y"))#configuracion de tabla
tabla.place(anchor = N, x=700, y=10, width=300, height=350)
tabla.heading("X", text="X")
tabla.heading("Y", text="Y")
tabla.column("#0", width=1)
tabla.column("X", width=10)
tabla.column("Y", width=10)
for i in range(len(pruebax)):#insercion de los datos de las listas en la tabla
    tabla.insert("","end",values=(pruebax[i],pruebay[i]))
btnVaciar = Button(ventana, text="Vaciar", command=lambda: nullDataset(exam))#boton para vaciar las listas
btnVaciar.place(anchor=N, x=600, y=400)
btnAgregar = Button(ventana, text="Agregar", command=lambda: inputData(exam))#boton para agregar un par de elementos x y
btnAgregar.place(anchor=N, x=700, y=400)
btnEliminar = Button(ventana, text="Eliminar", state=DISABLED, command=lambda: deleteData(exam))#boton para eliminar un par de elementos x y
btnEliminar.place(anchor=N, x=800, y=400)
lblB0 = Label(ventana, text="B0 = "+str(exam.getB0()), font="Arial 20 bold", background='white', anchor=W, width=20)
lblB1 = Label(ventana, text="B1 = "+str(exam.getB1()), font="Arial 20 bold", background='white', anchor=W, width=20)
lblB0.place(anchor=N, x=200, y=400)
lblB1.place(anchor=N, x=200, y=450)
lblR = Label(ventana, text="R = "+str(exam.getR()), font="Arial 20 bold", background='white', anchor=W, width=20)
lblR2 = Label(ventana, text="R2 = "+str(exam.getR2()), font="Arial 20 bold", background='white', anchor=W, width=20)
lblR.place(anchor=N, x=200, y=500)
lblR2.place(anchor=N, x=200, y=550)
exam.predict(24)
exam.predict(25)
exam.predict(27)
exam.predict(28)
exam.predict(29)
print("R squared = "+str(exam.getR2()))
print("R = "+str(exam.getR()))
px = IntVar()
py = IntVar()
lblX = Label(ventana, text="X=", font="Arial 14 bold", background='white')
inX = Entry(ventana, textvariable=px, width=5)
lblX.place(anchor=N, x=550, y=500)
inX.place(anchor=N, x=600, y=500)
lblY = Label(ventana, text="Y=", width=10, anchor=W, font="Arial 14 bold", background='white')
lblY.place(anchor=N, x=810, y=500)
btnPredecir = Button(ventana, text="Predecir", command=lambda: grafPredict(exam, px.get()))
btnPredecir.place(anchor=N, x=700, y=500)

def filaSeleccionada(event):#configuracion de evento de seleccion para eliminacion de elementos
    global seleccion, indice
    btnEliminar.configure(state=NORMAL)
    seleccion = tabla.selection()
    if seleccion:
        indice = tabla.index(seleccion[0])

tabla.bind_all('<<TreeviewSelect>>', filaSeleccionada)#captura de evento
ventana.mainloop()# Ejecutar el bucle principal de Tkinter