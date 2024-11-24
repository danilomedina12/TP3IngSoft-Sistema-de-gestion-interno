from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.promocion import Promocion
from database import db

promocion_bp = Blueprint('promocion', __name__)

@promocion_bp.route('/promociones', methods=['GET'])
def listar_promociones():
    promociones = Promocion.query.all()
    return render_template('promociones/listar.html', promociones=promociones)

@promocion_bp.route('/promociones/nueva', methods=['GET', 'POST'])
def nueva_promocion():
    if request.method == 'POST':
        cantidad_horas = request.form.get('cantidad_horas')
        porcentaje_descuento = request.form.get('porcentaje_descuento')
        
        try:
            promocion = Promocion(
                cantidad_horas=int(cantidad_horas),
                porcentaje_descuento=float(porcentaje_descuento)
            )
            db.session.add(promocion)
            db.session.commit()
            flash('Promoción creada con éxito.', 'success')
            return redirect(url_for('promocion.listar_promociones'))
        except Exception as e:
            flash('Error al crear la promoción.', 'danger')
            print(e)

    return render_template('promociones/nueva.html')
