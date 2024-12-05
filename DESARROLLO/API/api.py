from flask import Flask, jsonify,render_template,request,redirect
import pandas as pd
import requests
from flask_cors import CORS
import sqlite3
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

from sqlalchemy import null
from  services.adaptador import *
def create_app():
    app=Flask(__name__)
    CORS(app)
    return app

app = create_app() # CREATE THE FLASK APP
app.bd="novedades.db"

@app.route("/apilogin")
def datos():
    sql=f"SELECT * FROM USUARIO"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)


@app.route("/apilogin/<idUSUARIO>")
def loginn(idUSUARIO):
    sql = f"SELECT * FROM USUARIO WHERE idUSUARIO = {idUSUARIO}"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)


@app.route("/ambi")
def ambi():
    sql = "SELECT * FROM AMBIENTE WHERE IDCUENTADANTE IS NULL"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/ambippp/<id>")
def ambisss(id):
    sql = f"SELECT * FROM AMBIENTE WHERE IDCUENTADANTE = {id}"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/ambis")
def ambi2():
    sql = "SELECT * FROM AMBIENTE"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/allClassrooms")
def classrooms():
    sql = "SELECT idAMBIENTE FROM AMBIENTE"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/novedadesA/<idUSER>")
def listar(idUSER):
    sql = f"""
    SELECT 
    idNOVEDADES,
    NOMBRE as nombre,
    FECHA as fecha,
    DESCRIPCION as descripcion 
    FROM VNOVEDADUNO
    WHERE ESTADO = 0 AND idCUENTADANTE = {idUSER}
    """
    
    print(f"Executing SQL: {sql}")  # Debug output
    
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        print("No records found.")  # Log if no records found
    
    return jsonify(todo)  # Return JSON response


@app.route("/novedadesP/<idUSER>")
def listar2(idUSER):
    sql = f"""
    SELECT 
    idNOVEDADES,
    NOMBRE as nombre,
    FECHA as fecha,
    DESCRIPCION as descripcion 
    FROM VNOVEDADUNO
    WHERE ESTADO = 1 AND idCUENTADANTE = {idUSER}
    """
    
    print(f"Executing SQL: {sql}")  # Debug output
    
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        print("No records found.")  # Log if no records found
    
    return jsonify(todo)  # Return JSON response



@app.route("/novedadesC/<idUSER>")
def listar3(idUSER):
    sql = f"""
    SELECT 
    idNOVEDADES,
    NOMBRE as nombre,
    FECHA as fecha,
    DESCRIPCION as descripcion ,
    ESTADO as estado
    FROM VNOVEDADUNO
    WHERE ESTADO = 2 AND idCUENTADANTE = {idUSER}
    """
    
    print(f"Executing SQL: {sql}")  # Debug output
    
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        print("No records found.")  # Log if no records found
    
    return jsonify(todo)  # Return JSON response

@app.route("/ss")
def listarOne(ambi):    
    sql="select * from vambiente where idambiente="+ambi+""
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)
def FEstado(estado):
    estado=estado.upper()
    if estado=="A":
        estado="ABIERTA"
    elif estado=="P":
        estado="PROCESO"
    elif estado=="C":
        estado="CERRADA"
    return estado
    
@app.route("/ln/<estado>/<amb>")
def listarNovXamb(estado,amb):
    estado=FEstado(estado)
    if amb !="0":
        sql="select * from VNOVEDAD where estados='"+estado+"' and idambiente="+amb+" and padre=idnovedades"
        print(sql)
    else:
        sql="select * from vambiente where estado='"+estado+"'"
    print(sql)    
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/ln/l/<novedad>")
def listarNovedad(novedad): 
     sql="select * from VNOVEDAD where padre="+novedad
     u1=Usuario(app.bd)
     todo=u1.ConsultarJson(sql)
     return(todo)     

@app.route("/e/<amb>")
def equiparesumen(amb):    
    if amb !="0":
        sql="select * from EQUIRESUMEN where  idambiente="+amb
    else:
       sql="select * from EQUIRESUMEN" 
    
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)
@app.route("/e/a/<amb>")
def equipamiento(amb):    
    if amb !="0":
        sql="select * from VEQUIPAMIENTO where  idambiente="+amb
    else:
       sql="select * from VEQUIPAMIENTO" 
    
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)


