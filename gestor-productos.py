from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import db

root = Tk()
root.title("Registro de ventas")
root.resizable(width=False, height=False)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

#Funciones
def agregar():
    if not inputNombre.get():
        messagebox.showerror('Error en el nombre', 'El nombre es obligatorio')
        return
    if not inputPrecio.get():
        messagebox.showerror('Error en el precio', 'El precio es obligatorio')
        return 
    if not inputCantidad.get():
        messagebox.showerror('Error en la cantidad', 'La cantidad es obligatorio')
        return
    try:
        float(inputPrecio.get())

        try:
            int(inputCantidad.get())
            producto = {
                'nombre' : inputNombre.get(),
                'cantidad' : inputCantidad.get(),
                'precio': inputPrecio.get()
            }
            db.insertar(producto)
            listar_productos()
            inputNombre.delete(0, END)
            inputCantidad.delete(0, END)
            inputPrecio.delete(0, END)

        except ValueError:
            messagebox.showerror('Error en la cantidad', 'Solo Numeros')

    except ValueError:
        messagebox.showerror('Error en el precio', 'Solo Numeros')
    
    

def listar_productos():
    filas = db.obtener_productos()

    tree.delete(*tree.get_children())
    for fila in filas:
        tree.insert('', END, fila[0], values=(fila[0], fila[1], fila[2], fila[3]))

def eliminar():
    try:
        id = tree.selection()[0]
    
        respuesta = messagebox.askokcancel('Seguro?', 'Estas seguro de querer eliminar el producto?')
        if respuesta:
            db.borrar(id)
            listar_productos()
        else:
            pass
    except:
        messagebox.showwarning('Error en la tabla', 'Tiene que seleccionar un producto')
    

def editar():
    def editarProducto(id):
        if not nombre.get():
            messagebox.showerror('Error en el nombre', 'El nombre es obligatorio')
            return
        if not precio.get():
            messagebox.showerror('Error en el precio', 'El precio es obligatorio')
            return 
        if not cantidad.get():
            messagebox.showerror('Error en la cantidad', 'La cantidad es obligatorio')
            return
        producto = {
            'nombre' : nombre.get(),
            'cantidad' : cantidad.get(),
            'precio': precio.get()
        }
        db.modificar(id, producto)
        listar_productos()
        top.destroy()
    try:
        id = tree.selection()[0]
        selectNombre = tree.item(tree.selection())['values'][1]
        selectCantidad = tree.item(tree.selection())['values'][2]
        selectPrecio = tree.item(tree.selection())['values'][3]

        top = Toplevel()
        top.title('Editar producto')
        lnombre = Label(top, text='Nombre')
        nombre = Entry(top, width=40)
        lnombre.grid(row=0, column=0)
        nombre.grid(row=0, column=1)

        lcantidad = Label(top, text='Cantidad')
        cantidad = Entry(top, width=40, )
        lcantidad.grid(row=1, column=0)
        cantidad.grid(row=1, column=1)

        lprecio = Label(top, text='Precio')
        precio = Entry(top, width=40)
        lprecio.grid(row=2, column=0)
        precio.grid(row=2, column=1)

        nombre.insert(0, selectNombre)
        cantidad.insert(0, selectCantidad)
        precio.insert(0, selectPrecio)

        btnModificar = Button(top, text='Editar', command=lambda: editarProducto(id), font=('Arial', 13, 'bold'), bg="#1a9ae5", fg="#fff", width=30)
        btnModificar.grid(row=3, column=0, columnspan=2)

        top.mainloop()
    except:
        messagebox.showwarning('Error en la tabla', 'Tiene que seleccionar un producto')
    
def buscarProducto():
    search = inputSearch.get()
    if not search:
        filas = db.obtener_productos()
        tree.delete(*tree.get_children())
        for fila in filas:
            tree.insert('', END, fila[0], values=(fila[0], fila[1], fila[2], fila[3]))
    else:
        filas = db.filtrar_productos(search)
        tree.delete(*tree.get_children())
        for fila in filas:
            tree.insert('', END, fila[0], values=(fila[0], fila[1], fila[2], fila[3]))

    
    

#InicializamosDB
db.inicializarDB()

#LabelFrame
frame = LabelFrame(root, padx=10, pady=10)
frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

#Nombre
labelNombre = Label(frame, text="Nombre:", font=('Arial', 13, 'bold'))
labelNombre.grid(row=0, column=0, pady=10)

inputNombre = Entry(frame, width=40)
inputNombre.grid(row=0, column=1)

#Precio
labelPrecio = Label(frame, text="Precio:", font=('Arial', 13, 'bold'))
labelPrecio.grid(row=1, column=0, pady=10)

inputPrecio = Entry(frame, width=40)
inputPrecio.grid(row=1, column=1)

#Cantidad
labelCantidad = Label(frame, text="Cantidad:", font=('Arial', 13, 'bold'))
labelCantidad.grid(row=2, column=0, pady=10)

inputCantidad = Entry(frame, width=40)
inputCantidad.grid(row=2, column=1)

#Boton agregar
btnAgregar = Button(frame, text="Agregar producto", command=agregar, font=('Arial', 13, 'bold'), bg="#3fcb34", fg="#fff")
btnAgregar.grid(row=3, column=0, columnspan=2)

#Treeview tabla de productos
tree = ttk.Treeview(root)
tree['column'] = ('ID', 'Nombre', 'Cantidad', 'Precio')
tree.column('#0', width=0, stretch=NO)
tree.column('ID')
tree.column('Nombre')
tree.column('Cantidad')
tree.column('Precio')

tree.heading('ID', text='ID')
tree.heading('Nombre', text='Nombre')
tree.heading('Cantidad', text='Cantidad')
tree.heading('Precio', text='Precio')
tree.grid(column=0, row=2, columnspan=2)

#Boton eliminar
btnEliminar = Button(root, text="Eliminar producto", command=eliminar, font=('Arial', 13, 'bold'), bg="#d0432f", fg="#fff", padx=10)
btnEliminar.grid(row=3, column=0, pady=10)
#Boton editar
btnEditar = Button(root, text="Editar producto", command=editar, font=('Arial', 13, 'bold'), bg="#1a9ae5", fg="#fff", padx=20)
btnEditar.grid(row=3, column=1)

#Buscador
frameSearch = LabelFrame(root, padx=10, pady=10)
frameSearch.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

inputSearch = Entry(frameSearch, width=35)
inputSearch.grid(row=0, column=0, pady=10)

btnBuscar = Button(frameSearch, text="Buscar", padx=10, font=('Arial', 13, 'bold'), bg="#1a9ae5", fg="#fff", command=buscarProducto)
btnBuscar.grid(row=0, column=1, padx=10)

inputNombre.focus()
#Listar
listar_productos()

root.mainloop()