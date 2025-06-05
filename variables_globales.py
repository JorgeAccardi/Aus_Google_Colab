# Variables para almacenar datos crudos leídos desde diferentes fuentes
datos_gkn_inclinometros = None  # Datos de inclinómetros GKN
datos_excel_inclinometros = None  # Datos de inclinómetros en formato Excel
datos_puntos_fijos = None  # Datos de puntos fijos de referencia
datos_freatimetros = None  # Datos de freatímetros
datos_piezometros_electricos = None  # Datos de piezómetros eléctricos
datos_piezometros_cg_pe = None  # Datos de piezómetros Casagrande con Sensor Eléctrico
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
nombre_freatimetro = "Freatímetro X"
