import sqlite3

conn = sqlite3.connect('productos-db.db')

c = conn.cursor()

def inicializarDB():
    c.execute("""
        CREATE TABLE if not exists Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        );
    """)

def insertar(producto):
    c.execute("""
        INSERT INTO Producto (nombre, cantidad, precio) VALUES (?, ?, ?)
    """, (producto['nombre'], producto['cantidad'], producto['precio']))
    conn.commit()

def obtener_productos():
    filas = c.execute("SELECT * FROM Producto").fetchall()
    return filas

def borrar(id):
    c.execute('DELETE FROM Producto WHERE id = ?', (id, ))
    conn.commit()

def modificar(id, producto):
    c.execute("""UPDATE Producto SET 
        nombre = ?,
        cantidad = ?,
        precio = ?
        WHERE id = ?""", (producto['nombre'], producto['cantidad'], producto['precio'], id))
    conn.commit()

def filtrar_productos(search):
    c.execute("SELECT * FROM Producto WHERE nombre like ?", ('%' + search +'%', ))
    filas = c.fetchall()
    return filas
