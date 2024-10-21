import sqlite3
import json
import requests

configura = {
    "STATIC_FOLDERS": "static",
    "TEMPLATE_FOLDER": "templates",
    "DEBUG": True,
    "SERVER_NAME": "http://127.0.0.1",
    "SERVER_API": "http://127.0.0.1:5000",
    "PUERTOREST": 5000,
    "PUERTOAPP": 8000,
    "MODULO": "salud",
    "SMBD": "SQLITE",
    "DB": "./novedades.db"
}

class Usuario:
    
    def __init__(self, bd):
        self.bd = bd
        
    def ConsultarJson(self, sql, params=None):
        con = sqlite3.connect(self.bd)
        todo = []
        try:
            cur = con.cursor()
            if params:  # If parameters are provided, execute with them
                res = cur.execute(sql, params)
            else:
                res = cur.execute(sql)

            if cur.description is None:
                return []  # Return an empty list if there are no results

            # Get column names from the description
            nombres_columnas = [descripcion[0] for descripcion in cur.description]
            primer_resultado = res.fetchall()

            # Process each row and map it to the column names
            for valor in primer_resultado:
                aux3 = dict(zip(nombres_columnas, valor))   
                todo.append(aux3)
        finally:
            con.close() 
        return todo


    def consultarUno(self, sql):
        con = sqlite3.connect(self.bd)
        try:
            cur = con.cursor()
            res = cur.execute(sql)
            primer_resultado = res.fetchone()
            return json.dumps(primer_resultado) if primer_resultado else None
        finally:
            con.close()

    def Inserte(self, data):
        response = requests.post(self.url + "/i", json=data)
        return response.json() if response.status_code == 200 else None

    def Borra(self, cual, clave):
        try:
            response = requests.delete(self.url + clave + str(cual))
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error deleting: {e}")
            return None

    def Actualiza(self, data, clave="/u"):
        response = requests.put(self.url + clave, json=data)
        return response.json() if response.status_code == 200 else None

    def InserteAPI(self, sql):
        con = sqlite3.connect(self.bd)
        try:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            return "Registro insertado"
        finally:
            con.close()  # Ensure the connection is closed

def ListarJson(clave):    
    res = requests.get(url + clave)
    if res.status_code == 200:
        return res.json()  # Use .json() to automatically decode
    return False

def BorraAPI(cual, clave):
    try:
        response = requests.delete(url + clave + str(cual))
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f'Error occurred: {e}')
        return None

def ActualizaAPI(data, clave):
    response = requests.put(url + clave, json=data)
    return response.json() if response.status_code == 200 else None
