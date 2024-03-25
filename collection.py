class Tarea:
    def __init__(self, nombre, descripcion, encargado, inicio, entrega):
        self.nombre = nombre
        self.descripcion = descripcion
        self.encargado = encargado
        self.inicio = inicio
        self.entrega = entrega

    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'encargado': self.encargado,
            'inicio': self.inicio,
            'entrega': self.entrega
        }
    
class Integrante:
    def __init__(self, nombre, apellidos, rol):
        self.nombre = nombre
        self.apellidos = apellidos
        self.rol = rol

    def toDBCollection(self):
        return{
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'rol': self.rol
        }