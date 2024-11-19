import pandas as pd
import numpy as np

def limpiar_df_vivienda(df):
    """Limpia y procesa el dataframe de vivienda"""
    # Eliminar columnas innecesarias
    columnas_eliminar = [
        'Unnamed: 0', 'CONGLOME', 'VIVIENDA', 'HOGAR', 'AÑO',
        'Si Ud. alquilara esta vivienda, ¿Cuánto cree que le pagarían de alquiler mensual (en S/.)?',
        'Tipo de vivienda'
    ]
    df = df.drop(columns=columnas_eliminar)
    
    # Eliminar filas con más de 3 valores nulos
    nulos_por_fila = df.isnull().sum(axis=1)
    df = df[nulos_por_fila <= 3]
    
    # Eliminar columnas con más del 10% de valores nulos
    porcentaje_nulos = (df.isnull().sum() / len(df)) * 100
    df = df.drop(columns=porcentaje_nulos[porcentaje_nulos > 10].index)
    
    # Rellenar valores nulos restantes
    moda_acceso_agua = df['El hogar tiene acceso al servicio de agua todos los días de la semana'].mode()[0]
    df['El hogar tiene acceso al servicio de agua todos los días de la semana'].fillna(moda_acceso_agua, inplace=True)
    
    return df

def clasificar_calidad_vivienda(df):
    """Clasifica la calidad de la vivienda basado en los materiales"""
    materiales_bajos = [
        'Paja', 'Caña o estera con torta de barro o cemento', 
        'Quincha (caña con barro)', 'Piedra con barro', 'Tierra', 
        'Triplay/estera/carrizo', 'Otro material'
    ]
    materiales_medios = [
        'Planchas de calamina, fibra de cemento o similares', 
        'Madera', 'Adobe', 'Tapia', 'Cemento', 
        'Láminas asfálticas, vinílicos o similares'
    ]
    materiales_altos = [
        'Concreto armado', 'Tejas', 'Ladrillo o bloque de cemento', 
        'Losetas, terrazos o similares', 'Parquet o madera pulida'
    ]
    
    columnas_materiales = [
        'El material predominante en las paredes exteriores es:',
        'El material predominante en los pisos es:',
        'El material predominante en los techos es:'
    ]

    def clasificar(row):
        materiales = [row[col] for col in columnas_materiales]
        if any(m in materiales_bajos for m in materiales): return 'Baja'
        if any(m in materiales_medios for m in materiales): return 'Media'
        if any(m in materiales_altos for m in materiales): return 'Alta'
        return None

    df['Calidad_vivienda'] = df.apply(clasificar, axis=1)
    df.dropna(subset=['Calidad_vivienda'], inplace=True)
    df.drop(columns=columnas_materiales, inplace=True)
    
    return df

def clasificar_calidad_agua(df):
    """Clasifica la calidad del servicio de agua"""
    columnas_agua = [
        'El agua que utilizan en el hogar ¿Procede principalmente de:',
        '¿El agua es potable?',
        'El hogar tiene acceso al servicio de agua todos los días de la semana'
    ]

    def clasificar(row):
        fuente = row['El agua que utilizan en el hogar ¿Procede principalmente de:']
        potable = row['¿El agua es potable?']
        acceso = row['El hogar tiene acceso al servicio de agua todos los días de la semana']
        
        if potable == 'No' or acceso == 'No' or fuente == 'Pilón o pileta de uso público':
            return 'Baja'
        if fuente == 'Red pública, fuera de la vivienda pero dentro del edificio' and potable == 'Si':
            return 'Media'
        if fuente == 'Red pública, dentro de la vivienda' and potable == 'Si' and acceso == 'Si':
            return 'Alta'
        return None

    df['Calidad_servicio_agua'] = df.apply(clasificar, axis=1)
    df.drop(columns=columnas_agua, inplace=True)
    
    return df

