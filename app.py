from flask import Flask, flash, redirect, url_for, render_template
from database import db
from controllers.parking_controller import * 

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta' 
# configuracion de la base de datos 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://danilo:falilv@localhost/estacionamiento'
db.init_app(app)

#crear tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True)
