from models.vehiculo import Vehiculo
from datetime import datetime
from flask import request, redirect, url_for, flash, render_template
from database import db

def registrarVehiculo():
    if request.method == 'POST':
        patente = request.form['patente']
        nombre = request.form['nombre_del_cliente']
        hora_ingreso = datetime.now()
        ubicacion_cochera = request.form['ubicacion_cochera']

        flash(f'Ubicación cochera recibida: {ubicacion_cochera}')  # Esto mostrará un mensaje en el navegador

        nuevo_vehiculo = Vehiculo(patente=patente, nombre_cliente=nombre, hora_ingreso=hora_ingreso, ubicacion_cochera=ubicacion_cochera)
        db.session.add(nuevo_vehiculo)
        db.session.commit()
        
        flash("Vehículo registrado correctamente con cochera asignada.")
        return redirect(url_for('index'))

    # Enviar cocheras disponibles al template
    cocheras_disponibles = {
        'Planta Baja': [f'PB-{i+1}' for i in range(15)],
        'Primer Piso': [f'P1-{i+1}' for i in range(18)],
        'Segundo Piso': [f'P2-{i+1}' for i in range(18)]
    }
    return render_template('register_vehicle.html', cocheras_disponibles=cocheras_disponibles)
