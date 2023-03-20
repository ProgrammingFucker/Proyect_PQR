from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLdb.cursors import Cursor
# Crear app mediante instancia

app = Flask(__name__)


# Usuarios de prueba
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

# "secret_key" se utiliza para establecer una clave secreta para la aplicación. La clave secreta es una cadena de caracteres que se utiliza para cifrar y descifrar datos sensibles, como cookies de sesión, contraseñas, etc.
app.secret_key = 'Libra2004$#'


@app.route('/')
def home():
    return render_template('login.html')


# Funciones

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM login where correo = %s AND password = %s', (username, password))
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
        cursor.execute(
            'SELECT * FROM login where correo = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('index_lider'))
        else:
            msg = 'Usuario y/o contraseña incorrectos.'
            # El usuario y / o la contraseña son incorrectos
            return render_template('login_admin.html', msg=msg)



@app.route("/solicitudes")
def solicitudes():
        sql = "SELECT * FROM solicitud"
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        ver = cursor.fetchall()
        print(ver)
        cursor.close()
        return render_template('vistatwo.html', datos=ver)




# Editar consulta
def editar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM solicitudes WHERE id=%s", (id,))
    persona = cursor.fetchone()
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']

        # Actualizar los datos en la base de datos
        cursor.execute(
            "UPDATE personas SET nombre=%s, edad=%s WHERE id=%s", (nombre, edad, id))
        conn.commit()
        msg = 'Se ha actualizado la información de la persona.'
        return redirect('/')
    return render_template('editar.html', persona=persona, msg=msg)


# Borrar consulta/ Comentario realizada por Estudiante o Lider
@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM consulta WHERE id=%s", (id,))
    conn.commit()
    msg = 'Se ha eliminado la persona.'
    return redirect('/', msg=msg)


# Buscar consulta

@app.route('/buscar')
def buscar():
    sql = "SELECT * FROM solicitud"
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    solicitudes = cursor.fetchall()
    print(solicitudes)
    cursor.close()
    return render_template('vistatwo.html', datos=solicitudes)


# Rutas Básicas

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


# URl'S Lider
@app.route("/vistaone")
def vistaone():
    return render_template('dashboard/pages/vistaone.html')


@app.route("/vistatwo")
def vistatwo():
    return render_template('dashboard/pages/vistatwo.html')


@app.route("/buscarconsulta")
def buscarconsulta():
    return render_template('dashboard/pages/consulta.html')


# URL'S Students
@app.route("/vistados")
def vistados():
    return render_template('dashboard/pages/vistados.html')


@app.route("/vistatres")
def vistatres():
    return render_template('dashboard/pages/vistatres.html')


# Registrar casos
@app.route("/casos", methods=['POST'])
def casos():
    identificacion = request.form['identificacion']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    correo = request.form['correo']
    celular = request.form['celular']
    # Guardando los datos del checkbox del tipo de caso
    caso = request.form["caso"]
    # Guardando los datos del checkbox del programa
    programs = request.form["programas"]
    asunto = request.form['asunto']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO solicitud (identificacion, nombre, apellido, correo, celular, caso, programa, asunto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                   (identificacion, nombre, apellido, correo, celular, caso, programs, asunto))
    mysql.connection.commit()
    msg = 'Su caso se ha enviado de manera correcta!'
    return render_template('dashboard/pages/op_estudiantes.html', msg=msg)


# Ver todas las solicitudes Lider Totales





#Cerrar session
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


#Ejecutar nuestra app cuando ejecutemos este archivo app.py
if __name__ == '__main__':
    app.run(port=3000, debug=True)