import pandas as pd
import os
import variables_globales as vg  
from tkinter import messagebox

# Resto del código...


# Funciones para procesar datos

def procesar_carpeta_gkn(carpeta):
    try:
        if not os.path.exists(carpeta):
            raise FileNotFoundError(f"La carpeta especificada '{carpeta}' no se encuentra.")
        
        archivos = [f for f in os.listdir(carpeta) if f.lower().endswith('.gkn')]
        if not archivos:
            raise ValueError("No se encontraron archivos GKN en la carpeta.")
        
        print("Archivos encontrados:", archivos)  # Mensaje de depuración
        
        lista_df = [procesar_gkn_inclinometros(os.path.join(carpeta, archivo)) for archivo in archivos]
        lista_df = [df for df in lista_df if df is not None]
        
        if not lista_df:
            raise ValueError("No se pudo cargar ningún archivo GKN correctamente.")
        
        df_combinado = pd.concat(lista_df, ignore_index=True)
        vg.df_gkn_inclinometros = df_combinado
        
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
        print(f"Procesando el archivo: {file_path}")  # Mensaje de depuración
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
            
            print(f"Archivo procesado correctamente: {file_path}")  # Mensaje de depuración
            return df
    except Exception as e:
        print(f"Error procesando el archivo {file_path}: {e}")
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

def limpiar_datos(df):
    df = df.dropna(subset=['FECHA'])
    df.columns = [col.strip().upper().replace(" ", "_").translate(str.maketrans("ÁÉÍÓÚÑ", "AEIOUN")) for col in df.columns]
    return df

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

                    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
                    df = df.dropna(subset=['FECHA']).dropna(how='all')

                    columnas_numericas = ['PUNTO FIJO CASETA', 'COTA RIO (m.s.n.m)', 'LECTURA REGLETA (m)',
                                          'COTA "0" REGLETA (m)', 'COTA CELDA (m.s.n.m)', 'ASENTAMIENTO (cm)',
                                          'COTA RELLENO', 'MODULO DEFORMACION (ε)']
                    df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')
                    df['Celda de Asentamiento'] = nombre_hoja

                    # Cambiar la ubicación de la columna 'Celda de Asentamiento' a la segunda posición
                    cols = df.columns.tolist()
                    cols.insert(1, cols.pop(cols.index('Celda de Asentamiento')))
                    df = df[cols]

                    df.insert(2, 'Progresiva', progresiva)
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


