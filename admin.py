from flask import Blueprint, render_template, url_for, redirect, jsonify, session, request

from functions import get_admin

from collection import *

import database as dbase

db = dbase.dbConnection()

admin_routes = Blueprint('admin', __name__)


# Ruta para administradores
@admin_routes.route('/admin/')
def admin():
    if 'correo' in session:
        correo = session['correo']
        admin = get_admin(correo)
        if admin:
            return render_template('admin.html')
    else:
        return redirect(url_for('index'))


# Ruta para ver y agregar tareas
@admin_routes.route('/admin/tareas/')
def agregarTareas():
    if 'correo' in session:
        correo = session['correo']
        admin = get_admin(correo)
        tareas = db['tareas']
        tareasRecibidas = tareas.find()

        if admin:
            return render_template('addTarea.html', tareas=tareasRecibidas)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Method POST
@admin_routes.route('/addTarea/', methods=['POST'])
def addTarea():
    tareas = db['tareas']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    encargado = request.form['encargado']
    inicio = request.form['inicio']
    entrega = request.form['entrega']

    if nombre and descripcion and encargado and inicio and entrega:
        tarea = Tarea(nombre, descripcion, encargado, inicio, entrega)
        tareas.insert_one(tarea.toDBCollection())
        response = jsonify({
            'nombre': nombre,
            'descripcion': descripcion,
            'encargado': encargado,
            'inicio': inicio,
            'entrega': entrega
        })
        return redirect(url_for('agregarTareas'))
    else:
        return notFound()


# Method DELETE
@admin_routes.route('/deleteTarea/<string:nombre_tarea>/')
def deleteTarea(nombre_tarea):
    tareas = db['tareas']
    tareas.delete_one({'nombre': nombre_tarea})
    return redirect(url_for('agregarTareas'))


# Method PUT
@admin_routes.route('/editTarea/<string:nombre_tarea>/', methods=['POST'])
def editTarea(nombre_tarea):
    tareas = db['tareas']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    encargado = request.form['encargado']
    inicio = request.form['inicio']
    entrega = request.form['entrega']

    if nombre and descripcion and encargado and inicio and entrega:
        tareas.update_one({'nombre': nombre_tarea}, {
            '$set': {'nombre': nombre, 'descripcion': descripcion, 'encargado': encargado, 'inicio': inicio, 'entrega': entrega}})
        response = jsonify(
            {'message': 'Tarea ' + nombre_tarea + ' actualizada correctamente'})
        return redirect(url_for('agregarTareas'))
    else:
        return notFound()


# Ruta para ver y agregar integrantes
@admin_routes.route('/admin/integrantes/')
def agregarIntegrantes():
    if 'correo' in session:
        correo = session['correo']
        admin = get_admin(correo)
        integrantes = db['integrantes']
        integrantesAgregados = integrantes.find()

        if admin:
            return render_template('addIntegrante.html', integrantes=integrantesAgregados)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Method POST
@admin_routes.route('/addIntegrante/', methods=['POST'])
def addIntegrante():
    integrantes = db['integrantes']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    rol = request.form['rol']

    if nombre and apellidos and rol:
        integrante = Integrante(nombre, apellidos, rol)
        integrantes.insert_one(integrante.toDBCollection())
        response = jsonify({
            'nombre': nombre,
            'apellidos': apellidos,
            'rol': rol
        })
        return redirect(url_for('agregarIntegrantes'))
    else:
        return notFound()


# Method DELETE
@admin_routes.route('/deleteIntegrante/<string:nombre_integrante>/')
def deleteIntegrante(nombre_integrante):
    integrantes = db['integrantes']
    integrantes.delete_one({'nombre': nombre_integrante})
    return redirect(url_for('agregarIntegrantes'))


# Method PUT
@admin_routes.route('/editIntegrante/<string:nombre_integrante>/', methods=['POST'])
def editIntegrante(nombre_integrante):
    integrantes = db['integrantes']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    rol = request.form['rol']

    if nombre and apellidos and rol:
        integrantes.update_one({'nombre': nombre_integrante}, {
            '$set': {'nombre': nombre, 'apellidos': apellidos, 'rol': rol}})
        response = jsonify(
            {'message': 'Integrante ' + nombre_integrante + ' actualizado correctamente'})
        return redirect(url_for('agregarIntegrantes'))
    else:
        return notFound()


# Ruta para errores
@admin_routes.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'Not Found ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response
