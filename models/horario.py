from datetime import datetime, time

class Horario:
    hora_apertura = time(8, 30)  # 8:30 am
    hora_cierre = time(17,58)
 
    @staticmethod
    def hora_de_apertura(self):
        return self.hora_apertura
    
    @staticmethod
    def hora_de_cierre(self):
        return self.hora_cierre