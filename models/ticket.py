from database import db

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    hora_emision = db.Column(db.DateTime, nullable=False)
    monto_total = db.Column(db.Numeric(10, 2), nullable=False)
    detalles = db.Column(db.Text, nullable=False)

    vehiculo = db.relationship('Vehiculo', backref='tickets')

    def __init__(self, vehiculo_id, hora_emision, monto_total, detalles):
        self.vehiculo_id = vehiculo_id
        self.hora_emision = hora_emision
        self.monto_total = monto_total
        self.detalles = detalles
