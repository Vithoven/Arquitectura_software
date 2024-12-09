from gestor_pagos.app.controllers.gasto_controller import gasto_bp
from gestor_pagos.app.controllers.pago_controller import pago_bp

def register_blueprints(app):
    """
    Registra los controladores (blueprints) en la aplicación Flask.
    """
    app.register_blueprint(gasto_bp)
    app.register_blueprint(pago_bp)
