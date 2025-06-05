import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import messagebox
import variables_globales as vg  # Asegúrate de que vg es un alias para variables_globales
from matplotlib.ticker import AutoMinorLocator
from procesa_datos import (

    procesar_datos_piezometros_cg_pe   
)


# Bibliotecas para Visualización: Estas bibliotecas permiten crear gráficos y visualizaciones para analizar y presentar datos.
import matplotlib.pyplot as plt  # Proporciona una interfaz para crear gráficos 2D, como líneas, barras, dispersión e histogramas.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permite incrustar gráficos de matplotlib en una aplicación de Tkinter.
import seaborn as sns  # Ofrece una interfaz basada en matplotlib para crear visualizaciones estadísticas atractivas y complejas, como mapas de calor.
import plotly.express as px  # Proporciona una interfaz simple para crear gráficos interactivos y visualizaciones rápidas.
import plotly.graph_objects as go  # Permite crear gráficos interactivos detallados y personalizados.
from plotly.subplots import make_subplots  # Ofrece herramientas para crear subtramas (subplots) en gráficos, permitiendo visualizaciones más detalladas y complejas.
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
from tkinter.filedialog import askopenfilename  # Proporciona un cuadro de diálogo para seleccionar un archivo para abrir.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog, messagebox
import variables_globales as vg


# Funciones para graficar datos

def graficar_inclinometros_matplotlib():
    df_inclinometros = vg.df_inclinometros  # Usar la variable global

    # Verificar si la variable global contiene datos
    if df_inclinometros is None or df_inclinometros.empty:
        messagebox.showerror("Error", "No se han cargado datos de inclinómetros GKN.")
        return

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

def graficar_inclinometros_seaborn():
    df_inclinometros = vg.df_inclinometros  # Usar la variable global

    # Verificar si la variable global contiene datos
    if df_inclinometros is None or df_inclinometros.empty:
        messagebox.showerror("Error", "No se han cargado datos de inclinómetros GKN.")
        return

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

def graficar_inclinometros_plotly():
    df_inclinometros = vg.df_inclinometros  # Usar la variable global

    # Verificar si la variable global contiene datos
    if df_inclinometros is None or df_inclinometros.empty:
        messagebox.showerror("Error", "No se han cargado datos de inclinómetros GKN.")
        return

    # Obtener el nombre del inclinómetro
    nombre_inclinometro = df_inclinometros['Inclinometro'].iloc[0]

    # Crear la figura con subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Cum. A vs Elevation', 'Cum. B vs Elevation', 'Rot. A vs Elevation', 'Rot. B vs Elevation'))

    # Generar una paleta de colores amplia
    num_colors = df_inclinometros['Medición'].nunique()
    colores = px.colors.qualitative.Plotly

    for i, (name, group) in enumerate(df_inclinometros.groupby('Medición')):
        color = colores[i % len(colores)]
        fecha = group['Fecha'].iloc[0]  # Obtener la fecha del grupo de datos

        # Graficar Elevation vs Cum. A
        fig.add_trace(go.Scatter(x=group['Cum. A'], y=group['Elevation'], mode='lines', name=fecha, line=dict(color=color)), row=1, col=1)

        # Graficar Elevation vs Cum. B
        fig.add_trace(go.Scatter(x=group['Cum. B'], y=group['Elevation'], mode='lines', name=fecha, line=dict(color=color)), row=1, col=2)

        # Graficar Elevation vs Rot. A
        fig.add_trace(go.Scatter(x=group['Rot. A'], y=group['Elevation'], mode='lines', name=fecha, line=dict(color=color)), row=2, col=1)

        # Graficar Elevation vs Rot. B
        fig.add_trace(go.Scatter(x=group['Rot. B'], y=group['Elevation'], mode='lines', name=fecha, line=dict(color=color)), row=2, col=2)

    # Añadir título a la figura
    fig.update_layout(title_text=f'Gráficas del Inclinómetro: {nombre_inclinometro}', showlegend=True)

    # Ajustar diseño
    fig.update_xaxes(title_text="Acumulado A (mm)", row=1, col=1)
    fig.update_yaxes(title_text="Cota (m.s.n.m)", row=1, col=1)
    fig.update_xaxes(title_text="Acumulado B (mm)", row=1, col=2)
    fig.update_yaxes(title_text="Cota (m.s.n.m)", row=1, col=2)
    fig.update_xaxes(title_text="Rotación A (mm)", row=2, col=1)
    fig.update_yaxes(title_text="Cota (m.s.n.m)", row=2, col=1)
    fig.update_xaxes(title_text="Rotación B (mm)", row=2, col=2)
    fig.update_yaxes(title_text="Cota (m.s.n.m)", row=2, col=2)

    fig.show()

