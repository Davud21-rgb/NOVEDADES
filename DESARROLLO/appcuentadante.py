from flask import Flask,render_template,request, redirect, url_for, flash, session, g
import requests
from flask_cors import CORS
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


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
        self.res=requests.get(self.url+clave+dat)
        data1=json.loads(self.res.content)
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
    # va al api 8000:/i/.. dependiendo lo que traiga clave
    def Inserte(self,data,clave="/i"):
        print(self.url+clave)
        response = requests.post(self.url+clave, json=data)
    def Borra(self,cual,clave):
        response = requests.delete(self.url+clave+str(cual))
    def Actualiza(self,data,clave="/u"):
        response = requests.put(self.url+clave, json=data)
    #codigo david
    def espera(self, x):
        
        print('passaron dos segundos')
        time.sleep(3)
        return 'valimos verga'       
        
# Nueva ruta para el registro
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        email = request.form["email"]
        password = request.form["password"]
        
        if not email or not password:
            print("Faltan datos")
            mensaje="Faltan datos"
            flash(mensaje)
        
        user_data = {
            "email": email,
            "password": password
        }
        u1 = Usuario()
        cadena=u1.Consultlogin(email)
        
        if cadena==None:
            u1.Inserte(user_data, clave="/i/r")
            mensaje = "Usuario registrado correctamente"
            flash(mensaje)
            
            return redirect(url_for("login"))
            
        else:
            mensaje = "Usuario ya existe"
            flash(mensaje)
            return redirect(url_for("login"))
    return render_template("register.html")

#vista logeo // esta vista quedo siendo la principal
@app.route("/", methods=['POST','GET'])
def login():

    if request.method == 'POST':
        mail = request.form["email"]
        passwords = request.form["password"]
        print('aqui vot') 
        u1=Usuario()
        cadena=u1.Consultlogin(mail)
        if cadena==None:
            error = "No existe el usuario"
            flash(error)
        else:
            session.clear()
            session['id_user']= cadena[0]
            session['name'] = cadena[1]
            session['rol'] = cadena[3]
            print('se logeo bien')
            error = "Bienvenido"
            flash(error)
            return redirect(url_for("inicio"))

    return render_template("login.html")

# Para crear nuevo elemento
@app.route("/nuevo_elemento", methods=['GET', 'POST'])
def nuevo_elemento():
    u1 = Usuario()
    datos = u1.ConNovel('0')
    if request.method == 'POST':
        ambiente = request.form["ambiente"]
        estacion = request.form["estaciones"]
        serial = request.form["serial"]
        tip = request.form["tipo"]
        tipo = tip.upper()
        estado = request.form["estado"]

        if not ambiente or not serial or not tipo or not estado:
            print("Faltan datos")
            mensaje="Faltan datos"
            flash(mensaje)

        user_data = {
            "ambiente": ambiente,
            "estaciones": estacion,
            "serial": serial,
            "tipo": tipo,
            "estado": estado
        }
        
        cadena=u1.ConsultAmbi(ambiente, estacion, tipo)
        print(cadena)
        if 1==1:
            u1.Inserte(user_data, clave="/i/e")
            mensaje = "Elemento registrado correctamente"
            flash(mensaje)
            
            return redirect(url_for("equipamiento", amb=ambiente))
        
        else:
            print("Elemento ya existe")
            mensaje = "Elementos existe"
            flash(mensaje)
            return redirect(url_for("equipamiento", amb=ambiente))
    return render_template("nuevo_elemento.html", datos=datos)



@app.route("/home")
def inicio():
    return render_template("index.html")
@app.route("/menu")
def menu():
    return render_template("menu.html")
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

@app.route("/footer")
def footer():
    return render_template("footer.html")
@app.route("/novedada", methods=["GET","POST"])
def novedada():
    u1=Usuario()
    cadena=u1.ListarJson("/ln/a/1")
    llenos=1
    msg="NOVEDADES ABIERTAS"
    if cadena==False:
        return render_template("novedades.html",cadena=cadena,hay=0,msg=msg)

    return render_template("novedades.html",cadena=cadena,hay=1,msg=msg)

@app.route("/novedadp")
def novedadp():
    u1=Usuario()
    cadena=u1.ListarJson("/ln/p/1")
    msg="NOVEDADES EN PROCESO"
    
    if cadena==False:
        return render_template("novedades.html",cadena=cadena,hay=0,msg=msg)
    return render_template("novedades.html",cadena=cadena,hay=1,msg=msg)

@app.route("/novedadc")
def novedadc():
    u1=Usuario()
    cadena=u1.ListarJson("/ln/c/1")
    llenos=1
    msg="NOVEDADES CERRADAS"
    
    if cadena==False:
        return render_template("novedades.html",cadena=cadena,hay=0,msg=msg)
    return render_template("novedades.html",cadena=cadena,hay=1,msg=msg)

@app.route("/r/<amb>")
def resumen(amb):
    u1=Usuario()
    cadena=u1.ListarJson("/e/1")
    llenos=1
    msg="RESUMEN EQUIPAMIENTO DEL AMBIENTE"
    if cadena==False:
        return render_template("resumen.html",cadena=cadena,hay=0,msg=msg)
    return render_template("resumen.html",cadena=cadena,hay=1,msg=msg)

@app.route("/r/a/<amb>")
def equipamiento(amb):
    u1=Usuario()
    cadena=u1.ListarJson("/e/a/1")
    llenos=1
    msg=" EQUIPAMIENTO DEL AMBIENTE"
    
    if cadena==False:
        return render_template("equipamiento.html",cadena=cadena,hay=0,msg=msg)
    return render_template("equipamiento.html",cadena=cadena,hay=1,msg=msg)
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