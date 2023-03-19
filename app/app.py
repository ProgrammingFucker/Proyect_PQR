from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLdb.cursors import Cursor
#Crear app mediante instancia

app = Flask(__name__)


# Usuarios de prueba
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

app.secret_key = 'Libra2004$#'  #"secret_key" se utiliza para establecer una clave secreta para la aplicación. La clave secreta es una cadena de caracteres que se utiliza para cifrar y descifrar datos sensibles, como cookies de sesión, contraseñas, etc.


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM login where correo = %s AND password = %s',(username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['usuario'] = user[1]
            session['correo'] = user[2]
            session['password'] = user[3]
            return redirect(url_for('index_estudiante'))
        else:
            msg = 'Usuario y/o contraseña incorrectos.'
            # El usuario y / o la contraseña son incorrectos
            return render_template('login.html', msg=msg)
    

@app.route('/login_lider', methods=['POST'])
def login_lider():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM login where correo = %s AND password = %s',(username, password))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('index_lider'))
        else:
            msg = 'Usuario y/o contraseña incorrectos.'
            # El usuario y / o la contraseña son incorrectos
            return render_template('login.html', msg=msg)
    


@app.route("/lider")
def lider():
    return render_template('login_admin.html')


@app.route("/estudiante")
def estudiante():
    return render_template('login.html')


@app.route("/index_estudiante")
def index_estudiante():
    return render_template('dashboard/pages/op_estudiantes.html')



@app.route("/index_lider")
def index_lider():
    return render_template('dashboard/pages/lider.html')


#URl'S Lider
@app.route("/vistaone")
def vistaone():
    return render_template('dashboard/pages/vistaone.html')

@app.route("/vistatwo")
def vistatwo():
    return render_template('dashboard/pages/vistatwo.html')

@app.route("/vistathree")
def vistathree():
    return render_template('dashboard/pages/vistathree.html')

#URL'S Students


@app.route("/vistados")
def vistados():
    return render_template('dashboard/pages/vistados.html')

@app.route("/vistatres")
def vistatres():
    return render_template('dashboard/pages/vistatres.html')







#Logout 
@app.route("/logout")
def logout():
    session('loggedin', None)
    session('id', None)
    session('usuario', None) 
    session('correo', None)
    session('password', None)
    return redirect(url_for('home'))


#Ejecutar nuestra app cuando ejecutemos este archivo app.py
if __name__ == '__main__':
    app.run(port=3000, debug=True)