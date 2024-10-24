from flask import Flask, jsonify,render_template,request,redirect
import requests
from flask_cors import CORS
import sqlite3
import json
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

@app.route("/novedadesA")
def listar():
    sql = """
    SELECT DISTINCT
        n.idNOVEDADES,
        e.ESTACION AS estacion,
        n.FECHA AS fecha,
        n.DESCRIPCION AS descripcion
    FROM NOVEDADES n
    JOIN AMBIENTE a ON n.idAMBIENTE = a.idAMBIENTE
    JOIN EQUIPAMIENTO e ON a.idAMBIENTE = e.idAMBIENTE
    WHERE n.ESTADO = 0;
    """
    
    print(f"Executing SQL: {sql}")  # Debug output
    
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        print("No records found.")  # Log if no records found
    
    return jsonify(todo)  # Return JSON response


@app.route("/novedadesP")
def listar2():
    sql = """
    SELECT DISTINCT
        n.idNOVEDADES,
        e.ESTACION AS estacion,
        n.FECHA AS fecha,
        n.DESCRIPCION AS descripcion,
        e.OBSERVACION AS observacion
    FROM NOVEDADES n
    JOIN AMBIENTE a ON n.idAMBIENTE = a.idAMBIENTE
    JOIN EQUIPAMIENTO e ON a.idAMBIENTE = e.idAMBIENTE
    WHERE n.ESTADO = 1;
    """
    
    print(f"Executing SQL: {sql}")  # Debug output
    
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    
    if not todo:
        print("No records found.")  # Log if no records found
    
    return jsonify(todo)  # Return JSON response



@app.route("/novedadesC")
def listar3():
    sql = """
    SELECT DISTINCT
        n.idNOVEDADES,
        e.ESTACION AS estacion,
        n.FECHA AS fecha,
        n.DESCRIPCION AS descripcion,
        v.ESTADO AS estado
    FROM NOVEDADES n
    JOIN AMBIENTE a ON n.idAMBIENTE = a.idAMBIENTE
    JOIN EQUIPAMIENTO e ON a.idAMBIENTE = e.idAMBIENTE
    JOIN VAMBIENTE v ON n.idNOVEDADES = v.idNOVEDADES
    WHERE v.ESTADO = 'CERRADA';
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
    
    # estado=estado.upper()
    # if estado=="A":
    #     estado="ABIERTA"
    # elif estado=="P":
    #     estado="PROCESO"
    # elif estado=="C":
    #     estado="CERRADA"
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


@app.route("/allElements")
def allEle():
    sql = "select * from VEQUIPAMIENTO"
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)

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
    sql="select *,(select count(*) cantidad from novedades n  where n.idnovedades=v.idnovedades ) CANTNOV from VNOVEDADUNO v where  v.idnovedades="+nove    
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
    datos = request.get_json()
    nombre = datos['nombre']
    rol = datos['rol']
    email = datos['email']
    password = datos['password']

    sql = "INSERT INTO USUARIO (nombre, rol, email, password) VALUES (?, ?, ?, ?)"
    con = sqlite3.connect("novedades.db")
    cursor = con.cursor()

    try:
        cursor.execute(sql, (nombre, rol, email, password))
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
@app.route("/i/e" ,methods = ['POST'])
def InsertEqui(): 
        datos=request.get_json()
        ambiente=datos['ambiente']
        nombre=datos['nombre']  
        estado=datos['estado']
        serial=datos['serial']
        estacion=datos['estacion']
        # a = f"insert into EQUIPAMIENTO values(null, {ambie},{tip},{estado},{seri}, {estacion})"
        # sql= a
        # 
        con=sqlite3.connect("novedades.db")  
        cursor=con.cursor()
        
        sql=f"insert into EQUIPAMIENTO (idAMBIENTE,nombre,estado,serial,estacion) values( {ambiente},{nombre},{estado},'{serial}', {estacion})"
        print(sql)
        cursor.execute(sql)
        con.commit()
        con.close()
        return(sql)


@app.route("/n/i",methods = ['POST'])
def CrearNoved(): 
    
    datos=request.get_json()
    idA=datos['idAMBIENTE']
    idN=datos['idNOVEDADES']
    descri=datos['DESCRIPCION'].upper()
    descri1=datos['DESCRI1'].upper()
    estado=datos['ESTADO']
    padre=datos['PADRE']
    match = descri1.rfind   ("[PROCESO]")
    sql1="insert into NOVEDADES(idAMBIENTE, DESCRIPCION, ESTADO,PADRE) values("+str(idA)+",'"+descri+"',1,"+str(idN)+")"
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()

    if match>0:
        sql2="update NOVEDADES set ESTADO=1,DESCRIPCION=concat(DESCRIPCION,'') where idNOVEDADES="+str(idN)
    else:
        sql2="update NOVEDADES set ESTADO=1,DESCRIPCION=concat(DESCRIPCION,'[PROCESO]') where idNOVEDADES="+str(idN)
    print("-**********>",descri,match)
    
    cursor.execute(sql1)
    cursor.execute(sql2)
    con.commit()
    con.close()
    print(sql1)
    return(sql2)
@app.route("/n/d",methods = ['POST'])
def CerrarNoved(): 
    
    datos=request.get_json()
    idA=datos['idAMBIENTE']
    idN=datos['idNOVEDADES']
    descri=datos['DESCRPCION'].upper()
    estado=datos['ESTADO']
    padre=datos['PADRE']
    sql1="insert into NOVEDADES(idAMBIENTE, DESCRIPCION, ESTADO,PADRE) values("+str(idA)+",'"+descri+"',2,"+str(idN)+")"
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()
    sql2="update NOVEDADES set ESTADO=2,DESCRIPCION=concat(DESCRIPCION,'[CERRADA]')  where PADRE="+str(idN)
    cursor.execute(sql1)
    cursor.execute(sql2)
    con.commit()
    con.close()
    print(sql1)
    return(sql2)


@app.route("/nov/proceso", methods = ['GET'])
def novProceso():
    sql = "SELECT * FROM NOVEDADES WHERE ESTADO = 1"
    con=sqlite3.connect("novedades.db")  
    cursor=con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()
    return(sql)


    
  
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)