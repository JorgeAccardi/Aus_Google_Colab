# Bibliotecas para Tkinter: Estas bibliotecas permiten crear interfaces gráficas de usuario (GUI) en Python.
import tkinter as tk  # Biblioteca principal para crear ventanas y widgets básicos.
from tkinter import ttk  # Proporciona un conjunto de widgets estilizados que complementan los widgets estándar de Tkinter.
from tkinter import filedialog, messagebox  # Proporciona cuadros de diálogo para abrir/guardar archivos y mostrar mensajes.
from tkinter import simpledialog  # Proporciona cuadros de diálogo simples para entrada de datos por parte del usuario.
from tkinter import Toplevel  # Permite crear nuevas ventanas secundarias dentro de la aplicación principal.
from tkinter import Checkbutton, Button, IntVar  # Proporciona botones de verificación y botones de acción, y gestiona variables enteras.
from tkinter import scrolledtext  # Proporciona un widget de texto con barra de desplazamiento para mostrar grandes cantidades de texto.
from tkinter.filedialog import askopenfilename  # Proporciona un cuadro de diálogo para seleccionar un archivo para abrir.

# Biblioteca para Manipulación de Imágenes: Estas bibliotecas permiten trabajar con imágenes en diferentes formatos.
from PIL import Image, ImageTk  # Permite abrir, manipular y guardar varios formatos de imagen. ImageTk se utiliza para trabajar con imágenes en Tkinter.

# Bibliotecas para Manipulación de Datos: Estas bibliotecas proporcionan herramientas para manipular y analizar datos estructurados.
import pandas as pd  # Proporciona estructuras de datos (DataFrames) y herramientas para el análisis de datos, transformación, limpieza y agregación.
import numpy as np  # Ofrece soporte para arrays de grandes dimensiones y funciones matemáticas, algebraicas y estadísticas.


# Biblioteca del Sistema Operativo: Permite interactuar con el sistema operativo para realizar operaciones del sistema de archivos.
import os  # Proporciona funciones para leer, escribir y navegar por archivos y directorios en el sistema operativo.

# Bibliotecas para Visualización: Estas bibliotecas permiten crear gráficos y visualizaciones para analizar y presentar datos.
import matplotlib.pyplot as plt  # Proporciona una interfaz para crear gráficos 2D, como líneas, barras, dispersión e histogramas.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite incrustar gráficos de matplotlib en una aplicación de Tkinter.
import seaborn as sns  # Ofrece una interfaz basada en matplotlib para crear visualizaciones estadísticas atractivas y complejas, como mapas de calor.
import plotly.express as px  # Proporciona una interfaz simple para crear gráficos interactivos y visualizaciones rápidas.
import plotly.graph_objects as go  # Permite crear gráficos interactivos detallados y personalizados.
from plotly.subplots import make_subplots  # Ofrece herramientas para crear subtramas (subplots) en gráficos, permitiendo visualizaciones más detalladas y complejas.
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator


# Importa el módulo IsolationForest desde el subpaquete ensemble de sklearn
# IsolationForest se utiliza para la detección de anomalías y la estimación de la importancia de características
from sklearn.ensemble import IsolationForest

# Importa el módulo StandardScaler desde el subpaquete preprocessing de sklearn
# StandardScaler se utiliza para estandarizar características eliminando la media y escalando a varianza unitaria
from sklearn.preprocessing import StandardScaler

# Inicialización de variables globales

# Variables para almacenar datos crudos leídos desde diferentes fuentes
datos_gkn_inclinometros = None  # Datos de inclinómetros GKN
datos_excel_inclinometros = None  # Datos de inclinómetros en formato Excel
datos_puntos_fijos = None  # Datos de puntos fijos de referencia
datos_freatimetros = None  # Datos de freatímetros
datos_piezometros_electricos = None  # Datos de piezómetros eléctricos
datos_piezometros_cg_pe = None  # Datos de piezómetros Casagradnde con Sensor Eléctrico
datos_celdas_asentamiento = None  # Datos de celdas de asentamiento
datos_extensometros_recinto = None  # Datos de los extensómetros del recinto

# Variables para almacenar DataFrames procesados a partir de los datos crudos
df_gkn_inclinometros = None  # DataFrame para almacenar los datos de inclinómetros GKN
df_inclinometros = None  # DataFrame para almacenar los datos de inclinómetros Excel
df_puntos_fijos = None  # DataFrame para almacenar los datos de puntos fijos
df_freatimetros_combinado = None  # DataFrame para almacenar los datos combinados de freatímetros
df_piezometros_electricos = None  # DataFrame para almacenar los datos de piezómetros eléctricos
df_piezometros_cg_pe = None  # DataFrame para almacenar los datos de piezómetros CG y PE
df_celdas_asentamiento = None  # DataFrame para almacenar los datos de celdas de asentamiento
df_extensometros_recinto = None  # DataFrame para almacenar los datos de los extensómetros del recinto
# Definir variable global para el DataFrame 
df_puntos_fijos = None

def cargar_y_procesar_gkn_inclinometros():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos GKN")
    if not carpeta:
        messagebox.showerror("Error", "No se seleccionó ninguna carpeta.")
        return None
    return procesar_carpeta_gkn(carpeta)

def procesar_carpeta_gkn(carpeta):
    try:
        if not os.path.exists(carpeta):
            raise FileNotFoundError(f"La carpeta especificada '{carpeta}' no se encuentra.")
        
        archivos = [f for f in os.listdir(carpeta) if f.lower().endswith('.gkn')]
        if not archivos:
            raise ValueError("No se encontraron archivos GKN en la carpeta.")
        
        lista_df = [procesar_gkn_inclinometros(os.path.join(carpeta, archivo)) for archivo in archivos]
        lista_df = [df for df in lista_df if df is not None]
        
        if not lista_df:
            raise ValueError("No se pudo cargar ningún archivo GKN correctamente.")
        
        df_combinado = pd.concat(lista_df, ignore_index=True)
        global df_gkn_inclinometros
        df_gkn_inclinometros = df_combinado
        
        messagebox.showinfo("Éxito", "Datos de GKN Inclinómetros cargados y procesados correctamente.")
        return df_combinado
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Error inesperado: {e}")

