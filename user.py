from flask import Blueprint, render_template, redirect, url_for, flash, send_file, request, session

from functions import get_user

from io import BytesIO

from bson.binary import Binary

from bson import ObjectId

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
            return render_template('tareaEstado.html', tareasEstado=estadosRecibidos)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# Creamos la ruta para agregar el estado
@user_routes.route('/agregarEstado/', methods=['POST'])
def agregarEstado():
    if request.method == 'POST':
        tareasEstado = db['tareasEstado']
        nombre = request.form['nombre']
        tarea = request.form['tarea']
        estado = request.form['estado']

        # Procesar el archivo
        archivo = request.files['archivo']

        if archivo:
            if archivo.filename.endswith('.pdf'):
                archivo_data = archivo.read()
                archivo_bin = Binary(archivo_data)
            else:
                flash('El archivo debe ser PDF')
                return redirect(url_for('tareasEstado'))
        else:
            archivo_bin = None

        # Insertar los datos en la colección 'tareasEstado'
        tareasEstadoDict = {
            'nombre': nombre,
            'tarea': tarea,
            'estado': estado,
            'archivo': archivo_bin
        }

        tareasEstado.insert_one(tareasEstadoDict)

        flash('Tarea agregada correctamente')
        # Reemplaza 'nombre_de_tu_ruta' con la ruta a la que deseas redirigir después de agregar la tarea
        return redirect(url_for('tareasEstado'))

    return redirect(url_for('tareasEstado'))


@user_routes.route('/descargarArchivo/<string:estado_id>')
def descargarArchivo(estado_id):
    tareasEstado = db['tareasEstado']
    estado = tareasEstado.find_one({'_id': ObjectId(estado_id)})

    if estado and estado['archivo']:
        # Obtener el contenido binario del CV
        archivo_bin = estado['archivo']
        # Crear un objeto BytesIO para almacenar el contenido binario
        archivo_stream = BytesIO(archivo_bin)
        # Enviar el contenido binario como un archivo adjunto
        # Asegurar que la posición del cursor esté al inicio del archivo
        archivo_stream.seek(0)
        return send_file(archivo_stream, mimetype='application/pdf', as_attachment=True, download_name='archivo.pdf')
    else:
        flash('Archivo no encontrado')
        return redirect(url_for('tareasEstado'))
