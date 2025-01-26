import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import os
import chardet
import platform

server = platform.node()
database = 'Upysusa'
driver = 'ODBC Driver 17 for SQL Server'

tablelperlevel = [['SUCURSALES','PROVEEDORES','CATALOGO_GASTOS','TURNO','ESTATUS','PUESTO'],
                  ['PRODUCTOS','COMPRAS','GASTOS','CAJAS','EMPLEADOS'],
                  ['COMPRA_POR_PRODUCTO','ALMACEN_POR_SUCURSAL','TICKETS'],
                  ['TICKETS_DETALLE']]

for level in tablelperlevel:
    for table in level:
        with open(f'./csvs/{table}.csv','rb') as f:
            analysis = chardet.detect(f.read())#Lee el codigo para detectar su encoding y evitar problemas de "traduccion" con el dataframe(culpa de Moi)
            encoding = analysis['encoding']
        
            df = pd.read_csv(f'./csvs/{table}.csv', encoding=encoding) #convierte el csv en un dataframe

            conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes')#Establece la conexion
            table_name = table.split('.')[0]

            cursor = conn.cursor()
            engine = create_engine('mssql+pyodbc://', creator=lambda: conn)
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)#Inserta los datos en el csv a la tabla en sql

            conn.close()#ceirra conexion
            print(f"Se han agregado los datos del CSV a la tabla '{table_name}' en la base de datos '{database}'.")