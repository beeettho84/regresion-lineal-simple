from tkinter import *
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]
seleccion = None
indice = None

def getB0(x,y):
    Sx = sum(x)
    Sy = sum(y)
    Sxy = 0
    Sx2 = 0
    n = len(x)
    i=0
    for i in range(n):
        Sxy = Sxy + (x[i] * y[i])
        Sx2 = Sx2 + (x[i] * x[i])
    B1 = (n * Sxy - (Sx * Sy)) / (n * Sx2 - (Sx * Sx))
    B0 = (Sy - (B1 * Sx)) / n
    print("B0 es igual a ", B0)
    print("B1 es igual a ", B1)
    Bs = [B0,B1]
    return Bs

def nullDataset(): #vacia la tabla y los conjuntos
    global pruebax, pruebay
    tabla.delete(*tabla.get_children())
    pruebax = []
    pruebay = []
    nullScatter()
    print("Hecho")

def nullScatter():
    # Limpiar el gráfico de dispersión
    subplot.clear()
    canvas.draw()

def inputData():
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
    def insertData(x,y):
        b=True
        global pruebax, pruebay
        if x == 0 and y == 0:
            b=messagebox.askyesno("Error","Introduciendo datos vacios ¿Desea continuar?")
            print(b)
        if b:
            Ix.set(0)
            Iy.set(0)
            lblX.destroy()
            InX.destroy()
            lblY.destroy()
            InY.destroy()
            btnGuardar.destroy()
            pruebax.append(x)
            pruebay.append(y)
            tabla.insert("","end", values=(x,y))
            nullScatter()
            graficar()

def graficar():
    global pruebax, pruebay
    subplot.scatter(pruebax,pruebay)
    canvas.draw()
    B = getB0(pruebax,pruebay)
    Be0 = Label(ventana, text="B0 = " + str(B[0]), font="Arial 20 bold", background='white', anchor=W, width=20)
    Be1 = Label(ventana, text="B1 = " + str(B[1]), font="Arial 20 bold", background='white', anchor=W, width=20)
    Be0.place(anchor=N, x=200, y=450)
    Be1.place(anchor=N, x=200, y=500)
    print("Graficado")

def deleteData():
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


ventana = Tk()
ventana.title("Regresion lineal simple")
ventana.geometry("1000x600")
ventana.configure(background='white')
figura = Figure(figsize=(5,4), dpi=100)
subplot = figura.add_subplot(1,1,1)
subplot.scatter(pruebax,pruebay)
grafica = Frame(ventana, width=600, height=600)
grafica.place(anchor=N, x=300, y=10)
canvas = FigureCanvasTkAgg(figura, master=grafica)
canvas.draw()
canvas.get_tk_widget().pack()
tabla = ttk.Treeview(ventana, columns=("X", "Y"))
tabla.place(anchor = N, x=800, y=10, width=300, height=400)
btnVaciar = Button(ventana, text="Vaciar", command=nullDataset)
btnVaciar.place(anchor=N, x=700, y=450)
btnVaciar = Button(ventana, text="Agregar", command=inputData)
btnVaciar.place(anchor=N, x=800, y=450)
btnEliminar = Button(ventana, text="Eliminar", state=DISABLED,command=deleteData)
btnEliminar.place(anchor=N, x=900, y=450)

tabla.heading("X", text="X")
tabla.heading("Y", text="Y")
tabla.column("#0", width=0)
tabla.column("X", width=10)
tabla.column("Y", width=10)
for i in range(len(pruebax)):
    tabla.insert("","end",values=(pruebax[i],pruebay[i]))
B = getB0(pruebax, pruebay)
Be0 = Label(ventana, text="B0 = "+str(B[0]), font="Arial 20 bold", background='white', anchor=W, width=20)
Be1 = Label(ventana, text="B1 = "+str(B[1]), font="Arial 20 bold", background='white', anchor=W, width=20)
Be0.place(anchor=N, x=200, y=450)
Be1.place(anchor=N, x=200, y=500)

def filaSeleccionada(event):
    global seleccion, indice
    btnEliminar.configure(state=NORMAL)
    seleccion = tabla.selection()
    if seleccion:
        indice = tabla.index(seleccion[0])
    print("capturado", seleccion)
    print(indice)

tabla.bind_all('<<TreeviewSelect>>', filaSeleccionada)

# Ejecutar el bucle principal de Tkinter
ventana.mainloop()