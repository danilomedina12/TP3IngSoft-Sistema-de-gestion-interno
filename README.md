# Proyecto de Gestión de Estacionamiento

## Requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- pymysql (u otro driver compatible con MySQL/MariaDB)

## Instalación

1. Cloná el repositorio: Podés clonar este proyecto desde GitHub utilizando el método que prefieras (HTTPS, SSH, GitHub CLI, etc.).
    

2. Creá y activá el entorno virtual:

    python -m venv venv

    source venv/bin/activate  # En Linux/Mac
    
    venv\Scripts\activate     # En Windows

3. Instalá las dependencias:

    pip install -r requirements.txt

4. Configurá la base de datos:

    Creá la base de datos estacionamiento en tu servidor local de MariaDB/MySQL:

    CREATE DATABASE estacionamiento;

5. Configurá la conexión a la base de datos en app.py:

    Abrí app.py y actualizá la URI de la base de datos:

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contraseña@localhost/estacionamiento'

Reemplazá usuario y contraseña con tus credenciales de MariaDB/MySQL.

6. Inicializá las tablas:
    
    Ejecutá el proyecto para que SQLAlchemy cree las tablas en la base de datos:

    python app.py


## USO

1. Ejecutá la aplicación (asegurate de tener el entorno virtual activado):

    python app.py

2. Accedé a la aplicación en tu navegador en http://127.0.0.1:5000/.

## Mostrar vehiculos

Esta el endpoint http://127.0.0.1:5000/vehiculos donde se ven los vehiculos registrados.