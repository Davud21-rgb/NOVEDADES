from flask import Flask, jsonify,render_template,request, redirect, url_for, flash, session, g
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
    def __init__(self,murl='http://127.0.0.1:8000'):
        self.url=murl


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


    def Borra(self,cual):
        response = requests.delete(self.url+"/d/"+str(cual))
        
    # def Actualiza(self, data):
    #     # Send a PUT request to the API with the data as JSON
    #     response = requests.put(f"{self.url}/u", json=data)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()  # Return the response as JSON if successful
        else:
            return {"error": "Failed to update element"}  # Return error message
    #codigo david
    def espera(self, x):
        
        print('passaron dos segundos')
        time.sleep(3)
        return 'valimos verga'       
    
    def novedada(self, clave="/novedadesA"):
        self.res = requests.get(self.url + clave)
        data = json.loads(self.res.content)
        return data
    
    
@app.route("/ambi")
def ambi():
    # Query for environments with NULL IDCUENTADANTE
    sql = "SELECT * FROM AMBIENTE WHERE IDCUENTADANTE IS NULL"
    u1 = Usuario(app.bd)
    todo = u1.ConsultarJson(sql)
    return jsonify(todo)  # Return JSON data

@app.route("/register", methods=['POST', 'GET'])
def register():
    u = Usuario()
    a = u.ambientes()  # Fetch environments where IDCUENTADANTE is NULL
    accountant = 2  # Default role for new users

    if request.method == 'POST':
        nombre = request.form["nombre"]
        rol = accountant  # Default role
        cedula = request.form["cedula"]
        email = request.form["email"]
        password = request.form["password"]
        id_ambiente = request.form["ambiente"]

        if not email or not password:
            flash("Faltan datos")
            return redirect(url_for("register"))

        user_data = {
            "nombre": nombre,
            "rol": rol,
            "cedula": cedula,
            "email": email,
            "password": password
        }

        u1 = Usuario()
        existing_user = u1.Consultlogin(email)
        if existing_user is None:
            user_id = u1.Inserte(user_data)
            if user_id is not None:
                flash("Usuario registrado correctamente")

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
        else:
            flash("El usuario ya existe con ese correo electrónico.")
    
    return render_template("register.html", a=a, accountant=accountant)


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
    def __init__(self, murl='http://127.0.0.1:8000'):
        self.url = murl


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


    def Borra(self, id):
        # Send a DELETE request to the API to delete the element
        response = requests.delete(f"{self.url}/deleteEle/{id}")
        if response.status_code == 200:
            return 'OK'
        else:
            return 'Error'



    def Actualiza(self, data):
        response = requests.put(self.url, json=data)  # Use PUT method
        if response.status_code == 200:
            return response.json()  # Return JSON data if successful
        else:
            return {"error": "Failed to update element"}
        

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
        accountant = 2

        if request.method == 'POST':
            nombre = request.form["nombre"]
            rol = accountant
            cedula = request.form["cedula"]
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
                "cedula": cedula,
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
        return render_template("register.html", a=a,accountant=accountant)


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Fetch user data from your API
        u1 = Usuario()  # Assuming Usuario class is used to interact with your API
        users_data = u1.ListarJson("/apilogin")
        user_found = False

        for user in users_data:
            # Compare email and password
            if email == user['email'] and password == user['password']:
                # Ensure user role is valid (e.g., rol == 2 for 'cuentadante')
                if user['rol'] == 2:
                    user_obj = Login(user)  # Create the Login object
                    login_user(user_obj)  # Store user in the session
                    user_found = True
                    break
                else:
                    flash(f"The user with email {user['email']} is not a cuentadante.")
                    return redirect(url_for("login"))

        if user_found:
            return redirect(url_for('home'))
        else:
            flash("Incorrect email or password.")
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
    
    
@app.route("/alertas")
def show_alerta():
    msgito = request.args.get('msgito')  # Get the message from query parameters
    regreso = request.args.get('regreso')  # Get the redirect URL from query parameters
    return render_template('alertas.html', msgito=msgito, regreso=regreso)

        
@app.route("/nuevo_elemento", methods=['GET', 'POST'])
def nuevo_elemento():
    u1 = Usuario()
    current_classroom = None
    if current_user.is_authenticated:
        try:
            response = requests.get(f"http://127.0.0.1:8000/ambippp/{current_user.idUSUARIO}")
            if response.status_code == 200:
                lulo = response.json()
                
                if lulo:  # Check if there is at least one classroom in the response
                    current_classroom = lulo[0]["idAMBIENTE"]  # Get the first classroom's idAMBIENTE
                
                e = u1.elem()
                return render_template("nuevo_elemento.html", 
                                       e=e,
                                       current_classroom=current_classroom)
            else:
                flash("Failed to load classroom data.")
        except requests.exceptions.RequestException as e:
            flash(f"Error fetching data: {e}")
    
    return render_template("nuevo_elemento.html", current_classroom=current_classroom)


@app.route("/home")
@login_required
def home():
    return render_template("index.html")

@app.route("/menu")
@login_required
def menu():
    if current_user.is_authenticated:
        try:
            response = requests.get(f"http://127.0.0.1:8000/ambippp/{current_user.idUSUARIO}")
            
            if response.status_code == 200:
                lulo = response.json()
                classroom_names = [a["nombre"] for a in lulo]
                return render_template("menu.html", classroom_names=classroom_names)
            else:
                flash("Failed to load classroom data.")
                return redirect(url_for('home'))
        except requests.exceptions.RequestException as e:
            flash(f"Error fetching data: {e}")
            return redirect(url_for('home'))
    else:
        flash("You must be logged in to access this page.")
        return redirect(url_for('login'))

    
