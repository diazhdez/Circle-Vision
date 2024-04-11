from flask import Blueprint, render_template, url_for, redirect, flash, session, request

import bcrypt

import database as dbase

db = dbase.dbConnection()

session_routes = Blueprint('session', __name__)


# Ruta para iniciar sesión
@session_routes.route('/login/', methods=['POST'])
def login():
    admin = db['admin']
    correo = request.form['correo']
    password = request.form['password']

    # Buscar en la colección de admin
    login_admin = admin.find_one({'correo': correo})
    if login_admin and bcrypt.checkpw(password.encode('utf-8'), login_admin['password']):
        session['correo'] = correo
        return redirect(url_for('admin.admin'))

    flash('Correo o contraseña incorrectos')
    return redirect(url_for('index'))


# Ruta para registro
@session_routes.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        admin = db['admin']
        existing_user = admin.find_one({'correo': request.form['correo']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            admin.insert_one(
                {'nombre': request.form['nombre'], 'correo': request.form['correo'], 'password': hashpass})
            session['correo'] = request.form['correo']
            return redirect(url_for('index'))

        flash('El correo ya está en uso')
        return redirect(url_for('index'))

    return render_template('register.html')


# Ruta para cerrar sesión
@session_routes.route('/logout/')
def logout():
    session.clear()  # Elimina todas las variables de sesión
    return redirect(url_for('index'))  # Redirige al inicio de sesión
