# Proyecto de Gestión de Estacionamiento

## Requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- pymysql (u otro driver compatible con MySQL/MariaDB)

## Instalación

1. Cloná el repositorio a tu dispositivo (como prefieras)
    

2. Creá y activá el entorno virtual:

    python -m venv venv

    source venv/bin/activate  # En Linux/Mac
    
    venv\Scripts\activate     # En Windows

3. Instalá las dependencias:

    pip install -r requirements.txt

4. Configurá la base de datos:

    CREATE DATABASE estacionamiento;

5. Ejecutá el proyecto:

    python app.py


## USO

1. Configurá la conexión a la base de datos en app.py:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@localhost/estacionamiento'

2. Ejecutá la aplicación (con el entorno virtual activado):
    python app.py

Accedé a la aplicación en http://127.0.0.1:5000/

