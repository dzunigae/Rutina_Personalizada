import pandas as pd

# DEFINICIÓN DE OBJETOS

# 1. Definición objeto ejercicio
class ejercicio:
    def __init__(self,nombre,nivel,equipo,pagina,veces_realizado):
        self.nombre = nombre
        self.nivel = nivel
        self.equipo = equipo
        self.pagina = pagina
        self.veces_realizado = veces_realizado

# 2. Definición objeto musculo
class musculo:
    def __init__(self,nombre,lista_ejercicios,veces_ejercitado):
        self.nombre = nombre
        self.lista_ejercicios = lista_ejercicios
        self.veces_ejercitado = veces_ejercitado

# 3. Definición objeto Grupo muscular
class grupo_muscular:
    def __init__(self,nombre,lista_musculos,veces_ejercitado):
        self.nombre = nombre
        self.lista_musculos = lista_musculos
        self.veces_ejercitado = veces_ejercitado

# 4. Definición objeto rutina
class rutina:
    def __init__(self,index,lista_grupos_musculares,veces_realizada):
        self.index = index
        self.lista_grupos_musculares = lista_grupos_musculares
        self.veces_realizada = veces_realizada

# DEFINICIÓN DE VARIABLES GLOBALES
MODELO = './V1/Modelo_produccion.xlsx'
EJERCICIOS_LIST = []
MUSCULOS_LIST = []
GRUPOS_MUSCULARES_LIST = []

# DEFINICIÓN DE FUNCIONES

# 5. Definición de función que construye la rutina de hoy (Lista de objetos de tipo rutina que se pueden hacer hoy :: RUTINAS):
def construcción_de_la_rutina(lista_posibles_rutinas):
    # Obtener la lista de músculos del día anterior
    pass

# MAIN

if __name__ == "__main__":
    # Construir el df necesario del modelo
    MODELO_DF = pd.read_excel(MODELO)

    # xx. Crear los objetos ejercicio
    for i in range(len(MODELO_DF)):
        fila_a_revisar = MODELO_DF.iloc[i]
        if not pd.isna(fila_a_revisar['Ejercicios']):
            ejercicio_actual = ejercicio(fila_a_revisar['Ejercicios'],fila_a_revisar['Nivel'],fila_a_revisar['Equipo'],fila_a_revisar['Página'],fila_a_revisar['Frecuencia'])
            EJERCICIOS_LIST.append(ejercicio_actual)
    
    # xx. Crear los objetos musculo
    nombres_columnas = MODELO_DF.columns.to_list()[5:37]
    for nombre_musculo in nombres_columnas:
        lista_ejercicios_aprobados = []
        for j in range(len(MODELO_DF)):
            supuesta_x = MODELO_DF.iloc[j][nombre_musculo]
            if pd.notna(supuesta_x) and isinstance(supuesta_x, str) and len(supuesta_x) == 1:
                for ejercicio_especifico in EJERCICIOS_LIST:
                    if MODELO_DF.iloc[j]['Ejercicios'] == ejercicio_especifico.nombre:
                        lista_ejercicios_aprobados.append(ejercicio_especifico)
        musculo_actual = musculo(nombre_musculo,lista_ejercicios_aprobados,MODELO_DF.iloc[1][nombre_musculo])
        MUSCULOS_LIST.append(musculo_actual)

    # QUEDÉ AQUÍ, HAY QUE CORREGIR LO QUE DICE AHÍ

    # xx. Crear los objetos grupo muscular
    primera_fila_df = MODELO_DF.iloc[0:2]
    grupo_muscular_ya_creado = []
    for nombre_musculo in nombres_columnas:
        grupo_muscular_en_si = primera_fila_df.iloc[0][nombre_musculo].strip(',')
        for grupo_muscular_en_si_element in grupo_muscular_en_si:
            if grupo_muscular_en_si_element not in grupo_muscular_ya_creado:
                # Aquí hay algo por arreglar, la lista no debe ser sólo de los nombres sino del objeto músculo
                grupo_muscular_actual = grupo_muscular(grupo_muscular_en_si_element,[nombre_musculo],primera_fila_df.iloc[1][nombre_musculo])
                GRUPOS_MUSCULARES_LIST.append(grupo_muscular_actual)
                grupo_muscular_ya_creado.append(grupo_muscular_en_si_element)
            else:
                for elemento in GRUPOS_MUSCULARES_LIST:
                    if elemento.nombre == grupo_muscular_en_si_element:
                        elemento.lista_musculos.append(nombre_musculo)
                        break