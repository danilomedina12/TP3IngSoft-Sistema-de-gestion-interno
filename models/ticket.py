from database import db

cuilt = "20-12345678-9"
direccion = "Calle Falsa 123"

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    hora_emision = db.Column(db.DateTime, nullable=False)
    hora_entrada = db.Column(db.DateTime, nullable=False)
    tiempo = db.Column(db.Double, nullable=False)
    monto_total = db.Column(db.Numeric(10, 2), nullable=False)
    detalles = db.Column(db.Text, nullable=False)

    vehiculo = db.relationship('Vehiculo', backref='tickets')

    def __init__(self, vehiculo_id, hora_emision, hora_entrada, tiempo, monto_total):
        self.vehiculo_id = vehiculo_id
        self.hora_emision = hora_emision
        self.hora_entrada = hora_entrada
        self.tiempo = tiempo
        self.monto_total = monto_total
        self.detalles = f'Detalles:\nCUILT: {cuilt}\nDirección: {direccion}'