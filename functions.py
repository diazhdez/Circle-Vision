import database as dbase

db = dbase.dbConnection()


def get_user(correo):
    user = db['users'].find_one({'correo': correo})
    return user


def get_admin(correo):
    admin = db['admin'].find_one({'correo': correo})
    return admin

