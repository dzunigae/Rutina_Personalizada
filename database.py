import sqlite3
import pandas as pd

DF_INFORMACION_EJERCICIOS = pd.read_excel('./Modelo.xlsx')

DF_GRUPO = pd.DataFrame(columns=['Id', 'Nombre'])
DF_IDENTIFICADOR_RUTINA = pd.DataFrame(columns=['Id', 'Indicador', 'Frecuencia'])
DF_EJERCICIO = DF_GRUPO = pd.DataFrame(columns=['Id', 'Nombre', 'Nivel', 'Pagina', 'Repeticiones', 'Equipo', 'Peso', 'Tiempo', 'Frecuencia'])

def trabajo_pd():
    print(DF_INFORMACION_EJERCICIOS)

trabajo_pd()