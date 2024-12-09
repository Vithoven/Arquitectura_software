from app.models.gasto_model import GastoComun
from app.models.residente_model import Residente
from app.models.departamento_model import Departamento
from app import db

class GastoService:
    def generar_gastos(self, mes, anio, monto):
        residentes = Residente.query.all()
        if not residentes:
            raise Exception("No hay residentes disponibles.")
        for residente in residentes:
            gasto = GastoComun(
                descripcion=f"Gasto común {mes}/{anio}",
                monto=monto,
                mes=mes,
                anio=anio,
                residente_id=residente.id
            )
            db.session.add(gasto)
        db.session.commit()

    def obtener_pendientes(self):
        return db.session.query(
            GastoComun.descripcion,
            GastoComun.monto,
            GastoComun.mes,
            GastoComun.anio,
            Departamento.num_depto
        ).join(
            Departamento, GastoComun.residente_id == Departamento.run_propietario
        ).filter(GastoComun.estado == "Pendiente").all()