def limpiar_df_salud(df):
    """Limpia y procesa el dataframe de salud"""
    columnas_eliminar = [
        'Unnamed: 0', 'AÑO', 'CONGLOME', 'VIVIENDA', 'HOGAR',
        '¿Tiene Ud. limitaciones de forma permanente, para: Moverse o caminar, para usar brazos o piernas?',
        '¿Tiene Ud. limitaciones de forma permanente, para: Hablar o comunicarse, aún usando el lenguaje de señas u otro?',
        '¿Tiene Ud. limitaciones de forma permanente, para: Entender o aprender (concentrarse y recordar)?',
        '¿En qué día, mes y año nació? - Día', '¿En qué día, mes y año nació? - Mes',
        '¿En qué día, mes y año nació? - Año', 'En las últimas', 'En las últimas.1',
        'En las últimas.2', 'En las últimas.3', 'En las últimas.4',
        '¿Padece de alguna enfermedad o malestar crónico (Artritis, hipertensión, asma, reumatismo, diabetes, tuberculosis, VIH, colesterol, etc.)?',
        '¿Quién le atendió durante la consulta?: Médico',
        '¿Quién le atendió durante la consulta?: Enfermera(o)',
        '¿Los medicamentos que usted ha tomado fueron : Cloroquina?',
        '¿Los medicamentos que usted ha tomado fueron : Hidroxicloroquina?',
        '¿Los medicamentos que usted ha tomado fueron : Ivermectina?',
        '¿Los medicamentos que usted ha tomado fueron : Azitromicina?',
        '¿Los medicamentos que usted ha tomado fueron : Remedios caseros?',
        '(Imputado, Deflactado, anualizado) ¿Cuánto cree que le costaría si tuviera que pagar por este servicio o producto?: Hospitalización',
        '(Imputado, Deflactado, anualizado) ¿Cuánto cree que le costaría si tuviera que pagar por este servicio o producto?: Medicinas/Insumos',
        '(Imputado, Deflactado, anualizado) ¿Cuánto fue el monto total por la compra o servicio?: Hospitalización',
        '(Imputado, Deflactado, anualizado) ¿Cuánto fue el monto total por la compra o servicio?: Medicinas/Insumos'
    ]
    df = df.drop(columns=columnas_eliminar)
    
    # Procesar columnas de consulta por enfermedad
    columnas_consulta = [col for col in df.columns if col.startswith('¿A dónde acudió para consultar')]
    df[columnas_consulta[:-1]] = df[columnas_consulta[:-1]].fillna(0)
    df[columnas_consulta[-1]] = df[columnas_consulta[-1]].fillna(1)
    
    # Procesar columnas de tiempo de espera
    columnas_tiempo = [
        'La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta?: No lo atendieron',
        'La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta?: N° Horas',
        'La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta? N° Minutos'
    ]
    df[columnas_tiempo] = df[columnas_tiempo].fillna(0)
    
    # Procesar columnas de cita
    columnas_cita = [col for col in df.columns if col.startswith('Desde que solicitó la cita')]
    df[columnas_cita] = df[columnas_cita].fillna(0)
    
    # Procesar razones de no atención
    columnas_razones = [col for col in df.columns if col.startswith('¿Cuáles son las razones')]
    df[columnas_razones] = df[columnas_razones].fillna(0)
    
    # Procesar columnas de medicamentos
    df['¿Los medicamentos que usted ha tomado fueron : Administración de oxígeno?'] = df['¿Los medicamentos que usted ha tomado fueron : Administración de oxígeno?'].replace({'Pase': 0, 'Administración de oxígeno': 1})
    df['¿Ha tomado medicamentos por prevención o como parte de un tratamiento para el covid-'] = df['¿Ha tomado medicamentos por prevención o como parte de un tratamiento para el covid-'].replace({2:0})
    
    return df

def procesar_lugar_consulta(df):
    """Procesa y combina la información del lugar de consulta"""
    def combinar_lugar_consulta(row):
        if row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: Puesto de salud MINSA'] == 1:
            return 'Puesto de salud MINSA'
        elif row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: Centro de salud MINSA'] == 1:
            return 'Centro de salud MINSA'
        elif row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: Posta, policlínico, EsSalud'] == 1:
            return 'Posta, policlínico, EsSalud'
        elif row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: Consultorio médico particular'] == 1:
            return 'Consultorio médico particular'
        elif row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: Farmacia o botica'] == 1:
            return 'Farmacia o botica'
        elif row['¿A dónde acudió para consultar por esta enfermedad, síntoma o malestar y/o accidente?: No buscó atención'] == 1:
            return 'No buscó atención'
        else:
            return 'Otro'

    df['Lugar_de_consulta'] = df.apply(combinar_lugar_consulta, axis=1)
    columnas_drop = [col for col in df.columns if col.startswith('¿A dónde acudió para consultar')]
    df.drop(columns=columnas_drop, inplace=True)
    
    return df

