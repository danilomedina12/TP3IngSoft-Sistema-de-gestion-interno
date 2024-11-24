from database import db

class Promocion(db.Model):
    __tablename__ = 'promociones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad_horas = db.Column(db.Integer, nullable=False)
    porcentaje_descuento = db.Column(db.Float, nullable=False)

    def __init__(self, cantidad_horas, porcentaje_descuento):
        self.cantidad_horas = cantidad_horas
        self.porcentaje_descuento = porcentaje_descuento


    def __repr__(self):
        return f'<Promocion {self.id} - {self.cantidad_horas} horas, {self.porcentaje_descuento}% descuento>'