def plot_delta_norte_este_cota():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None o no contiene las columnas necesarias.")

def plot_distancia_m():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def plot_distancia_mm():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def plot_azimut():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None o no contiene las columnas necesarias.")

def plot_tasa_norte_este_cota():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None o no contiene las columnas necesarias.")

def plot_tasa_distancia():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None o no contiene las columnas necesarias.")

def plot_combinados_pf():
    df = vg.df_puntos_fijos  # Usar la variable global

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
        messagebox.showerror("Error", "El DataFrame df es None, está vacío o no contiene las columnas necesarias.")

def grafica_cota_freatico_cota_rio_seaborn():
    df = vg.df_freatimetros_combinado  # Usar la variable global

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

def graficos_freatimetros_matplotlib():
    df = vg.df_freatimetros_combinado  # Usar la variable global

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

def graficos_freatimetros_seaborn():
    df = vg.df_freatimetros_combinado  # Usar la variable global

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

def graficar_mca2_tiempo_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'MCA 2 (Factor G y K)' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df['MCA 2 (Factor G y K)'] = df['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df['Piezómetro'].unique():
            datos_piezometro = df[df['Piezómetro'] == piezometro]
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
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'MCA 2 (Factor G y K)' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df['MCA 2 (Factor G y K)'] = df['MCA 2 (Factor G y K)'].astype(float)

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x='FECHA', y='MCA 2 (Factor G y K)', hue='Piezómetro', marker='o')
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
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'MCA 2 (Factor G y K)' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'MCA 2 (Factor G y K)'])
        df['MCA 2 (Factor G y K)'] = df['MCA 2 (Factor G y K)'].astype(float)

        fig = px.line(df, x='FECHA', y='MCA 2 (Factor G y K)', title='Metros Columna de Agua (MCA 2) en Función del Tiempo',
                      labels={'FECHA': 'Fecha', 'MCA 2 (Factor G y K)': 'MCA 2 (m)'}, color='Piezómetro')
        fig.show()
    else:
        print("Los datos no contienen las columnas necesarias.")
        messagebox.showerror("Error", "Los datos no contienen las columnas necesarias.")

def graficar_linea_cuerda_vibrante_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'LECTURA CUERDA VIBRANTE' in df.columns:

        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE'])
        df['LECTURA CUERDA VIBRANTE'] = df['LECTURA CUERDA VIBRANTE'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df['Piezómetro'].unique():
            datos_piezometro = df[df['Piezómetro'] == piezometro]
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

def graficar_lineas_temperatura_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'TEMPERATURA (°C)' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'TEMPERATURA (°C)'])
        df['TEMPERATURA (°C)'] = df['TEMPERATURA (°C)'].astype(float)

        plt.figure(figsize=(10, 5))
        for piezometro in df['Piezómetro'].unique():
            datos_piezometro = df[df['Piezómetro'] == piezometro]
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

def verificar_columnas_necesarias(columnas_necesarias, df):
    columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
    if columnas_faltantes:
        return False, columnas_faltantes
    return True, None

