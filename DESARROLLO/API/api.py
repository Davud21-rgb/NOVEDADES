from flask import Flask,render_template,request,redirect
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
app.bd="nov.db"

@app.route("/apilogin/<dat>")
def datos(dat):
    sql=f"select * from REGISTER where email='{dat}'"
    u1=Usuario(app.bd)
    todo=u1.consultarUno(sql)
    return(todo)
    

@app.route("/ln")
def listar():    
    
    sql="select * from vambiente"  #usuarios where corroe={2}   if 
    u1=Usuario(app.bd)
    todo=u1.ConsultarJson(sql)
    return(todo)
     
    # return json.dumps(todo)
@app.route("/ln/<ambi>")
def listarOne(ambi):    
    
    sql="select * from vambiente where idambiente="+ambi+" and padre is null"
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
    if amb !="0":
        a = f"select "
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
#CODIGO PARA INSERTAR / DAVID
#INSERTAR REGISTER
@app.route("/i/r", methods = ['POST'])
def InsertRegis():
    datos=request.get_json()
    email=datos['email']
    password=datos['password']
    sql="insert into REGISTER values (null, '"+email+"','"+password+"','1')"
    con=sqlite3.connect("nov.db")  
    cursor=con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()
    return(sql)
#INSERTAR EQUIPAMIENTO
@app.route("/i/e" ,methods = ['POST'])
def InsertEqui(): 
        datos=request.get_json()
        ambie=datos['ambiente']
        tip=datos['tipo']
        tipo= str(tip)
        estado=datos['estado']
        seri=datos['serial']
        estacion=datos['estaciones']
        a = f"insert into EQUIPAMIENTO values(null, {ambie},{tipo},{estado},{seri}, {estacion})"
        sql= a
        print(sql)
        con=sqlite3.connect("nov.db")  
        cursor=con.cursor()
        cursor.execute(f"insert into EQUIPAMIENTO values(null, {ambie},{tipo},{estado},{seri}, {estacion})")
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
    con=sqlite3.connect("nov.db")  
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
    con=sqlite3.connect("nov.db")  
    cursor=con.cursor()
    sql2="update NOVEDADES set ESTADO=2,DESCRIPCION=concat(DESCRIPCION,'[CERRADA]')  where PADRE="+str(idN)
    cursor.execute(sql1)
    cursor.execute(sql2)
    con.commit()
    con.close()
    print(sql1)
    return(sql2)
    
  
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)