import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

# Inicializar Prolog y cargar los archivos
prolog = Prolog()
prolog.consult("guiaturistico.pl")
prolog.consult("reglas_guiaturistico.pl")

# Función para realizar consultas y mostrar resultados en una tabla
def mostrar_resultados(resultados, tree, columnas):
    # Limpiar la tabla antes de agregar nuevos resultados
    for item in tree.get_children():
        tree.delete(item)
    
    # Insertar los resultados en la tabla
    for resultado in resultados:
        valores = [resultado[col] for col in columnas]
        tree.insert("", "end", values=valores)

# Funciones de búsqueda con parámetros de entrada
def buscar_por_interes(entry, tree):
    interes = entry.get().strip()
    if not interes:
        messagebox.showerror("Error", "Por favor, ingresa un interés.")
        return
    
    try:
        consulta = f"recomendar_por_interes('{interes}', Nombre, Canton, Provincia)"
        resultados = list(prolog.query(consulta))
        if resultados:
            mostrar_resultados(resultados, tree, ["Nombre", "Canton", "Provincia"])
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron destinos para ese interés.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar Prolog: {e}")

def buscar_por_presupuesto(entry1, entry2, tree):
    tipo_visitante = entry1.get().strip()
    presupuesto = entry2.get().strip()
    if not tipo_visitante or not presupuesto:
        messagebox.showerror("Error", "Por favor, ingresa el tipo de visitante y el presupuesto máximo.")
        return
    
    try:
        consulta = f"recomendar_por_presupuesto('{tipo_visitante}', {presupuesto}, Nombre, Canton, Provincia)"
        resultados = list(prolog.query(consulta))
        if resultados:
            mostrar_resultados(resultados, tree, ["Nombre", "Canton", "Provincia"])
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron destinos para ese presupuesto.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar Prolog: {e}")

def buscar_por_tiempo(entry, tree):
    tiempo_max = entry.get().strip()
    if not tiempo_max:
        messagebox.showerror("Error", "Por favor, ingresa el tiempo disponible.")
        return
    
    try:
        consulta = f"recomendar_por_tiempo({tiempo_max}, Nombre, Canton, Provincia)"
        resultados = list(prolog.query(consulta))
        if resultados:
            mostrar_resultados(resultados, tree, ["Nombre", "Canton", "Provincia"])
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron destinos para ese tiempo disponible.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar Prolog: {e}")

def listar_por_provincia(entry, tree):
    provincia = entry.get().strip()
    if not provincia:
        messagebox.showerror("Error", "Por favor, ingresa una provincia.")
        return
    
    try:
        consulta = f"listar_destinos_provincia('{provincia}', Nombre, Canton, Interes)"
        resultados = list(prolog.query(consulta))
        if resultados:
            mostrar_resultados(resultados, tree, ["Nombre", "Canton", "Interes"])
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron destinos en esa provincia.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar Prolog: {e}")

def recomendar_destino_ideal(entry1, entry2, entry3, entry4, tree):
    interes = entry1.get().strip()
    tipo_visitante = entry2.get().strip()
    presupuesto = entry3.get().strip()
    tiempo_max = entry4.get().strip()
    
    if not interes or not tipo_visitante or not presupuesto or not tiempo_max:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return
    
    try:
        consulta = f"recomendar_destino_ideal('{interes}', '{tipo_visitante}', {presupuesto}, {tiempo_max}, Nombre, Canton, Provincia)"
        resultados = list(prolog.query(consulta))
        if resultados:
            mostrar_resultados(resultados, tree, ["Nombre", "Canton", "Provincia"])
        else:
            messagebox.showinfo("Sin Resultados", "No se encontraron destinos ideales según los criterios ingresados.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al consultar Prolog: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Recomendador Turístico")
root.geometry("600x500")
root.resizable(False, False)

# Pestañas para diferentes tipos de búsqueda
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# Función auxiliar para crear pestañas y tablas
def crear_pestana(notebook, titulo, campos, comando, columnas):
    frame = tk.Frame(notebook)
    notebook.add(frame, text=titulo)
    
    entries = []
    for etiqueta in campos:
        tk.Label(frame, text=etiqueta).pack(pady=5)
        entry = tk.Entry(frame, width=30)
        entry.pack(pady=5)
        entries.append(entry)
    
    # Botón de búsqueda
    btn_buscar = tk.Button(frame, text="Buscar", command=lambda: comando(*entries, tree))
    btn_buscar.pack(pady=10)
    
    # Tabla para mostrar resultados
    tree = ttk.Treeview(frame, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col.capitalize())
    tree.pack(expand=1, fill="both")
    
    # Barra de desplazamiento
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    
    return entries, tree

# Crear las pestañas
entries_interes, tree_interes = crear_pestana(notebook, "Por Interés", ["Interés (naturaleza, cultura, gastronomia):"], buscar_por_interes, ["Nombre", "Canton", "Provincia"])
entries_presupuesto, tree_presupuesto = crear_pestana(notebook, "Por Presupuesto", ["Tipo de Visitante:", "Presupuesto Máximo:"], buscar_por_presupuesto, ["Nombre", "Canton", "Provincia"])
entries_tiempo, tree_tiempo = crear_pestana(notebook, "Por Tiempo", ["Tiempo Máximo (en horas):"], buscar_por_tiempo, ["Nombre", "Canton", "Provincia"])
entries_provincia, tree_provincia = crear_pestana(notebook, "Por Provincia", ["Provincia:"], listar_por_provincia, ["Nombre", "Canton", "Interes"])
entries_ideal, tree_ideal = crear_pestana(notebook, "Destino Ideal", ["Interés:", "Tipo de Visitante:", "Presupuesto Máximo:", "Tiempo Máximo:"], recomendar_destino_ideal, ["Nombre", "Canton", "Provincia"])

# Iniciar el bucle principal
root.mainloop()
