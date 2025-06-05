import tkinter as tk
from tkinter import filedialog, messagebox
import variables_globales as vg  # Importar el módulo de variables globales
from carga_datos import (
    cargar_y_procesar_gkn_inclinometros,
    cargar_y_procesar_excel_inclinometros,
    cargar_datos_puntos_fijos,
    cargar_datos_freatimetros,
    cargar_datos_piezometros_electricos,
    cargar_datos_piezometros_cg_pe,
    cargar_datos_celdas_asentamiento,
    cargar_datos_extensometros_recinto
)
from muestra_datos import (
    mostrar_datos_gkn_inclinometros,
    mostrar_datos_excel_inclinometros,
    mostrar_datos_puntos_fijos,
    mostrar_datos_freatimetros,
    mostrar_datos_piezometros_electricos,
    mostrar_datos_piezometros_cg_pe,
    mostrar_datos_celdas_asentamiento,
    mostrar_datos_extensometros_recinto
)
from grafica_datos import (
    graficar_inclinometros_matplotlib,
    graficar_inclinometros_seaborn,
    graficar_inclinometros_plotly,
    plot_delta_norte_este_cota,
    plot_distancia_m,
    plot_distancia_mm,
    plot_azimut,
    plot_tasa_norte_este_cota,
    plot_tasa_distancia,
    plot_combinados_pf,
    grafica_cota_freatico_cota_rio_seaborn,
    graficos_freatimetros_matplotlib,
    graficos_freatimetros_seaborn,
    graficar_mca2_tiempo_matplotlib,
    graficar_linea_cuerda_vibrante_matplotlib,
    graficar_lineas_temperatura_matplotlib,
    graficar_nivel_freatico_rio_matplotlib,
    graficar_precip_temperatura_matplotlib,
    graficar_cuerda_temperatura_matplotlib,
    cg_plot_nivel_freatico_fecha,
    cg_plot_mca_fecha,
    cg_plot_lectura_cuerda_fecha,
    cg_plot_precipitaciones_fecha,
    cg_plot_temperatura_fecha,
    plot_asentamiento_fecha,
    plot_cota_celda_relleno,
    plot_punto_fijo_caseta,
    plot_ext_acumulado_tiempo
)


