import logging
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app import db
from app.models import Residente, GastoComun, Pago, Departamento  # Asegúrate de importar Departamento
from datetime import datetime

# Configuración del registro de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/gastos/generar', methods=['GET', 'POST'])
def generar_gastos():
    if request.method == 'POST':
        try:
            logger.info("Procesando los datos del formulario para generar gastos")
            mes = request.form['mes']
            anio = request.form['anio']
            monto = float(request.form.get('monto', 10000))

            logger.info(f"Datos recibidos del formulario: mes={mes}, anio={anio}, monto={monto}")
            
            residentes = Residente.query.all()
            if not residentes:
                logger.warning("No se encontraron residentes para asignar los gastos.")
                flash("No se encontraron residentes para asignar los gastos.", "warning")
                return render_template('generar_gasto.html')

            for residente in residentes:
                logger.info(f"Asignando gasto al residente con ID {residente.id}")
                gasto = GastoComun(
                    descripcion=f'Gasto común {mes}/{anio}',
                    monto=monto,
                    mes=int(mes),
                    anio=int(anio),
                    residente_id=residente.id
                )
                db.session.add(gasto)
            db.session.commit()

            logger.info("Gastos generados con éxito")
            flash('Gastos generados con éxito', 'success')
            return redirect(url_for('main.listar_pendientes'))
        except Exception as e:
            logger.error(f"Error al generar los gastos: {e}", exc_info=True)
            db.session.rollback()
            flash(f"Error al generar los gastos: {e}", "danger")
    return render_template('generar_gasto.html')

@main_bp.route('/gastos/pagar', methods=['GET', 'POST'])
def pagar_gasto():
    if request.method == 'POST':
        try:
            logger.info("Procesando los datos del formulario para registrar un pago")
            gasto_id = int(request.form['gasto_id'])
            fecha_pago = datetime.strptime(request.form['fecha_pago'], "%Y-%m-%d")

            logger.info(f"Datos recibidos del formulario: gasto_id={gasto_id}, fecha_pago={fecha_pago}")
            
            gasto = GastoComun.query.get_or_404(gasto_id)
            if gasto.estado == "Pagado":
                logger.warning(f"Intento de pagar un gasto ya pagado: ID {gasto_id}")
                flash('El gasto ya está pagado', 'danger')
                return redirect(url_for('main.listar_pendientes'))

            gasto.estado = "Pagado"
            pago = Pago(monto=gasto.monto, fecha_pago=fecha_pago, gasto_id=gasto.id)
            db.session.add(pago)
            db.session.commit()

            logger.info(f"Pago registrado con éxito para el gasto con ID {gasto_id}")
            flash('Pago registrado con éxito', 'success')
            return redirect(url_for('main.listar_pendientes'))
        except Exception as e:
            logger.error(f"Error al registrar el pago: {e}", exc_info=True)
            db.session.rollback()
            flash(f"Error al registrar el pago: {e}", "danger")
    return render_template('pagar_gasto.html')

@main_bp.route('/gastos/pendientes', methods=['GET'])
def listar_pendientes():
    try:
        logger.info("Obteniendo los gastos pendientes con información del departamento")
        
        # Realizar el join entre GastoComun y Departamento
        pendientes = db.session.query(
            GastoComun.descripcion,
            GastoComun.monto,
            GastoComun.mes,
            GastoComun.anio,
            Departamento.num_depto  # Obtener el número de departamento
        ).join(
            Departamento,  # Relacionamos la tabla GastoComun con Departamento
            GastoComun.residente_id == Departamento.run_propietario  # Relación entre las tablas
        ).filter(
            GastoComun.estado == "Pendiente"  # Filtramos solo los gastos pendientes
        ).all()

        logger.info(f"Se encontraron {len(pendientes)} gastos pendientes")
        return render_template('pendientes.html', pendientes=pendientes)
    except Exception as e:
        logger.error(f"Error al obtener los gastos pendientes: {e}", exc_info=True)
        flash(f"Error al obtener los gastos pendientes: {e}", "danger")
        return render_template('pendientes.html', pendientes=[])

@main_bp.route('/')
def index():
    logger.info("Renderizando la página de inicio")
    return render_template('index.html')