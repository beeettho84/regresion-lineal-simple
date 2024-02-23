from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]
seleccion = None
indice = None

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
    print("B0 es igual a ", B0) #imprimimos los valores en consola, para implementaciones sin interfaz grafica
    print("B1 es igual a ", B1)
    Bs = [B0,B1]
    return Bs #retornamos ambos valores

def nullDataset(): #vacia la tabla y los conjuntos
    global pruebax, pruebay
    tabla.delete(*tabla.get_children())
    pruebax = []
    pruebay = []
    nullScatter()
    print("Hecho")

def nullScatter(): #vacia el scatter plot
    subplot.clear()
    canvas.draw()

def inputData(): #permite entrada de valores por pares
    Ix = IntVar()
    Iy = IntVar()
    InX = Entry(ventana, textvariable=Ix, width=5)
    InY = Entry(ventana, textvariable=Iy, width=5)
    lblX = Label(ventana, text="X:", anchor=W, background='white')
    lblY = Label(ventana, text="Y:", anchor=W, background='white')
    btnGuardar = Button(ventana, text="Guardar", command=lambda:insertData(Ix.get(), Iy.get()))
    lblX.place(anchor=N, x=660, y=500)
    InX.place(anchor=N, x=700, y=500)
    lblY.place(anchor=N, x=760, y=500)
    InY.place(anchor=N, x=800, y=500)
    btnGuardar.place(anchor=N, x=900, y=500)
    def insertData(x,y): #introduce los valores en las listas y vacia las variables auxiliares
        b=True
        global pruebax, pruebay
        if x == 0 and y == 0: #en caso de que ambos valores sean 0 se pide una confirmacion de inserte
            b=messagebox.askyesno("Error","Introduciendo datos vacios ¿Desea continuar?")
            print(b)
        if b: #si los valores no son 0 o son 0 pero se autoriza la entrada
            Ix.set(None) #se vacian las variables auxiliares
            Iy.set(None)
            lblX.destroy()
            InX.destroy()
            lblY.destroy()
            InY.destroy()
            btnGuardar.destroy()
            pruebax.append(x)#se agregan los datos a las listas y tabla
            pruebay.append(y)
            tabla.insert("","end", values=(x,y))
            nullScatter()#borramos el plot anterior
            graficar()#y dibujamos uno nuevo

def graficar():#funcion para dibujar la grafica de puntos en base a las listas
    global pruebax, pruebay
    subplot.scatter(pruebax,pruebay)
    canvas.draw()
    B = getB0(pruebax,pruebay)#se recalculan B0 y B1 para actualizarlos
    Be0 = Label(ventana, text="B0 = " + str(B[0]), font="Arial 20 bold", background='white', anchor=W, width=20)
    Be1 = Label(ventana, text="B1 = " + str(B[1]), font="Arial 20 bold", background='white', anchor=W, width=20)
    Be0.place(anchor=N, x=200, y=450)
    Be1.place(anchor=N, x=200, y=500)
    print("Graficado")#impresion de control

def predict(x)
    B = getB0(pruebax, pruebay)
    y = B[0]+(x*B[1])
    print y
    return y

def deleteData():#borra un par de elementos de tabla, grafica y listas
    global seleccion,indice
    print(seleccion, indice)
    tabla.delete(seleccion)
    btnEliminar.configure(state=DISABLED)
    pruebax.pop(indice)
    pruebay.pop(indice)
    nullScatter()
    graficar()
    tabla.selection_remove(seleccion)
    indice = None
    seleccion = None


ventana = Tk() #configuracion de ventana
ventana.title("Regresion lineal simple")
ventana.geometry("900x550")
ventana.configure(background='white')
figura = Figure(figsize=(5,4), dpi=100)#configuracion de grafica
subplot = figura.add_subplot(1,1,1)
subplot.scatter(pruebax,pruebay)
grafica = Frame(ventana, width=600, height=600)
grafica.place(anchor=N, x=300, y=10)
canvas = FigureCanvasTkAgg(figura, master=grafica)
canvas.draw()
canvas.get_tk_widget().pack()
tabla = ttk.Treeview(ventana, columns=("X", "Y"))#configuracion de tabla
tabla.place(anchor = N, x=700, y=10, width=300, height=400)
tabla.heading("X", text="X")
tabla.heading("Y", text="Y")
tabla.column("#0", width=1)
tabla.column("X", width=10)
tabla.column("Y", width=10)
for i in range(len(pruebax)):#insercion de los datos de las listas en la tabla
    tabla.insert("","end",values=(pruebax[i],pruebay[i]))
btnVaciar = Button(ventana, text="Vaciar", command=nullDataset)#boton para vaciar las listas
btnVaciar.place(anchor=N, x=600, y=450)
btnVaciar = Button(ventana, text="Agregar", command=inputData)#boton para agregar un par de elementos x y
btnVaciar.place(anchor=N, x=700, y=450)
btnEliminar = Button(ventana, text="Eliminar", state=DISABLED,command=deleteData)#boton para eliminar un par de elementos x y
btnEliminar.place(anchor=N, x=800, y=450)
B = getB0(pruebax, pruebay)#obtencion hardcodeada de valores en base al conjunto de prueba
Be0 = Label(ventana, text="B0 = "+str(B[0]), font="Arial 20 bold", background='white', anchor=W, width=20)
Be1 = Label(ventana, text="B1 = "+str(B[1]), font="Arial 20 bold", background='white', anchor=W, width=20)
Be0.place(anchor=N, x=300, y=450)
Be1.place(anchor=N, x=300, y=500)
predict(24)
predict(25)
predict(27)
predict(28)
predict(29)

def filaSeleccionada(event):#configuracion de evento de seleccion para eliminacion de elementos
    global seleccion, indice
    btnEliminar.configure(state=NORMAL)
    seleccion = tabla.selection()
    if seleccion:
        indice = tabla.index(seleccion[0])
    print("capturado", seleccion)
    print(indice)

tabla.bind_all('<<TreeviewSelect>>', filaSeleccionada)#captura de evento

ventana.mainloop()# Ejecutar el bucle principal de Tkinter