@app.route("/allElements/<idUSER>", methods=['GET'])
def allEle(idUSER):
    sql = f"""
    SELECT DISTINCT
    equi.idEQUIPAMIENTO,
    equi.idAMBIENTE,
    equi.idTIPOELEMENTO as idTIPOELEMENTO,
    equi.ESTADO as estado,
    equi.SERIAL as serial,
    equi.ESTACION as estacion
    FROM EQUIPAMIENTO equi
    JOIN AMBIENTE a ON equi.idAMBIENTE = a.idAMBIENTE
    WHERE a.idCUENTADANTE = {idUSER};
    """
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    # Ensure the result is a valid JSON response
    if todo is None:
        return jsonify({"error": "No data found"}), 404
    
    return jsonify(todo)

#getting one element to edit
@app.route("/editEle/<ele>", methods = ['GET'])
def allEle2(ele):
    sql = f"""    
    SELECT DISTINCT
    idEQUIPAMIENTO,
    idAMBIENTE,
    idTIPOELEMENTO as tipo,
    ESTADO as estado,
    SERIAL as serial,
    ESTACION as estacion FROM equipamiento equi WHERE idEQUIPAMIENTO = {ele}"""
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        return jsonify({"error": "No data found for the given ID"}), 404
    
    return jsonify(todo)

#EDIT THE ELEMENT
# @app.route("/elemento/u", methods = ['PUT'])
# def EditaElemento():
#     datos = request.get_json()
#     id = datos['idEQUIPAMIENTO']
#     idAMBIENTE = datos['idAMBIENTE']
#     idTIPOELEMENTO = datos['idTIPOELEMENTO']
#     NOMBRE = datos['nombre']
#     ESTADO = datos['estado']
#     SERIAL = datos['serial']
#     ESTACION = datos['estacion']
#     OBSERVACION = datos['observacion']
#     sql = "UPDATE EQUIPAMIENTO SET nombrePT = '"+nombrePT+"' WHERE idPuestoTrabajo = "+str(id)
#     try:
#         con = sqlite3.connect("novedades.db")
#         todo = con.Ejecutar("novedades.db", sql)
#         return "OK"
#     except Exception as e:
#         print("An error occurred:", str(e))
#         return "Error: Internal Server Error"

@app.route("/allEle")
def allElle():
    sql = "SELECT * FROM VEQUIPAMIENTO"
    ele = Usuario(app.bd)
    todo = ele.ConsultarJson(sql)
    return (todo)  

@app.route("/tipoElementos")
def tipoEle():
    sql = "SELECT * FROM TIPOELEMENTO"
    ele = Usuario(app.bd)
    todo = ele.ConsultarJson(sql)
    return (todo)

@app.route("/elem/<amb>/<e>/<n>")
def elemento(amb,e,n):    
    if amb !="0":
        a = f"select * from VEQUIPAMIENTO where AMBIENTE='{amb}' AND ESTACION='{e}' AND TIPO='{n}'"
        sql= a
    else:
       sql="select * from VEQUIPAMIENTO" 
    print(sql)
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    print(todo)
    return json.dumps(todo)

@app.route("/busca/<tap>/<id>")
def Consult(tap,id):
    a=f'select * from {tap} WHERE id_Ambiente= {id} '
    sql=a
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    print(todo)
    return json.dumps(todo)

# consultar x datos x tablas
@app.route("/items/<amb>")
def infoD(amb):    
    if amb =="1":
        a = f"select * from AMBIENTE2 "
        sql= a
    elif amb=="0":
        a = f"select * from AMBIENTE"
        sql= a
    else:
       sql="select * from AMBIENTE" 
    print(sql)
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    print(todo)
    return todo

@app.route("/n/<nove>")
def actualizanov(nove):    
    sql="select *,(select count(*) cantidad from novedades n where n.idNOVEDADES=v.idNOVEDADES ) CANTNOV from VNOVEDADUNO v where  v.idNOVEDADES="+nove    
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

