from flask import Blueprint, render_template, request, redirect, url_for, flash
from gestor_pagos.app.services.pago_service import PagoService
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
pago_bp = Blueprint('pago', __name__)
pago_service = PagoService()

@pago_bp.route('/gastos/pagar', methods=['GET', 'POST'])
def pagar_gasto():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            gasto_id = int(request.form['gasto_id'])
            fecha_pago = datetime.strptime(request.form['fecha_pago'], "%Y-%m-%d")
            
            # Registrar el pago a través del servicio
            pago_service.registrar_pago(gasto_id, fecha_pago)

            flash('Pago registrado con éxito', 'success')
            return redirect(url_for('gasto.listar_pendientes'))
        except ValueError as ve:
            logger.error(f"Error de validación: {ve}")
            flash(f"Datos inválidos: {ve}", 'danger')
        except Exception as e:
            logger.error(f"Error al registrar el pago: {e}", exc_info=True)
            flash(f"Error al registrar el pago: {e}", 'danger')
    return render_template('pagar_gasto.html')
