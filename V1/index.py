import pandas as pd

# Cargar el archivo Excel
df = pd.read_excel('./V1/Modelo_produccion.xlsx')

# Guardar el DataFrame en un nuevo archivo Excel
df.to_excel('./V1/archivo_salida.xlsx', index=False)