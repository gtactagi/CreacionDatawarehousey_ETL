import pyodbc
from pymongo import MongoClient
from datetime import datetime

# Conectar a SQL Server
conn_sql = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-NETFFJ02\\SQLEXPRESS;'
    'DATABASE=MeteorologiaDB;'
    'Trusted_Connection=yes;'
)
cursor_sql = conn_sql.cursor()

# Conectar a MongoDB
client = MongoClient('localhost', 27017)
db_mongo = client.meteorologiaDB
collection_calidad_aire = db_mongo.calidad_aire

# Conectar al Data Warehouse
conn_dw = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-NETFFJ02\\SQLEXPRESS;'
    'DATABASE=DataWarehouse;'
    'Trusted_Connection=yes;'
)
cursor_dw = conn_dw.cursor()

# Extraer datos de SQL Server
cursor_sql.execute('SELECT * FROM Temperaturas')
temperaturas = cursor_sql.fetchall()

# Extraer datos de MongoDB
calidad_aire = list(collection_calidad_aire.find())

# Transformar y cargar datos en el Data Warehouse
cursor_dw.execute('DELETE FROM DatosClimaticosDW')

for temp in temperaturas:
    ciudad = temp.Ciudad
    fecha_str = temp.Fecha  # Asumimos que es una cadena
    temp_max = temp.TemperaturaMax
    temp_min = temp.TemperaturaMin

    # Convertir `fecha_str` a un objeto `datetime`
    fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()  # Asegúrate del formato correcto

    # Encontrar el índice de calidad del aire correspondiente en MongoDB
    calidad = next(
        (item for item in calidad_aire if item['ciudad'] == ciudad and item['fecha'].date() == fecha_dt),
        None
    )

    if calidad:
        indice_calidad = calidad['indice_calidad']
    else:
        indice_calidad = None

    # Cargar datos en el Data Warehouse
    cursor_dw.execute('''
        INSERT INTO DatosClimaticosDW (Ciudad, Fecha, TemperaturaMax, TemperaturaMin, IndiceCalidadAire)
        VALUES (?, ?, ?, ?, ?)
    ''', (ciudad, fecha_str, temp_max, temp_min, indice_calidad))

conn_dw.commit()

# Cerrar conexiones
cursor_sql.close()
conn_sql.close()
cursor_dw.close()
conn_dw.close()

print("Proceso ETL completado con éxito.")
