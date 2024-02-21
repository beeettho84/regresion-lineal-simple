from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

ventana = Tk()
ventana.title("Regresion lineal simple")
ventana.geometry("1000x600")
ventana.configure(background='white')
figura = Figure(figsize=(5,4), dpi=100)
subplot = figura.add_subplot(1,1,1)
pruebax = [23, 26, 30, 34, 43, 48, 52, 57, 58]
pruebay = [651, 762, 856, 1063, 1190, 1298, 1421, 1440, 1518]
subplot.scatter(pruebax,pruebay)
grafica = Frame(ventana, width=600, height=600)
grafica.place(anchor = N, x=300, y=10)
canvas = FigureCanvasTkAgg(figura, master=grafica)
canvas.draw()
canvas.get_tk_widget().pack()
tabla = ttk.Treeview(ventana, columns=("X", "Y"))
tabla.place(anchor = N, x=800, y=10, width=300, height=400)
tabla.heading("X", text="X")
tabla.heading("Y", text="Y")
tabla.column("#0", width=0)
tabla.column("X", width=10)
tabla.column("Y", width=10)
for i in range(len(pruebax)):
    tabla.insert("","end",values=(pruebax[i],pruebay[i]))
B = getB0(pruebax, pruebay)
Be0 = Label(ventana, text="B0 = "+str(B[0]), font="Arial 20 bold", background='white', anchor=W, width=20).place(anchor=N, x=200, y=450)
Be1 = Label(ventana, text="B1 = "+str(B[1]), font="Arial 20 bold", background='white', anchor=W, width=20).place(anchor=N, x=200, y=500)

# Ejecutar el bucle principal de Tkinter
ventana.mainloop()



