from flask import Flask, render_template, url_for, redirect, session

from session import session_routes

from user import user_routes

from admin import admin_routes

from functions import *

import database as dbase

db = dbase.dbConnection()

app = Flask(__name__)

app.secret_key = 'M0i1Xc$GfPw3Yz@2SbQ9lKpA5rJhDtE7'


# Ruta principal
@app.route('/')
def index():
    if 'correo' in session:  # Verificar si hay una sesión activa
        correo = session['correo']
        # Buscar el correo en la colección de admin
        admin_email = db.admin.find_one({'correo': correo})
        user_email = db.users.find_one({'correo': correo})

        if admin_email:  # Si el correo está presente en la colección de admin
            # Redireccionar a la página de administrador
            return redirect(url_for('admin.admin'))

        if user_email:
            # Redireccionar a la página de user
            return redirect(url_for('user.user'))
    else:
        # Si no hay una sesión activa, mostrar la página de inicio de sesión
        return render_template('login.html')


# Registrar blueprints
app.register_blueprint(session_routes)

app.register_blueprint(admin_routes)

app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
