from flask import Flask , render_template, request, redirect, url_for
from config import config
from flask_mysqldb import MySQL

app=Flask(__name__)

db = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        request.form['username']
        request.form['password']
        return render_template("login.html")
    
    else:

        return render_template("login.html")







@app.route('/home.html')
def home():
    return render_template("home.html")

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



if __name__ =='__main__':
    app.config.from_object(config['development'])
    app.run()



