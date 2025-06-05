import pandas as pd
import tkinter as tk  # Importar tkinter para la interfaz gráfica
from tkinter import ttk  # Importar ttk para los widgets mejorados
from tkinter import messagebox
import variables_globales as vg  # Importar el módulo de variables globales
import matplotlib.pyplot as plt  # Importar matplotlib para graficar datos

# Funciones para mostrar los datos
def mostrar_datos(df, titulo):
    if df is not None and not df.empty:
        print(f"Mostrando datos para {titulo}: \n{df.head()}")

        ventana_datos = tk.Toplevel()
        ventana_datos.title(titulo)

        frame = ttk.Frame(ventana_datos)
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
        tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=tree.yview)
        
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        print("Datos mostrados en la ventana.")
    else:
        messagebox.showerror("Error", "No se han cargado datos. Por favor, cargue un archivo Excel primero.")
        print("No se han cargado datos.")

def mostrar_datos_gkn_inclinometros():
    if vg.df_gkn_inclinometros is not None and not vg.df_gkn_inclinometros.empty:
        mostrar_datos(vg.df_gkn_inclinometros, "Datos GKN Inclinómetros")

def mostrar_datos_excel_inclinometros():
    print("Verificando vg.df_inclinometros:", vg.df_inclinometros)  # Mensaje de depuración
    if vg.df_inclinometros is not None and not vg.df_inclinometros.empty:
        mostrar_datos(vg.df_inclinometros, "Datos Inclinómetros")
    else:
        print("No hay datos para mostrar en vg.df_inclinometros")  # Mensaje de depuración
        messagebox.showerror("Error", "No se han cargado datos de inclinómetros.")

def mostrar_datos_puntos_fijos():
    if vg.df_puntos_fijos is not None and not vg.df_puntos_fijos.empty:
        mostrar_datos(vg.df_puntos_fijos, "Datos Puntos Fijos")
    else:
        print("No se han cargado datos de puntos fijos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos de puntos fijos o los datos están vacíos.")

def mostrar_datos_freatimetros():
    if vg.df_freatimetros_combinado is not None and not vg.df_freatimetros_combinado.empty:
        mostrar_datos(vg.df_freatimetros_combinado, "Datos Freatímetros Combinados")

def mostrar_datos_piezometros_electricos():
    if vg.df_piezometros_electricos is not None and not vg.df_piezometros_electricos.empty:
        mostrar_datos(vg.df_piezometros_electricos, "Datos Piezómetros Eléctricos")

def mostrar_datos_piezometros_cg_pe():
    if vg.df_piezometros_cg_pe is not None and not vg.df_piezometros_cg_pe.empty:
        mostrar_datos(vg.df_piezometros_cg_pe, "Datos Piezómetros CG con PE")

def mostrar_datos_celdas_asentamiento():
    if vg.df_celdas_asentamiento is not None and not vg.df_celdas_asentamiento.empty:
        mostrar_datos(vg.df_celdas_asentamiento, "Datos Celdas de Asentamiento")

def mostrar_datos_extensometros_recinto():
    if vg.df_extensometros_recinto is not None and not vg.df_extensometros_recinto.empty:
        mostrar_datos(vg.df_extensometros_recinto, "Datos Extensómetros Recinto")

# Funciones para mostrar los datos
def mostrar_seleccion_piezometros():
    if vg.df_piezometros_electricos is None or vg.df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    # Crear una nueva ventana para la selección de piezómetros
    top = tk.Toplevel()
    top.title("Seleccionar Piezómetros")

    # Variables para mantener el estado de los checkbuttons
    seleccion = {}
    for piezometro in vg.df_piezometros_electricos['Piezómetro'].unique():
        seleccion[piezometro] = tk.IntVar()
    
    # Variable para seleccionar todos
    seleccion_todos = tk.IntVar()

    def seleccionar_todos():
        estado = seleccion_todos.get()
        for var in seleccion.values():
            var.set(estado)

    # Crear checkbuttons para cada piezómetro
    row = 0
    for piezometro, var in seleccion.items():
        tk.Checkbutton(top, text=piezometro, variable=var).grid(row=row, sticky='w')
        row += 1

    # Crear un checkbutton para seleccionar todos
    tk.Checkbutton(top, text="Todos", variable=seleccion_todos, command=seleccionar_todos).grid(row=row, sticky='w')
    
    # Botón para confirmar la selección
    tk.Button(top, text="Graficar", command=lambda: graficar_seleccion_piezometros(seleccion, seleccion_todos.get())).grid(row=row+1, pady=10)

def graficar_seleccion_piezometros(seleccion, todos):
    if vg.df_piezometros_electricos is None or vg.df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    piezometros_seleccionados = [piezometro for piezometro, var in seleccion.items() if var.get() == 1]

    if todos:
        datos = vg.df_piezometros_electricos
    elif not piezometros_seleccionados:
        print("No se seleccionaron piezómetros.")
        messagebox.showerror("Error", "No se seleccionaron piezómetros.")
        return
    else:
        datos = vg.df_piezometros_electricos[vg.df_piezometros_electricos['Piezómetro'].isin(piezometros_seleccionados)]

    if 'FECHA' in datos.columns and 'COTA NF' in datos.columns:
        datos['FECHA'] = pd.to_datetime(datos['FECHA'], format='%d/%m/%Y', errors='coerce')
        datos = datos.dropna(subset=['FECHA', 'COTA NF'])
        datos = datos[datos['COTA NF'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]
        datos['COTA NF'] = datos['COTA NF'].astype(float)

        fig, ax = plt.subplots(figsize=(10, 5))
        for piezometro in datos['Piezómetro'].unique():
            piezometro_datos = datos[datos['Piezómetro'] == piezometro]
            x = piezometro_datos['FECHA']
            y = piezometro_datos['COTA NF']
            ax.plot(x, y, marker='o', linestyle='-', label=piezometro)

        ax.set_title('Cota Nivel Freático en Función del Tiempo')
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Cota Nivel Freático')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")
