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
    def __init__(self,index,lista_grupos_musculares):
        self.index = index
        self.lista_grupos_musculares = lista_grupos_musculares

# DEFINICIÓN DE VARIABLES GLOBALES
MODELO = './V1/Modelo_produccion.xlsx'
EJERCICIOS_LIST = []
MUSCULOS_LIST = []
GRUPOS_MUSCULARES_LIST = []
RUTINAS_LIST = []

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

    # xx. Crear los objetos grupo muscular
    nombres_musculos = MODELO_DF.columns.to_list()[5:37]
    grupos_ya_verificados = set()
    for nombre in nombres_musculos:
        grupo_en_si = str(MODELO_DF.loc[0,nombre]).split(',')
        frecuencia = MODELO_DF.loc[1,nombre]
        for el in grupo_en_si:
            if el not in grupos_ya_verificados:
                grupos_ya_verificados.add(el)
                objeto_encontrado = None
                for objeto in MUSCULOS_LIST:
                    if objeto.nombre == nombre:
                        objeto_encontrado = objeto
                        break  # Sale del bucle una vez que encuentra el objeto
                grupo_muscular_actual = grupo_muscular(el,[objeto_encontrado],frecuencia)
                GRUPOS_MUSCULARES_LIST.append(grupo_muscular_actual)
            else:
                for objeto in GRUPOS_MUSCULARES_LIST:
                    if objeto.nombre == el:
                        objeto_encontrado = None
                        for objeto_m in MUSCULOS_LIST:
                            if objeto_m.nombre == nombre:
                                objeto_encontrado = objeto_m
                                break
                        objeto.lista_musculos.append(objeto_encontrado)
                        break

    # xx. Crear los objetos tipo Rutina
    rutinas_index = MODELO_DF.columns.to_list()[50:60]
    for id in rutinas_index:
        list_elements_column = list(MODELO_DF[id].dropna().unique())
        list_grupos_musculares = []
        for objeto in GRUPOS_MUSCULARES_LIST:
            if objeto.nombre in list_elements_column:
                list_grupos_musculares.append(objeto)
        rutina_actual = rutina(id,list_grupos_musculares)
        RUTINAS_LIST.append(rutina_actual)

    # PREPARAR LA RUTINA DE HOY
    # xx. Sumar una unidad al valor de Rutina de hoy, en caso de ser 3, será una rutina de tren inferior, en caso de
    # ser menor, será una de tren superior, en caso de ser 4, es un día de descanso y se retorna el valor a 0
    # xx. Recordar que los músculos del abdomen no necesitan periodos de descanso, añadir la variable de excepción
    # xx. Revisar que músculos están en descanso y eliminarlos de todas las listas de los grupos musculares 
    # xx. Revisar que ejercicios están relacionados a los músculos en descanso y eliminarlos de las listas de ejercicios de los músculos restantes
    # ALGORITMO ESPECIAL PARA SEPARAR LAS PLAZAS DE LOS EJERCICIOS Y ESCOGER LOS PROPIOS EJERCICIOS
    # xx. Repetir esto para las 3 plazas de ejercicios
        # xx. valor_general = principante+intermedio+avanzado
        # xx. Generar un número aleatorio entre 0 y valor_general
        # xx. Se escoge el valor de intensidad(principante,intermedio,avanzado) que tenga el menor valor numérico,
        #     Si el número aleatorio va de 0 al menor valor, se escoge ese menor valor
        # xx. Hacer lo mismo pero con los siguientes rangos:
        #     menor valor - valor intermedio
        #     valor intermedio - mayor valor
    # NOTA: Las plazas deben ser listas o tuplas que contengan su id (momento secuencial en el cual saldrá el ejercicio
    # relacionado), su intensidad y un espacio para poner finalmente el ejercicio que se realizará, inicialmente vacío.
    # LAS PLAZAS YA ESTÁN CREADAS, AHORA A ESCOGER LOS EJERCICIOS
    # xx. Se ordenan las plazas desde la que tiene mayor intensidad hasta la de menor intensidad
    # xx. A cada rutina le asignamos un valor dependiendo de la suma de las frecuencias con que hayan sido 
    # ejercitados sus grupos musculares. (Para priorizar aquellas cuyos grupos musculares se hayan ejercitado menos)
    # xx. Ordenamos la lista de rutinas desde la de menor valor anterior hasta el mayor
    # xx. for rutina in lista_rutinas:
        # xx. lista_grupo_muscular_actual = rutina.lista_grupos_musculares
        # xx. Verificar si cada grupo muscular de lista_grupo_muscular_actual tiene por lo menos un músculo libre para entrenar
        # En caso de que no, se procede a la siguiente iteración.
        # xx. Se crea una nueva estructura de datos que contiene la siguiente información:
        # Tuplas con nombre de músculo, ejercicio e intensidad. El objetivo es que estas tuplas vayan siendo obtenidas en un orden específico.
        # xx. Se ordenan de menor frecuencia a mayor frecuencia todos los músculos presentes en el conjunto de
        # grupos musculares de la rutina.
        # xx. Para cada uno de estos músculos, se ordena su lista de ejercicios también de menor a mayor frecuencia,
        # y se crea la tupla con la información y se añade a la lista con un append
        # xx. for plaza in plazas_ordenadas:
            # xx. Se busca la primera tupla que cumpla con el requisito de intensidad de la plaza

    # xx. Si el for de rutinas termina sin posibilidad de hacer una rutina hoy, se decreta descanso anticipado.