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

@app.route("/login.html")
def index_login():
    return render_template("login.html")


@app.route('/pacientes.html')
def pacientes():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM PACIENTES')
    pacientes = cur.fetchall()
    cur.close()
    return render_template('pacientes.html', pacientes=pacientes)
    

@app.route('/servicios.html')
def servicios():
    return render_template("servicios.html")


@app.route('/quienessomos.html')
def quienessomos():
    return render_template("quienessomos.html")

@app.route('/contactanos.html')
def contactanos():
    return render_template("contactanos.html")

@app.route('/registro.html')
def registro():
    return render_template("registro.html")


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
    email = request.form['username']
    contrasena = request.form['password']

    try:
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM usuarios WHERE nombre = %s or email = %s AND contrasena = %s", (nombre, email , contrasena))

        usuario = mycursor.fetchone()

        if usuario:
                session['username'] = nombre # Almacenar el nombre de usuario en la sesión
                return render_template('/home.html',  correcta = 'Has iniciado sesión correctamente')
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


#App route para el registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro_verificacion():
    if request.method == 'POST':
        nombre = request.form['name_register']
        email = request.form['email_register']
        contrasena = request.form['password_register']
        
        # Verificar si el usuario ya existe en la base de datos
        cur = mydb.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s OR nombre = %s", (email, nombre))
        usuario_existente = cur.fetchone()
        
        if usuario_existente:
            mensaje_error = "Ya existe un usuario con ese correo electrónico o nombre de usuario."
            return render_template('registro.html', error_register=mensaje_error)
        else:
            # Insertar los datos en la tabla de la base de datos
            cur.execute("INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)", (nombre, email, contrasena))
            mydb.commit()
            cur.close()
            
            return render_template('registro.html', mensaje_exitoso="Registro existoso inicia sesión")
    
    return render_template('registro.html')





#CODIGO PARA CRUD ===============================================




    

@app.route('/agregar_paciente', methods=['POST'])
def agregar_paciente():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ciudad = request.form['ciudad']
    codigo_postal = request.form['codigo_postal']
    telefono = request.form['telefono']
    tipo_sangre = request.form['tipo_sangre']
    folio_paciente = request.form['folio_paciente']
    pdf = request.files['pdf'].read() if 'pdf' in request.files else None
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO pacientes (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre, folio_paciente, pdf) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre, folio_paciente, pdf))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/ver_pdf/<folio>')
def ver_pdf(folio):
    cur = mysql.connection.cursor()
    cur.execute('SELECT pdf FROM pacientes WHERE folio_paciente = %s', (folio,))
    pdf_data = cur.fetchone()[0]
    cur.close()
    return pdf_data

@app.route('/editar_paciente', methods=['POST'])
def editar_paciente():
    folio = request.form['folio']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ciudad = request.form['ciudad']
    codigo_postal = request.form['codigo_postal']
    telefono = request.form['telefono']
    tipo_sangre = request.form['tipo_sangre']
    cur = mysql.connection.cursor()
    cur.execute('UPDATE pacientes SET nombre = %s, apellido = %s, ciudad = %s, codigo_postal = %s, telefono = %s, tipo_sangre = %s WHERE folio_paciente = %s', (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre, folio))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('crud'))

@app.route('/eliminar_paciente/<folio>', methods=['POST'])
def eliminar_paciente(folio):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pacientes WHERE folio_paciente = %s', (folio,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('crud'))





if __name__ == "__main__":

    app.run(port=4000, host="0.0.0.0")