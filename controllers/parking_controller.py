# controllers/parking_controller.py

from flask import request, redirect, url_for, flash, render_template
from database import db
from models.vehiculo import Vehiculo
from models.ticket import Ticket
from models.precio_estadia import Precio
from models.horario import Horario
from datetime import datetime
from utils.validations import validar_patente
from models.promocion import Promocion
from sqlalchemy.sql import func
from sqlalchemy.sql import text

def obtener_vehiculo_por_patente(patente):
    """
    Busca un vehículo en la base de datos dado su patente.
    Retorna el objeto Vehiculo si existe, de lo contrario, None.
    """
    return Vehiculo.query.filter_by(patente=patente).first()

def tiempo_total_estadia(hora_ingreso, hora_egreso):
    # Calcula la duración en horas
    duracion = (hora_egreso - hora_ingreso).total_seconds() / 3600
    return duracion

def tiempo_total_estadia_minutos(hora_ingreso, hora_egreso):
    # Calcula la duración en horas
    duracion = (hora_egreso - hora_ingreso).total_seconds() / 60
    return duracion

# Función para calcular el costo con el descuento
def calcular_costo_estacionamiento(hora_ingreso, hora_egreso, vehiculo):
    # Obtenemos el precio base por hora del vehículo
    precio = Precio.query.filter(Precio.tipo_vehiculo == vehiculo.tipo_vehiculo).first()
    
    # Calculamos la duración total en horas
    duracion = tiempo_total_estadia(hora_ingreso, hora_egreso)
    
    # Calculamos el costo sin descuento
    costo = duracion * precio.precio
    
    # Obtenemos las promociones aplicables
    promociones = Promocion.query.filter(Promocion.cantidad_horas <= duracion).all()
    
    # Si hay promociones disponibles, seleccionamos la mejor
    if promociones:
        mejor_promocion = max(promociones, key=lambda p: p.porcentaje_descuento)
        # Aplicamos el descuento
        costo_con_descuento = costo * (1 - mejor_promocion.porcentaje_descuento / 100)
    else:
        # Si no hay promociones, el costo no tiene descuento
        costo_con_descuento = costo
    
    return round(costo_con_descuento, 2)

# @app.route('/registerEgreso', methods=['GET', 'POST'])
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
        if vehiculo is None:
            flash('El vehículo no se encuentra en estacionamiento', 'error')
            return redirect(url_for('registerEgreso'))
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
                monto_total=calcular_costo_estacionamiento(vehiculo.hora_ingreso, vehiculo.hora_egreso, vehiculo)
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
            ticket.tiempo=tiempo_total_estadia(vehiculo.hora_ingreso, vehiculo.hora_egreso)
            return render_template('ticket_detalle.html', ticket=ticket)

        else:
            flash("Vehículo no encontrado en la base de datos.", "error")

    return render_template('registerEgreso.html')


#@app.route('/register', methods=['GET', 'POST'])
def registrarVehiculo():
    # Obtener la hora actual
    hora_actual = datetime.now().time()

    # Verificar si la hora está fuera del horario permitido
    if hora_actual < Horario.hora_apertura or hora_actual >= Horario.hora_cierre:
        flash("Registro de ingreso permitido solo entre las {} y {}.".format(
            Horario.hora_apertura.strftime("%H:%M"), 
            Horario.hora_cierre.strftime("%H:%M")
        ), "warning")
        return redirect(url_for('index'))  # Redirige al inicio o a una página adecuada

    if request.method == 'POST':
        patente = request.form['patente']
        nombre = request.form['nombre_del_cliente']
        hora_ingreso = datetime.now()
        ubicacion_cochera = request.form['ubicacion_cochera']
        tipo_vehiculo = request.form['tipo_vehiculo']

        if not validar_patente(patente):
            flash("La patente no tiene un formato valido.", "error")
            return redirect(url_for('register'))


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
                    vehiculo.tipo_vehiculo = tipo_vehiculo
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
                    tipo_vehiculo = tipo_vehiculo,
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
    tipos_vehiculos = Precio.tipos_vehiculos() 
        # obtener las cocheras ocupadas
    cocheras_ocupadas = Vehiculo.query.filter(
        Vehiculo.hora_egreso == None
        ).with_entities(Vehiculo.ubicacion_cochera).all()
    
    cocheras_ocupadas = [c[0] for c in cocheras_ocupadas] #lista de cocheras ocupadas

    for planta, cocheras in cocheras_disponibles.items():
        cocheras_disponibles[planta] = [c for c in cocheras if c not in cocheras_ocupadas]

    return render_template('register_vehiculo.html', cocheras_disponibles=cocheras_disponibles, tipos_vehiculos=tipos_vehiculos)