@app.route("/delete")
def d():
    dele = requests.delete("http://127.0.0.1:8000/delete/equipamiento")
    return render_template("menu.html", dele=dele)

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
    if current_user.is_authenticated:
        a=requests.get(f"http://127.0.0.1:8000/novedadesA/{current_user.idUSUARIO}").json()
        msg = "NOVEDADES ABIERTAS"
        return render_template("novedades.html", msg=msg,a=a)

@app.route("/novedadp")
@login_required
def novedadp():
    if current_user.is_authenticated:
        cadena=requests.get(F"http://127.0.0.1:8000/novedadesP/{current_user.idUSUARIO}").json()
        msg="NOVEDADES EN PROCESO"
        print (cadena)
        return render_template("PROCESO.html",msg=msg,cadena=cadena)

@app.route("/novedadc")
@login_required
def novedadc():
    if current_user.is_authenticated:
        cadena=requests.get(f"http://127.0.0.1:8000/novedadesC/{current_user.idUSUARIO}").json()
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
    if current_user.is_authenticated:
        response = requests.get(f"http://127.0.0.1:8000/allElements/{current_user.idUSUARIO}").json()
        
        # Check if response contains an error
        if "error" in response:
            elementos = []  # No data found
        else:
            elementos = response  # Pass the valid data
        
        msg = "ELEMENTOS DEL AMBIENTE DE FORMACION EN CUENTADANCIA"
        return render_template("equipamiento.html", msg=msg, elementos=elementos)



@app.route("/carga_masiva", methods=["GET", "POST"])
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


#upding my element
@app.route("/u", methods=['POST'])
@login_required
def actualizaElemento():
    # Collect form data
    id = request.form.get("idEQUIPAMIENTO")
    idAmbi = request.form.get("idAMBIENTE")
    idTIPOELEMENTO = request.form.get("idTIPOELEMENTO")
    estado = request.form.get("estado")
    serial = request.form.get("serial")
    estacion = request.form.get("estacion")
    observacion = None

    data = {
        "idEQUIPAMIENTO": id,
        "idAMBIENTE": idAmbi,
        "idTIPOELEMENTO": idTIPOELEMENTO,
        "estado": estado,
        "serial": serial,
        "estacion": estacion,
        "observacion": observacion
    }

    u1 = Usuario("http://127.0.0.1:8000/update")
    response = u1.Actualiza(data)

    if response.get("message") == "Element edited successfully":
        msg = "ELEMENTO EDITADO CORRECTAMENTE"
        status_code = 200
    else:
        msg = "Error al editar el elemento"
        status_code = 500

    return render_template("alertas.html", msgito=msg, regreso="/ele"), status_code



@app.route("/elemento/<ele>", methods=['GET','post'])
@login_required
def editaEle(ele):
    u1 = Usuario()
    cadena = u1.ListarJson("/editEle/" + ele)
    e = requests.get("http://127.0.0.1:8000/tipoElementos").json()
    msg = "EDITANDO ELEMENTO"
    return render_template("editaElemento.html", cadena=cadena, msg=msg, e=e)


@app.route("/d/<id>", methods=['GET'])
@login_required
def deleteEle(id):
    e = Usuario("http://127.0.0.1:8000")
    e.Borra(id)
    msg = "ELEMENTO ELIMINADO CORRECTAMENTE"
    return render_template("alertas.html", msgito=msg, regreso="/ele")


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


# @app.route("/web/email", methods=["GET", "POST"])
# def email():
#     if request.method == "POST":
#         descripcion = request.form.get("descripcion", "").strip()
#         respuesta = request.form.get("respuesta", "").strip()

#         if not descripcion or not respuesta:
#             return "Faltan datos en el formulario", 400

#         try:
#             servidor = smtplib.SMTP("smtp.gmail.com", 587)
#             servidor.starttls()
#             servidor.login("davisanquevedovan@gmail.com", "LAZV FYJD OTSN RCWL")

#             msg = MIMEMultipart()
#             contenido = f"{descripcion}\n\n{respuesta}"  
#             msg.attach(MIMEText(contenido,'plain'))
#             msg["From"] = "davisanquevedovan@gmail.com"
#             msg["To"] = "davisanquevedovan@gmail.com"  # Tu dirección de correo
#             msg["Subject"] = " Novedad " 

#             servidor.sendmail("davisanquevedovan@gmail.com", "davisanquevedovan@gmail.com", msg.as_string())
#             servidor.quit()

#             return "Correo enviado correctamente"
#         except Exception as e:
#             return f"Error al enviar el correo: {str(e)}", 500
#     else:
#         # Aquí debes pasar los datos necesarios para renderizar el formulario
#         cadena = [
#             {"FECHA": "2023-10-01", "DESCRIPCION": "Descripción de ejemplo"}
#         ]
#         return render_template("novprocesa.html")
    

@login_manager.user_loader
def load_user(user_id):
    try:
        # Fetch all users (or fetch by ID if your API supports that)
        response = requests.get(f"http://127.0.0.1:8000/apilogin")
        if response.status_code == 200:
            users = response.json()  # List of users

            # Find the user by idUSUARIO
            for user in users:
                if user["idUSUARIO"] == int(user_id):
                    return Login(user)  # Return the Login object

    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")

    return None


@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)