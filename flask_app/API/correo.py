from . import BASE_API
from .. import app
from .. import correo
from flask import request, jsonify
from flask_jwt_extended import jwt_required
import threading

correo.init_mail(app)

def wrapper_envia_correos(destinatarios, asunto, mensaje):
    with app.app_context():
        correo.envia_correos_con_informe(destinatarios, asunto, mensaje)
        # correo.guarda_correo(destinatarios,asunto,mensaje)


@app.post(f"{BASE_API}/correo")
@jwt_required()
def enviar_correos():
    datos_correo = request.json

    thread = threading.Thread(target=wrapper_envia_correos, args=(datos_correo['destinatarios'], datos_correo['asunto'], datos_correo['mensaje']))
    thread.start()


    return jsonify({
        'msg': "Correo en proceso de envío"
    }), 202