def graficar_nivel_freatico_rio_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    print("Verificando datos...")

    if df is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df.columns)

    columnas_necesarias = ['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'COTA RIO (m.s.n.m)', 'COTA NF'])
        
        # Convertir la columna a cadenas y luego reemplazar las comas por puntos decimales
        df['COTA RIO (m.s.n.m)'] = df['COTA RIO (m.s.n.m)'].astype(str).str.replace(',', '.').astype(float)
        
        # Reemplazar los valores 'SIN NF' con NaN para poder convertir la columna a float
        df['COTA NF'] = df['COTA NF'].replace('SIN NF', np.nan).astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.plot(df['FECHA'], df['COTA NF'], marker='o', color='tab:blue', label='Cota NF')
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Cota NF', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        ax2.plot(df['FECHA'], df['COTA RIO (m.s.n.m)'], marker='x', linestyle='--', color='tab:red', label='Cota Río')
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

def graficar_precip_temperatura_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    print("Verificando datos...")

    if df is None:
        print("df_piezometros_electricos es None")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return
    if df.empty:
        print("df_piezometros_electricos está vacío")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    print("Columnas del DataFrame:")
    print(df.columns)

    columnas_necesarias = ['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)']
    columnas_presentes, columnas_faltantes = verificar_columnas_necesarias(columnas_necesarias, df)

    if not columnas_presentes:
        print(f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        messagebox.showerror("Error", f"Los datos no contienen las columnas necesarias: {columnas_faltantes}")
        return

    try:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'TEMPERATURA (°C)', 'PRECIPITACIONES (mm)'])
        
        df['TEMPERATURA (°C)'] = df['TEMPERATURA (°C)'].astype(float)
        df['PRECIPITACIONES (mm)'] = df['PRECIPITACIONES (mm)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.plot(df['FECHA'], df['PRECIPITACIONES (mm)'], marker='o', color='blue', label='Precipitaciones (mm)')
        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Precipitaciones (mm)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(df['FECHA'], df['TEMPERATURA (°C)'], marker='x', linestyle='--', color='red', label='Temperatura (°C)')
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

def graficar_cuerda_temperatura_matplotlib():
    df = vg.df_piezometros_electricos  # Usar la variable global

    if df is None or df.empty:
        print("No se han cargado datos o los datos están vacíos.")
        messagebox.showerror("Error", "No se han cargado datos o los datos están vacíos.")
        return

    if 'FECHA' in df.columns and 'LECTURA CUERDA VIBRANTE' in df.columns and 'TEMPERATURA (°C)' in df.columns:
        df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['FECHA', 'LECTURA CUERDA VIBRANTE', 'TEMPERATURA (°C)'])
        df['LECTURA CUERDA VIBRANTE'] = df['LECTURA CUERDA VIBRANTE'].astype(float)
        df['TEMPERATURA (°C)'] = df['TEMPERATURA (°C)'].astype(float)

        fig, ax1 = plt.subplots(figsize=(10, 5))

        for piezometro in df['Piezómetro'].unique():
            datos_piezometro = df[df['Piezómetro'] == piezometro]
            ax1.plot(datos_piezometro['FECHA'], datos_piezometro['LECTURA CUERDA VIBRANTE'], marker='o', label=f'Lectura Cuerda {piezometro}')

        ax1.set_xlabel('Fecha')
        ax1.set_ylabel('Lectura Cuerda Vibrante', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()
        for piezometro in df['Piezómetro'].unique():
            datos_piezometro = df[df['Piezómetro'] == piezometro]
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

def cg_plot_nivel_freatico_fecha(margen):
    df = vg.df_piezometros_cg_pe  # Usar la variable global

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

def cg_plot_mca_fecha(margen):
    df = vg.df_piezometros_cg_pe  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return

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
    df = vg.df_piezometros_cg_pe  # Usar la variable global

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

def cg_plot_precipitaciones_fecha(margen):
    if vg.df_piezometros_cg_pe is None:  # Verificar si los datos ya están cargados
        archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if not archivo:
            messagebox.showerror("Error", "No se seleccionó ningún archivo.")
            return
        vg.df_piezometros_cg_pe = procesar_datos_piezometros_cg_pe(archivo)
    
    df = vg.df_piezometros_cg_pe  # Usar la variable global
    
    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime utilizando .loc para evitar advertencias
    df_margen.loc[:, 'FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
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

def cg_plot_temperatura_fecha(margen):
    if vg.df_piezometros_cg_pe is None:  # Verificar si los datos ya están cargados
        archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel files", "*.xlsx *.xls")])
        if not archivo:
            messagebox.showerror("Error", "No se seleccionó ningún archivo.")
            return
        vg.df_piezometros_cg_pe = procesar_datos_piezometros_cg_pe(archivo)
    
    df = vg.df_piezometros_cg_pe  # Usar la variable global

    # Filtrar datos por margen
    df_margen = df[df['Margen'] == margen]

    # Convertir la columna de fechas a formato datetime utilizando .loc para evitar advertencias
    df_margen.loc[:, 'FECHA'] = pd.to_datetime(df_margen['FECHA'], dayfirst=True, errors='coerce')
    
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
    df = vg.df_celdas_asentamiento  # Usar la variable global

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

def cg_plot_lectura_cuerda_fecha(margen):
    df = vg.df_piezometros_cg_pe  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return

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

def cg_plot_precipitaciones_fecha(margen):
    df = vg.df_piezometros_cg_pe  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return

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

def cg_plot_temperatura_fecha(margen):
    df = vg.df_piezometros_cg_pe  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return

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

def plot_asentamiento_fecha():
    df = vg.df_celdas_asentamiento  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Asegurarse de que las fechas están en formato datetime y en el formato dd/mm/yyyy
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')
    
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

    # Ajustar el rango del eje X para que cubra todo el rango de fechas del DataFrame
    fecha_inicio = df['FECHA'].min()
    fecha_fin = df['FECHA'].max()
    ax.set_xlim([fecha_inicio, fecha_fin])

    # Ajustar el número de divisiones en el eje X
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=12))  # Dividir el eje X en 12 partes

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

