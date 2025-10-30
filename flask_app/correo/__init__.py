from flask_mail import Mail, Message
from dotenv import dotenv_values, get_key
import datetime
import imaplib
import ssl
import time
import os

# Inicializar Flask-Mail
mail = Mail()
PATH_ENV = os.path.join(os.path.dirname(__file__), '.env')

def init_mail(app):
    """
    Inicializa la extensión Flask-Mail con la app de Flask
    a la que se le añadirán los parámetros de configuración de .env

    Args:
        app (Flask): aplicación de Flask
    """

    config = dotenv_values(PATH_ENV) # Devuelve un diccionario con las variables cargadas
    app.config.from_mapping(config)

    app.config['MAIL_PORT'] = int(app.config['MAIL_PORT'])
    app.config['MAIL_USE_TLS'] = to_bool(app.config['MAIL_USE_TLS'])
    app.config['MAIL_USE_SSL'] = to_bool(app.config['MAIL_USE_SSL'])

    mail.init_app(app)



def to_bool(cadena):
    return cadena == "True"


def envia_correos(destinatarios, asunto, mensaje):
    con_exito = []
    fallidos = []

    # Código de https://flask-mail.readthedocs.io/en/latest/#bulk-emails
    with mail.connect() as conn:
        for destino in destinatarios:
            try:
                msg = Message(
                    subject=asunto,
                    body=mensaje,
                    recipients=[destino]
                )
                conn.send(msg)
                con_exito.append(destino)

            except Exception as e:
                fallidos.append(destino)


    return {
        'con_exito': con_exito,
        'fallidos': fallidos
    }


def envia_correos_con_informe(destinatarios, asunto, mensaje):
    today = datetime.datetime.today()
    respuesta = envia_correos(destinatarios, asunto, mensaje)

    new_asunto = f"INFORME: {asunto}"
    new_body = f"""
INFORME ENVÍO DE CORREOS
------------------------
Ha envíado un correo a través de la plataforma FarmaList el {today.day}/{today.month}/{today.year} a las {today.hour}:{today.minute}.

* Mensajes enviados con éxito: {len(respuesta['con_exito'])}
* Mensajes fallidos: {len(respuesta['fallidos'])}
"""

    if (len(respuesta['fallidos']) > 0):
        new_body += f"""

Emails que han fallado:
{respuesta['fallidos']}
"""
        
    new_body += f"""
Destinatarios:
{destinatarios}
"""

    msg = Message(
        subject=new_asunto,
        body=new_body,
        recipients=[get_key(PATH_ENV, "MAIL_USERNAME")]
    )

    mail.send(msg)


# Función para guardar en "Enviados" un correo usando IMAP
# Con imaplib.IMAP4 funciona, pero la conexión no usa SSL y por tanto
# no es seguro. Se ha intentado con la versión SSL pero obtenemos un 
# error, seguramente porque debemos configurar algo de SSL, ya que no
# disponemos de certificado

# def guarda_correo(destinatarios, asunto, mensaje):
#     with imaplib.IMAP4("correo.ugr.es", 143) as imap:
#         imap.login(get_key(PATH_ENV, "MAIL_USERNAME"), get_key(PATH_ENV, "MAIL_PASSWORD"))

#         # print("Listado", imap.list())

#         res = imap.select('INBOX.Sent')
#         # print("Después de select", res)

#         msg = Message(
#             subject=asunto,
#             body="",
#             recipients=[""],
#             bcc=["josecarlosxd27@gmail.com", "josegalva1o@gmail.com"]
#         )

#         res = imap.append('INBOX.Sent', None, imaplib.Time2Internaldate(time.time()), str(msg).encode('utf-8'))

#         # print("Después de append", res)