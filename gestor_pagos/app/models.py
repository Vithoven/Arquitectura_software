from app import db

class Residente(db.Model):
    run = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Departamento(db.Model):
    num_depto = db.Column(db.Integer, primary_key=True)
    nombre_propietario = db.Column(db.String(50), nullable=False)
    run_propietario = db.Column(db.Integer, db.ForeignKey('residente.run'), nullable=False)
    propietario = db.relationship('Residente', backref='departamentos', lazy=True)

class GastoComun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')
    residente_id = db.Column(db.Integer, db.ForeignKey('residente.run'), nullable=False)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=False)
    gasto_id = db.Column(db.Integer, db.ForeignKey('gasto_comun.id'), nullable=False)