def plot_cota_celda_relleno():
    df = vg.df_celdas_asentamiento  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Asegurarse de que las fechas están en formato datetime y en el formato dd/mm/yyyy
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')
    
    # Crear la figura
    fig, ax1 = plt.subplots(figsize=(25, 7))
    fig.suptitle('Cota Celda y Cota Relleno en Función del Tiempo', fontsize=14, fontweight='bold')

    # Cambiar el fondo del área de la gráfica a turquesa
    ax1.set_facecolor('turquoise')

    # Definir la paleta de colores brillantes
    unique_cells = df['Celda de Asentamiento'].unique()
    paleta = sns.color_palette("bright", n_colors=len(unique_cells))

    # Graficar Cota Celda en el eje Y principal para todas las celdas
    for i, celda in enumerate(unique_cells):
        df_celda = df[df['Celda de Asentamiento'] == celda]
        ax1.plot(df_celda['FECHA'], df_celda['COTA CELDA (m.s.n.m)'], linestyle='-', color=paleta[i], linewidth=1.5, label=f'Celda {celda}')

    # Crear un segundo eje Y para Cota Relleno
    ax2 = ax1.twinx()
    ax2.set_facecolor('none')  # Dejar el fondo del eje Y secundario transparente
    
    # Tomar la cota de relleno de la primera celda del DataFrame
    primera_celda = unique_cells[0]
    df_celda = df[df['Celda de Asentamiento'] == primera_celda]
    ax2.plot(df_celda['FECHA'], df_celda['COTA RELLENO'], linestyle='--', color='black', linewidth=1.5, label='Cota Relleno')

    # Configurar etiquetas y título
    ax1.set_xlabel('Fecha', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cota Celda (m.s.n.m)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cota Relleno', fontsize=12, fontweight='bold')

    ax1.tick_params(axis='x', rotation=45, labelsize=12, colors='black')
    ax1.tick_params(axis='y', labelsize=12, colors='black')
    ax2.tick_params(axis='y', labelsize=12, colors='black')

    # Colocar la leyenda fuera del gráfico y ajustar el tamaño de la fuente
    legend_fontsize = 10
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles=handles1 + handles2, labels=labels1 + labels2, loc='center left', bbox_to_anchor=(1.1, 0.5), borderaxespad=0, fontsize=legend_fontsize)

    # Ajustar el rango del eje X para que cubra todo el rango de fechas del DataFrame
    fecha_inicio = df['FECHA'].min()
    fecha_fin = df['FECHA'].max()
    ax1.set_xlim([fecha_inicio, fecha_fin])

    # Ajustar el número de divisiones en el eje X
    ax1.xaxis.set_major_locator(plt.MaxNLocator(nbins=12))  # Dividir el eje X en 12 partes

    # Añadir líneas divisorias principales y menores
    ax1.grid(True)  # Líneas divisorias principales
    ax1.xaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje X
    ax1.yaxis.set_minor_locator(AutoMinorLocator())  # Configurar localizador menor para el eje Y
    ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='black')  # Líneas divisorias menores

    # Cambiar el título de la ventana del gráfico
    fig.canvas.manager.set_window_title('Cota Celda y Cota Relleno en Función del Tiempo')

    # Ajustar los márgenes de la ventana del gráfico para maximizar la gráfica
    plt.subplots_adjust(left=0.08, right=0.82, top=0.92, bottom=0.17)  # Ajustar según tus necesidades

    plt.show()

def plot_punto_fijo_caseta():
    df = vg.df_celdas_asentamiento  # Usar la variable global

    if df is None or df.empty:
        print("El DataFrame está vacío o no se ha cargado correctamente.")
        return
    
    # Asegurarse de que las fechas están en formato datetime y en el formato dd/mm/yyyy
    df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y')

    # Crear la figura
    fig, ax = plt.subplots(figsize=(35, 7))
    fig.suptitle('Punto Fijo Caseta en Función del Tiempo', fontsize=14)

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
    ax.legend(loc='center left', bbox_to_anchor=(1.03, 0.5), borderaxespad=0)

    # Ajustar el rango del eje X para que cubra toda la línea de tiempo del DataFrame
    fecha_inicio = df['FECHA'].min()
    fecha_fin = df['FECHA'].max()
    ax.set_xlim([fecha_inicio, fecha_fin])  # Ajustar la amplitud del eje X

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

def plot_ext_acumulado_tiempo():
    df = vg.df_extensometros_recinto  # Usar la variable global

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

    plt.show()
