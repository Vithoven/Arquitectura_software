from flask import Blueprint, jsonify, request
from app import db
from app.models import Residente, GastoComun, Pago
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Generar gastos comunes
@main_bp.route('/gastos/generar', methods=['POST'])
def generar_gastos():
    data = request.json
    mes = data.get('mes')
    anio = data.get('anio')
    monto = data.get('monto', 10000)
    
    residentes = Residente.query.all()
    for residente in residentes:
        gasto = GastoComun(
            descripcion=f'Gasto común {mes}/{anio}',
            monto=monto,
            mes=mes,
            anio=anio,
            residente_id=residente.id
        )
        db.session.add(gasto)
    db.session.commit()
    
    return jsonify({"mensaje": "Gastos generados con éxito"}), 201

# Marcar gasto como pagado
@main_bp.route('/gastos/pagar', methods=['POST'])
def pagar_gasto():
    data = request.json
    gasto_id = data.get('gasto_id')
    fecha_pago = datetime.strptime(data.get('fecha_pago'), "%Y-%m-%d")
    
    gasto = GastoComun.query.get_or_404(gasto_id)
    if gasto.estado == "Pagado":
        return jsonify({"mensaje": "Pago duplicado"}), 400
    
    gasto.estado = "Pagado"
    pago = Pago(monto=gasto.monto, fecha_pago=fecha_pago, gasto_id=gasto.id)
    db.session.add(pago)
    db.session.commit()
    
    return jsonify({"mensaje": "Pago registrado con éxito", "gasto": gasto.id}), 200

# Listar gastos pendientes
@main_bp.route('/gastos/pendientes', methods=['GET'])
def listar_pendientes():
    mes_hasta = int(request.args.get('mes_hasta'))
    anio_hasta = int(request.args.get('anio_hasta'))
    
    pendientes = GastoComun.query.filter(
        GastoComun.estado == "Pendiente",
        (GastoComun.anio < anio_hasta) | 
        ((GastoComun.anio == anio_hasta) & (GastoComun.mes <= mes_hasta))
    ).all()
    
    if not pendientes:
        return jsonify({"mensaje": "Sin montos pendientes"}), 200
    
    return jsonify([{
        "id": gasto.id,
        "descripcion": gasto.descripcion,
        "monto": gasto.monto,
        "mes": gasto.mes,
        "anio": gasto.anio
    } for gasto in pendientes]), 200
