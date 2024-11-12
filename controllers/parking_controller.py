# controllers/parking_controller.py

from flask import request, redirect, url_for, flash, render_template
from database import db
from models.vehiculo import Vehiculo
from models.ticket import Ticket
from datetime import datetime
from app import app

def obtener_vehiculo_por_patente(patente):
    """
    Busca un vehículo en la base de datos dado su patente.
    Retorna el objeto Vehiculo si existe, de lo contrario, None.
    """
    return Vehiculo.query.filter_by(patente=patente).first()


# Tarifa por hora
COSTO_POR_HORA = 10 

def tiempo_total_estadia(hora_ingreso, hora_egreso):
    # Calcula la duración en horas
    duracion = (hora_egreso - hora_ingreso).total_seconds() / 3600
    return duracion

def calcular_costo_estacionamiento(hora_ingreso, hora_egreso):
    # Calcula la duración en horas
    duracion = tiempo_total_estadia(hora_ingreso, hora_egreso)
    costo = duracion * COSTO_POR_HORA
    return round(costo, 2)

@app.route('/registerEgreso', methods=['GET', 'POST'])
def registrarEgreso():
    if request.method == 'POST':
        patente = request.form['patente']
        hora_egreso = datetime.now()

        # Verifica que el campo 'patente' no esté vacío
        if not patente:
            flash("Patente es obligatorio.", "error")
            return render_template('registerEgreso.html')

        # Llama a la función para obtener el vehículo por patente
        vehiculo = obtener_vehiculo_por_patente(patente)

        if vehiculo.hora_egreso is None:
            # Cambia el valor del atributo `hora_egreso` por la variable `hora_egreso`
            vehiculo.hora_egreso = hora_egreso
            db.session.commit()  # Guarda los cambios en la base de datos
            # Crear y guardar el ticket en la base de datos
            ticket = Ticket(
                vehiculo_id=vehiculo.id,
                hora_emision=hora_egreso,
                hora_entrada=vehiculo.hora_ingreso,
                tiempo=tiempo_total_estadia(vehiculo.hora_ingreso, vehiculo.hora_egreso),
                monto_total=calcular_costo_estacionamiento(vehiculo.hora_ingreso, vehiculo.hora_egreso)
            )
            try:
                db.session.add(ticket)
                db.session.commit()
                flash("Salida registrada y ticket generado correctamente.", "success")
                vehiculo.ubicacion_cochera = "SALIO" # Se libera la ubicación de la cochera, así está disponible otra vez
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f"Error al registrar la salida: {str(e)}", "error")
                return render_template('registerEgreso.html')
            
            # Renderizar el ticket generado en un HTML
            return render_template('ticket_detalle.html', ticket=ticket)

        else:
            flash("Vehículo no encontrado en la base de datos.", "error")

    return render_template('registerEgreso.html')


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

        # Buscar si ya existe el vehículo
        vehiculo = obtener_vehiculo_por_patente(patente)

        if vehiculo:
            if vehiculo.hora_egreso is None:
                flash("El vehículo ya está en el estacionamiento. No se guarda ingreso", "error")
                return redirect(url_for('index'))
            else:
                #Actualiza los datos para un nuevo ingreso
                try:
                    vehiculo.hora_ingreso = hora_ingreso
                    vehiculo.hora_egreso = None
                    vehiculo.nombre_cliente = nombre
                    vehiculo.ubicacion_cochera = ubicacion_cochera
                    db.session.commit()
                    flash("Vehículo re-ingresado y datos actualizados correctamente.")
                except Exception as e:
                    db.session.rollback()  # Revertir cambios en caso de error
                    flash(f"Ocurrió un error al registrar el vehículo: {str(e)}", "error")
                
        else:
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

    # obtener las cocheras ocupadas
    cocheras_ocupadas = Vehiculo.query.filter(
        Vehiculo.hora_egreso == None
        ).with_entities(Vehiculo.ubicacion_cochera).all()
    
    cocheras_ocupadas = [c[0] for c in cocheras_ocupadas] #lista de cocheras ocupadas

    for planta, cocheras in cocheras_disponibles.items():
        cocheras_disponibles[planta] = [c for c in cocheras if c not in cocheras_ocupadas]

    return render_template('register_vehiculo.html', cocheras_disponibles=cocheras_disponibles)

@app.route('/vehiculos', methods=['GET'])
def verVehiculos():
    # Consultar todos los vehículos registrados
    vehiculos = Vehiculo.query.all()  # Obtiene todos los registros de la tabla vehiculos

    # Renderizar la plantilla y pasar la lista de vehículos
    return render_template('ver_vehiculos.html', vehiculos=vehiculos)
