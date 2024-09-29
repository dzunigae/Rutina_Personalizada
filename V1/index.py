import pandas as pd

#Variables
rutinas = {
    'A': ['Pecho','Abdomen'],
    'B': ['Biceps','Triceps','Abdomen'],
    'C': ['Pecho','Biceps','Triceps'],
    'D': ['Biceps','Triceps','Hombros'],
    'E': ['Espalda','Hombros','Abdomen'],
    'F': ['Pecho','Espalda','Abdomen'],
    'G': ['Espalda','Abdomen'],
    'H': ['Pecho','Espalda','Hombros'],
    'I': ['Piernas','Pantorrillas','Abdomen'],
    'J': ['Gluteos','Pantorrillas','Abdomen']
}

# Cargar el archivo Excel
df = pd.read_excel('./V1/Modelo_produccion.xlsx')

#1. Verificación de que tipo de rutina toca hoy (Tronco superior o inferior - El sistema es dos rutinas de tren 
#superior y una de tren inferior), la sesión de tren inferior se dará en cada sesión múltiplo de 3.
sesion = df.loc[0,'Sesion']

if (sesion+3) % 3 == 0: #Rutina tren inferior
    #2. Se escoje la rutina que menos se haya hecho hasta el momento, en caso de haber empate, se hace al azar.
    frecuencia_rutinas = df.loc[0,list(rutinas.keys())]
    print(frecuencia_rutinas)

    #grupos_musculares = ['Piernas', 'Gluteos', 'Pantorrillas', 'Abdomen']
    #frecuencia_grupos_musculares = df.loc[0,grupos_musculares].to_dict()
    #print(frecuencia_grupos_musculares)
else: #Rutina tren superior
    grupos_musculares = ['Abdomen', 'Pecho', 'Biceps', 'Triceps', 'Espalda', 'Hombros']

# Guardar el DataFrame en un nuevo archivo Excel
#df.to_excel('./V1/archivo_salida.xlsx', index=False)