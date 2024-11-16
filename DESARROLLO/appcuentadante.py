from flask import Flask,render_template,request, redirect, url_for, flash, session, g
import requests
from flask_cors import CORS
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
import time

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

import pandas as pd
import os


from flask_mail import Mail, Message
mail = Mail()


def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='AWFSDGF134VDS'
    )

    mail.init_app(app)
       
    return app
app = create_app() # CREATE THE FLASK APP
app.ruta="http://127.0.0.1:8000"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Login(UserMixin):
    def __init__(self, data):
        self.email = data['email']
        self.idUSUARIO = data['idUSUARIO']
        self.nombre = data['nombre']
        self.password = data['password']
        self.rol = data['rol']


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.idUSUARIO)

class Usuario:
    
    res=None
    data=None
    def __init__(self):
        self.url=app.ruta
        print("---->",app.ruta)


    def ListarTodos(self,clave="/ln"):
        self.res=requests.get(self.url+clave)
        data1=json.loads(self.res.content)
        return data1
    
    def ListarUno_a(self,cual):    
        self.res=requests.get(self.url+"/ppa/"+str(cual))
        data1=json.loads(self.res.content)
        if data1!=[]:
            return(data1)
        else:
            return False  
    def ListarJson(self,clave):    
        self.res=requests.get(self.url+clave)
        data1=json.loads(self.res.content)
        if data1!=[]:
            return(data1)
        else:
            return False  
        
    def Consultlogin(self, dat, clave="/apilogin/"):
        try:
            self.res = requests.get(self.url + clave + dat)
            if self.res.status_code == 200:
                try:
                    data1 = json.loads(self.res.content)
                    return data1
                except json.JSONDecodeError:
                    print("Error decoding JSON, response is not valid JSON.")
                    return None
            else:
                print(f"Error: Received status code {self.res.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
    def ambientes(self, clave="/ambi"):
        self.res = requests.get(self.url + clave)
        data1 = json.loads(self.res.content)
        return data1
    
    def ambientesss(self, clave="/ambis"):
        self.res = requests.get(self.url + clave, timeout=5)
        data1 = json.loads(self.res.content)
        return data1
    
    def elem(self,clave="/tipoElementos"):
        self.res = requests.get(self.url+clave, timeout=5)
        data1 = json.loads(self.res.content)
        return data1
    
    def allEle(self,clave="/allEle"):
        self.res = requests.get(self.url+clave)
        data = json.loads(self.res.content)
        return data
    
    def ConsultAmbi(self, dat, e, n, clave="/elem/"):
        extend= f"{dat}/{e}/{n}"
        self.res=requests.get(self.url+clave+extend)
        data1=json.loads(self.res.content)
        print('se ejecuto correctamente')
        print(data1)
        return data1
    def ConNovel(self, dat, clave="/items/"):
        self.res=requests.get(self.url+clave+dat)
        data1=json.loads(self.res.content)
        return data1

    def AsignarAmbiente(self, data, clave="/actualizar"):
        self.res = requests.put(self.url + clave, json=data)
        print(f"Response Status Code: {self.res.status_code}")
        print("Response Content:", self.res.content)

        if self.res.status_code == 200:
            try:
                return json.loads(self.res.content)
            except json.JSONDecodeError:
                print("Error decoding JSON, response content:", self.res.content)
                return None
        else:
            print(f"Error: Received status code {self.res.status_code}")
            return None


    # va al api 8000:/i/.. dependiendo lo que traiga clave
    def Inserte(self, dat, clave="/i"):
        self.res = requests.post(self.url + clave, json=dat)
        
        if self.res.status_code == 200:
            try:
                return json.loads(self.res.content).get('id')
            except json.JSONDecodeError:
                print("Error decoding JSON, response content:", self.res.content)
                return None
        else:
            print(f"An error occurred: {self.res.text}")
            return None
        

    def InserteElementos(self, dat):
        response = requests.post(self.url+"/i/e", json=dat)


    def Borra(self,cual,clave):
        response = requests.delete(self.url+clave+str(cual))
    def Actualiza(self,data,clave="/u"):
        response = requests.put(self.url+clave, json=data)
    #codigo david
    def espera(self, x):
        
        print('passaron dos segundos')
        time.sleep(3)
        return 'valimos verga'       
    
    def novedada(self, clave="/novedadesA"):
        self.res = requests.get(self.url + clave)
        data = json.loads(self.res.content)
        return data
    
    
        
@app.route("/register", methods=['POST', 'GET'])
def register():
    u = Usuario()
    a = u.ambientes()

    if request.method == 'POST':
        nombre = request.form["nombre"]
        rol = request.form["rol"]
        email = request.form["email"]
        password = request.form["password"]
        id_ambiente = request.form["ambiente"]

        if not email or not password:
            mensaje = "Faltan datos"
            flash(mensaje)
            return redirect(url_for("register"))

        user_data = {
            "nombre": nombre,
            "rol": rol,
            "email": email,
            "password": password
        }

        u1 = Usuario()
        existing_user = u1.Consultlogin(email)
        if existing_user is None:
            user_id = u1.Inserte(user_data)
            if user_id is not None:
                mensaje = "Usuario registrado correctamente"
                flash(mensaje)

                if id_ambiente:
                    data_to_assign = {
                        "user_id": user_id,
                        "ambiente_id": id_ambiente
                    }
                    result = u1.AsignarAmbiente(data_to_assign)
                    if result is None:
                        flash("Error assigning the environment.")
            else:
                flash("Error inserting the user.")
    return render_template("register.html", a=a)


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        passwords = request.form.get("password")

        u1 = Usuario()
        cadena = u1.ListarJson("/apilogin")
        cuentadante_encontrado = False

        for c in cadena:
            if len(c) >= 5 and email == c['email'] and passwords == c['password']:
                if c['rol'] == 2:
                    user = Login(c)
                    login_user(user)
                    cuentadante_encontrado = True
                    break
                else:
                    flash(f"El instructor con el email... {c['email']} NO es un cuentadante.")
                    return redirect(url_for("login"))

        if cuentadante_encontrado:
            return redirect(url_for('home'))
        else:
            flash("The email or password is incorrect")
            return redirect(url_for("login"))

    return render_template("login.html")





#Asignacion de ambientes
@app.route("/asignacion", methods=['GET', 'POST'])
def asignacion():
    dat=session['id_user']
    u1 = Usuario()
    if request.method == 'POST':
        asignado = request.form["asignado"]
        user_data = {
             "ambiente": asignado
        }
        print(asignado)
        print(dat)
        u1.AsiAmbi(user_data, dat)
    return render_template("asignar.html")
@app.route("/noasig", methods=['GET', 'POST'])
def dirigir():
    id=session['id_user']
    u1 = Usuario()
    c=u1.ConsultAmbi('ambiente2','IDCUENTADANTE',id)
    if c == None:
        return redirect(url_for("asignacion"))
    else:
        return redirect(url_for("inicio"))
    
        
@app.route("/nuevo_elemento", methods=['GET', 'POST'])
def nuevo_elemento():
    u1=Usuario()
    am = u1.ambientesss()
    e =u1.elem()
    return render_template("nuevo_elemento.html",am=am,e=e)
        

@app.route("/home")
@login_required
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    current_user_id = session.get('user_id')
    if current_user_id:
        lulo = requests.get(f"http://127.0.0.1:8000/ambippp/{current_user_id}").json()
        classroom_names = [a['nombre'] for a in lulo]
        return render_template("menu.html", classroom_names=classroom_names)
    
# @app.route("/delete")
# def d():
#     dele = requests.delete("http://127.0.0.1:8000/delete/novedades")
#     return render_template("menu.html", dele=dele)

@app.route("/banner")
def banner():
    return render_template("banner.html")
@app.route("/centro")
def centro():
    return render_template("centro.html")

def homeInstru():
    return render_template("centro.html")

@app.route("/inventario")
def inventario():
    return render_template("inventario.html")

@app.route("/footer")
def footer():
    return render_template("footer.html")

@app.route("/novedada", methods=["GET", "POST"])
@login_required
def ada():
    idUSER = session.get('user_id')
    a=requests.get(f"http://127.0.0.1:8000/novedadesA/{idUSER}").json()
    msg = "NOVEDADES ABIERTAS"
    return render_template("novedades.html", msg=msg,a=a)

@app.route("/novedadp")
@login_required
def novedadp():
    idUSER = session.get('user_id')
    cadena=requests.get(F"http://127.0.0.1:8000/novedadesP/{idUSER}").json()
    msg="NOVEDADES EN PROCESO"
    print (cadena)
    return render_template("PROCESO.html",msg=msg,cadena=cadena)

@app.route("/novedadc")
@login_required
def novedadc():
    idUSER = session.get('user_id')
    cadena=requests.get(f"http://127.0.0.1:8000/novedadesC/{idUSER}").json()
    print (cadena)
    msg="NOVEDADES EN CERRADAS"
    return render_template("CERRADAS.html",msg=msg,cadena=cadena)

@app.route("/r/<amb>")
@login_required
def resumen(amb):
    u1=Usuario()
    cadena=u1.ListarJson("/e/1")
    llenos=1
    msg="RESUMEN EQUIPAMIENTO DEL AMBIENTE"
    if cadena==False:
        return render_template("resumen.html",cadena=cadena,hay=0,msg=msg)
    return render_template("resumen.html",cadena=cadena,hay=1,msg=msg)

@app.route("/r2")
@login_required
def resumen2():
    u1=Usuario()
    cadena=u1.ListarJson("/e/1")
    llenos=1
    msg="RESUMEN EQUIPAMIENTO DEL AMBIENTE"
    return render_template("resumen.html",cadena=cadena,hay=1,msg=msg)


@app.route("/ele")
@login_required
def equipamiento2():
    idUSER = session.get('user_id')
    elementos=requests.get(f"http://127.0.0.1:8000/allElements/{idUSER}").json()
    print (elementos)
    msg=" ELEMENTOS DEL AMBIENTE DE FORMACION EN CUENTADANCIA"
    return render_template("equipamiento.html",msg=msg,elementos=elementos)


@app.route("/carga_masiva", methods=['GET', 'POST'])
@login_required
def carga_masiva():
    return render_template("carga_masiva.html")


@app.route("/res/<nov>")
@login_required
def respuestanov(nov):
    u1=Usuario()
    cadena=u1.ListarJson("/n/"+nov)
    msg=" RESPUESTA A NOVEDAD"
    return render_template("novprocesa.html",cadena=cadena,msg=msg)

@app.route("/n/i",methods=['POST'])
@login_required
def salvarespuestanov():
    idN=request.form.get("NOVEDADES")
    idA=request.form.get("AMBIENTE")
    estado=request.form.get("ESTADO")
    respuesta=request.form.get("respuesta").upper()
    descri1=request.form.get("DESCRI1").upper()
    if estado==0:
        estado=1
    else:
        estado=1
    
    
    datos={
            "idAMBIENTE":idA,
            "idNOVEDADES":idN,
            "DESCRIPCION":respuesta,
            "ESTADO":estado,
            "PADRE":idA,
            "DESCRI1":descri1
        }
    print(datos)
    
    response = requests.post("http://127.0.0.1:8000/n/i", json=datos)
    msg=" RESPUESTA A LA NOVEDAD GRABADA CORRECTAMENTE..."
    return render_template("alertas.html",msgito=msg,regreso="/centro")

@app.route("/n/d",methods=['POST','GET'])
@login_required
def cierrarespuestanov():
    idN=request.form.get("NOVEDADES")
    idA=request.form.get("AMBIENTE")
    estado=request.form.get("ESTADO")
    respuesta=request.form.get("respuesta").upper()
    if estado == 0:
        estado = 1  # In process
    else:
        estado = 2  # Closed
    
    datos={
            "idAMBIENTE":idA,
            "idNOVEDADES":idN,
            "DESCRIPCION":respuesta,
            "ESTADO":estado,
            "PADRE":idA
        }
    print(datos)
    
    response = requests.post("http://127.0.0.1:8000/n/d", json=datos)
    msg=" LA NOVEDAD CERRADA CORRECTAMENTE..."
    return render_template("alertas.html",msgito=msg,regreso="/centro")


@app.route("/aprendiz", methods = ['GET'])
def aprendiz():
    e = Usuario()
    elementos = e.allEle()
    search_number = request.args.get('ESTACION', type=int)
    filtered_data = [dato for dato in elementos if dato['ESTACION'] == search_number]
    return render_template("estudiante.html", elementos=filtered_data)

@app.route("/web/email", methods=["GET", "POST"])
def email():
    if request.method == "POST":
        descripcion = request.form.get("descripcion", "").strip()
        respuesta = request.form.get("respuesta", "").strip()

        if not descripcion or not respuesta:
            return "Faltan datos en el formulario", 400

        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login("davisanquevedovan@gmail.com", "LAZV FYJD OTSN RCWL")

            msg = MIMEMultipart()
            contenido = f"{descripcion}\n\n{respuesta}"  
            msg.attach(MIMEText(contenido,'plain'))
            msg["From"] = "davisanquevedovan@gmail.com"
            msg["To"] = "davisanquevedovan@gmail.com"  # Tu dirección de correo
            msg["Subject"] = " Novedad " 

            servidor.sendmail("davisanquevedovan@gmail.com", "davisanquevedovan@gmail.com", msg.as_string())
            servidor.quit()

            return "Correo enviado correctamente"
        except Exception as e:
            return f"Error al enviar el correo: {str(e)}", 500
    else:
        # Aquí debes pasar los datos necesarios para renderizar el formulario
        cadena = [
            {"FECHA": "2023-10-01", "DESCRIPCION": "Descripción de ejemplo"}
        ]
        return render_template("novprocesa.html")
    

@login_manager.user_loader
def load_user(user_id):
    USER = requests.get(f"http://127.0.0.1:8000/apilogin").json()
    for u in USER:
        if u["idUSUARIO"] == int(user_id):
            return Login(u)  
    return None

@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)