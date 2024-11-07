

# Tarifa por hora
COSTO_POR_HORA = 10 

def calcular_costo_estacionamiento(hora_ingreso, hora_salida):
    # Calcula la duración en horas
    duracion = (hora_salida - hora_ingreso).total_seconds() / 3600
    costo = duracion * COSTO_POR_HORA
    return round(costo, 2)

def registrar_egreso(patente):
    try:
        # Conexión a la base de datos
        conn = mariadb.connect(**config)
        cursor = conn.cursor()

        # Obtén la hora de ingreso de la base de datos
        cursor.execute("SELECT hora_ingreso FROM vehiculos WHERE patente = %s", (patente,))
        registro = cursor.fetchone()

        if registro is None:
            print("No se encontró la patente.")
            return

        hora_ingreso = registro[0]
        hora_salida = datetime.now()

        # Calcula el costo
        costo = calcular_costo_estacionamiento(hora_ingreso, hora_salida)

        # Actualiza el registro con la hora de salida y el costo
        cursor.execute("""
            UPDATE vehiculos
            SET hora_salida = %s, costo_total = %s
            WHERE patente = %s
        """, (hora_salida, costo, patente))
        conn.commit()

        print(f"Vehículo {patente} registrado con éxito. Costo total: ${costo}")

    except mariadb.Error as e:
        print(f"Error al conectar con la base de datos: {e}")

    finally:
        if conn:
            conn.close()