@app.route("/elem/ambiente2/<col>/<dat>")
def ambiente2(col,dat):    
    sql="select * from AMBIENTE2 where "+col+"='"+dat+"'"
    u1=Usuario(app.bd)
    todo=u1.consultarUno(sql)
    return(todo)
#CODIGO PARA INSERTAR / DAVID
#INSERTAR REGISTER
@app.route("/i", methods=['POST'])
def InserteUsuario():
    accountant = 2
    datos = request.get_json()
    nombre = datos['nombre']
    rol = accountant
    cedula = datos['cedula']
    email = datos['email']
    password = datos['password']

    sql = "INSERT INTO USUARIO (nombre, rol, cedula, email, password) VALUES (?, ?, ?, ?, ?)"
    con = sqlite3.connect("novedades.db")
    cursor = con.cursor()

    try:
        cursor.execute(sql, (nombre, rol, cedula, email, password))
        con.commit()
        user_id = cursor.lastrowid
        return jsonify({"id": user_id, "message": "User inserted successfully"}), 200 # Return the ID
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        con.close()


#ACUTALIZAR ID
@app.route("/actualizar", methods=['PUT', 'POST'])
def Actu():
    datos = request.get_json()
    
    if not datos or 'user_id' not in datos or 'ambiente_id' not in datos:
        return jsonify({"error": "Invalid input"}), 400

    user_id = datos['user_id']
    ambiente_id = datos['ambiente_id']
    
    sql = "UPDATE AMBIENTE SET IDCUENTADANTE = ? WHERE idAMBIENTE = ?"
    print(f"Executing SQL: {sql} with data: {user_id}, {ambiente_id}")

    con = sqlite3.connect("novedades.db")
    cursor = con.cursor()
    
    try:
        cursor.execute(sql, (user_id, ambiente_id))
        con.commit()
        return jsonify({"message": "Assignment successful"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        con.close()



@app.route("/pp", methods = ['POST'])
def jjj():
    sql = ""

#ASIGNAR AMBIENTE
@app.route("/asigamb", methods = ['UPDATE'])
def AsigAmb():
    datos=request.get_json()
    id=datos['id']
    amb=datos['amb']
    sql="update USUARIO set ambasing="+amb+" where Id_regis="+id
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()
    return(sql)

#INSERTAR EQUIPAMIENTO
@app.route("/i/e", methods=['POST'])
def InsertEqui():
    idAMBIENTE = request.form['idAMBIENTE']
    idTIPOELEMENTO = request.form['idTIPOELEMENTO']
    estado = request.form['estado']
    serial = request.form['serial']
    estacion = request.form['estacion']
    observacion = None

    con = sqlite3.connect("novedades.db", timeout=2)
    cursor = con.cursor()

    try:
        sql = """
        INSERT INTO EQUIPAMIENTO (idAMBIENTE, idTIPOELEMENTO, ESTADO, SERIAL, ESTACION, OBSERVACION)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, (idAMBIENTE, idTIPOELEMENTO, estado, serial, estacion, observacion))
        con.commit()
        print("Insert successful")
    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return "Database error", 500
    finally:
        con.close()  # Ensure connection is closed

    return "Insert successful"



@app.route("/massive/load", methods=["POST","GET"])
def massive_load():
    file = request.files.get('myfile')
    if file and (file.filename.endswith('.xls') or file.filename.endswith('.xlsx')):
        df = pd.read_excel(file)
        conn = sqlite3.connect("novedades.db")  
        cursor = conn.cursor()

        for _, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO EQUIPAMIENTO (idAMBIENTE, idTIPOELEMENTO, ESTADO, SERIAL, ESTACION, OBSERVACION)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['idAMBIENTE'],
                        row['idTIPOELEMENTO'],
                        row['ESTADO'],
                        row['SERIAL'],
                        row['ESTACION'],
                        row['OBSERVACION']
                    ))

        conn.commit()
        conn.close()
        return "Insert successful"



from datetime import datetime
import sqlite3
from flask import request, jsonify


# Function to send the email
def send_email(to_email, subject, body):
    try:
        sender_email = "" #Mi email
        sender_password = "" #Mi contraseña de las apps de Google
        smtp_server = "smtp.gmail.com" #Gmail
        smtp_port = 587 #Puerto de Gmail

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        #CONFIGURACION PARA ENVIAR EMAIL
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, to_email, message.as_string())
        server.close()

        print("Email sent successfully")

    except Exception as e:
        print(f"Error sending email: {e}")


#INSERTAR UNA NOVEDAD POR CONSOLA
@app.route("/newNovelty", methods=['POST'])
def newNovelty():
    idNovedades = 52
    idAMBIENTE = 3
    current_date = datetime.now()
    current_date_without_ms = current_date.replace(microsecond=0)
    DESCRIPCION = 'prueba con correo 3'
    ESTADO = 0
    PADRE = None

    con = sqlite3.connect("novedades.db", timeout=5)
    cursor = con.cursor()

    try:
        sql = """
        INSERT INTO NOVEDADES (idNovedades, idAMBIENTE, FECHA, DESCRIPCION, ESTADO, PADRE)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (idNovedades, idAMBIENTE, current_date_without_ms, DESCRIPCION, ESTADO, PADRE))
        con.commit()
        print("Insert successful")

        cursor.execute("SELECT IDCUENTADANTE FROM AMBIENTE WHERE idAMBIENTE = ?", (idAMBIENTE,))
        accountant_id = cursor.fetchone()

        if accountant_id:
            cursor.execute("SELECT email FROM USUARIO WHERE idUSUARIO = ? AND rol = 2", (accountant_id[0],))
            accountant_email = cursor.fetchone()

            if accountant_email:
                subject = "Nueva novedad insertada"
                body = f"Una nueva novedad ha sido agregada:\n\nID: {idNovedades}\nDescripción: {DESCRIPCION}\nFecha: {current_date_without_ms}"
                send_email(accountant_email[0], subject, body)
            else:
                print(f"No accountant found for ID {accountant_id[0]}")
        else:
            print(f"No accountant associated with classroom ID {idAMBIENTE}")

    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return "Database error", 500

    finally:
        con.close()

    return "Insert and email sent successfully"

    

@app.route("/n/i", methods=['POST'])
def CrearNoved():
    datos = request.get_json()
    idA = datos['idAMBIENTE']
    idN = datos['idNOVEDADES']
    descri = datos['DESCRIPCION']
    estado = datos['ESTADO']
    current_date = datetime.now()
    current_date_without_ms = current_date.replace(microsecond=0)

    con = sqlite3.connect("novedades.db")
    cursor = con.cursor()

    # Update the existing novelty's status and description
    if estado > 0:
        sql2 = "UPDATE NOVEDADES SET ESTADO = 1, DESCRIPCION = ?, FECHA = ? WHERE idNOVEDADES = ?"
        cursor.execute(sql2, (descri, current_date_without_ms, idN))
    else:
        sql2 = "UPDATE NOVEDADES SET ESTADO = 1, DESCRIPCION = ?, FECHA = ? WHERE idNOVEDADES = ?"
        cursor.execute(sql2, (descri, current_date_without_ms, idN))

    con.commit()
    con.close()
    return "Updated novelty to in-process."

@app.route("/n/d", methods=['POST'])
def CerrarNoved():
    datos = request.get_json()
    idA = datos['idAMBIENTE']
    idN = datos['idNOVEDADES']
    descri = datos['DESCRIPCION']
    current_date = datetime.now()
    current_date_without_ms = current_date.replace(microsecond=0)

    con = sqlite3.connect("novedades.db")
    cursor = con.cursor()

    # Update the existing novelty to closed status and append '[CERRADA]' to description
    sql2 = "UPDATE NOVEDADES SET ESTADO = 2, DESCRIPCION = ?, FECHA = ? WHERE idNOVEDADES = ?"
    cursor.execute(sql2, (descri, current_date_without_ms, idN))

    con.commit()
    con.close()
    return "Updated novelty to closed."




@app.route("/nov/proceso", methods = ['GET'])
def novProceso():
    sql = "SELECT * FROM NOVEDADES WHERE ESTADO = 1"
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()
    return(sql)


@app.route("/delete/novedades", methods=['DELETE'])
def deleteAll():
    sql = "DELETE FROM NOVEDADES"
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()
    return(sql)

    
  
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)