import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename 
import variables_globales as vg 
from procesa_datos import (
    procesar_carpeta_gkn,
    procesar_excel_inclinometros,
    procesar_datos_puntos_fijos,
    procesar_datos_freatimetros,
    procesar_datos_piezometros_electricos,
    procesar_datos_piezometros_cg_pe,
    procesar_datos_celdas_asentamiento,
    procesar_datos_extensometros_recinto
)

# Funciones para cargar datos

def cargar_y_procesar_gkn_inclinometros():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos GKN")
    if not carpeta:
        messagebox.showerror("Error", "No se seleccionó ninguna carpeta.")
        return None
    resultado = procesar_carpeta_gkn(carpeta)
    setattr(vg, 'datos_gkn_inclinometros', resultado)  # Asignar a la variable global
    return resultado

def cargar_y_procesar_excel_inclinometros():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    file_path = askopenfilename(title="Selecciona el archivo Excel", filetypes=[("Archivos Excel", "*.xlsx")])
    
    if not file_path:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    try:
        df = procesar_excel_inclinometros(file_path)
        if df is not None:
            vg.df_inclinometros = df  # Asignar a la variable global
            print("Datos cargados y asignados a vg.df_inclinometros")  # Mensaje de depuración
            print(df.head())  # Imprime las primeras filas para verificar
            messagebox.showinfo("Éxito", "Datos del archivo Excel cargados y procesados correctamente.")
            return df
        else:
            messagebox.showerror("Error", "No se pudo procesar el archivo Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando el archivo: {e}")
    return None

def cargar_datos_puntos_fijos():
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de puntos fijos", filetypes=[("Excel files", "*.xlsx;*.xls")])
    if not file_path:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    try:
        resultado = procesar_datos_puntos_fijos(file_path)
        vg.df_puntos_fijos = resultado  # Asignar a la variable global
        print("Datos de puntos fijos cargados y asignados a la variable global.")
        print(vg.df_puntos_fijos.head())  # Imprimir las primeras filas para verificar
        return resultado
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {e}")
        print(f"Ocurrió un error al procesar el archivo: {e}")
        return None

def cargar_datos_freatimetros():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_freatimetros(archivo)
    if df_combinado is not None and not df_combinado.empty:
        vg.df_freatimetros_combinado = df_combinado
        # Actualizar el nombre del freatímetro basado en los datos cargados
        vg.nombre_freatimetro = df_combinado['Freatimetro'].unique()[0]  # Suponiendo que hay una columna 'Freatimetro'
        messagebox.showinfo("Éxito", "Datos de Freatímetros cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se pudo procesar el archivo Excel.")
        return None

def cargar_datos_piezometros_electricos():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_piezometros_electricos(archivo)
    if df_combinado is not None and not df_combinado.empty:
        vg.df_piezometros_electricos = df_combinado  # Utilizar la variable global
        print(vg.df_piezometros_electricos.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Piezómetros Eléctricos cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None

def cargar_datos_piezometros_cg_pe():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_piezometros_cg_pe(archivo)
    if df_combinado is not None and not df_combinado.empty:
        vg.df_piezometros_cg_pe = df_combinado  # Utilizar la variable global
        print(vg.df_piezometros_cg_pe.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Piezómetros CG con PE cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None

def cargar_datos_celdas_asentamiento():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_celdas_asentamiento(archivo)
    if df_combinado is not None and not df_combinado.empty:
        vg.df_celdas_asentamiento = df_combinado  # Utilizar la variable global
        print(vg.df_celdas_asentamiento.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Celdas de Asentamiento cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None

def cargar_datos_extensometros_recinto():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_extensometros_recinto(archivo)
    if df_combinado is not None and not df_combinado.empty:
        vg.df_extensometros_recinto = df_combinado  # Utilizar la variable global
        print(vg.df_extensometros_recinto.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Extensómetros Recinto cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None


