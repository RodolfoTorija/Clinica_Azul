from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_mysqldb import MySQL
from jinja2 import Template

app = Flask(__name__)

app.secret_key = 'fcea920f7412b5da7be0cf42b8c93759'




@app.route("/home.html")
def home():
    return render_template("home.html")

@app.route("/")
def index():
    return render_template("login.html")



@app.route('/especialidades.html')
def especialidades():
    return render_template("especialidades.html")

@app.route('/servicios.html')
def servicios():
    return render_template("servicios.html")


@app.route('/quienessomos.html')
def quienessomos():
    return render_template("quienessomos.html")

@app.route('/contactanos.html')
def contactanos():
    return render_template("contactanos.html")


# Configuración de la base de datos
...


try:
    mydb = mysql.connector.connect(
        host = "localhost",
        port = "3306",
        user= "root",
        password = "Zeromainj0.",
        database = "clinica_azul"
    )

    print("Conexión exitosa a la base de datos. \n")

except mysql.connector.Error as error:
    print("Error al conectarse a la base de datos: {}".format(error))
    mydb = None

#Conexion de base de datos
@app.route('/login', methods = ['GET','POST'])
def login():
    if mydb is None:
        return render_template('/login.html', mensaje='Error al conectarse a la base de datos')
    

    nombre = request.form['username']
    contrasena = request.form['password']

    try:
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND contrasena = %s", (nombre, contrasena))

        usuario = mycursor.fetchone()

        if usuario:
                session['username'] = nombre # Almacenar el nombre de usuario en la sesión
                return render_template('/home.html', correcta = 'Has iniciado sesión correctamente')
        else:
           
            # Nombre de usuario o contraseña incorrectos
            return render_template('/login.html', error='Nombre de usuario o contraseña incorrectos')

    except mysql.connector.Error as error:
        print("Error al ejecutar la consulta a la base de datos: {}".format(error))
        return render_template('/login.html', error='Error al ejecutar la consulta a la base de datos')
    

@app.route('/logout')
def logout():
    session.pop('username', None) #Eliminar la variable de sesión username
    return render_template ('/login.html')




if __name__ == '__main__':
    app.run()