def procesar_tiempos_espera(df):
    """Procesa los tiempos de espera y citas"""
    # Tiempo total de espera para cita
    df['Tiempo_total_espera_minutos'] = (
        df['Desde que solicitó la cita en el establecimiento de salud a donde acudió, ¿Cuánto tiempo transcurrió, hasta la fecha que fue programada su atención?: N° Meses'] * 30 * 1440 + 
        df['Desde que solicitó la cita en el establecimiento de salud a donde acudió, ¿Cuánto tiempo transcurrió, hasta la fecha que fue programada su atención?: N° Días'] * 1440 + 
        df['Desde que solicitó la cita en el establecimiento de salud a donde acudió, ¿Cuánto tiempo transcurrió, hasta la fecha que fue programada su atención?: N° Horas'] * 60 + 
        df['Desde que solicitó la cita en el establecimiento de salud a donde acudió, ¿Cuánto tiempo transcurrió, hasta la fecha que fue programada su atención?: N° Minutos']
    )
    
    columnas_drop = [col for col in df.columns if col.startswith('Desde que solicitó la cita')]
    df.drop(columns=columnas_drop, inplace=True)
    
    # Tiempo de espera final
    def calcular_tiempo_espera_final(row):
        if row['La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta?: No lo atendieron'] == 1:
            return 0
        return (row['La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta?: N° Horas'] * 60 + 
                row['La última vez que acudió al establecimiento de salud, ¿Cuánto tiempo esperó para ser atendido en su consulta? N° Minutos'])

    df['Tiempo_espera_final_minutos'] = df.apply(calcular_tiempo_espera_final, axis=1)
    columnas_drop = [col for col in df.columns if col.startswith('La última vez que acudió')]
    df.drop(columns=columnas_drop, inplace=True)
    
    return df

def procesar_motivo_no_atencion(df):
    """Procesa los motivos de no atención"""
    def combinar_motivo_no_atencion(row):
        if row['¿Cuáles son las razones por las que no acudió a un centro o establecimento de salud?: No tuvo dinero'] == 1:
            return 'No tuvo dinero'
        elif row['¿Cuáles son las razones por las que no acudió a un centro o establecimento de salud?: Se encuentra lejos'] == 1:
            return 'Se encuentra lejos'
        elif row['¿Cuáles son las razones por las que no acudió a un centro o establecimento de salud?: Demoran mucho en atender'] == 1:
            return 'Demoran mucho en atender'
        else:
            return 'Sin razón específica'

    df['Motivo_no_atencion'] = df.apply(combinar_motivo_no_atencion, axis=1)
    columnas_drop = [col for col in df.columns if col.startswith('¿Cuáles son las razones')]
    df.drop(columns=columnas_drop, inplace=True)
    
    return df

def procesar_datos_meteorologicos(df):
    """Procesa los datos meteorológicos"""
    # Convertir fecha y filtrar año 2022
    df['AÑO'] = df['FECHA'].str[:4].astype(int)
    df['MES'] = df['FECHA'].str[4:6].astype(int)
    df['DIA'] = df['FECHA'].str[6:].astype(int)
    
    df_2022 = df[df['AÑO'] == 2022].copy()
    
    # Eliminar columnas innecesarias
    columnas_eliminar = [
        'ID', 'FECHA_CORTE', 'FECHA', 'RED', 'HORA', 'LONGITUD', 
        'LATITUD', 'ALTITUD', 'ESTACION', 'AÑO', 'DEPARTAMENTO', 
        'PROVINCIA', 'DISTRITO'
    ]
    df_2022.drop(columns=columnas_eliminar, inplace=True)
    
    # Rellenar valores nulos con la media
    df_2022[['TEMP', 'HR', 'PP']] = df_2022[['TEMP', 'HR', 'PP']].fillna(df_2022[['TEMP', 'HR', 'PP']].mean())
    
    # Crear ubigeo_departamento y agrupar
    df_2022['ubigeo_departamento'] = df_2022['UBIGEO'].astype(str).str[:2].astype(int)
    df_2022.drop(columns=['UBIGEO'], inplace=True)
    
    return df_2022.groupby(['MES', 'ubigeo_departamento'])[['TEMP', 'HR', 'PP']].mean().reset_index()

