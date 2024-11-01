from database import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'

    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), nullable=False)
    nombre_cliente = db.Column(db.String(100), nullable=False)
    hora_ingreso = db.Column(db.DateTime, nullable=False)
    hora_egreso = db.Column(db.DateTime, nullable=True)
    ubicacion_cochera = db.Column(db.String(50), nullable=True) 

    def __init__(self, patente, nombre_cliente, hora_ingreso, ubicacion_cochera=None):
        self.patente = patente
        self.nombre_cliente = nombre_cliente
        self.hora_ingreso = hora_ingreso
        self.ubicacion_cochera = ubicacion_cochera