#@app.route('/vehiculos', methods=['GET'])
def verVehiculos():
    # Consultar todos los vehículos registrados
    vehiculos = Vehiculo.query.all()  # Obtiene todos los registros de la tabla vehiculos

    # Renderizar la plantilla y pasar la lista de vehículos
    return render_template('ver_vehiculos.html', vehiculos=vehiculos)

#@app.route('/precios', methods=['GET'])
def verPrecio():
    # Consulto todos los precios que existen
    precios = Precio.query.all()
    
    return render_template('precios.html', precios=precios)  # Cambiado a `precios`


#@app.route('/editar_precio', methods=['GET', 'POST'])
def editar_precio():
    tipos_vehiculos = Precio.tipos_vehiculos()

    if request.method == 'POST':
        tipo_vehiculo = request.form['tipo_vehiculo']
        nuevo_precio = float(request.form['nuevo_precio'])

        # Buscar el precio actual del tipo de vehículo
        precio = Precio.query.filter_by(tipo_vehiculo=tipo_vehiculo).first()

        if precio:
            # Si ya existe, actualiza el precio
            precio.precio = nuevo_precio
            flash("Precio actualizado correctamente.")
        else:
            # Si no existe, crea un nuevo registro
            precio = Precio(tipo_vehiculo=tipo_vehiculo, precio=nuevo_precio)
            db.session.add(precio)
            flash("Precio registrado correctamente.")

        db.session.commit()

        # Redirige después de actualizar o crear el precio
        return redirect(url_for('verPrecios'))

    return render_template('editar_precio.html', tipos_vehiculos=tipos_vehiculos)

from datetime import datetime, timedelta
from flask import request, render_template
from sqlalchemy import func

#@app.route('/reporte_diario', methods=['GET'])
def reporte_diario():
    # Obtener la fecha desde el parámetro de la URL o usar la fecha actual
    fecha_param = request.args.get('fecha')
    try:
        fecha_hoy = datetime.strptime(fecha_param, '%Y-%m-%d').date() if fecha_param else datetime.now().date()
    except ValueError:
        return "Formato de fecha inválido. Use 'YYYY-MM-DD'.", 400

    # Vehículos que ingresaron en la fecha especificada
    vehiculos_ingresados = Ticket.query.filter(func.date(Ticket.hora_entrada) == fecha_hoy).count()

    # Vehículos que salieron en la fecha especificada
    vehiculos_salidos = Ticket.query.filter(
        func.date(Ticket.hora_emision) == fecha_hoy,
        Ticket.hora_emision.isnot(None)
    ).count()

    # Calcular ingresos totales del día
    ingresos_totales = db.session.query(func.sum(Ticket.monto_total)).filter(
        func.date(Ticket.hora_emision) == fecha_hoy,
        Ticket.hora_emision.isnot(None)
    ).scalar() or 0.0

    # Calcular tiempo promedio de estacionamiento con mayor precisión
    result = db.session.execute(
        text("""
            SELECT AVG(TIMESTAMPDIFF(SECOND, hora_entrada, hora_emision)) / 60 AS tiempo_promedio
            FROM tickets
            WHERE DATE(hora_emision) = :fecha_hoy AND hora_emision IS NOT NULL
        """), {"fecha_hoy": fecha_hoy}
    ).scalar()

    # Convertir el resultado a float, o usar 0.0 si es None
    tiempos_estacionamiento = float(result) if result is not None else 0.0

    # Convertir a timedelta
    tiempo_promedio = timedelta(minutes=tiempos_estacionamiento)

    # Obtener detalles de vehículos (tabla)
    detalle_vehiculos = Ticket.query.filter(
        func.date(Ticket.hora_emision) == fecha_hoy,
        Ticket.hora_emision.isnot(None)
    ).all()

    # Renderizar el reporte diario
    return render_template('reporte_diario.html', 
                           fecha_hoy=fecha_hoy, 
                           vehiculos_ingresados=vehiculos_ingresados, 
                           vehiculos_salidos=vehiculos_salidos,
                           ingresos_totales=ingresos_totales, 
                           tiempo_promedio=tiempo_promedio, 
                           detalle_vehiculos=detalle_vehiculos)
