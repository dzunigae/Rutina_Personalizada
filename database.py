import sqlite3
import pandas as pd

# Modelo con los datos
DF_INFORMACION_EJERCICIOS = pd.read_excel('./Modelo.xlsx')

# Data frames con los datos para pasarlos a la base de datos
DF_GRUPO = pd.DataFrame(columns=['Nombre'])
DF_IDENTIFICADOR_RUTINA = pd.DataFrame(columns=['Indicador', 'Frecuencia'])
DF_EJERCICIO = pd.DataFrame(columns=['Nombre', 'Nivel', 'Pagina', 'Repeticiones', 'Equipo', 'Peso', 'Tiempo', 'Frecuencia'])
DF_MUSCULO = pd.DataFrame(columns=['Nombre', 'Grupo', 'Frecuencia'])
DF_TRABAJO_MUSCULAR = pd.DataFrame(columns=['Ejercicio', 'Musculo'])
DF_RUTINA = pd.DataFrame(columns=['Rutina', 'Grupo'])

def trabajo_pd(DF_GRUPO,DF_IDENTIFICADOR_RUTINA,DF_EJERCICIO,DF_MUSCULO,DF_TRABAJO_MUSCULAR,DF_RUTINA):
    #DF_GRUPO
    grupos = set()
    grupos = set(DF_INFORMACION_EJERCICIOS.loc[0].tolist())
    grupos = {x for x in grupos if not isinstance(x, float)}
    grupos.remove('Biceps,Triceps')
    grupos_list = []
    for element in grupos:
        grupos_dict = dict()
        grupos_dict['Nombre'] = element
        grupos_list.append(grupos_dict)
    for element in grupos_list:
        DF_GRUPO = DF_GRUPO._append(element, ignore_index=True)
    
    #DF_IDENTIFICADOR_RUTINA
    rutinas = ['a','b','c','d','e','f','g','h','i','j']
    rutinas_list = []
    for element in rutinas:
        rutinas_dict = dict()
        rutinas_dict['Indicador'] = element
        rutinas_dict['Frecuencia'] = 0
        rutinas_list.append(rutinas_dict)
    for element in rutinas_list:
        DF_IDENTIFICADOR_RUTINA = DF_IDENTIFICADOR_RUTINA._append(element, ignore_index=True)

    #DF_EJERCICIO
    ejercicio_list = []
    for id in range(len(DF_INFORMACION_EJERCICIOS)):
        ejercicio = DF_INFORMACION_EJERCICIOS.loc[id,'Ejercicios']
        if isinstance(ejercicio,str):
            ejercicio_dict = dict()
            ejercicio_dict['Nombre'] = ejercicio
            ejercicio_dict['Nivel'] = DF_INFORMACION_EJERCICIOS.loc[id,'Nivel']
            ejercicio_dict['Pagina'] = DF_INFORMACION_EJERCICIOS.loc[id,'Página']
            ejercicio_dict['Repeticiones'] = 0
            ejercicio_dict['Equipo'] = DF_INFORMACION_EJERCICIOS.loc[id,'Equipo']
            ejercicio_dict['Peso'] = 0
            ejercicio_dict['Tiempo'] = 0
            ejercicio_dict['Frecuencia'] = 0
            ejercicio_list.append(ejercicio_dict)
    for element in ejercicio_list:
        DF_EJERCICIO = DF_EJERCICIO._append(element,ignore_index=True)
    
    #DF_MUSCULO
    musculos_list = []
    df_separado = DF_INFORMACION_EJERCICIOS.iloc[:, 4:].loc[0]
    df_separado = df_separado.to_dict()
    for clave in df_separado:
        musculo_dict_1 = dict()
        musculo_en_si = df_separado[clave]
        #Separación del inconveniente de más de un músculo
        if ',' in musculo_en_si:
            musculo_dict_2 = dict()
            musculo_en_si_partes = musculo_en_si.split(',')
            musculo_dict_1['Nombre'] = clave
            musculo_dict_1['Grupo'] = DF_GRUPO[DF_GRUPO['Nombre'] == musculo_en_si_partes[0]].index[0]
            musculo_dict_1['Frecuencia'] = 0
            musculo_dict_2['Nombre'] = clave
            musculo_dict_2['Grupo'] = DF_GRUPO[DF_GRUPO['Nombre'] == musculo_en_si_partes[1]].index[0]
            musculo_dict_2['Frecuencia'] = 0
            musculos_list.append(musculo_dict_1)
            musculos_list.append(musculo_dict_2)
        else:
            musculo_dict_1['Nombre'] = clave
            musculo_dict_1['Grupo'] = DF_GRUPO[DF_GRUPO['Nombre'] == musculo_en_si].index[0]
            musculo_dict_1['Frecuencia'] = 0
            musculos_list.append(musculo_dict_1)
    for element in musculos_list:
        DF_MUSCULO = DF_MUSCULO._append(element,ignore_index=True)

    #DF_TRABAJO_MUSCULAR
    trabajo_muscular_list = []
    DF_MODELO_SIN_FILA_0 = DF_INFORMACION_EJERCICIOS.iloc[1:]
    for id in range(len(DF_MODELO_SIN_FILA_0)):
        fila_actual = DF_MODELO_SIN_FILA_0.loc[id+1]
        ejercicio = fila_actual['Ejercicios']
        index_ejercicio = DF_EJERCICIO[DF_EJERCICIO['Nombre'] == ejercicio].index[0]
        fila_actual_musculos = fila_actual.iloc[4:]
        musculos_que_trabaja_este_ejercicio = list(fila_actual_musculos.dropna().to_dict().keys())
        indexs_musculos_filtrados = DF_MUSCULO[DF_MUSCULO['Nombre'].isin(musculos_que_trabaja_este_ejercicio)].index.tolist()
        for id in indexs_musculos_filtrados:
            trabajo_muscular_dict = dict()
            trabajo_muscular_dict['Ejercicio'] = index_ejercicio
            trabajo_muscular_dict['Musculo'] = id
            trabajo_muscular_list.append(trabajo_muscular_dict)
    for element in trabajo_muscular_list:
        DF_TRABAJO_MUSCULAR = DF_TRABAJO_MUSCULAR._append(element,ignore_index=True)
    
    #DF_RUTINA
    DF_RUTINA = DF_RUTINA._append({'Rutina':0, 'Grupo':3},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':0, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':1, 'Grupo':2},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':1, 'Grupo':4},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':1, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':2, 'Grupo':3},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':2, 'Grupo':2},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':2, 'Grupo':4},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':3, 'Grupo':2},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':3, 'Grupo':4},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':3, 'Grupo':8},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':4, 'Grupo':0},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':4, 'Grupo':8},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':4, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':5, 'Grupo':3},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':5, 'Grupo':0},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':5, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':6, 'Grupo':0},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':6, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':7, 'Grupo':3},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':7, 'Grupo':0},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':7, 'Grupo':8},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':8, 'Grupo':1},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':8, 'Grupo':5},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':8, 'Grupo':6},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':9, 'Grupo':7},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':9, 'Grupo':5},ignore_index=True)
    DF_RUTINA = DF_RUTINA._append({'Rutina':9, 'Grupo':6},ignore_index=True)

    #Conección con la base de datos
    conn = sqlite3.connect('./db.db')

    #Preparación de los DataFrame
    DF_GRUPO.reset_index(inplace=True)
    DF_GRUPO.rename(columns={'index':'id'},inplace=True)

    DF_IDENTIFICADOR_RUTINA.reset_index(inplace=True)
    DF_IDENTIFICADOR_RUTINA.rename(columns={'index':'id'},inplace=True)

    DF_EJERCICIO.reset_index(inplace=True)
    DF_EJERCICIO.rename(columns={'index':'id'},inplace=True)

    DF_MUSCULO.reset_index(inplace=True)
    DF_MUSCULO.rename(columns={'index':'id'},inplace=True)

    DF_TRABAJO_MUSCULAR.reset_index(inplace=True)
    DF_TRABAJO_MUSCULAR.rename(columns={'index':'id'},inplace=True)

    DF_RUTINA.reset_index(inplace=True)
    DF_RUTINA.rename(columns={'index':'id'},inplace=True)

    #Guardar la información en las tablas
    DF_GRUPO.to_sql('grupo',conn,if_exists='replace',index=False)
    DF_IDENTIFICADOR_RUTINA.to_sql('identificador_rutina',conn,if_exists='replace',index=False)
    DF_EJERCICIO.to_sql('ejercicio',conn,if_exists='replace',index=False)
    DF_MUSCULO.to_sql('musculo',conn,if_exists='replace',index=False)
    DF_TRABAJO_MUSCULAR.to_sql('trabajo_muscular',conn,if_exists='replace',index=False)
    DF_RUTINA.to_sql('rutina',conn,if_exists='replace',index=False)

    # Cierre de la conexión
    conn.close()

trabajo_pd(DF_GRUPO,DF_IDENTIFICADOR_RUTINA,DF_EJERCICIO,DF_MUSCULO,DF_TRABAJO_MUSCULAR,DF_RUTINA)