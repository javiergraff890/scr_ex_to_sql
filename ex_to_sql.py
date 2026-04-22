import pandas as p
import mysql.connector

#archivo origen que esta en la raiz
archivo = "data.xlsx"

#variables para conexion en la bd
conexion = None
cursor = None

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",     
        database="words_en"
    )

    cursor = conexion.cursor()

    df = p.read_excel(archivo, sheet_name="an_insider")

    #solo cargo las variables que estan en el excel, las que me interesan
    sql = """
        INSERT INTO translations (termino, pron, traduccion, contexto)
        VALUES (%s, %s, %s, %s)
        """
    
    for _, fila in df.iterrows():
        valores = (fila["termino"], fila["pron"], fila["traduccion"], fila["contexto"] )
        cursor.execute(sql, valores)

    conexion.commit()

except Exception as e:
    print("Error: ",e)

    if conexion:
        conexion.rollback()
    
finally:
    if cursor:
        cursor.close()
    if conexion:
        conexion.close()