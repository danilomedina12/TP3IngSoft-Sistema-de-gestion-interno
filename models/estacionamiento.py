class Estacionamiento:
    def __init__(self):
        self.vehiculos = []

    def registrarIngreso(self, vehiculo):
        # Lógica para registrar el ingreso del vehículo
        self.vehiculos.append(vehiculo)

    def registrarEgreso(self, patente):
        # Lógica para registrar el egreso del vehículo
        self.vehiculos.remove(self.obtenerVehiculoPorPatente(patente))

    def obtenerVehiculoPorPatente(self, patente):
        for vehiculo in self.vehiculos:
            if self.vehiculos.patente == patente:
                return vehiculo
        return None
            
