from flask import Flask,render_template,request, redirect, url_for, flash, session, g
import requests
from flask_cors import CORS
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from email.mime.text import MIMEText
import time
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
        self.res = requests.get(self.url + clave)
        data1 = json.loads(self.res.content)
        return data1
    
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


#vista logeo // esta vista quedo siendo la principal
@app.route("/SSS", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        mail = request.form.get("email")
        passwords = request.form.get("password")

        # Check for empty form fields
        if not mail or not passwords:
            error = "Please enter both email and password."
            flash(error)
            return redirect(url_for("login"))

        u1 = Usuario()
        cadena = u1.Consultlogin(mail)

        if not cadena:  # If no user is found
            error = "No such user found."
            flash(error)
        else:
            # Successful login: store user details in session
            session['idUSUARIO'] = cadena[0]
            session['name'] = cadena[1]
            session['rol'] = cadena[3]

            flash("Welcome!")
            # Redirect to /menu after successful login
            return redirect(url_for("home"))

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
    

# Para crear nuevo elemento
@app.route("/nuevo_elementoi", methods=['GET', 'POST'])
def nuevo_elementoi():
    u1 = Usuario()
    datos = u1.ConNovel('0')
    if request.method == 'POST':
        ambiente = request.form["ambiente"]
        estacion = request.form["estacion"]
        serial = request.form["serial"]
        nombre = request.form["nombre"]
        tipo = nombre.upper()
        estado = request.form["estado"]

        if not ambiente or not serial or not tipo or not estado:
            print("Faltan datos")
            mensaje="Faltan datos"
            flash(mensaje)

        user_data = {
            "ambiente": ambiente,
            "estaciones": estacion,
            "serial": serial,
            "nombre": nombre,
            "estado": estado
        }

        u1.InserteElementos(user_data)
        mensaje = "Elemento registrado correctamente"
        flash(mensaje)
    return redirect("/ele")
        
@app.route("/nuevo_elemento", methods=['GET', 'POST'])
def nuevo_elemento():
    u1=Usuario()
    am = u1.ambientesss()
    return render_template("nuevo_elemento.html",am=am)
        

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/menu")
def menu():
    ambi = requests.get("http://127.0.0.1:8000/ambi").json()
    classroom_names = [a['NOMBRE'] for a in ambi if 'NOMBRE' in a]
    return render_template("menu.html",classroom_names=classroom_names)
@app.route("/banner")
def banner():
    return render_template("banner.html")
@app.route("/centro")
def centro():
    return render_template("centro.html")
@app.route('/estudiante')
def estudiante():
    return render_template("estudiante.html")
def homeInstru():
    return render_template("centro.html")

@app.route("/inventario")
def inventario():
    return render_template("inventario.html")

@app.route("/footer")
def footer():
    return render_template("footer.html")

@app.route("/novedada", methods=["GET", "POST"])
def ada():
    a=requests.get("http://127.0.0.1:8000/novedadesA").json()
    msg = "NOVEDADES ABIERTAS"
    return render_template("novedades.html", msg=msg,a=a)


@app.route("/novedadp")
def novedadp():
    cadena=requests.get("http://127.0.0.1:8000/novedadesP").json()
    msg="NOVEDADES EN PROCESO"
    return render_template("PROCESO.html",msg=msg,cadena=cadena)

@app.route("/novedadc")
def novedadc():
    cadena=requests.get("http://127.0.0.1:8000/novedadesC").json()
    msg="NOVEDADES EN CERRADAS"
    return render_template("CERRADAS.html",msg=msg,cadena=cadena)

@app.route("/r/<amb>")
def resumen(amb):
    u1=Usuario()
    cadena=u1.ListarJson("/e/1")
    llenos=1
    msg="RESUMEN EQUIPAMIENTO DEL AMBIENTE"
    if cadena==False:
        return render_template("resumen.html",cadena=cadena,hay=0,msg=msg)
    return render_template("resumen.html",cadena=cadena,hay=1,msg=msg)

@app.route("/r2")
def resumen2():
    u1=Usuario()
    cadena=u1.ListarJson("/e/1")
    llenos=1
    msg="RESUMEN EQUIPAMIENTO DEL AMBIENTE"
    return render_template("resumen.html",cadena=cadena,hay=1,msg=msg)

# @app.route("/r/a/<amb>")
# def equipamiento(amb):
#     u1=Usuario()
#     cadena=u1.ListarJson("/e/a/1")
#     llenos=1
#     msg=" EQUIPAMIENTO DEL AMBIENTE"
    
#     if cadena==False:
#         return render_template("equipamiento.html",cadena=cadena,hay=0,msg=msg)
#     return render_template("equipamiento.html",cadena=cadena,hay=1,msg=msg)


@app.route("/ele")
def equipamiento2():
    elementos=requests.get("http://127.0.0.1:8000/allElements").json()
    msg=" ELEMENTOS DEL AMBIENTE DE FORMACION EN CUENTADANCIA"
    return render_template("equipamiento.html",msg=msg,elementos=elementos)


@app.route("/res/<nov>")
def respuestanov(nov):
    u1=Usuario()
    cadena=u1.ListarJson("/n/"+nov)
    llenos=1
    msg=" RESPUESTA A NOVEDAD"
    
    # if cadena==False:
    # return render_template("novprocesa.html",msg=msg)
    # return render_template("novprocesa.html",msg=msg)
    return render_template("novprocesa.html",cadena=cadena,msg=msg)

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

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)