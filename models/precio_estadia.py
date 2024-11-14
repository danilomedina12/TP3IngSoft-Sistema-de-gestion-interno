from database import db

class Precio(db.Model):
    __tablename__ = 'precio'

    tipo_vehiculo = db.Column(db.String(50), primary_key=True)
    precio = db.Column(db.Float, nullable=False)  # Cambiado a Float por precisión en precio
    
    def __init__(self, precio, tipo_vehiculo):
        self.precio = precio
        self.tipo_vehiculo = tipo_vehiculo
    
    def __repr__(self):
        return f"<Precio tipo_vehiculo='{self.tipo_vehiculo}', precio={self.precio}>"

    @staticmethod
    def tipos_vehiculos():
        return ['AUTO', 'MOTO', 'CAMION']