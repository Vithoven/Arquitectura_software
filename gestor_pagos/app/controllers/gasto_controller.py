from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.gasto_service import GastoService
import logging

logger = logging.getLogger(__name__)
gasto_bp = Blueprint('gasto', __name__)
gasto_service = GastoService()

@gasto_bp.route('/gastos/generar', methods=['GET', 'POST'])
def generar_gastos():
    if request.method == 'POST':
        try:
            mes = request.form['mes']
            anio = request.form['anio']
            monto = float(request.form['monto'])
            gasto_service.generar_gastos(mes, anio, monto)
            flash('Gastos generados con éxito', 'success')
            return redirect(url_for('gasto.listar_pendientes'))
        except Exception as e:
            logger.error(f"Error al generar gastos: {e}")
            flash(f"Error: {e}", 'danger')
    return render_template('generar_gasto.html')

@gasto_bp.route('/gastos/pendientes', methods=['GET'])
def listar_pendientes():
    try:
        pendientes = gasto_service.obtener_pendientes()
        return render_template('pendientes.html', pendientes=pendientes)
    except Exception as e:
        flash(f"Error: {e}", 'danger')
        return render_template('pendientes.html', pendientes=[])
