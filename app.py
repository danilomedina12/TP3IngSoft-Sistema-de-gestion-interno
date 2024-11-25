from flask import Flask, flash, redirect, url_for, render_template
from database import db
from controllers.parking_controller import * 
from controllers.controlador_promocion import promocion_bp

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta' 
# configuracion de la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbuser:1234@localhost/estacionamiento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#crear tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

#  Rutas principales de promociones
app.register_blueprint(promocion_bp, url_prefix = '/promocion')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    return registrarVehiculo()

@app.route('/registerEgreso', methods=['GET', 'POST'])
def registerEgreso():
    return registrarEgreso()

@app.route('/vehiculos', methods=['GET'])
def vehiculos():
    return verVehiculos()

@app.route('/editar_precio', methods=['GET','POST'])
def editarPrecios():
    return editar_precio()

@app.route('/precios', methods=['GET'])
def verPrecios():
    return verPrecio()

@app.route('/reporte_diario', methods=['GET'])
def reporte():
    return reporte_diario()

if __name__ == '__main__':
    app.run(debug=True)