def procesar_datos_sinadef(df_sinadef, df_etiquetas, df_ubigeos):
    """Procesa los datos de SINADEF"""
    # Definir causas respiratorias de interés
    causas_respiratorias = [
        "INSUFICIENCIA RESPIRATORIA AGUDA", "INSUFICIENCIA RESPIRATORIA",
        "NEUMONÍA", "NEUMONÍA BACTERIANA", "NEUMONÍA ASPIRATIVA", 
        "ENFERMEDAD PULMONAR OBSTRUCTIVA CRONICA", "BRONCONEUMONIA", 
        "FIBROSIS PULMONAR", "SINDROME DE DIFICULTAD RESPIRATORIO DEL ADULTO",
        "TUBERCULOSIS DEL PULMON", "COLAPSO PULMONAR", "NEUMONITIS", 
        "NEUMOTORAX"
    ]
    
    # Eliminar columnas innecesarias
    columnas_eliminar = [
        'Unnamed: 0', 'N°', 'CAUSA B (CIE-X)', 'CAUSA C (CIE-X)',
        'CAUSA D (CIE-X)', 'CAUSA E (CIE-X)', 'CAUSA F (CIE-X)',
        'ETNIA', 'ESTADO CIVIL', 'PAIS DOMICILIO', 'NIVEL DE INSTRUCCIONN',
        'NECROPSIA', 'COD# UBIGEO DOMICILIO', 'MUERTE VIOLENTA',
        'TIPO LUGAR', 'INSTITUCION'
    ]
    df_sinadef.drop(columns=columnas_eliminar, inplace=True)
    
    # Unir con datos de ubigeos
    df_sinadef = df_sinadef.merge(
        df_ubigeos[['ubigeo_inei', 'departamento', 'provincia', 'distrito', 'macroregion_inei']],
        how='left',
        left_on=['DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO'],
        right_on=['departamento', 'provincia', 'distrito']
    )
    
    # Procesar fecha y limpiar columnas
    df_sinadef['MES'] = pd.to_datetime(df_sinadef['FECHA']).dt.month
    df_sinadef.drop(columns=[
        'FECHA', 'DEPARTAMENTO DOMICILIO', 'PROVINCIA DOMICILIO', 'DISTRITO DOMICILIO',
        'departamento', 'provincia', 'distrito'
    ], inplace=True)
    
    # Unir con etiquetas de causas
    df_sinadef = df_sinadef.merge(
        df_etiquetas[['CAUSA A (CIE-X)', 'DEBIDO A (CAUSA A)']].drop_duplicates(),
        how='left',
        on='CAUSA A (CIE-X)'
    )
    df_sinadef.rename(columns={'DEBIDO A (CAUSA A)': 'CAUSA'}, inplace=True)
    
    # Filtrar por causas respiratorias y top 5
    df_sinadef = df_sinadef[df_sinadef['CAUSA'].isin(causas_respiratorias)]
    top_5_causas = df_sinadef['CAUSA'].value_counts().head(5).index
    df_sinadef = df_sinadef[df_sinadef['CAUSA'].isin(top_5_causas)]
    
    # Limpiar datos faltantes y crear ubigeo_departamento
    df_sinadef.dropna(subset=['ubigeo_inei', 'macroregion_inei'], inplace=True)
    df_sinadef['ubigeo_inei'] = df_sinadef['ubigeo_inei'].astype(int)
    df_sinadef['ubigeo_departamento'] = df_sinadef['ubigeo_inei'].astype(str).str[:2].astype(int)
    
    return df_sinadef

