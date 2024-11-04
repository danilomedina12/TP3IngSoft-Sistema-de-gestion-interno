# controllers/parking_controller.py

from flask import request, redirect, url_for, flash, render_template
from database import db
from models.vehiculo import Vehiculo
from datetime import datetime
from app import app

@app.route('/register', methods=['GET', 'POST'])
def registrarVehiculo():
    if request.method == 'POST':
        patente = request.form['patente']
        nombre = request.form['nombre_del_cliente']
        hora_ingreso = datetime.now()
        ubicacion_cochera = request.form['ubicacion_cochera']

        if not patente or not nombre:
            flash("Patente y nombre del cliente son obligatorios.", "error")
            return redirect(url_for('register_vehiculo'))  # Redirige a la página de registro

        # Flash para mostrar ubicación cochera recibida
        flash(f'Ubicación cochera recibida: {ubicacion_cochera}')  

        try:
            nuevo_vehiculo = Vehiculo(
                patente=patente, 
                nombre_cliente=nombre, 
                hora_ingreso=hora_ingreso, 
                ubicacion_cochera=ubicacion_cochera
            )
            db.session.add(nuevo_vehiculo)
            db.session.commit()
            flash("Vehículo registrado correctamente con cochera asignada.")
        except Exception as e:
            db.session.rollback()  # Revertir cambios en caso de error
            flash(f"Ocurrió un error al registrar el vehículo: {str(e)}", "error")

        return redirect(url_for('index'))  # Redirige a la página de inicio o donde corresponda

    # Enviar cocheras disponibles al template
    cocheras_disponibles = {
        'Planta Baja': [f'PB-{i+1}' for i in range(15)],
        'Primer Piso': [f'P1-{i+1}' for i in range(18)],
        'Segundo Piso': [f'P2-{i+1}' for i in range(18)]
    }
    return render_template('register_vehicle.html', cocheras_disponibles=cocheras_disponibles)

@app.route('/vehiculos', methods=['GET'])
def verVehiculos():
    # Consultar todos los vehículos registrados
    vehiculos = Vehiculo.query.all()  # Obtiene todos los registros de la tabla vehiculos

    # Renderizar la plantilla y pasar la lista de vehículos
    return render_template('ver_vehiculos.html', vehiculos=vehiculos)
