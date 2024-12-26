import pandas as pd
import random

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

def rellenar_una_plaza(plaz,tgmei):
    for tupla_element in tgmei:
        # xx. Si se encuentra:
        if plaz[1] == tupla_element[3]:
            # xx. La plaza queda asociada al ejercicio en cuestión.
            plaz[2] = next(obj for obj in EJERCICIOS_LIST if obj.nombre == tupla_element[2])
            # xx. Se da por ejercitado el grupo muscular y se eliminan las tuplas de la lista que tengan ese grupo muscular.
            tgmei = [tupla for tupla in tgmei if tupla_element[0] not in tupla]
            # xx. También se eliminan de la estructura de datos de tuplas todas aquellas que repitan el ejercicio que acaba de salir.
            tgmei = [tupla for tupla in tgmei if tupla_element[2] not in tupla]
            break
    return tgmei

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

    # Variables
    rutina_de_hoy = int(MODELO_DF['Rutina de hoy'].iloc[0])
    diccionario_de_rutinas_por_valor = {
        0:['A','B','C','D','E','F','G','H'],
        1:['A','B','C','D','E','F','G','H'],
        2:['I','J'],
        3:'Descanso'
    }
    musculos_de_abdomen_excepcion_de_descanso = set() # Sólo los nombres, no todo el objeto
    RUTINAS_FILTRADAS = []
    musculos_en_descanso = MODELO_DF['Musculos en descanso'].dropna().tolist()
    ejercicios_vetados = set()
    valor_principiante = int(MODELO_DF['Principiante'].dropna().iloc[0])
    valor_intermedio = int(MODELO_DF['Intermedio'].dropna().iloc[0])
    valor_avanzado = int(MODELO_DF['Avanzado'].dropna().iloc[0])
    plazas = []
    intensidad_dict = {'Principiante': 1, 'Intermedio': 2, 'Avanzado': 3}
    pares_rutina_frecuencia = dict()
    lista_frecuencias_de_grupos_musculares_df = pd.DataFrame()

    # PREPARAR LA RUTINA DE HOY
    # xx. Sumar una unidad al valor de Rutina de hoy, en caso de ser 2, será una rutina de tren inferior, en caso de
    # ser menor, será una de tren superior, en caso de ser 3, es un día de descanso y se retorna el valor a 0
    valor_rutina_de_hoy = diccionario_de_rutinas_por_valor[rutina_de_hoy]
    if valor_rutina_de_hoy != 'Descanso':
        rutina_de_hoy = rutina_de_hoy+1
        # xx. Filtrar las rutinas con índices válidos
        RUTINAS_FILTRADAS = [rt for rt in RUTINAS_LIST if rt.index in valor_rutina_de_hoy]
        # xx. Recordar que los músculos del abdomen no necesitan periodos de descanso, añadir la variable de excepción
        grupo_muscular_abdomen = next((gm for gm in GRUPOS_MUSCULARES_LIST if gm.nombre == 'Abdomen'), None)
        for mus in grupo_muscular_abdomen.lista_musculos:
            musculos_de_abdomen_excepcion_de_descanso.add(mus.nombre)
        # xx. Revisar que músculos están en descanso y eliminarlos de todas las listas de los grupos musculares 
        for gp in GRUPOS_MUSCULARES_LIST:
            gp.lista_musculos = [
                musculo for musculo in gp.lista_musculos
                if musculo.nombre not in musculos_en_descanso
            ]
        # xx. Revisar que ejercicios están relacionados a los músculos en descanso y eliminarlos de las listas de ejercicios de los músculos restantes
        # Recorremos la lista de músculos extrayendo los nombres de los ejercicios
        for mus in MUSCULOS_LIST:
            if mus.nombre in musculos_en_descanso:
                for ej in mus.lista_ejercicios:
                    ejercicios_vetados.add(ej.nombre)
        # Eliminamos de las listas de músculos todos los ejercicios vetados
        for mus in MUSCULOS_LIST:
            mus.lista_ejercicios = [
                ejer for ejer in mus.lista_ejercicios
                if ejer.nombre not in ejercicios_vetados
            ]
        # ALGORITMO ESPECIAL PARA SEPARAR LAS PLAZAS DE LOS EJERCICIOS Y ESCOGER LOS PROPIOS EJERCICIOS
        # xx. Repetir esto para las 3 plazas de ejercicios
        for plaza in range(3):
            intensidad = ''
            # xx. valor_general = principante+intermedio+avanzado
            valor_general = valor_principiante+valor_intermedio+valor_avanzado
            # xx. Generar un número aleatorio entre 1 y valor_general
            entero_aleatorio = random.randint(1, valor_general)
            # xx. Escoger la intensidad relacionada a la plaza
            if 0 < entero_aleatorio <= valor_principiante:
                intensidad = 'Principiante'
            elif valor_principiante < entero_aleatorio <= valor_principiante+valor_intermedio:
                intensidad = 'Intermedio'
            elif valor_principiante+valor_intermedio < entero_aleatorio <= valor_general:
                intensidad = 'Avanzado'
            # NOTA: Las plazas deben ser listas que contengan su id (momento secuencial en el cual saldrá el ejercicio
            # relacionado), su intensidad y un espacio para poner finalmente el ejercicio que se realizará, inicialmente vacío.
            plazas.append([plaza+1,intensidad,None])
        # LAS PLAZAS YA ESTÁN CREADAS, AHORA A ESCOGER LOS EJERCICIOS
        # xx. Se ordenan las plazas desde la que tiene mayor intensidad hasta la de menor intensidad
        # Ordenar la lista usando la intensidad como clave
        plazas = sorted(plazas, key=lambda x: intensidad_dict[x[1]], reverse=True)
        # xx. A cada rutina le asignamos un valor dependiendo de la suma de las frecuencias con que hayan sido 
        # ejercitados sus grupos musculares. (Para priorizar aquellas cuyos grupos musculares se hayan ejercitado menos)
        for rut in RUTINAS_FILTRADAS:
            g_musculares = [
                gp.nombre for gp in rut.lista_grupos_musculares
            ]
            lista_frecuencias_de_grupos_musculares = MODELO_DF[g_musculares].iloc[0].to_list()
            pares_rutina_frecuencia[rut.index] = sum(lista_frecuencias_de_grupos_musculares)
        # xx. Ordenamos el dict de rutinas desde la de menor valor anterior hasta el mayor
        rutinas_ordenadas = sorted(pares_rutina_frecuencia.items(), key=lambda item: item[1])
        # xx. for rutina in lista_rutinas:
        for rutina_ordenada in rutinas_ordenadas:
            rutina_actual = [obj for obj in RUTINAS_FILTRADAS if obj.index == rutina_ordenada[0]][0]
            # xx. lista_grupo_muscular_actual = rutina.lista_grupos_musculares
            lista_grupo_muscular_actual = rutina_actual.lista_grupos_musculares
            # xx. Verificar si cada grupo muscular de lista_grupo_muscular_actual tiene por lo menos un músculo libre para entrenar
            # En caso de que no, se procede a la siguiente iteración.
            saltar_a_la_siguiente = False
            for gp in lista_grupo_muscular_actual:
                if len(gp.lista_musculos) < 1:
                    saltar_a_la_siguiente = True
                    break
            if saltar_a_la_siguiente:
                continue
            # xx. Se crea una nueva estructura de datos que contiene la siguiente información:
            # Tuplas con nombre del grupo muscular, nombre de músculo, ejercicio e intensidad. 
            # El objetivo es que estas tuplas vayan siendo obtenidas en un orden específico.
            tuplas_gp_mus_ejr_intensidad = []
            # xx. Se ordenan de menor frecuencia a mayor frecuencia todos los grupos musculares presentes en la rutina.
            lista_frecuencias_de_grupos_musculares_df = MODELO_DF[[objeto.nombre for objeto in lista_grupo_muscular_actual]].iloc[0]
            tupla_grupo_muscular_frecuencia_ordenada = sorted(list(lista_frecuencias_de_grupos_musculares_df.items()),key=lambda x: x[1])
            # xx. Para cada uno de estos grupos musculares, se ordena su lista de músculos también de menor a mayor frecuencia.
            for tupla_gp in tupla_grupo_muscular_frecuencia_ordenada:
                objeto_gp_musculos_lista = next(obj for obj in GRUPOS_MUSCULARES_LIST if obj.nombre == tupla_gp[0]).lista_musculos
                lista_frecuencias_de_musculos_df = MODELO_DF[[objeto.nombre for objeto in objeto_gp_musculos_lista]].iloc[1]
                tupla_musculo_frecuencia_ordenada = sorted(list(lista_frecuencias_de_musculos_df.items()),key=lambda x: x[1])
                # xx. Para cada uno de los musculos se ordena de menor a mayor frecuencia sus ejercicios asociados
                for tupla_mus in tupla_musculo_frecuencia_ordenada:
                    objeto_mus_ejercicios_lista = next(obj for obj in MUSCULOS_LIST if obj.nombre == tupla_mus[0]).lista_ejercicios
                    ejercicios_frecuencias_series = MODELO_DF.set_index('Ejercicios')['Frecuencia'].loc[[objeto.nombre for objeto in objeto_mus_ejercicios_lista]]
                    tupla_ejercicio_frecuencia_ordenada = sorted(ejercicios_frecuencias_series.items(),key=lambda x: x[1])
                    # y se crea la tupla con la información y se añade a la lista con un append
                    for tupla_ejr in tupla_ejercicio_frecuencia_ordenada:
                        gp = tupla_gp[0]
                        mus = tupla_mus[0]
                        ejr = tupla_ejr[0]
                        niv = ''
                        for ejr_nivel in objeto_mus_ejercicios_lista:
                            if ejr_nivel.nombre == ejr:
                                niv = ejr_nivel.nivel
                        if niv == '':
                            raise ValueError(f'No hay intensidad definida para el ejercicio {ejr}')
                        tuplas_gp_mus_ejr_intensidad.append((gp,mus,ejr,niv))
            copia_tuplas_gp_mus_ejr_intensidad = tuplas_gp_mus_ejr_intensidad.copy()

            # RECORDAR QUE PASA CUANDO EN LA ESTRUCTURA CON LAS TUPLAS YA NO HAY EJERCICIOS POSIBLES CUANDO AÚN NO SE
            # HAN LLENADO TODAS LAS PLAZAS

            # xx. for plaza in plazas_ordenadas:
            for plaza in plazas:
                print(len(tuplas_gp_mus_ejr_intensidad))
                # xx. Se busca la primera tupla que cumpla con el requisito de intensidad de la plaza
                tuplas_gp_mus_ejr_intensidad = rellenar_una_plaza(plaza, tuplas_gp_mus_ejr_intensidad)
                # xx. Si no se encuentra, se cambia la intensidad de esa plaza a su intensidad inmediatamente menor 
                # y se realiza nuevamente la búsqueda.
                # Si en la intensidad más baja no se encuentra cómo rellenar la plaza, se salta a verificar la siguiente rutina.
                niveles = {'Avanzado': 'Intermedio', 'Intermedio': 'Principiante', 'Principiante': None}
                while plaza[2] is None:
                    if plaza[1] == 'Principiante':
                        saltar_a_la_siguiente = True
                        break
                    # Reducir la intensidad al siguiente nivel
                    plaza[1] = niveles[plaza[1]]
                    if plaza[1] is None:  # Si ya está en el nivel más bajo, se detiene
                        saltar_a_la_siguiente = True
                        break
                    tuplas_gp_mus_ejr_intensidad = rellenar_una_plaza(plaza, tuplas_gp_mus_ejr_intensidad)
            if saltar_a_la_siguiente:
                continue
            else:
                break
        #for plaza in plazas:
        #    print(plaza[2].nombre)
            # xx. Si al final todas las plazas fueron llenadas, se da por concluído el proceso.
            # xx. Si queda alguna plaza por llenar, verificar si es porque todos los grupos musculares ya fueron sacados de las posibilidades.
            # En dado caso, se reinicia el proceso para llenar las plazas faltantes.
        # xx. Si el for de rutinas termina y hay plazas que no fueron llenadas, se declara el día como de descanso anticipado.
        # xx. Si todas las plazas están llenadas, se reemplazan los músculos a descansar y se actualizan todas las demás variables necesarias.
        # xx. Se crea un txt con la rutina.
        # xx. Se da espacio a esperar que la rutina culmine para dar la retroalimentación:
            # xx. Si la rutina fue hecha satisfactoriamente, se realizan las modificaciones necesarias en las probabilidades de las intensidades.
            # xx. Si no, se realiza la modificación contraria a las probabilidades para bajar el nivel de la siguiente rutina.
    # Opción de día de descanso
    else:
        pass
        # xx. Vaciar la columna de músculos en descanso
        # xx. Actualizar la variable de rutina de hoy


#print([objeto.index for objeto in RUTINAS_FILTRADAS])