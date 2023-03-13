from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_mysqldb import MySQL
from jinja2 import Template
from reportlab.pdfgen import canvas
import database as db

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
    return render_template('pacientes.html')
    


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


#Rutas del Registro de Pacientes
@app.route('/pacientes.html')
def register_pacientes():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM pacientes")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('pacientes.html', data=insertObject)
    
@app.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ciudad = request.form['ciudad']
    codigo_postal = request.form['codigo_postal']
    telefono = request.form['telefono']
    tipo_sangre = request.form['tipo_sangre']
    

    if nombre and apellido and ciudad and codigo_postal and telefono and tipo_sangre:
        cursor = db.database.cursor()
        sql = "INSERT INTO pacientes (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('register_pacientes'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('register_pacientes'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ciudad = request.form['ciudad']
    codigo_postal = request.form['codigo_postal']
    telefono = request.form['telefono']
    tipo_sangre = request.form['tipo_sangre']

    if nombre and apellido and ciudad and codigo_postal and telefono and tipo_sangre:
        cursor = db.database.cursor()
        sql = "UPDATE users SET nombre = %s, apellido = %s, ciudad = %s, codigo_postal = %s, telefono = %s, tipo_sangre = %s,  WHERE id = %s"
        data = (nombre, apellido, ciudad, codigo_postal, telefono, tipo_sangre, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('register_pacientes'))

@app.route('/pdf/<string:id>')
def generar_pdf(id):
    cursor = db.database.cursor()
    sql = "SELECT * FROM pacientes WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    paciente = cursor.fetchone()
    
    # Crear el PDF
    nombre_pdf = f"{paciente[2]}.pdf"
    c = canvas.Canvas(nombre_pdf)
    c.drawString(100, 750, f"ID: {paciente[0]}")
    c.drawString(100, 700, f"Nombre: {paciente[1]}")
    c.drawString(100, 650, f"Apellido: {paciente[2]}")
    c.drawString(100, 600, f"Ciudad: {paciente[3]}")

    c.drawString(260, 250, f"Clinica Azul")
    c.drawImage("static/images/logo.png",220, 300, 150, 150)
    c.save()






if __name__ == "__main__":

    app.run(debug = True, port=4000, host="0.0.0.0")