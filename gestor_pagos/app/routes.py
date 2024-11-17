from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app import db
from app.models import Residente, GastoComun, Pago
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/gastos/generar', methods=['GET', 'POST'])
def generar_gastos():
    if request.method == 'POST':
        mes = request.form['mes']
        anio = request.form['anio']
        monto = float(request.form.get('monto', 10000))

        residentes = Residente.query.all()
        for residente in residentes:
            gasto = GastoComun(
                descripcion=f'Gasto común {mes}/{anio}',
                monto=monto,
                mes=int(mes),
                anio=int(anio),
                residente_id=residente.id
            )
            db.session.add(gasto)
        db.session.commit()

        flash('Gastos generados con éxito', 'success')
        return redirect(url_for('main.listar_pendientes'))

    return render_template('generar_gasto.html')

@main_bp.route('/gastos/pagar', methods=['GET', 'POST'])
def pagar_gasto():
    if request.method == 'POST':
        gasto_id = request.form['gasto_id']
        fecha_pago = datetime.strptime(request.form['fecha_pago'], "%Y-%m-%d")

        gasto = GastoComun.query.get_or_404(gasto_id)
        if gasto.estado == "Pagado":
            flash('El gasto ya está pagado', 'danger')
            return redirect(url_for('main.listar_pendientes'))

        gasto.estado = "Pagado"
        pago = Pago(monto=gasto.monto, fecha_pago=fecha_pago, gasto_id=gasto.id)
        db.session.add(pago)
        db.session.commit()

        flash('Pago registrado con éxito', 'success')
        return redirect(url_for('main.listar_pendientes'))

    return render_template('pagar_gasto.html')

@main_bp.route('/gastos/pendientes', methods=['GET'])
def listar_pendientes():
    pendientes = GastoComun.query.filter_by(estado="Pendiente").all()
    return render_template('pendientes.html', pendientes=pendientes)

@main_bp.route('/')
def index():
    return render_template('index.html')