def combinar_datasets(df_sinadef, df_meteo, df_vivienda, df_salud):
    """Combina todos los datasets procesados"""
    # Unir SINADEF con datos meteorológicos
    df_combined = df_sinadef.merge(
        df_meteo,
        on=['MES', 'ubigeo_departamento']
    )
    
    # Crear campo departamento_provincia
    df_combined['departamento_provincia'] = df_combined['ubigeo_inei'].astype(str).str[:4]
    
    # Unir con datos de vivienda
    df_combined = df_combined.merge(
        df_vivienda,
        how='left',
        left_on=['MES', 'ubigeo_inei'],
        right_on=['MES', 'UBIGEO']
    )
    
    # Unir con datos de salud
    df_combined = df_combined.merge(
        df_salud,
        how='left',
        left_on=['MES', 'ubigeo_inei'],
        right_on=['MES', 'UBIGEO']
    )
    
    # Limpiar duplicados y columnas innecesarias
    df_combined = df_combined.drop_duplicates()
    df_combined = df_combined.drop(columns=['UBIGEO_x', 'UBIGEO_y', 'DOMINIO_y', 'ESTRATO_y'])
    
    # Rellenar valores faltantes por departamento_provincia
    columnas_a_rellenar = [
        'DOMINIO', 'ESTRATO', 
        '¿Los medicamentos que usted ha tomado fueron : Administración de oxígeno?',
        '¿Ha tomado medicamentos por prevención o como parte de un tratamiento para el covid-',
        'Lugar_de_consulta', 'Tiempo_total_espera_minutos',
        'Motivo_no_atencion', 'Tiempo_espera_final_minutos',
        'Calidad_vivienda', 'Calidad_servicio_agua'
    ]
    
    for columna in columnas_a_rellenar:
        if columna in df_combined.columns:
            df_combined[columna] = df_combined.groupby('departamento_provincia')[columna].transform(
                lambda x: x.fillna(x.mode()[0]) if not x.mode().empty else x
            )
    
    # Eliminar filas con demasiados valores faltantes
    df_combined = df_combined.dropna(thresh=df_combined.shape[1] - 7)
    
    return df_combined

def asignar_estacion(df):
    """Asigna la estación del año según el mes"""
    def get_estacion(mes):
        if mes in [1, 2, 3]:
            return 'Verano'
        elif mes in [4, 5, 6]:
            return 'Otoño'
        elif mes in [7, 8, 9]:
            return 'Invierno'
        else:
            return 'Primavera'
    
    df['Estacion'] = df['MES'].apply(get_estacion)
    return df

def main():
    """Función principal que ejecuta todo el proceso"""
    # Cargar datos
    print("Cargando datos...")
    df_vivienda = pd.read_csv('enaho_vivienda.csv')
    df_salud = pd.read_csv('enaho_salud.csv')
    df_meteo = pd.read_csv('variables_meteorologicas.csv')
    df_sinadef = pd.read_excel('etiquetas_sinadef.xlsx')
    df_sinadef_etiquetas = pd.read_csv('fallecidos_sinadef.csv', sep='|')
    df_ubigeos = pd.read_csv('ubigeos.csv', sep=';')
    
    # Procesar datos de vivienda
    print("Procesando datos de vivienda...")
    df_vivienda = limpiar_df_vivienda(df_vivienda)
    df_vivienda = clasificar_calidad_vivienda(df_vivienda)
    df_vivienda = clasificar_calidad_agua(df_vivienda)
    
    # Procesar datos de salud
    print("Procesando datos de salud...")
    df_salud = limpiar_df_salud(df_salud)
    df_salud = procesar_lugar_consulta(df_salud)
    df_salud = procesar_tiempos_espera(df_salud)
    df_salud = procesar_motivo_no_atencion(df_salud)
    
    # Procesar datos meteorológicos
    print("Procesando datos meteorológicos...")
    df_meteo = procesar_datos_meteorologicos(df_meteo)
    
    # Procesar datos SINADEF
    print("Procesando datos SINADEF...")
    df_sinadef = procesar_datos_sinadef(df_sinadef, df_sinadef_etiquetas, df_ubigeos)
    
    # Combinar todos los datasets
    print("Combinando datasets...")
    df_final = combinar_datasets(df_sinadef, df_meteo, df_vivienda, df_salud)
    
    # Asignar estaciones
    print("Asignando estaciones...")
    df_final = asignar_estacion(df_final)
    
    # Guardar resultado final
    print("Guardando resultado final...")
    df_final.to_excel('processed_data.xlsx', index=False)
    print("Proceso completado exitosamente.")

if __name__ == "__main__":
    main()