def create_menu(root):
    menu_bar = tk.Menu(root)

    # Menú para Cargar Datos
    menu_datos_monitoreo = tk.Menu(menu_bar, tearoff=0)

    # Submenú para Inclinómetros
    submenu_inclinometros = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_inclinometros.add_command(label="Cargar Datos GKN", command=lambda: setattr(vg, 'datos_gkn_inclinometros', cargar_y_procesar_gkn_inclinometros()))
    submenu_inclinometros.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_excel_inclinometros', cargar_y_procesar_excel_inclinometros()))
    menu_datos_monitoreo.add_cascade(label="Inclinómetros", menu=submenu_inclinometros)

    # Submenú para Puntos Fijos
    submenu_puntos_fijos = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_puntos_fijos.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_puntos_fijos', cargar_datos_puntos_fijos()))
    menu_datos_monitoreo.add_cascade(label="Puntos Fijos", menu=submenu_puntos_fijos)

    # Submenú para Freatímetros
    submenu_freatimetros = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_freatimetros.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_freatimetros', cargar_datos_freatimetros()))
    menu_datos_monitoreo.add_cascade(label="Freatímetros", menu=submenu_freatimetros)

    # Submenú para Piezómetros Eléctricos
    submenu_piezometros_electricos = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_piezometros_electricos.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_piezometros_electricos', cargar_datos_piezometros_electricos()))
    menu_datos_monitoreo.add_cascade(label="Piezómetros Eléctricos", menu=submenu_piezometros_electricos)

    # Submenú para Piezómetros CG con PE
    submenu_piezometros_cg_pe = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_piezometros_cg_pe.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_piezometros_cg_pe', cargar_datos_piezometros_cg_pe()))
    menu_datos_monitoreo.add_cascade(label="Piezómetros CG con PE", menu=submenu_piezometros_cg_pe)

    # Submenú para Celdas de Asentamiento
    submenu_celdas_asentamiento = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_celdas_asentamiento.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_celdas_asentamiento', cargar_datos_celdas_asentamiento()))
    menu_datos_monitoreo.add_cascade(label="Celdas de Asentamiento", menu=submenu_celdas_asentamiento)

    # Submenú para Extensómetros Recinto
    submenu_extensometros_recinto = tk.Menu(menu_datos_monitoreo, tearoff=0)
    submenu_extensometros_recinto.add_command(label="Cargar Datos Excel", command=lambda: setattr(vg, 'datos_extensometros_recinto', cargar_datos_extensometros_recinto()))
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
    submenu_inclinometros.add_command(label="Visualización 1", command=lambda: graficar_inclinometros_matplotlib())
    submenu_inclinometros.add_command(label="Visualización 2", command=lambda: graficar_inclinometros_seaborn())
    submenu_inclinometros.add_command(label="Visualización 3", command=lambda: graficar_inclinometros_plotly())
    menu_graficas.add_cascade(label="Inclinómetros", menu=submenu_inclinometros)

    # Menú para Puntos Fijos
    menu_puntos_fijos = tk.Menu(menu_graficas, tearoff=0)
    menu_puntos_fijos.add_command(label="Delta Norte, Este y Cota en Función de la Fecha", command=lambda: plot_delta_norte_este_cota())
    menu_puntos_fijos.add_command(label="Distancia (m) en Función de la Fecha", command=lambda: plot_distancia_m())
    menu_puntos_fijos.add_command(label="Distancia (mm) en Función de la Fecha", command=lambda: plot_distancia_mm())
    menu_puntos_fijos.add_command(label="Azimut en Función de la Fecha", command=lambda: plot_azimut())
    menu_puntos_fijos.add_command(label="Tasa Norte, Este y Cota en Función de la Fecha", command=lambda: plot_tasa_norte_este_cota())
    menu_puntos_fijos.add_command(label="Tasa Distancia en Función de la Fecha", command=lambda: plot_tasa_distancia())
    menu_puntos_fijos.add_command(label="4 Graficos Combinados", command=lambda: plot_combinados_pf())
    menu_graficas.add_cascade(label="Puntos Fijos", menu=menu_puntos_fijos)

    # Submenú para Freatímetros
    submenu_freatimetros = tk.Menu(menu_graficas, tearoff=0)
    submenu_freatimetros.add_command(label="Gráficas Cotas vs Fechas", command=lambda: grafica_cota_freatico_cota_rio_seaborn())
    submenu_freatimetros.add_command(label="Gráficas Múltiples en Matplotlib", command=lambda: graficos_freatimetros_matplotlib())
    submenu_freatimetros.add_command(label="Gráficas Múltiples en Seaborn", command=lambda: graficos_freatimetros_seaborn())
    menu_graficas.add_cascade(label="Freatímetros", menu=submenu_freatimetros)

    # Submenú para Piezómetros Eléctricos
    submenu_piezometros_electricos = tk.Menu(menu_graficas, tearoff=0)
    submenu_piezometros_electricos.add_command(label="Cota Nivel Freático en Función del Tiempo", command=lambda: graficar_nivel_freatico_rio_matplotlib())
    submenu_piezometros_electricos.add_command(label="Metros Columna de Agua (MCA 2) en Función del Tiempo", command=lambda: graficar_mca2_tiempo_matplotlib())
    submenu_piezometros_electricos.add_command(label="Lectura de Cuerda Vibrante en Función del Tiempo", command=lambda: graficar_linea_cuerda_vibrante_matplotlib())
    submenu_piezometros_electricos.add_command(label="Temperatura en Función del Tiempo", command=lambda: graficar_lineas_temperatura_matplotlib())
    submenu_piezometros_electricos.add_command(label="Cota Nivel Freático y Cota Río en Función de la Fecha", command=lambda: graficar_nivel_freatico_rio_matplotlib())
    submenu_piezometros_electricos.add_command(label="Precipitaciones y Temperatura en Función del Tiempo", command=lambda: graficar_precip_temperatura_matplotlib())
    submenu_piezometros_electricos.add_command(label="Cuerda Vibrante y Temperatura en Función del Tiempo", command=lambda: graficar_cuerda_temperatura_matplotlib())
    menu_graficas.add_cascade(label="Piezómetros Eléctricos", menu=submenu_piezometros_electricos)

    # Submenú para Piezómetros CG con PE
    submenu_piezometros_cg_pe = tk.Menu(menu_graficas, tearoff=0)
    submenu_piezometros_cg_pe.add_command(label="MI - Nivel Freático", command=lambda: cg_plot_nivel_freatico_fecha('MI'))
    submenu_piezometros_cg_pe.add_command(label="MD - Nivel Freático", command=lambda: cg_plot_nivel_freatico_fecha('MD'))
    submenu_piezometros_cg_pe.add_command(label="MI - MCA", command=lambda: cg_plot_mca_fecha('MI'))
    submenu_piezometros_cg_pe.add_command(label="MD - MCA", command=lambda: cg_plot_mca_fecha('MD'))
    submenu_piezometros_cg_pe.add_command(label="MI - Cuerda Vibrante", command=lambda: cg_plot_lectura_cuerda_fecha('MI'))
    submenu_piezometros_cg_pe.add_command(label="MD - Cuerda Vibrante", command=lambda: cg_plot_lectura_cuerda_fecha('MD'))
    submenu_piezometros_cg_pe.add_command(label="MI - Precipitaciones", command=lambda: cg_plot_precipitaciones_fecha('MI'))
    submenu_piezometros_cg_pe.add_command(label="MD - Precipitaciones", command=lambda: cg_plot_precipitaciones_fecha('MD'))
    submenu_piezometros_cg_pe.add_command(label="MI - Temperatura", command=lambda: cg_plot_temperatura_fecha('MI'))
    submenu_piezometros_cg_pe.add_command(label="MD - Temperatura", command=lambda: cg_plot_temperatura_fecha('MD'))
    menu_graficas.add_cascade(label="Piezómetro Casagrande con PE", menu=submenu_piezometros_cg_pe)

    # Submenú para Celdas de Asentamiento
    submenu_celdas_asentamiento = tk.Menu(menu_graficas, tearoff=0)
    submenu_celdas_asentamiento.add_command(label="Asentamiento Acumulado (cm)", command=lambda: plot_asentamiento_fecha())
    submenu_celdas_asentamiento.add_command(label="Cota Celda en función del tiempo", command=lambda: plot_cota_celda_relleno())
    submenu_celdas_asentamiento.add_command(label="Cota Caseta en función del tiempo", command=lambda: plot_punto_fijo_caseta())
    menu_graficas.add_cascade(label="Celdas de Asentamiento", menu=submenu_celdas_asentamiento)

    # Submenú para Extensómetros Recinto
    submenu_ext_recinto = tk.Menu(menu_graficas, tearoff=0)
    submenu_ext_recinto.add_command(label="Acumulado", command=lambda: plot_ext_acumulado_tiempo())
    menu_graficas.add_cascade(label="Extensómetros Recinto", menu=submenu_ext_recinto)

    # Añadir Gráficas a la barra de menú principal
    menu_bar.add_cascade(label="Gráficas", menu=menu_graficas)

    # Configurar la barra de menú en la ventana principal
    root.config(menu=menu_bar)