def procesar_gkn_inclinometros(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Extraer fecha, número de la sonda (Nro. Sonda) y nombre del inclinómetro (Hole NO.)
            fecha = next((line.split(":")[1].strip() for line in lines if line.startswith("DATE")), None)
            nro_sonda = next((line.split(":")[1].strip() for line in lines if line.startswith("PROBE NO.")), None)
            hole_no = next((line.split(":")[1].strip() for line in lines if line.startswith("HOLE NO.")), None)
            
            # Buscar inicio de lecturas
            start_idx = next((i + 2 for i, line in enumerate(lines) if '#READINGS:' in line), None)
            
            if start_idx is None:
                raise ValueError(f"No se encontraron lecturas en el archivo {file_path}")
            
            data = [line.strip().split(',') for line in lines[start_idx:]]
            df = pd.DataFrame(data, columns=['Profundidad', 'A+', 'A-', 'B+', 'B-'])
            df = df.apply(pd.to_numeric, errors='coerce')

            # Agregar columnas de fecha, número de sonda (Nro. Sonda) y nombre del inclinómetro (Hole NO.)
            df['Fecha'] = pd.to_datetime(fecha, dayfirst=True, errors='coerce').strftime('%d/%m/%Y')
            df['Inclinómetro'] = hole_no
            df['Nro. Sonda'] = nro_sonda
            df = df[['Fecha', 'Inclinómetro', 'Profundidad', 'A+', 'A-', 'B+', 'B-', 'Nro. Sonda']]
            
            return df
    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")
        return None

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
            global df_inclinometros
            df_inclinometros = df
            print(df_inclinometros.head())  # Imprime las primeras filas para verificar
            messagebox.showinfo("Éxito", "Datos del archivo Excel cargados y procesados correctamente.")
            return df
        else:
            messagebox.showerror("Error", "No se pudo procesar el archivo Excel.")
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando el archivo: {e}")
    return None

def procesar_excel_inclinometros(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        hoja = xls.sheet_names[2]  # Seleccionamos la tercera hoja
        df_info = pd.read_excel(xls, hoja, header=None)
        
        nombre_inclinometro = df_info.iloc[3, 1]  # Fila 4, Columna B
        alpha = df_info.iloc[3, 4]  # Fila 4, Columna E
        profundidad_pozo = df_info.iloc[3, 10] + 0.5  # Fila 4, Columna K, sumando 0.5

        tamaño_bloque = int(profundidad_pozo * 2)
        num_filas_totales = df_info.shape[0]
        num_bloques = (num_filas_totales - 94) // (tamaño_bloque + 5)

        dataframes = []
        for i in range(num_bloques):
            fila_inicio = 94 + i * (tamaño_bloque + 4)
            fecha_bloque = pd.to_datetime(df_info.iloc[91 + i * (tamaño_bloque + 4) - 1, 1], dayfirst=True, errors='coerce').strftime('%d/%m/%Y')

            df_bloque = pd.read_excel(xls, hoja, skiprows=fila_inicio-1, nrows=tamaño_bloque, usecols="A:M", header=None)
            df_bloque.columns = ['Point', 'Elevation', 'Depth', 'Cum. A', 'Cum. B', 'Rot. A', 'Rot. B', 'Chk. A', 'Chk. B', 'A0', 'B0', 'Inc. A', 'Inc. B']
            df_bloque['Fecha'] = fecha_bloque
            df_bloque['Inclinometro'] = nombre_inclinometro
            df_bloque['Medición'] = i + 1
            df_bloque['Alpha'] = alpha

            dataframes.append(df_bloque)

        df_final = pd.concat(dataframes, ignore_index=True)
        columnas_ordenadas = ['Fecha', 'Inclinometro', 'Point', 'Elevation', 'Depth', 'Cum. A', 'Cum. B', 'Rot. A', 'Rot. B', 'Chk. A', 'Chk. B', 'A0', 'B0', 'Inc. A', 'Inc. B', 'Alpha', 'Medición']
        df_final = df_final[columnas_ordenadas]

        return df_final
    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")
        return None

def cargar_datos_puntos_fijos():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    return procesar_datos_puntos_fijos(archivo)

def procesar_datos_puntos_fijos(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        hojas_validas = [hoja for hoja in xls.sheet_names[3:] if 'HOJA' not in hoja and 'Graficas' not in hoja and 'GRAFICAS' not in hoja]
        
        lista_df = []
        for nombre_hoja in hojas_validas:
            df = pd.read_excel(xls, sheet_name=nombre_hoja, header=1).iloc[:, 1:12]  # Leer y seleccionar las columnas
            if df.shape[1] != 11:
                print(f"Error: La hoja {nombre_hoja} no tiene 11 columnas.")
                continue
            
            df.columns = [
                'Fecha', 'Delta Norte [m]', 'Delta Este [m]', 'Delta cota [m]',
                'Distancia [m]', 'Distancia (mm)', 'Azimut ref. al Norte',
                'Tasa Norte (mm/día)', 'Tasa Este (mm/día)', 'Tasa Cota (mm/día)',
                'Tasa Distancia (mm/día)'
            ]
            df['Instrumento'] = nombre_hoja
            df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
            cols_numericas = df.columns.drop(['Fecha', 'Instrumento'])
            df[cols_numericas] = df[cols_numericas].apply(pd.to_numeric, errors='coerce')
            df.dropna(subset=['Fecha'], inplace=True)  # Eliminar filas con fechas no válidas
            df = df[(df[cols_numericas] != 0).any(axis=1)]  # Eliminar filas con todas columnas numéricas con 0 o NaN
            
            # Agregar la columna 'Margen'
            df['Margen'] = 'Izquierda' if 'MI' in file_path else 'Derecha' if 'MD' in file_path else 'Desconocido'
            
            # Reordenar columnas para que 'Margen' sea la segunda columna
            columnas_reordenadas = ['Fecha', 'Margen', 'Instrumento'] + cols_numericas.tolist()
            df = df[columnas_reordenadas]

            lista_df.append(df)

        if lista_df:
            df_combinado = pd.concat(lista_df, ignore_index=True)
            global df_puntos_fijos
            df_puntos_fijos = df_combinado
            messagebox.showinfo("Éxito", "Datos de Puntos Fijos cargados y procesados correctamente.")
            print(df_combinado.head())
            return df_combinado
        else:
            print("No se encontraron hojas válidas con datos suficientes.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")
        messagebox.showerror("Error", f"Error procesando el archivo: {e}")
        return None

# Definir el nombre del freatímetro de forma global
nombre_freatimetro = "Freatímetro X"

def cargar_datos_freatimetros():
    global df_freatimetros_combinado, nombre_freatimetro
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_freatimetros(archivo)
    if df_combinado is not None and not df_combinado.empty:
        df_freatimetros_combinado = df_combinado
        # Actualizar el nombre del freatímetro basado en los datos cargados
        nombre_freatimetro = df_combinado['Freatimetro'].unique()[0]  # Suponiendo que hay una columna 'Freatimetro'
        messagebox.showinfo("Éxito", "Datos de Freatímetros cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se pudo procesar el archivo Excel.")
        return None

def procesar_datos_freatimetros(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        hojas = [hoja for hoja in xls.sheet_names if hoja.lower().startswith('fr')]
        lista_df = []
        
        for hoja in hojas:
            try:
                print(f"Procesando hoja: {hoja}")
                df = pd.read_excel(file_path, sheet_name=hoja, skiprows=14, usecols="B:G")
                df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
                df = limpiar_datos(df)
                df.insert(1, 'Freatimetro', hoja)
                lista_df.append(df)
            except Exception as e:
                print(f"Error al procesar la hoja {hoja}: {e}")
        
        if lista_df:
            return pd.concat(lista_df, ignore_index=True)
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None

def limpiar_datos(df):
    df = df.dropna(subset=['FECHA'])
    df.columns = [col.strip().upper().replace(" ", "_").translate(str.maketrans("ÁÉÍÓÚÑ", "AEIOUN")) for col in df.columns]
    return df

def cargar_datos_piezometros_electricos():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_piezometros_electricos(archivo)
    if df_combinado is not None and not df_combinado.empty:
        global df_piezometros_electricos
        df_piezometros_electricos = df_combinado
        print(df_piezometros_electricos.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Piezómetros Eléctricos cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None
        
def procesar_datos_piezometros_electricos(file_path):
    try:
        hojas = pd.read_excel(file_path, sheet_name=None, skiprows=14, usecols="B:I")
        lista_df = []
        for nombre_hoja, df in hojas.items():
            print(f"Procesando hoja: {nombre_hoja}")
            try:
                if df.isnull().values.all():
                    print(f"Hoja {nombre_hoja} contiene solo NaN y será ignorada.")
                    continue
                
                # Leer el valor de Progresiva de la celda H9 como texto
                progresiva = pd.read_excel(file_path, sheet_name=nombre_hoja, skiprows=7, usecols="H", nrows=1).astype(str).iloc[0, 0]

                if 'FECHA' in df.columns:
                    print(f"Hoja válida: {nombre_hoja}")
                    df.columns = ['FECHA', 'COTA RIO (m.s.n.m)', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)',
                                  'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'COTA NF', 'PRECIPITACIONES (mm)']
                    print(f"Columnas después de aplicar encabezados:\n{df.columns}")
                    print(f"Primeras filas después de aplicar encabezados:\n{df.head(20)}")

                    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
                    df = df.dropna(subset=['FECHA'])
                    df = df.dropna(how='all')
                    df[['COTA RIO (m.s.n.m)', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)',
                        'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'PRECIPITACIONES (mm)']] = df[
                        ['COTA RIO (m.s.n.m)', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)',
                         'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'PRECIPITACIONES (mm)']].apply(pd.to_numeric, errors='coerce')
                    df['Piezómetro'] = nombre_hoja
                    df.insert(1, 'Progresiva', progresiva)  # Insertar 'Progresiva' en la segunda columna como texto
                    df = df[['FECHA', 'Progresiva', 'Piezómetro', 'COTA RIO (m.s.n.m)', 'LECTURA CUERDA VIBRANTE',
                             'TEMPERATURA (°C)', 'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'COTA NF', 'PRECIPITACIONES (mm)']]
                    lista_df.append(df)
                else:
                    print(f"Hoja {nombre_hoja} no contiene la columna 'FECHA'.")
            except Exception as e:
                print(f"Error procesando la hoja {nombre_hoja}: {e}")

        if lista_df:
            df_combinado = pd.concat(lista_df, ignore_index=True)
            print(f"Datos combinados:\n{df_combinado.head(20)}")
            return df_combinado
        else:
            print("No se encontraron datos válidos en el archivo.")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None

def cargar_datos_piezometros_cg_pe():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_piezometros_cg_pe(archivo)
    if df_combinado is not None and not df_combinado.empty:
        global df_piezometros_cg_pe
        df_piezometros_cg_pe = df_combinado
        print(df_piezometros_cg_pe.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Piezómetros CG con PE cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None

def procesar_datos_piezometros_cg_pe(file_path):
    try:
        hojas = pd.read_excel(file_path, sheet_name=None, skiprows=14, usecols="B:H")  # Ajustar para 7 columnas de datos
        lista_df = []
        for nombre_hoja, df in hojas.items():
            print(f"Procesando hoja: {nombre_hoja}")

            if df.isnull().values.all():
                print(f"Hoja {nombre_hoja} contiene solo NaN y será ignorada.")
                continue

            print(f"Contenido de la hoja:\n{df.head(20)}")
            try:
                margen = pd.read_excel(file_path, sheet_name=nombre_hoja, skiprows=7, usecols="H", nrows=1).astype(str).iloc[0, 0]
                
                if 'FECHA' in df.columns:
                    print(f"Hoja válida: {nombre_hoja}")

                    df.columns = ['FECHA', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)', 
                                  'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'COTA NF', 'PRECIPITACIONES (mm)']
                    print(f"Columnas después de aplicar encabezados:\n{df.columns}")
                    print(f"Primeras filas después de aplicar encabezados:\n{df.head(20)}")

                    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
                    df = df.dropna(subset=['FECHA'])
                    df = df.dropna(how='all')
                    df[['LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)', 
                        'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'PRECIPITACIONES (mm)']] = df[
                        ['LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)', 
                         'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'PRECIPITACIONES (mm)']].apply(pd.to_numeric, errors='coerce')
                    df['Piezómetro'] = nombre_hoja
                    df.insert(1, 'Margen', margen)
                    df = df[['FECHA', 'Margen', 'Piezómetro', 'LECTURA CUERDA VIBRANTE',
                             'TEMPERATURA (°C)', 'MCA 1 (Factor G)', 'MCA 2 (Factor G y K)', 'COTA NF', 'PRECIPITACIONES (mm)']]
                    lista_df.append(df)
                else:
                    print(f"Hoja {nombre_hoja} será ignorada por no contener datos relevantes.")
            except Exception as e:
                print(f"Error procesando la hoja {nombre_hoja}: {e}")

        if lista_df:
            df_combinado = pd.concat(lista_df, ignore_index=True)
            print(f"Datos combinados:\n{df_combinado.head(20)}")
            return df_combinado
        else:
            print("No se encontraron datos válidos en el archivo.")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None

def cargar_datos_celdas_asentamiento():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_celdas_asentamiento(archivo)
    if df_combinado is not None and not df_combinado.empty:
        global df_celdas_asentamiento
        df_celdas_asentamiento = df_combinado
        print(df_celdas_asentamiento.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Celdas de Asentamiento cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None

def procesar_datos_celdas_asentamiento(file_path):
    try:
        hojas = pd.read_excel(file_path, sheet_name=None, header=14, usecols="B:J")  # Nombres de columnas en la fila 15
        lista_df = []

        for nombre_hoja, df in hojas.items():
            print(f"Procesando hoja: {nombre_hoja}")

            if df.isnull().values.all():
                print(f"Hoja {nombre_hoja} contiene solo NaN y será ignorada.")
                continue

            print(f"Contenido de la hoja:\n{df.head(20)}")
            try:
                progresiva = pd.read_excel(file_path, sheet_name=nombre_hoja, skiprows=7, usecols="H", nrows=1).iloc[0, 0]

                if 'FECHA' in df.columns:
                    print(f"Hoja válida: {nombre_hoja}")

                    df.columns = ['FECHA', 'PUNTO FIJO CASETA', 'COTA RIO (m.s.n.m)', 'LECTURA REGLETA (m)',
                                  'COTA "0" REGLETA (m)', 'COTA CELDA (m.s.n.m)', 'ASENTAMIENTO (cm)',
                                  'COTA RELLENO', 'MODULO DEFORMACION (ε)']
                    print(f"Columnas después de aplicar encabezados:\n{df.columns}")
                    print(f"Primeras filas después de aplicar encabezados:\n{df.head(20)}")

                    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce')
                    df = df.dropna(subset=['FECHA']).dropna(how='all')

                    columnas_numericas = ['PUNTO FIJO CASETA', 'COTA RIO (m.s.n.m)', 'LECTURA REGLETA (m)',
                                          'COTA "0" REGLETA (m)', 'COTA CELDA (m.s.n.m)', 'ASENTAMIENTO (cm)',
                                          'COTA RELLENO', 'MODULO DEFORMACION (ε)']
                    df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')
                    df['Celda de Asentamiento'] = nombre_hoja
                    df.insert(1, 'Progresiva', progresiva)
                    lista_df.append(df)
                else:
                    print(f"Hoja {nombre_hoja} será ignorada por no contener datos relevantes.")
            except Exception as e:
                print(f"Error procesando la hoja {nombre_hoja}: {e}")

        if lista_df:
            df_combinado = pd.concat(lista_df, ignore_index=True)
            print(f"Datos combinados:\n{df_combinado.head(20)}")
            return df_combinado
        else:
            print("No se encontraron datos válidos en el archivo.")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None

def cargar_datos_extensometros_recinto():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
    if not archivo:
        messagebox.showerror("Error", "No se seleccionó ningún archivo.")
        return None
    
    df_combinado = procesar_datos_extensometros_recinto(archivo)
    if df_combinado is not None and not df_combinado.empty:
        global df_extensometros_recinto
        df_extensometros_recinto = df_combinado
        print(df_extensometros_recinto.head())  # Imprime las primeras filas para verificar
        messagebox.showinfo("Éxito", "Datos de Extensómetros Recinto cargados y procesados correctamente.")
        return df_combinado
    else:
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        print("No se han cargado datos o los datos están vacíos.")
        return None
    
def procesar_datos_extensometros_recinto(file_path):
    try:
        hojas = pd.read_excel(file_path, sheet_name=None, skiprows=6, usecols="B:H")
        lista_df = []

        for nombre_hoja, df in hojas.items():
            if df.isnull().values.all():
                print(f"Hoja {nombre_hoja} contiene solo NaN y será ignorada.")
                continue

            if 'FECHA' in df.columns:
                df.columns = ['FECHA', 'COTA EXCAV. (msnm)', 'PROFUNDIDAD', 'Z/COTA RELEV.', 
                              'DIFERENCIAS (mm)', 'ACUMULADO (mm)', 'COTA FINAL EXCAV. (msnm)']
                
                df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
                df = df.dropna(subset=['FECHA']).dropna(how='all')

                numeric_cols = ['COTA EXCAV. (msnm)', 'PROFUNDIDAD', 'Z/COTA RELEV.', 
                                'DIFERENCIAS (mm)', 'ACUMULADO (mm)', 'COTA FINAL EXCAV. (msnm)']
                df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
                df['Extensómetro'] = nombre_hoja
                df = df[['FECHA', 'Extensómetro', 'COTA EXCAV. (msnm)', 'PROFUNDIDAD', 'Z/COTA RELEV.', 
                         'DIFERENCIAS (mm)', 'ACUMULADO (mm)', 'COTA FINAL EXCAV. (msnm)']]
                
                lista_df.append(df)
            else:
                print(f"Hoja {nombre_hoja} no contiene la columna 'FECHA' y será ignorada.")

        if lista_df:
            df_combinado = pd.concat(lista_df, ignore_index=True)
            print(f"Datos combinados:\n{df_combinado.head(20)}")
            return df_combinado
        else:
            print("No se encontraron datos válidos en el archivo.")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None

# Funciones para mostrar los datos
def mostrar_datos(df, titulo):
    if df is not None and not df.empty:
        print(f"Mostrando datos para {titulo}: \n{df.head()}")

        ventana_datos = tk.Toplevel(root)
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
    global df_gkn_inclinometros
    if df_gkn_inclinometros is not None and not df_gkn_inclinometros.empty:
        mostrar_datos(df_gkn_inclinometros, "Datos GKN Inclinómetros")
    
def mostrar_datos_excel_inclinometros():
    global df_inclinometros
    if df_inclinometros is not None and not df_inclinometros.empty:
        mostrar_datos(df_inclinometros, "Datos Inclinómetros")


def mostrar_datos_puntos_fijos():
    global df_puntos_fijos
    if df_puntos_fijos is not None and not df_puntos_fijos.empty:
        mostrar_datos(df_puntos_fijos, "Datos Puntos Fijos")


def mostrar_datos_freatimetros():
    global df_freatimetros_combinado
    if df_freatimetros_combinado is not None and not df_freatimetros_combinado.empty:
        mostrar_datos(df_freatimetros_combinado, "Datos Freatímetros Combinados")

def mostrar_datos_piezometros_electricos():
    global df_piezometros_electricos
    if df_piezometros_electricos is not None and not df_piezometros_electricos.empty:
        mostrar_datos(df_piezometros_electricos, "Datos Piezómetros Eléctricos")

def mostrar_datos_piezometros_cg_pe():
    global df_piezometros_cg_pe
    if df_piezometros_cg_pe is not None and not df_piezometros_cg_pe.empty:
        mostrar_datos(df_piezometros_cg_pe, "Datos Piezómetros CG con PE")

def mostrar_datos_celdas_asentamiento():
    global df_celdas_asentamiento
    if df_celdas_asentamiento is not None and not df_celdas_asentamiento.empty:
        mostrar_datos(df_celdas_asentamiento, "Datos Celdas de Asentamiento")

def mostrar_datos_extensometros_recinto():
    global df_extensometros_recinto
    if df_extensometros_recinto is not None and not df_extensometros_recinto.empty:
        mostrar_datos(df_extensometros_recinto, "Datos Extensómetros Recinto")

# Funciones para mostrar los datos
def mostrar_seleccion_piezometros():
    global df_piezometros_electricos
    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    # Crear una nueva ventana para la selección de piezómetros
    top = Toplevel()
    top.title("Seleccionar Piezómetros")

    # Variables para mantener el estado de los checkbuttons
    seleccion = {}
    for piezometro in df_piezometros_electricos['Piezómetro'].unique():
        seleccion[piezometro] = IntVar()
    
    # Variable para seleccionar todos
    seleccion_todos = IntVar()

    def seleccionar_todos():
        estado = seleccion_todos.get()
        for var in seleccion.values():
            var.set(estado)

    # Crear checkbuttons para cada piezómetro
    row = 0
    for piezometro, var in seleccion.items():
        Checkbutton(top, text=piezometro, variable=var).grid(row=row, sticky='w')
        row += 1

    # Crear un checkbutton para seleccionar todos
    Checkbutton(top, text="Todos", variable=seleccion_todos, command=seleccionar_todos).grid(row=row, sticky='w')
    
    # Botón para confirmar la selección
    Button(top, text="Graficar", command=lambda: graficar_seleccion_piezometros(seleccion, seleccion_todos.get())).grid(row=row+1, pady=10)

#### `graficar_seleccion_piezometros`

def graficar_seleccion_piezometros(seleccion, todos):
    global df_piezometros_electricos
    piezometros_seleccionados = [piezometro for piezometro, var in seleccion.items() if var.get() == 1]

    if todos:
        datos = df_piezometros_electricos
    elif not piezometros_seleccionados:
        print("No se seleccionaron piezómetros.")
        messagebox.showerror("Error", "No se seleccionaron piezómetros.")
        return
    else:
        datos = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'].isin(piezometros_seleccionados)]

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

#Esta es la funcion plotly basica (no se esta usando sino la mejorada)
def graficar_lineas_cota_nivel_freatico_plotly():
    global df_piezometros_electricos
    
    # Graficar los datos
    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'COTA NF' in df_piezometros_electricos.columns:
        # Asegurarnos de que la columna FECHA sea de tipo datetime
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        
        # Filtrar filas con fechas inválidas y datos nulos
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA NF'])
        
        # Filtrar valores no convertibles a float en 'COTA NF'
        df_piezometros_electricos = df_piezometros_electricos[df_piezometros_electricos['COTA NF'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]

        # Convertir la columna 'COTA NF' a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].astype(float)

        # Crear la gráfica interactiva con Plotly
        fig = px.line(df_piezometros_electricos, x='FECHA', y='COTA NF', title='Cota Nivel Freático en Función del Tiempo - Plotly',
                      labels={'FECHA': 'Fecha', 'COTA NF': 'Cota Nivel Freático'}, color='Piezómetro')
        
        # Mostrar la gráfica
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")


#Esta es la funcion plotly que se está usando
def graficar_interactivo_plotly_mejorado():
    global df_piezometros_electricos
    
    # Graficar los datos
    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'COTA NF' in df_piezometros_electricos.columns:
        # Asegurarnos de que la columna FECHA sea de tipo datetime
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        
        # Filtrar filas con fechas inválidas y datos nulos
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA NF'])
        
        # Filtrar valores no convertibles a float en 'COTA NF'
        df_piezometros_electricos = df_piezometros_electricos[df_piezometros_electricos['COTA NF'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]

        # Convertir la columna 'COTA NF' a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].astype(float)

        # Crear la gráfica interactiva con Plotly
        fig = px.line(df_piezometros_electricos, x='FECHA', y='COTA NF', title='Cota Nivel Freático en Función del Tiempo - Plotly Mejorado',
                      labels={'FECHA': 'Fecha', 'COTA NF': 'Cota Nivel Freático'}, color='Piezómetro')

        # Ajustes visuales
        fig.update_layout(
            template='plotly_white',
            xaxis=dict(
                tickformat='%d-%m-%Y',
                title_font=dict(size=18),
                tickfont=dict(size=14)
            ),
            yaxis=dict(
                title_font=dict(size=18),
                tickfont=dict(size=14)
            ),
            legend=dict(
                title_text='Piezómetros',
                title_font=dict(size=16),
                font=dict(size=14)
            )
        )

        # Añadir barras de error basadas en la desviación estándar
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            piezometro_datos = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            error_y = piezometro_datos['COTA NF'].std() / np.sqrt(len(piezometro_datos))
            fig.add_trace(go.Scatter(
                x=piezometro_datos['FECHA'], y=piezometro_datos['COTA NF'],
                mode='markers+lines',
                name=piezometro,
                error_y=dict(
                    type='data', array=[error_y] * len(piezometro_datos),
                    visible=True
                )
            ))

        # Mostrar la gráfica
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_lineas_cota_nivel_freatico_seaborn():
    global df_piezometros_electricos
    
    # Graficar los datos
    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'COTA NF' in df_piezometros_electricos.columns:
        # Asegurarnos de que la columna FECHA sea de tipo datetime
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        
        # Filtrar filas con fechas inválidas y datos nulos
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA NF'])
        
        # Filtrar valores no convertibles a float en 'COTA NF'
        df_piezometros_electricos = df_piezometros_electricos[df_piezometros_electricos['COTA NF'].apply(lambda x: str(x).replace('.', '', 1).isdigit())]

        # Convertir la columna 'COTA NF' a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].astype(float)

        # Crear la gráfica con Seaborn
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='COTA NF', hue='Piezómetro', marker='o')
        plt.title('Cota Nivel Freático en Función del Tiempo - Seaborn')
        plt.xlabel('Fecha')
        plt.ylabel('Cota Nivel Freático')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Mostrar la gráfica
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_mca2_tiempo_matplotlib():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.plot(datos_piezometro['FECHA'], datos_piezometro['MCA 2 (Factor G y K)'], marker='o', label=piezometro)

        plt.title('Metros Columna de Agua (MCA 2) en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('MCA 2 (m)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_mca2_tiempo_seaborn():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='MCA 2 (Factor G y K)', hue='Piezómetro', marker='o')
        plt.title('Metros Columna de Agua (MCA 2) en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('MCA 2 (m)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_mca2_tiempo_plotly():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        fig = px.line(df_piezometros_electricos, x='FECHA', y='MCA 2 (Factor G y K)', title='Metros Columna de Agua (MCA 2) en Función del Tiempo',
                      labels={'FECHA': 'Fecha', 'MCA 2 (Factor G y K)': 'MCA 2 (m)'}, color='Piezómetro')
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_area_mca2():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.fill_between(datos_piezometro['FECHA'], datos_piezometro['MCA 2 (Factor G y K)'], alpha=0.5, label=piezometro)

        plt.title('Metros Columna de Agua (MCA 2) en Función del Tiempo - Área')
        plt.xlabel('Fecha')
        plt.ylabel('MCA 2 (m)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_suavizadas_mca2():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        df_piezometros_electricos['MCA 2 Suavizada'] = df_piezometros_electricos.groupby('Piezómetro')['MCA 2 (Factor G y K)'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.plot(datos_piezometro['FECHA'], datos_piezometro['MCA 2 Suavizada'], marker='o', label=piezometro)

        plt.title('Metros Columna de Agua (MCA 2) en Función del Tiempo - Suavizado')
        plt.xlabel('Fecha')
        plt.ylabel('MCA 2 (m)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_anotaciones_mca2():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'MCA 2 (Factor G y K)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df_piezometros_electricos['MCA 2 (Factor G y K)'] = df_piezometros_electricos['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.plot(datos_piezometro['FECHA'], datos_piezometro['MCA 2 (Factor G y K)'], marker='o', label=piezometro)
            for _, row in datos_piezometro.iterrows():
                if row['MCA 2 (Factor G y K)'] > 20:  # Ejemplo de condición para anotación
                    plt.annotate(f"{row['MCA 2 (Factor G y K)']}", (row['FECHA'], row['MCA 2 (Factor G y K)']))

        plt.title('Metros Columna de Agua (MCA 2) en Función del Tiempo - Anotaciones')
        plt.xlabel('Fecha')
        plt.ylabel('MCA 2 (m)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_cuerda_temperatura_matplotlib():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            ax1.plot(datos_piezometro['FECHA'], datos_piezometro['LECTURA CUERDA VIBRANTE'], marker='o', label=f'Lectura Cuerda {piezometro}')

        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Lectura Cuerda Vibrante', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            ax2.plot(datos_piezometro['FECHA'], datos_piezometro['TEMPERATURA (°C)'], marker='x', linestyle='--', label=f'Temperatura {piezometro}', color='tab:red')

        ax2.set_ylabel('Temperatura (°C)', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        plt.title('Lectura de Cuerda Vibrante y Temperatura en Función del Tiempo')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_cuerda_temperatura_seaborn():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='LECTURA CUERDA VIBRANTE', hue='Piezómetro', marker='o', ax=ax1)
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Lectura Cuerda Vibrante', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='TEMPERATURA (°C)', hue='Piezómetro', marker='x', linestyle='--', ax=ax2)
        ax2.set_ylabel('Temperatura (°C)', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        plt.title('Lectura de Cuerda Vibrante y Temperatura en Función del Tiempo')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_cuerda_temperatura_plotly():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        fig = go.Figure()

        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            fig.add_trace(go.Scatter(
                x=datos_piezometro['FECHA'], 
                y=datos_piezometro['LECTURA CUERDA VIBRANTE'],
                mode='lines+markers', 
                name=f'Lectura Cuerda {piezometro}'
            ))

        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            fig.add_trace(go.Scatter(
                x=datos_piezometro['FECHA'], 
                y=datos_piezometro['TEMPERATURA (°C)'],
                mode='lines+markers', 
                name=f'Temperatura {piezometro}', 
                yaxis="y2"
            ))

        fig.update_layout(
            title='Lectura de Cuerda Vibrante y Temperatura en Función del Tiempo',
            xaxis=dict(title='Fecha'),
            yaxis=dict(title='Lectura Cuerda Vibrante', titlefont=dict(color='blue'), tickfont=dict(color='blue')),
            yaxis2=dict(
                title='Temperatura (°C)',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',
                side='right'
            ),
            legend=dict(x=0.01, y=0.99)
        )

        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_linea_cuerda_vibrante_matplotlib():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns:

        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.plot(datos_piezometro['FECHA'], datos_piezometro['LECTURA CUERDA VIBRANTE'], marker='o', label=piezometro)

        plt.title('Lectura de Cuerda Vibrante en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Lectura Cuerda Vibrante')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_linea_cuerda_vibrante_seaborn():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='LECTURA CUERDA VIBRANTE', hue='Piezómetro', marker='o')
        plt.title('Lectura de Cuerda Vibrante en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Lectura Cuerda Vibrante')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_linea_cuerda_vibrante_plotly():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'LECTURA CUERDA VIBRANTE' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE'])
        df_piezometros_electricos['LECTURA CUERDA VIBRANTE'] = df_piezometros_electricos['LECTURA CUERDA VIBRANTE'].astype(float)

        fig = px.line(df_piezometros_electricos, x='FECHA', y='LECTURA CUERDA VIBRANTE', title='Lectura de Cuerda Vibrante en Función del Tiempo',
                      labels={'FECHA': 'Fecha', 'LECTURA CUERDA VIBRANTE': 'Lectura Cuerda Vibrante'}, color='Piezómetro')
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_lineas_temperatura_matplotlib():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df_piezometros_electricos['Piezómetro'].unique():
            datos_piezometro = df_piezometros_electricos[df_piezometros_electricos['Piezómetro'] == piezometro]
            plt.plot(datos_piezometro['FECHA'], datos_piezometro['TEMPERATURA (°C)'], marker='o', label=piezometro)

        plt.title('Temperatura en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Temperatura (°C)')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_lineas_temperatura_seaborn():
    global df_piezometros_electricos

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='TEMPERATURA (°C)', hue='Piezómetro', marker='o')
        plt.title('Temperatura en Función del Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_lineas_temperatura_plotly():
    global df_piezometros_electricos

    print(df_piezometros_electricos.columns)

    if df_piezometros_electricos is None or df_piezometros_electricos.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df_piezometros_electricos.columns and 'TEMPERATURA (°C)' in df_piezometros_electricos.columns:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)'])
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)

        fig = px.line(df_piezometros_electricos, x='FECHA', y='TEMPERATURA (°C)', title='Temperatura en Función del Tiempo',
                      labels={'FECHA': 'Fecha', 'TEMPERATURA (°C)': 'Temperatura (°C)'}, color='Piezómetro')
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def verificar_columnas_necesarias(columnas_necesarias, df):
    columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
    if columnas_faltantes:
        return False, columnas_faltantes
    return True, None

def graficar_nivel_freatico_rio_matplotlib():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF'])
        
        # Convertir la columna a cadenas y luego reemplazar las comas por puntos decimales
        df_piezometros_electricos['COTA RIO (m.s.n.m)'] = df_piezometros_electricos['COTA RIO (m.s.n.m)'].astype(str).str.replace(',', '.').astype(float)
        
        # Reemplazar los valores 'SIN NF' con NaN para poder convertir la columna a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].replace('SIN NF', np.nan).astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.plot(df_piezometros_electricos['FECHA'], df_piezometros_electricos['COTA NF'], marker='o', color='tab:blue', label='Cota NF')
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Cota NF', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.plot(df_piezometros_electricos['FECHA'], df_piezometros_electricos['COTA RIO (m.s.n.m)'], marker='x', linestyle='--', color='tab:red', label='Cota Río')
        ax2.set_ylabel('Cota Río', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()
        fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        plt.title('Cota NF y Cota Río en Función de la Fecha')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_nivel_freatico_rio_seaborn():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF'])
        
        # Convertir la columna a cadenas y luego reemplazar las comas por puntos decimales
        df_piezometros_electricos['COTA RIO (m.s.n.m)'] = df_piezometros_electricos['COTA RIO (m.s.n.m)'].astype(str).str.replace(',', '.').astype(float)
        
        # Reemplazar los valores 'SIN NF' con NaN para poder convertir la columna a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].replace('SIN NF', np.nan).astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='COTA NF', ax=ax1, color='tab:blue', marker='o', label='Cota NF')
        ax1.set_ylabel('Cota NF', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='COTA RIO (m.s.n.m)', ax=ax2, color='tab:red', marker='x', linestyle='--', label='Cota Río')
        ax2.set_ylabel('Cota Río', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        fig.tight_layout()
        plt.title('Cota NF y Cota Río en Función de la Fecha')
        ax1.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
        ax2.legend(loc='upper right', bbox_to_anchor=(0.9, 0.9))
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_nivel_freatico_rio_plotly():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF'])
        
        # Reemplazar las comas por puntos decimales y convertir a float
        df_piezometros_electricos['COTA RIO (m.s.n.m)'] = df_piezometros_electricos['COTA RIO (m.s.n.m)'].apply(lambda x: float(str(x).replace(',', '.')) if isinstance(x, str) else x)
        
        # Reemplazar los valores 'SIN NF' con NaN para poder convertir la columna a float
        df_piezometros_electricos['COTA NF'] = df_piezometros_electricos['COTA NF'].replace('SIN NF', np.nan)
        df_piezometros_electricos['COTA NF'] = pd.to_numeric(df_piezometros_electricos['COTA NF'], errors='coerce')

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df_piezometros_electricos['FECHA'], y=df_piezometros_electricos['COTA NF'],
                                 mode='lines+markers', name='Cota NF', line=dict(color='blue')))
        
        fig.add_trace(go.Scatter(x=df_piezometros_electricos['FECHA'], y=df_piezometros_electricos['COTA RIO (m.s.n.m)'],
                                 mode='lines+markers', name='Cota Río', line=dict(color='red', dash='dash')))

        fig.update_layout(
            title='Cota NF y Cota Río en Función de la Fecha',
            xaxis_title='Fecha',
            yaxis_title='Cota NF',
            yaxis=dict(
                title='Cota NF',
                titlefont=dict(
                    color='blue'
                ),
                tickfont=dict(
                    color='blue'
                )
            ),
            yaxis2=dict(
                title='Cota Río',
                titlefont=dict(
                    color='red'
                ),
                tickfont=dict(
                    color='red'
                ),
                anchor='free',
                overlaying='y',
                side='right',
                position=1
            ),
            legend=dict(x=0.1, y=1.1),
            xaxis=dict(tickformat='%d/%m/%Y'),
            margin=dict(l=40, r=40, t=40, b=40),
            template='plotly_white'
        )

        fig.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_precip_temperatura_matplotlib():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)'])
        
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)
        df_piezometros_electricos['PRECIPITACIONES (mm)'] = df_piezometros_electricos['PRECIPITACIONES (mm)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.plot(df_piezometros_electricos['FECHA'], df_piezometros_electricos['PRECIPITACIONES (mm)'], marker='o', color='blue', label='Precipitaciones (mm)')
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Precipitaciones (mm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(df_piezometros_electricos['FECHA'], df_piezometros_electricos['TEMPERATURA (°C)'], marker='x', linestyle='--', color='red', label='Temperatura (°C)')
        ax2.set_ylabel('Temperatura (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        fig.tight_layout()
        fig.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        plt.title('Precipitaciones y Temperatura en Función del Tiempo')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_precip_temperatura_seaborn():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)'])
        
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)
        df_piezometros_electricos['PRECIPITACIONES (mm)'] = df_piezometros_electricos['PRECIPITACIONES (mm)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='PRECIPITACIONES (mm)', ax=ax1, color='blue', marker='o', label='Precipitaciones (mm)')
        ax1.set_ylabel('Precipitaciones (mm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        sns.lineplot(data=df_piezometros_electricos, x='FECHA', y='TEMPERATURA (°C)', ax=ax2, color='red', marker='x', linestyle='--', label='Temperatura (°C)')
        ax2.set_ylabel('Temperatura (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        fig.tight_layout()
        plt.title('Precipitaciones y Temperatura en Función del Tiempo')
        ax1.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        ax2.legend(loc='upper right', bbox_to_anchor=(1.25, 1), borderaxespad=0.)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_precip_temperatura_plotly():
    global df_piezometros_electricos

    print("Verificando datos...")

    if df_piezometros_electricos is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df_piezometros_electricos.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df_piezometros_electricos.columns)

    columnas_necesarias = ['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df_piezometros_electricos)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df_piezometros_electricos['FECHA'] = pd.to_datetime(df_piezometros_electricos['FECHA'], format='%d/%m/%Y', errors='coerce')
        df_piezometros_electricos = df_piezometros_electricos.dropna(subset=['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)'])
        
        df_piezometros_electricos['TEMPERATURA (°C)'] = df_piezometros_electricos['TEMPERATURA (°C)'].astype(float)
        df_piezometros_electricos['PRECIPITACIONES (mm)'] = df_piezometros_electricos['PRECIPITACIONES (mm)'].astype(float)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df_piezometros_electricos['FECHA'], y=df_piezometros_electricos['PRECIPITACIONES (mm)'],
                                 mode='lines+markers', name='Precipitaciones (mm)', line=dict(color='blue')))
        
        fig.add_trace(go.Scatter(x=df_piezometros_electricos['FECHA'], y=df_piezometros_electricos['TEMPERATURA (°C)'],
                                 mode='lines+markers', name='Temperatura (°C)', line=dict(color='red', dash='dash')))

        fig.update_layout(
            title='Precipitaciones y Temperatura en Función del Tiempo',
            xaxis_title='Fecha',
            yaxis_title='Precipitaciones (mm)',
            yaxis=dict(
                title='Precipitaciones (mm)',
                titlefont=dict(
                    color='blue'
                ),
                tickfont=dict(
                    color='blue'
                )
            ),
            yaxis2=dict(
                title='Temperatura (°C)',
                titlefont=dict(
                    color='red'
                ),
                tickfont=dict(
                    color='red'
                ),
                anchor='free',
                overlaying='y',
                side='right',
                position=1
            ),
            legend=dict(
                x=1.1, 
                y=1,
                traceorder='normal',
                orientation="v"
            ),
            xaxis=dict(tickformat='%d/%m/%Y'),
            margin=dict(l=40, r=40, t=40, b=40),
            template='plotly_white'
        )

        fig.show()
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
        messagebox.showerror("Error", f"Error al procesar los datos: {e}")

def graficar_inclinometros_matplotlib(df_inclinometros):
    # Obtener el nombre del inclinómetro
    nombre_inclinometro = df_inclinometros['Inclinometro'].iloc[0]

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # Generar una paleta de colores amplia y variada
    num_colors = df_inclinometros['Medición'].nunique()
    colores = plt.cm.get_cmap('tab20c', num_colors)  # Usar una paleta más amplia

    for i, (name, group) in enumerate(df_inclinometros.groupby('Medición')):
        color = colores(i)
        fecha = group['Fecha'].iloc[0]  # Obtener la fecha del grupo de datos

        # Graficar Elevation vs Cum. A
        axes[0, 0].plot(group['Cum. A'], group['Elevation'], color=color, linewidth=2, label=fecha)
        axes[0, 0].set_xlabel('Acumulado A (mm)', fontweight='bold', fontsize=7)
        axes[0, 0].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[0, 0].grid(True)
        axes[0, 0].legend(fontsize='small', loc='best')
        axes[0, 0].tick_params(axis='both', which='major', labelsize=6)
        axes[0, 0].set_facecolor('#f5e6d3')  # Fondo marrón super claro

        # Graficar Elevation vs Cum. B
        axes[0, 1].plot(group['Cum. B'], group['Elevation'], color=color, linewidth=2)
        axes[0, 1].set_xlabel('Acumulado B (mm)', fontweight='bold', fontsize=7)
        axes[0, 1].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[0, 1].grid(True)
        axes[0, 1].tick_params(axis='both', which='major', labelsize=6)
        axes[0, 1].set_facecolor('#f5e6d3')  # Fondo marrón super claro

        # Graficar Elevation vs Rot. A
        axes[1, 0].plot(group['Rot. A'], group['Elevation'], color=color, linewidth=2)
        axes[1, 0].set_xlabel("Rotación A (mm)", fontweight='bold', fontsize=7)
        axes[1, 0].set_ylabel("Cota (m.s.n.m)", fontweight='bold', fontsize=7)
        axes[1, 0].grid(True)
        axes[1, 0].tick_params(axis='both', which='major', labelsize=6)
        axes[1, 0].set_facecolor('#f5e6d3')  # Fondo marrón super claro

        # Graficar Elevation vs Rot. B
        axes[1, 1].plot(group['Rot. B'], group['Elevation'], color=color, linewidth=2)
        axes[1, 1].set_xlabel("Rotación B (mm)", fontweight='bold', fontsize=7)
        axes[1, 1].set_ylabel("Cota (m.s.n.m)", fontweight='bold', fontsize=7)
        axes[1, 1].grid(True)
        axes[1, 1].tick_params(axis='both', which='major', labelsize=6)
        axes[1, 1].set_facecolor('#f5e6d3')  # Fondo marrón super claro

    # Añadir título a la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Gráficas del Inclinómetro: {nombre_inclinometro}')

    # Ajustar los márgenes para separar un poco más los gráficos
    plt.subplots_adjust(wspace=2, hspace=2)
    
    plt.tight_layout()
    plt.show()

def graficar_inclinometros_seaborn(df_inclinometros):
    # Obtener el nombre del inclinómetro
    nombre_inclinometro = df_inclinometros['Inclinometro'].iloc[0]

    # Crear la figura y los subgráficos
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Generar una paleta de colores amplia
    num_colors = df_inclinometros['Medición'].nunique()
    colores = sns.color_palette('tab20c', num_colors)
    
    # Configurar un fondo marrón super claro
    fondo_color = '#f5e6d3'
    fig.patch.set_facecolor(fondo_color)

    for i, (name, group) in enumerate(df_inclinometros.groupby('Medición')):
        color = colores[i]
        fecha = group['Fecha'].iloc[0]  # Obtener la fecha del grupo de datos

        # Graficar Elevation vs Cum. A
        sns.lineplot(x='Cum. A', y='Elevation', data=group, ax=axes[0, 0], color=color, linewidth=2, label=fecha)
        axes[0, 0].set_xlabel('Acumulado A (mm)', fontweight='bold', fontsize=7)
        axes[0, 0].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[0, 0].grid(True)
        axes[0, 0].legend(fontsize='small', loc='best')
        axes[0, 0].tick_params(axis='both', which='major', labelsize=6)
        axes[0, 0].set_facecolor(fondo_color)

        # Graficar Elevation vs Cum. B
        sns.lineplot(x='Cum. B', y='Elevation', data=group, ax=axes[0, 1], color=color, linewidth=2)
        axes[0, 1].set_xlabel('Acumulado B (mm)', fontweight='bold', fontsize=7)
        axes[0, 1].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[0, 1].grid(True)
        axes[0, 1].tick_params(axis='both', which='major', labelsize=6)
        axes[0, 1].set_facecolor(fondo_color)

        # Graficar Elevation vs Rot. A
        sns.lineplot(x='Rot. A', y='Elevation', data=group, ax=axes[1, 0], color=color, linewidth=2)
        axes[1, 0].set_xlabel('Rotación A (mm)', fontweight='bold', fontsize=7)
        axes[1, 0].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[1, 0].grid(True)
        axes[1, 0].tick_params(axis='both', which='major', labelsize=6)
        axes[1, 0].set_facecolor(fondo_color)

        # Graficar Elevation vs Rot. B
        sns.lineplot(x='Rot. B', y='Elevation', data=group, ax=axes[1, 1], color=color, linewidth=2)
        axes[1, 1].set_xlabel('Rotación B (mm)', fontweight='bold', fontsize=7)
        axes[1, 1].set_ylabel('Cota (m.s.n.m)', fontweight='bold', fontsize=7)
        axes[1, 1].grid(True)
        axes[1, 1].tick_params(axis='both', which='major', labelsize=6)
        axes[1, 1].set_facecolor(fondo_color)

    # Ajustar los márgenes para separar un poco más los gráficos
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    
    # Título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Gráficas del Inclinómetro: {nombre_inclinometro}')
    
    plt.tight_layout()
    plt.show()

def graficar_inclinometros_plotly(df_inclinometros):
    # Obtener el nombre del inclinómetro
    nombre_inclinometro = df_inclinometros['Inclinometro'].iloc[0]

    # Crear subgráficos
    fig = make_subplots(rows=2, cols=2, subplot_titles=(
        "Elevation vs Acumulado A (mm)", "Elevation vs Acumulado B (mm)",
        "Elevation vs Rotación A (mm)", "Elevation vs Rotación B (mm)"
    ))

    # Generar una paleta de colores amplia
    num_colors = df_inclinometros['Medición'].nunique()
    colores = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

    for i, (name, group) in enumerate(df_inclinometros.groupby('Medición')):
        color = colores[i % len(colores)]
        fecha = group['Fecha'].iloc[0]  # Obtener la fecha del grupo de datos

        # Graficar Elevation vs Cum. A
        fig.add_trace(go.Scatter(x=group['Cum. A'], y=group['Elevation'], mode='lines', line=dict(color=color, width=2), name=fecha), row=1, col=1)

        # Graficar Elevation vs Cum. B
        fig.add_trace(go.Scatter(x=group['Cum. B'], y=group['Elevation'], mode='lines', line=dict(color=color, width=2), name=fecha), row=1, col=2)

        # Graficar Elevation vs Rot. A
        fig.add_trace(go.Scatter(x=group['Rot. A'], y=group['Elevation'], mode='lines', line=dict(color=color, width=2), name=fecha), row=2, col=1)

        # Graficar Elevation vs Rot. B
        fig.add_trace(go.Scatter(x=group['Rot. B'], y=group['Elevation'], mode='lines', line=dict(color=color, width=2), name=fecha), row=2, col=2)

    # Ajustar el diseño y añadir el fondo
    fig.update_layout(height=700, width=1000, title_text=f'Gráficas del Inclinómetro: {nombre_inclinometro}', plot_bgcolor='#f5e6d3', paper_bgcolor='#f5e6d3')

    fig.show()

def graficos_freatimetros_matplotlib(df, nombre_freatimetro):
    # Verificar existencia de las columnas requeridas
    columnas_requeridas = ['FECHA', 'COTA_RÌO_(M.S.N.M)', 'COTA_NIVEL_FREATICO_(M.S.N.M.)', 'CARGA_(M.C.A)', 'PROF_NIVEL_FREATICO_(M)', 'Freatimetro']
    
    for columna in columnas_requeridas:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no está en el DataFrame.")
    
    # Formatear fechas
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')

    # Obtener los nombres de los freatímetros únicos
    nombres_freatimetros = df['Freatimetro'].unique()
    titulo_freatimetros = ', '.join(nombres_freatimetros)

    # Crear figura y ejes
    fig, axs = plt.subplots(2, 2, figsize=(15, 10), facecolor='w', num='Freatímetros')
    fig.suptitle(f"Visualización de Freatímetros: {titulo_freatimetros}", fontsize=16, y=1.02)

    # Colores
    colores = plt.cm.tab10.colors

    # Establecer color de fondo marrón claro
    color_fondo = '#D2B48C'

    # Gráfico 1: Cota del Nivel Freático y Cota del Río en Función del Tiempo
    ax1 = axs[0, 0]
    ax1.plot(df['FECHA'], df['COTA_NIVEL_FREATICO_(M.S.N.M.)'], label='Cota Nivel Freático', color=colores[0])
    ax2 = ax1.twinx()
    ax2.plot(df['FECHA'], df['COTA_RÌO_(M.S.N.M)'], label='Cota Río', color=colores[1])
    ax1.set_title('Cota del Nivel Freático y Cota del Río en Función del Tiempo')
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Cota Nivel Freático (m.s.n.m.)')
    ax2.set_ylabel('Cota Río (m.s.n.m.)')
    ax1.set_facecolor(color_fondo)
    ax2.set_facecolor(color_fondo)

    # Leyendas
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Gráfico 2: Carga en Función del Tiempo
    axs[0, 1].plot(df['FECHA'], df['CARGA_(M.C.A)'], label='Carga', color=colores[2])
    axs[0, 1].set_title('Carga en Función del Tiempo')
    axs[0, 1].set_xlabel('Fecha')
    axs[0, 1].set_ylabel('Carga (m.c.a)')
    axs[0, 1].set_facecolor(color_fondo)
    axs[0, 1].legend()

    # Gráfico 3: Profundidad del Nivel Freático en Función del Tiempo
    axs[1, 0].plot(df['FECHA'], df['PROF_NIVEL_FREATICO_(M)'], label='Profundidad Nivel Freático', color=colores[3])
    axs[1, 0].set_title('Profundidad del Nivel Freático en Función del Tiempo')
    axs[1, 0].set_xlabel('Fecha')
    axs[1, 0].set_ylabel('Profundidad Nivel Freático (m)')
    axs[1, 0].set_facecolor(color_fondo)
    axs[1, 0].legend()

    # Gráfico 4: Nivel Freático en Función del Tiempo
    axs[1, 1].plot(df['FECHA'], df['COTA_NIVEL_FREATICO_(M.S.N.M.)'], label='Nivel Freático', color=colores[4])
    axs[1, 1].set_title('Nivel Freático en Función del Tiempo')
    axs[1, 1].set_xlabel('Fecha')
    axs[1, 1].set_ylabel('Nivel Freático (m.s.n.m.)')
    axs[1, 1].set_facecolor(color_fondo)
    axs[1, 1].legend()

    # Ajustar formato de fecha en el eje X
    for ax in axs.flat:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Ajustar el espaciado alrededor de la gráfica y separar los gráficos
    plt.tight_layout(pad=2.0, rect=[0, 0, 1, 0.93])
    
    plt.show()

def graficos_freatimetros_seaborn(df, nombre_freatimetro):
    # Verificar existencia de las columnas requeridas
    columnas_requeridas = ['FECHA', 'COTA_RÌO_(M.S.N.M)', 'COTA_NIVEL_FREATICO_(M.S.N.M.)', 'CARGA_(M.C.A)', 'PROF_NIVEL_FREATICO_(M)', 'Freatimetro']
    
    for columna in columnas_requeridas:
        if columna not in df.columns:
            messagebox.showerror("Error", f"La columna '{columna}' no está en el DataFrame.")
            return

    # Formatear fechas
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')

    # Obtener los nombres de los freatímetros únicos
    nombres_freatimetros = df['Freatimetro'].unique()
    titulo_freatimetros = ', '.join(nombres_freatimetros)

    # Configurar la figura
    fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, num='Freatímetros')
    fig.suptitle(f"Visualización de Freatímetros: {titulo_freatimetros}")

    # Establecer color de fondo marrón claro
    color_fondo = '#FE9900'

    # Gráfico 1: Cota del Nivel Freático y Cota del Río en Función del Tiempo
    ax1 = axs[0, 0]
    sns.lineplot(x='FECHA', y='COTA_NIVEL_FREATICO_(M.S.N.M.)', hue='Freatimetro', data=df, ax=ax1)
    ax1.set_facecolor(color_fondo)
    ax1.set_ylabel('Cota Nivel Freático (m.s.n.m.)')
    ax1b = ax1.twinx()
    sns.lineplot(x='FECHA', y='COTA_RÌO_(M.S.N.M)', data=df, ax=ax1b, label='Cota Río', color='red')
    ax1b.set_facecolor(color_fondo)
    ax1b.set_ylabel('Cota Río (m.s.n.m.)')
    ax1.set_title("Cota del Nivel Freático y Cota del Río en Función del Tiempo")

    # Gráfico 2: Carga en Función del Tiempo
    ax2 = axs[0, 1]
    sns.lineplot(x='FECHA', y='CARGA_(M.C.A)', hue='Freatimetro', data=df, ax=ax2)
    ax2.set_facecolor(color_fondo)
    ax2.set_ylabel('Carga (m.c.a)')
    ax2.set_title("Carga en Función del Tiempo")

    # Gráfico 3: Profundidad del Nivel Freático en Función del Tiempo
    ax3 = axs[1, 0]
    sns.lineplot(x='FECHA', y='PROF_NIVEL_FREATICO_(M)', hue='Freatimetro', data=df, ax=ax3)
    ax3.set_facecolor(color_fondo)
    ax3.set_ylabel('Profundidad Nivel Freático (m)')
    ax3.set_title("Profundidad del Nivel Freático en Función del Tiempo")

    # Gráfico 4: Nivel Freático en Función del Tiempo
    ax4 = axs[1, 1]
    sns.lineplot(x='FECHA', y='COTA_NIVEL_FREATICO_(M.S.N.M.)', hue='Freatimetro', data=df, ax=ax4)
    ax4.set_facecolor(color_fondo)
    ax4.set_ylabel('Nivel Freático (m.s.n.m.)')
    ax4.set_title("Nivel Freático en Función del Tiempo")

    # Formato de fecha en el eje X
    for ax in axs.flat:
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=6))  # Limitar el número de etiquetas en el eje X
        ax.tick_params(axis='x', rotation=45)

    # Ajustar leyenda y diseño
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def grafica_cota_freatico_cota_rio_seaborn(df):
    # Verificar existencia de las columnas requeridas
    columnas_requeridas = ['FECHA', 'COTA_RÌO_(M.S.N.M)', 'COTA_NIVEL_FREATICO_(M.S.N.M.)', 'Freatimetro']
    
    for columna in columnas_requeridas:
        if columna not in df.columns:
            messagebox.showerror("Error", f"La columna '{columna}' no está en el DataFrame.")
            return

    # Obtener todos los freatímetros presentes en el DataFrame
    freatimetros = df['Freatimetro'].unique()
    
    # Filtrar los datos para los freatímetros presentes
    df_filtrado = df[df['Freatimetro'].isin(freatimetros)]

    # Formatear fechas
    df_filtrado['FECHA'] = pd.to_datetime(df_filtrado['FECHA'], format='%d/%m/%Y')

    plt.figure(figsize=(12, 6), num='Freatímetro')
    ax = sns.lineplot(x='FECHA', y='COTA_NIVEL_FREATICO_(M.S.N.M.)', hue='Freatimetro', data=df_filtrado, palette='Set1')
    ax.set_ylabel('Cota Nivel Freático (m.s.n.m.)', fontsize=12)
    ax.set_xlabel('Fecha', fontsize=12)
    
    ax2 = ax.twinx()
    sns.lineplot(x='FECHA', y='COTA_RÌO_(M.S.N.M)', data=df_filtrado, ax=ax2, label='Cota Río', color='cyan', linestyle='dashed')
    ax2.set_ylabel('Cota Río (m.s.n.m.)', fontsize=12)
    
    plt.title("Cota del Nivel Freático y Cota del Río en Función del Tiempo", fontsize=14)
    ax.tick_params(axis='x', rotation=45)

    # Cambiar el color de fondo a marrón brillante
    ax.set_facecolor('#F5DB91')  # Código de color hexadecimal para marrón brillante


    plt.tight_layout(pad=2.0)  # Ajustar el espaciado alrededor de la gráfica

    ax.legend(title='Freatímetros', loc='upper left')
    ax2.legend(title='Cota Río', loc='upper right')
    plt.show()

def plot_delta_norte_este_cota(df):
    if df is not None and 'Fecha' in df.columns and 'Margen' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        # Establecer la paleta de colores
        sns.set_palette("deep")
        
        # Obtener el valor único del campo Margen
        margen = df['Margen'].iloc[0]
        
        # Construir el título dinámico
        title = f"Puntos Fijos {margen}"
        
        # Crear la figura y el subgráfico
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Establecer el color de fondo
        ax.set_facecolor('turquoise')
        
        sns.lineplot(x='Fecha', y='Delta Norte [m]', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        sns.lineplot(x='Fecha', y='Delta Este [m]', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        sns.lineplot(x='Fecha', y='Delta cota [m]', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Deltas [m]')
        ax.set_title(title)
        
        # Mostrar la leyenda completa
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotar etiquetas y alinearlas a la derecha
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Limitar el número de etiquetas en el eje X
        ax.grid(True)
        plt.tight_layout()
        
        # Cambiar el título de la ventana del gráfico
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None o no contiene las columnas necesarias.")

def plot_distancia_m(df):
    if df is not None and not df.empty and 'Fecha' in df.columns and 'Distancia [m]' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        # Establecer la paleta de colores
        sns.set_palette("deep")
        
        # Construir el título
        title = "Distancia (m) en Función de la Fecha"
        
        # Crear la figura y el subgráfico
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Establecer el color de fondo
        ax.set_facecolor('turquoise')
        
        # Graficar la Distancia (m) en función de la Fecha
        sns.lineplot(x='Fecha', y='Distancia [m]', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Distancia [m]')
        ax.set_title(title)
        
        # Mostrar la leyenda completa
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotar etiquetas y alinearlas a la derecha
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Limitar el número de etiquetas en el eje X
        ax.grid(True)
        plt.tight_layout()
        
        # Cambiar el título de la ventana del gráfico
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def plot_distancia_mm(df):
    if df is not None and not df.empty and 'Fecha' in df.columns and 'Distancia (mm)' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        sns.set_palette("deep")
        
        title = "Distancia (mm) en Función de la Fecha"
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_facecolor('turquoise')
        
        sns.lineplot(x='Fecha', y='Distancia (mm)', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Distancia (mm)')
        ax.set_title(title)
        
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
        ax.grid(True)
        plt.tight_layout()
        
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def plot_azimut(df):
    if df is not None and 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        sns.set_palette("bright")
        
        title = "Azimut en Función de la Fecha"
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_facecolor('turquoise')
        
        sns.lineplot(x='Fecha', y='Azimut ref. al Norte', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Azimut ref. al Norte')
        ax.set_title(title)
        
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
        ax.grid(True)
        plt.tight_layout()
        
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None o no contiene las columnas necesarias.")

def plot_tasa_norte_este_cota(df):
    if df is not None and 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        sns.set_palette("bright")
        
        title = "Tasa Norte, Este y Cota en Función de la Fecha"
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_facecolor('turquoise')
        
        sns.lineplot(x='Fecha', y='Tasa Norte (mm/día)', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        sns.lineplot(x='Fecha', y='Tasa Este (mm/día)', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        sns.lineplot(x='Fecha', y='Tasa Cota (mm/día)', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Tasa (mm/día)')
        ax.set_title(title)
        
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
        ax.grid(True)
        plt.tight_layout()
        
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None o no contiene las columnas necesarias.")

def plot_tasa_distancia(df):
    if df is not None and 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        sns.set_palette("bright")
        
        title = "Tasa Distancia en Función de la Fecha"
        
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.set_facecolor('turquoise')
        
        sns.lineplot(x='Fecha', y='Tasa Distancia (mm/día)', hue='Instrumento', data=df, linewidth=1.5, ax=ax)
        ax.set_xlabel('Fecha')
        ax.set_ylabel('Tasa Distancia (mm/día)')
        ax.set_title(title)
        
        ax.legend(title='Instrumento', loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.xticks(rotation=45, ha='right')
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
        ax.grid(True)
        plt.tight_layout()
        
        fig.canvas.manager.set_window_title(title)
        
        plt.show()
    else:
        print("Error: El DataFrame df es None o no contiene las columnas necesarias.")

def plot_combinados_pf(df):
    if df is not None and not df.empty and 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')

        # Crear la figura y los subgráficos con un tamaño mayor
        fig, axs = plt.subplots(2, 2, figsize=(20, 16))  # Aumentar el tamaño total de la figura
        fig.suptitle('Gráficos Combinados de Puntos Fijos')

        # Definir las paletas de colores
        paleta1 = sns.color_palette("Set1")  # Para gráfica 1
        paleta2 = sns.color_palette("Set2")  # Para gráfica 2
        paleta3 = sns.color_palette("Set3")  # Para gráfica 3
        paleta4 = sns.color_palette("Dark2")  # Para gráfica 4

        # Gráfico 1: Distancia (mm) en función de la Fecha
        sns.lineplot(x='Fecha', y='Distancia (mm)', hue='Instrumento', palette=paleta1, data=df, linewidth=1, ax=axs[0, 0])
        axs[0, 0].set_title('Distancia (mm) en Función de la Fecha')
        axs[0, 0].set_xlabel('Fecha')
        axs[0, 0].set_ylabel('Distancia (mm)')
        axs[0, 0].get_legend().remove()  # Eliminar la leyenda de este gráfico

        # Gráfico 2: Tasa Distancia (mm/día) en función de la Fecha
        sns.lineplot(x='Fecha', y='Tasa Distancia (mm/día)', hue='Instrumento', palette=paleta2, data=df, linewidth=1, ax=axs[0, 1])
        axs[0, 1].set_title('Tasa Distancia (mm/día) en Función de la Fecha')
        axs[0, 1].set_xlabel('Fecha')
        axs[0, 1].set_ylabel('Tasa Distancia (mm/día)')
        axs[0, 1].legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 8})  # Mantener la leyenda solo en esta gráfica

        # Gráfico 3: Deltas (Norte, Este y Cota) en función de la Fecha
        sns.lineplot(x='Fecha', y='Delta Norte [m]', hue='Instrumento', palette=paleta3, data=df, linewidth=1, ax=axs[1, 0])
        sns.lineplot(x='Fecha', y='Delta Este [m]', hue='Instrumento', palette=paleta3, data=df, linewidth=1, ax=axs[1, 0])
        sns.lineplot(x='Fecha', y='Delta cota [m]', hue='Instrumento', palette=paleta3, data=df, linewidth=1, ax=axs[1, 0])
        axs[1, 0].set_title('Deltas (Norte, Este y Cota) en Función de la Fecha')
        axs[1, 0].set_xlabel('Fecha')
        axs[1, 0].set_ylabel('Delta [m]')
        axs[1, 0].get_legend().remove()  # Eliminar la leyenda de este gráfico

        # Gráfico 4: Tasas (Norte, Este y Cota) en función de la Fecha
        sns.lineplot(x='Fecha', y='Tasa Norte (mm/día)', hue='Instrumento', palette=paleta4, data=df, linewidth=1, ax=axs[1, 1])
        sns.lineplot(x='Fecha', y='Tasa Este (mm/día)', hue='Instrumento', palette=paleta4, data=df, linewidth=1, ax=axs[1, 1])
        sns.lineplot(x='Fecha', y='Tasa Cota (mm/día)', hue='Instrumento', palette=paleta4, data=df, linewidth=1, ax=axs[1, 1])
        axs[1, 1].set_title('Tasas (Norte, Este y Cota) en Función de la Fecha')
        axs[1, 1].set_xlabel('Fecha')
        axs[1, 1].set_ylabel('Tasa (mm/día)')
        axs[1, 1].get_legend().remove()  # Eliminar la leyenda de este gráfico

        # Rotar etiquetas y alinearlas a la derecha
        for ax in axs.flatten():
            ax.tick_params(axis='x', rotation=25)
            ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
            ax.grid(True)

        # Ajustar el diseño para una mejor separación y ajuste a la ventana
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.subplots_adjust(hspace=0.4, wspace=0.3, left=0.05)  # Ajustar espacios verticales y horizontales y alineación a la izquierda

        # Cambiar el título de la ventana del gráfico
        fig.canvas.manager.set_window_title('Gráficos Combinados de Puntos Fijos')
        
        plt.show()
    else:
        print("Error: El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def cg_plot_nivel_freatico_fecha(df, margen):
    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Reemplazar "SIN NF" con NaN en la columna 'COTA NF'
    df['COTA NF'] = df['COTA NF'].replace('SIN NF', np.nan).astype(float)
    
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]
    
    # Convertir la columna de fechas a formato datetime
    df_margen['FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
    # Ordenar el DataFrame por 'Piezómetro' y 'FECHA'
    df_margen = df_margen.sort_values(by=['Piezómetro', 'FECHA'])

    # Crear la figura
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.suptitle(f'Cota Nivel Freático en Función del Tiempo - Margen {margen}')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    paleta = sns.color_palette("bright", n_colors=len(df_margen['Piezómetro'].unique()))

    # Gráfica para el margen correspondiente con líneas sólidas
    sns.lineplot(x='FECHA', y='COTA NF', hue='Piezómetro', palette=paleta, data=df_margen, ax=ax, linewidth=2.5)

    ax.set_title(f'Margen {margen}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cota Nivel Freático')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df_margen['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])

    # Ajustar el diseño para que no se solapen las etiquetas de fecha
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Ajustar el número de etiquetas en el eje x

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Piezómetros Casagran - Margen {margen}')

    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar para dejar espacio para la leyenda
    plt.show()

def cg_plot_mca_fecha(df, margen):
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime
    df_margen['FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
    # Ordenar el DataFrame por 'Piezómetro' y 'FECHA'
    df_margen = df_margen.sort_values(by=['Piezómetro', 'FECHA'])

    # Crear la figura
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.suptitle(f'Metro Columna de Agua en Función del Tiempo - Margen {margen}')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    paleta = sns.color_palette("bright", n_colors=len(df_margen['Piezómetro'].unique()))

    # Gráfica
    sns.lineplot(x='FECHA', y='MCA 1 (Factor G)', hue='Piezómetro', palette=paleta, data=df_margen, ax=ax, linewidth=2.5)

    ax.set_title(f'Margen {margen}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Metro Columna de Agua (MCA 1)')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df_margen['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])

    # Ajustar el diseño para que no se solapen las etiquetas de fecha
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Ajustar el número de etiquetas en el eje x

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Piezómetros Casagran - Margen {margen}')

    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar para dejar espacio para la leyenda
    plt.show()

def cg_plot_lectura_cuerda_fecha(df, margen):
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime
    df_margen['FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
    # Ordenar el DataFrame por 'Piezómetro' y 'FECHA'
    df_margen = df_margen.sort_values(by=['Piezómetro', 'FECHA'])

    # Crear la figura
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.suptitle(f'Lectura Cuerda Vibrante en Función del Tiempo - Margen {margen}')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    paleta = sns.color_palette("bright", n_colors=len(df_margen['Piezómetro'].unique()))

    # Gráfica
    sns.lineplot(x='FECHA', y='LECTURA CUERDA VIBRANTE', hue='Piezómetro', palette=paleta, data=df_margen, ax=ax, linewidth=2.5)

    ax.set_title(f'Margen {margen}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Lectura Cuerda Vibrante')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df_margen['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])

    # Ajustar el diseño para que no se solapen las etiquetas de fecha
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Ajustar el número de etiquetas en el eje x

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Piezómetros Casagran - Margen {margen}')

    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar para dejar espacio para la leyenda
    plt.show()

def cg_plot_precipitaciones_fecha(df, margen):
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime
    df_margen['FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
    # Ordenar el DataFrame por 'Piezómetro' y 'FECHA'
    df_margen = df_margen.sort_values(by=['Piezómetro', 'FECHA'])

    # Crear la figura
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.suptitle(f'Precipitaciones en Función del Tiempo - Margen {margen}')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    paleta = sns.color_palette("bright", n_colors=len(df_margen['Piezómetro'].unique()))

    # Gráfica de barras
    sns.barplot(x='FECHA', y='PRECIPITACIONES (mm)', hue='Piezómetro', palette=paleta, data=df_margen, ax=ax)

    ax.set_title(f'Margen {margen}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precipitaciones (mm)')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df_margen['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])

    # Ajustar el diseño para que no se solapen las etiquetas de fecha
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Ajustar el número de etiquetas en el eje x

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Piezómetros Casagran - Margen {margen}')

    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar para dejar espacio para la leyenda
    plt.show()

def cg_plot_temperatura_fecha(df, margen):
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime
    df_margen['FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
    # Ordenar el DataFrame por 'Piezómetro' y 'FECHA'
    df_margen = df_margen.sort_values(by=['Piezómetro', 'FECHA'])

    # Crear la figura
    fig, ax = plt.subplots(figsize=(15, 6))
    fig.suptitle(f'Temperatura en Función del Tiempo - Margen {margen}')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    paleta = sns.color_palette("bright", n_colors=len(df_margen['Piezómetro'].unique()))

    # Gráfica de barras
    sns.barplot(x='FECHA', y='TEMPERATURA (°C)', hue='Piezómetro', palette=paleta, data=df_margen, ax=ax)

    ax.set_title(f'Margen {margen}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Temperatura (°C)')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df_margen['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])

    # Ajustar el diseño para que no se solapen las etiquetas de fecha
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Ajustar el número de etiquetas en el eje x

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title(f'Piezómetros Casagran - Margen {margen}')

    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Ajustar para dejar espacio para la leyenda
    plt.show()

def plot_asentamiento_fecha(df):
    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=(25, 7))
    fig.suptitle('Asentamiento en Función del Tiempo')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    unique_cells = df['Celda de Asentamiento'].unique()
    paleta = sns.color_palette("bright", n_colors=len(unique_cells))

    # Graficar los datos con líneas sólidas sin marcadores
    for i, celda in enumerate(unique_cells):
        df_celda = df[df['Celda de Asentamiento'] == celda]
        ax.plot(df_celda['FECHA'], df_celda['ASENTAMIENTO (cm)'], linestyle='-', color=paleta[i], linewidth=1.5, label=celda)

    # Configurar etiquetas y título
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Asentamiento (cm)')
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])  # Ajustar la amplitud del eje X

    # Ajustar el número de divisiones en el eje X
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    # Añadir líneas divisorias principales y menores
    ax.grid(True)  # Líneas divisorias principales
    ax.xaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje X
    ax.yaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje Y
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')  # Líneas divisorias menores

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title('Asentamiento en Función del Tiempo')

    # Ajustar los márgenes de la ventana del gráfico
    plt.tight_layout(rect=[0, 0, 0.9, 0.96])  # Puedes ajustar estos valores según tus necesidades
    plt.show()

# Ejemplo de llamada a la función con el DataFrame cargado
# plot_asentamiento_fecha(df_celdas_asentamiento)

def plot_cota_celda_relleno(df):
    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Crear la figura
    fig, ax1 = plt.subplots(figsize=(25, 7))
    fig.suptitle('Cota Celda y Cota Relleno en Función del Tiempo')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax1.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    unique_cells = df['Celda de Asentamiento'].unique()
    paleta = sns.color_palette("bright", n_colors=len(unique_cells))

    # Graficar Cota Celda en el eje Y principal
    for i, celda in enumerate(unique_cells):
        df_celda = df[df['Celda de Asentamiento'] == celda]
        ax1.plot(df_celda['FECHA'], df_celda['COTA CELDA (m.s.n.m)'], linestyle='-', color=paleta[i], linewidth=1.5, label=celda)

    # Crear un segundo eje Y para Cota Relleno
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')  # Dejar el fondo del eje Y secundario transparente
    for i, celda in enumerate(unique_cells):
        df_celda = df[df['Celda de Asentamiento'] == celda]
        ax2.plot(df_celda['FECHA'], df_celda['COTA RELLENO'], linestyle='--', color=paleta[i], linewidth=1.5)

    # Configurar etiquetas y título
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Cota Celda (m.s.n.m)')
    ax2.set_ylabel('Cota Relleno')

    ax1.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax1.tick_params(axis='y', labelsize=12, colors='black')
    ax2.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico en la esquina superior derecha
    ax1.legend(loc='upper left', bbox_to_anchor=(1.1, 1), borderaxespad=0)

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df['FECHA'].dropna().sort_values()
    ax1.set_xlim([fechas_validas.min(), fechas_validas.max()])  # Ajustar la amplitud del eje X

    # Ajustar el número de divisiones en el eje X
    ax1.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    # Añadir líneas divisorias principales y menores
    ax1.grid(True)  # Líneas divisorias principales
    ax1.xaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje X
    ax1.yaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje Y
    ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='black')  # Líneas divisorias menores

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title('Cota Celda y Cota Relleno en Función del Tiempo')

    # Ajustar los márgenes de la ventana del gráfico para maximizar la gráfica
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.15)  # Ajustar según tus necesidades

    plt.show()

# Ejemplo de llamada a la función con el DataFrame cargado
# plot_cota_celda_relleno(df_celdas_asentamiento)

def plot_punto_fijo_caseta(df):
    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=(25, 7))
    fig.suptitle('Punto Fijo Caseta en Función del Tiempo', fontsize=20)

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    unique_cells = df['Celda de Asentamiento'].unique()
    paleta = sns.color_palette("bright", n_colors=len(unique_cells))

    # Graficar Punto Fijo Caseta en el eje Y
    for i, celda in enumerate(unique_cells):
        df_celda = df[df['Celda de Asentamiento'] == celda]
        ax.plot(df_celda['FECHA'], df_celda['PUNTO FIJO CASETA'], linestyle='-', color=paleta[i], linewidth=2.5, label=celda)

    # Configurar etiquetas y título
    ax.set_xlabel('Fecha', fontsize=14)
    ax.set_ylabel('Punto Fijo Caseta', fontsize=14)
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico en la esquina superior derecha
    ax.legend(loc='upper left', bbox_to_anchor=(1.2, 1), borderaxespad=0)

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])  # Ajustar la amplitud del eje X

    # Ajustar el número de divisiones en el eje X
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    # Añadir líneas divisorias principales y menores
    ax.grid(True)  # Líneas divisorias principales
    ax.xaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje X
    ax.yaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje Y
    ax.grid(which='minor', linestyle=':', linewidth='0.1', color='black')  # Líneas divisorias menores

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title('Punto Fijo Caseta en Función del Tiempo')

    # Ajustar los márgenes de la ventana del gráfico para maximizar la gráfica
    plt.subplots_adjust(left=0.07, right=0.90, top=0.92, bottom=0.20)  # Ajustar según tus necesidades
    plt.show()

# Ejemplo de llamada a la función con el DataFrame cargado
# plot_punto_fijo_caseta(df_celdas_asentamiento)

def plot_ext_acumulado_tiempo(df):
    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=(25, 7))
    fig.suptitle('Acumulado en Función del Tiempo', fontsize=16)

    # Cambiar el fondo del área de la gráfica a turquesa
    ax.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    unique_extensometros = df['Extensómetro'].unique()
    paleta = sns.color_palette("bright", n_colors=len(unique_extensometros))

    # Graficar Acumulado en el eje Y
    for i, extensometro in enumerate(unique_extensometros):
        df_ext = df[df['Extensómetro'] == extensometro]
        ax.plot(df_ext['FECHA'], df_ext['ACUMULADO (mm)'], linestyle='-', color=paleta[i], linewidth=1.5, label=extensometro)

    # Configurar etiquetas y título
    ax.set_xlabel('Fecha', fontsize=14)
    ax.set_ylabel('Acumulado (mm)', fontsize=14)
    ax.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico en la esquina superior derecha
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1.2, 1), borderaxespad=0)
    for text in legend.get_texts():
        text.set_fontsize(12)  # Ajustar el tamaño de la fuente de la leyenda

    # Ajustar el rango del eje X para que termine en la última fecha
    fechas_validas = df['FECHA'].dropna().sort_values()
    ax.set_xlim([fechas_validas.min(), fechas_validas.max()])  # Ajustar la amplitud del eje X

    # Ajustar el número de divisiones en el eje X
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    # Añadir líneas divisorias principales y menores
    ax.grid(True)  # Líneas divisorias principales
    ax.xaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje X
    ax.yaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje Y
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')  # Líneas divisorias menores

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title('Acumulado en Función del Tiempo')

    # Ajustar los márgenes de la ventana del gráfico para maximizar la gráfica
    plt.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.20)

    # Mostrar la leyenda para el rótulo de los instrumentos
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)

    plt.show()

# Ejemplo de llamada a la función con el DataFrame cargado
# plot_acumulado_tiempo(df_extensometros_recinto)

# Crear la ventana principal
root = tk.Tk()
root.title('Sistema de Auscultación en Instrumentación de Presas - "Represas Condor Cliff"')
root.configure(bg='red')

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill='both', expand=True)

# Ruta a la imagen de fondo
ruta_imagen = 'Imagenes/instrumentos.jpg'
imagen = Image.open(ruta_imagen)
imagen_fondo = ImageTk.PhotoImage(imagen)
imagen_ancho, imagen_alto = imagen.size

# Función para centrar y ajustar la imagen de fondo
def centrar_ajustar_imagen(event):
    canvas.delete("all")
    canvas_ancho = event.width
    canvas_alto = event.height

    ratio = min(canvas_ancho / imagen_ancho, canvas_alto / imagen_alto)
    new_width = int(imagen_ancho * ratio)
    new_height = int(imagen_alto * ratio)

    imagen_resized = imagen.resize((new_width, new_height), Image.LANCZOS)
    imagen_fondo_resized = ImageTk.PhotoImage(imagen_resized)

    x = (canvas_ancho - new_width) // 2
    y = (canvas_alto - new_height) // 2
    canvas.create_image(x, y, image=imagen_fondo_resized, anchor='nw')
    canvas.imagen_fondo = imagen_fondo_resized

canvas.bind('<Configure>', centrar_ajustar_imagen)

footer_label = tk.Label(root, text="Sistema desarrollado por Ing. Jorge Gaspar Accardi", bg='lightblue', anchor='e')
footer_label.pack(side='bottom', fill='x')

# Crear la barra de menú
menu_bar = tk.Menu(root)

# Menú para Cargar Datos
menu_datos_monitoreo = tk.Menu(menu_bar, tearoff=0)

# Submenú para Inclinómetros
submenu_inclinometros = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_inclinometros.add_command(label="Cargar Datos GKN", command=cargar_y_procesar_gkn_inclinometros)
submenu_inclinometros.add_command(label="Cargar Datos Excel", command=cargar_y_procesar_excel_inclinometros)
menu_datos_monitoreo.add_cascade(label="Inclinómetros", menu=submenu_inclinometros)

# Submenú para Puntos Fijos
submenu_puntos_fijos = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_puntos_fijos.add_command(label="Cargar Datos Excel", command=cargar_datos_puntos_fijos)
menu_datos_monitoreo.add_cascade(label="Puntos Fijos", menu=submenu_puntos_fijos)

# Submenú para Freatímetros
submenu_freatimetros = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_freatimetros.add_command(label="Cargar Datos Excel", command=cargar_datos_freatimetros)
menu_datos_monitoreo.add_cascade(label="Freatímetros", menu=submenu_freatimetros)

# Submenú para Piezómetros Eléctricos
submenu_piezometros_electricos = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_piezometros_electricos.add_command(label="Cargar Datos Excel", command=cargar_datos_piezometros_electricos)
menu_datos_monitoreo.add_cascade(label="Piezómetros Eléctricos", menu=submenu_piezometros_electricos)

# Submenú para Piezómetros CG con PE
submenu_piezometros_cg_pe = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_piezometros_cg_pe.add_command(label="Cargar Datos Excel", command=cargar_datos_piezometros_cg_pe)
menu_datos_monitoreo.add_cascade(label="Piezómetros CG con PE", menu=submenu_piezometros_cg_pe)

# Submenú para Celdas de Asentamiento
submenu_celdas_asentamiento = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_celdas_asentamiento.add_command(label="Cargar Datos Excel", command=cargar_datos_celdas_asentamiento)
menu_datos_monitoreo.add_cascade(label="Celdas de Asentamiento", menu=submenu_celdas_asentamiento)

# Submenú para Extensómetros Recinto
submenu_extensometros_recinto = tk.Menu(menu_datos_monitoreo, tearoff=0)
submenu_extensometros_recinto.add_command(label="Cargar Datos Excel", command=cargar_datos_extensometros_recinto)
menu_datos_monitoreo.add_cascade(label="Extensómetros Recinto", menu=submenu_extensometros_recinto)

menu_datos_monitoreo.add_separator()
menu_datos_monitoreo.add_command(label="Salir", command=root.quit)
menu_bar.add_cascade(label="Cargar Datos", menu=menu_datos_monitoreo)
# Menú para Ver Datos Cargados
menu_datos_cargados = tk.Menu(menu_bar, tearoff=0)

# Submenú para Inclinómetros
submenu_mostrar_inclinometros = tk.Menu(menu_datos_cargados, tearoff=0)
submenu_mostrar_inclinometros.add_command(label="Mostrar Datos GKN", command=mostrar_datos_gkn_inclinometros)
submenu_mostrar_inclinometros.add_command(label="Mostrar Datos Excel", command=mostrar_datos_excel_inclinometros)
menu_datos_cargados.add_cascade(label="Inclinómetros", menu=submenu_mostrar_inclinometros)

# Submenú para Puntos Fijos
menu_datos_cargados.add_command(label="Mostrar Datos Puntos Fijos", command=mostrar_datos_puntos_fijos)

# Submenú para Freatímetros
menu_datos_cargados.add_command(label="Mostrar Datos Freatímetros", command=mostrar_datos_freatimetros)

# Submenú para Piezómetros Eléctricos
menu_datos_cargados.add_command(label="Mostrar Datos Piezómetros Eléctricos", command=mostrar_datos_piezometros_electricos)

# Submenú para Piezómetros CG con PE
menu_datos_cargados.add_command(label="Mostrar Datos Piezómetros CG con PE", command=mostrar_datos_piezometros_cg_pe)

# Submenú para Celdas de Asentamiento
menu_datos_cargados.add_command(label="Mostrar Datos Celdas de Asentamiento", command=mostrar_datos_celdas_asentamiento)

# Submenú para Extensómetros Recinto
menu_datos_cargados.add_command(label="Mostrar Datos Extensómetros Recinto", command=mostrar_datos_extensometros_recinto)

menu_bar.add_cascade(label="Ver Datos Cargados", menu=menu_datos_cargados)
# Menú para Gráficas
menu_graficas = tk.Menu(menu_bar, tearoff=0)

# Submenú para Inclinómetros
submenu_inclinometros = tk.Menu(menu_graficas, tearoff=0)
submenu_inclinometros.add_command(label="Visualización 1", command=lambda: graficar_inclinometros_matplotlib(df_inclinometros))
submenu_inclinometros.add_command(label="Visualización 2", command=lambda: graficar_inclinometros_seaborn(df_inclinometros))
submenu_inclinometros.add_command(label="Visualización 3", command=lambda: graficar_inclinometros_plotly(df_inclinometros))
menu_graficas.add_cascade(label="Inclinómetros", menu=submenu_inclinometros)

# Menú para Puntos Fijos
menu_puntos_fijos = tk.Menu(menu_graficas, tearoff=0)
menu_puntos_fijos.add_command(label="Delta Norte, Este y Cota en Función de la Fecha", command=lambda: plot_delta_norte_este_cota(df_puntos_fijos))
menu_puntos_fijos.add_command(label="Distancia (m) en Función de la Fecha", command=lambda: plot_distancia_m(df_puntos_fijos))
menu_puntos_fijos.add_command(label="Distancia (mm) en Función de la Fecha", command=lambda: plot_distancia_mm(df_puntos_fijos))
menu_puntos_fijos.add_command(label="Azimut en Función de la Fecha", command=lambda: plot_azimut(df_puntos_fijos))
menu_puntos_fijos.add_command(label="Tasa Norte, Este y Cota en Función de la Fecha", command=lambda: plot_tasa_norte_este_cota(df_puntos_fijos))
menu_puntos_fijos.add_command(label="Tasa Distancia en Función de la Fecha", command=lambda: plot_tasa_distancia(df_puntos_fijos))
menu_puntos_fijos.add_command(label="4 Graficos Combinados", command=lambda: plot_combinados_pf(df_puntos_fijos))
menu_graficas.add_cascade(label="Puntos Fijos", menu=menu_puntos_fijos)

# Submenú para Freatímetros
submenu_freatimetros = tk.Menu(menu_graficas, tearoff=0)
submenu_freatimetros.add_command(label="Gráficas Cotas vs Fechas", command=lambda: grafica_cota_freatico_cota_rio_seaborn(df_freatimetros_combinado))
submenu_freatimetros.add_command(label="Gráficas Múltiples en Matplotlib", command=lambda: graficos_freatimetros_matplotlib(df_freatimetros_combinado, nombre_freatimetro))
submenu_freatimetros.add_command(label="Gráficas Múltiples en Seaborn", command=lambda: graficos_freatimetros_seaborn(df_freatimetros_combinado, nombre_freatimetro))
menu_graficas.add_cascade(label="Freatímetros", menu=submenu_freatimetros)

# Submenú para Piezómetros Eléctricos
submenu_piezometros_electricos = tk.Menu(menu_graficas, tearoff=0)
submenu_piezometros_electricos.add_command(label="Cota Nivel Freático en Función del Tiempo", command=mostrar_seleccion_piezometros)
submenu_piezometros_electricos.add_command(label="Metros Columna de Agua (MCA 2) en Función del Tiempo", command=lambda: graficar_mca2_tiempo_matplotlib(df_piezometros_electricos))
submenu_piezometros_electricos.add_command(label="Lectura de Cuerda Vibrante en Función del Tiempo", command=lambda: graficar_linea_cuerda_vibrante_matplotlib(df_piezometros_electricos))
submenu_piezometros_electricos.add_command(label="Temperatura en Función del Tiempo", command=lambda: graficar_lineas_temperatura_matplotlib(df_piezometros_electricos))
submenu_piezometros_electricos.add_command(label="Cota Nivel Freático y Cota Río en Función de la Fecha", command=lambda: graficar_nivel_freatico_rio_matplotlib(df_piezometros_electricos))
submenu_piezometros_electricos.add_command(label="Precipitaciones y Temperatura en Función del Tiempo", command=lambda: graficar_precip_temperatura_matplotlib(df_piezometros_electricos))
submenu_piezometros_electricos.add_command(label="Cuerda Vibrante y Temperatura en Función del Tiempo", command=lambda: graficar_cuerda_temperatura_matplotlib(df_piezometros_electricos))
menu_graficas.add_cascade(label="Piezómetros Eléctricos", menu=submenu_piezometros_electricos)

# Submenú para Piezómetros CG con PE
submenu_piezometros_cg_pe = tk.Menu(menu_graficas, tearoff=0)
submenu_piezometros_cg_pe.add_command(label="MI - Nivel Freático", command=lambda: cg_plot_nivel_freatico_fecha(df_piezometros_cg_pe, 'MI'))
submenu_piezometros_cg_pe.add_command(label="MD - Nivel Freático", command=lambda: cg_plot_nivel_freatico_fecha(df_piezometros_cg_pe, 'MD'))
submenu_piezometros_cg_pe.add_command(label="MI - MCA", command=lambda: cg_plot_mca_fecha(df_piezometros_cg_pe, 'MI'))
submenu_piezometros_cg_pe.add_command(label="MD - MCA", command=lambda: cg_plot_mca_fecha(df_piezometros_cg_pe, 'MD'))
submenu_piezometros_cg_pe.add_command(label="MI - Cuerda Vibrante", command=lambda: cg_plot_lectura_cuerda_fecha(df_piezometros_cg_pe, 'MI'))
submenu_piezometros_cg_pe.add_command(label="MD - Cuerda Vibrante", command=lambda: cg_plot_lectura_cuerda_fecha(df_piezometros_cg_pe, 'MD'))
submenu_piezometros_cg_pe.add_command(label="MI - Precipitaciones", command=lambda: cg_plot_precipitaciones_fecha(df_piezometros_cg_pe, 'MI'))
submenu_piezometros_cg_pe.add_command(label="MD - Precipitaciones", command=lambda: cg_plot_precipitaciones_fecha(df_piezometros_cg_pe, 'MD'))
submenu_piezometros_cg_pe.add_command(label="MI - Temperatura", command=lambda: cg_plot_temperatura_fecha(df_piezometros_cg_pe, 'MI'))
submenu_piezometros_cg_pe.add_command(label="MD - Temperatura", command=lambda: cg_plot_temperatura_fecha(df_piezometros_cg_pe, 'MD'))
menu_graficas.add_cascade(label="Piezómetro Casagrande con PE", menu=submenu_piezometros_cg_pe)

# Submenú para Celdas de Asentamiento
submenu_celdas_asentamiento = tk.Menu(menu_graficas, tearoff=0)
submenu_celdas_asentamiento.add_command(label="Asentamiento Acumulado (cm)", command=lambda: plot_asentamiento_fecha(df_celdas_asentamiento))
submenu_celdas_asentamiento.add_command(label="Cota Celda en función del tiempo", command=lambda: plot_cota_celda_relleno(df_celdas_asentamiento))
submenu_celdas_asentamiento.add_command(label="Cota Caseta en función del tiempo", command=lambda: plot_punto_fijo_caseta(df_celdas_asentamiento))
menu_graficas.add_cascade(label="Celdas de Asentamiento", menu=submenu_celdas_asentamiento)

# Submenú para Extensómetros Recinto
submenu_ext_recinto = tk.Menu(menu_graficas, tearoff=0)
submenu_ext_recinto.add_command(label="Acumulado", command=lambda: plot_ext_acumulado_tiempo(df_extensometros_recinto))
menu_graficas.add_cascade(label="Extensómetros Recinto", menu=submenu_ext_recinto)

# Añadir Gráficas a la barra de menú principal
menu_bar.add_cascade(label="Gráficas", menu=menu_graficas)

# Configurar la barra de menú en la ventana principal
root.config(menu=menu_bar)

# Ejecutar la aplicación
root.mainloop()