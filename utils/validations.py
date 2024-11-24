import re

def validar_patente(patente):
    """
    Valida si la patente cumple con el formato nuevo (AA123AA) o el formato viejo (AAA123).
    """
    formato_nuevo = r"^[A-Z]{2}\d{3}[A-Z]{2}$"  # AA123AA
    formato_viejo = r"^[A-Z]{3}\d{3}$"          # AAA123
    
    if re.match(formato_nuevo, patente) or re.match(formato_viejo, patente):
        return True
    return False

#aaaaaaa

def holaMundo():
    print("hola")