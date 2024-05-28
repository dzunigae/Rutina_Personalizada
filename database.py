import sqlite3
import pandas as pd
import math

# Modelo con los datos
DF_INFORMACION_EJERCICIOS = pd.read_excel('./Modelo.xlsx')

# Data frames con los datos para pasarlos a la base de datos
DF_GRUPO = pd.DataFrame(columns=['Nombre'])
DF_IDENTIFICADOR_RUTINA = pd.DataFrame(columns=['Indicador', 'Frecuencia'])
DF_EJERCICIO = pd.DataFrame(columns=['Nombre', 'Nivel', 'Pagina', 'Repeticiones', 'Equipo', 'Peso', 'Tiempo', 'Frecuencia'])
DF_MUSCULO = pd.DataFrame(columns=['Nombre', 'Grupo', 'Frecuencia'])
DF_TRABAJO_MUSCULAR = pd.DataFrame(columns=['Ejercicio', 'Musculo'])
DF_RUTINA = pd.DataFrame(columns=['Rutina', 'Grupo'])
DF_REGISTRO = pd.DataFrame(columns=['Fecha','Rutina','Tiempo'])

# Estructuras de datos
grupos = set()

def trabajo_pd(DF_GRUPO,DF_IDENTIFICADOR_RUTINA):
    #GRUPO
    grupos = set(DF_INFORMACION_EJERCICIOS.loc[0].tolist())
    grupos = {x for x in grupos if not isinstance(x, float)}
    grupos.remove('Biceps - Triceps')
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

    print(DF_IDENTIFICADOR_RUTINA)

trabajo_pd(DF_GRUPO,DF_IDENTIFICADOR_RUTINA)