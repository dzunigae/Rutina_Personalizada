import sqlite3
import pandas as pd

DF_INFORMACION_EJERCICIOS = pd.read_excel('./Modelo.xlsx')

def trabajo_pd():
    print(DF_INFORMACION_EJERCICIOS)

trabajo_pd()