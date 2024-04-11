from flask import Blueprint, render_template, redirect, url_for, session

from functions import get_user

import database as dbase

db = dbase.dbConnection()

user_routes = Blueprint('user', __name__)


# Ruta para users
@user_routes.route('/user/')
def user():
    if 'correo' in session:
        correo = session['correo']
        user = get_user(correo)
        if user:
            return render_template('user.html')
    else:
        return redirect(url_for('index'))


# Ruta para ver las tareas
@user_routes.route('/tareas/')
def tareas():
    if 'correo' in session:
        correo = session['correo']
        user = get_user(correo)
        tareas = db['tareas']
        tareasRecibidas = tareas.find()

        if user:
            return render_template('tareas.html', tareas=tareasRecibidas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Ruta para ver los integrantes
@user_routes.route('/integrantes/')
def integrantes():
    if 'correo' in session:
        correo = session['correo']
        user = get_user(correo)
        integrantes = db['integrantes']
        integrantesAgregados = integrantes.find()

        if user:
            return render_template('integrantes.html', integrantes=integrantesAgregados)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Ruta para enviar avances de tareas
@user_routes.route('/tareas/estado/')
def tareasEstado():
    if 'correo' in session:
        correo = session['correo']
        user = get_user(correo)
        tareasEstado = db['tareasEstado']
        estadosRecibidos = tareasEstado.find()

        if user:
            return render_template('tareaEstado.html', tareasEstado=estadosRecibidos, user=user)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


