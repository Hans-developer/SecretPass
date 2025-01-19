from flask import Flask, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

db = sqlite3.connect('gestor.db')

cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT NOT NULL )
''')
db.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS cuentas (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
sitio TEXT NOT NULL,
usuario TEXT NOT NULL,
contrasena TEXT NOT NULL)
''')
db.commit()

# base de datos y tablas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'H1q2w3e4r.'


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        conpassword = request.form['conpassword'].strip()

        if password == conpassword:
            hashed_password = generate_password_hash(password)
            new_acount = 'INSERT INTO user (email, password) VALUES (?, ?)'
            cursor.execute(new_acount, (email, hashed_password))
            db.commit()
            msg = "Usuario creado con exito!"
            return render_template('index.html', msg=msg)
        else:
            error = "Las claves deben ser iguales intenta nuevamente"
            return render_template('index.html', error=error)
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        cursor.execute('SELECT password FROM user WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[0], password):
            user_id = cursor.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
            session['user_id'] = user_id[0]
            cuentas = cursor.execute('SELECT * FROM cuentas WHERE user_id = ?', (user_id[0],))
            return render_template('dashboard.html', cuentas=cuentas)
        else:
            error = "Credenciales incorrectas"
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    if request.method == 'POST':
        user_id = session['user_id'].strip()
        sitio = request.form['sitio'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['password'].strip()
        new_acount = cursor.execute('INSERT INTO cuentas (user_id, sitio, usuario, contrasena) VALUES (?, ?, ?, ?)', (user_id, sitio, usuario, contrasena))
        db.commit()
        if new_acount:
            return redirect(url_for('dashboard'))
        
@app.route('/v_editar/<int:id>')
def veditar(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cuentas WHERE id = ?', (id,))
    cuenta = cursor.fetchall()
    return render_template('editar.html', cuenta=cuenta)

        
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    if request.method == 'POST':
        sitio = request.form['sitio'].strip()
        usuario = request.form['usuario'].strip()
        contrasena = request.form['password'].strip()
        cursor.execute('UPDATE cuentas SET sitio = ?, usuario = ?, contrasena = ? WHERE id = ?', (sitio, usuario, contrasena, id))
        db.commit()
        return redirect(url_for('dashboard'))
    
@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    cursor.execute('DELETE FROM cuentas WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('dashboard'))



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = sqlite3.connect('gestor.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM cuentas WHERE user_id = ?', (session['user_id'],))
    cuentas = cursor.fetchall()
    return render_template('dashboard.html', cuentas=cuentas)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

    





