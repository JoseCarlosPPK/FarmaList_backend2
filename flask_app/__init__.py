from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values # cargar variables de entorno de .env
import os 



app = Flask(__name__)
PATH_DIR = os.path.dirname(__file__)
PATH_ENV = os.path.join(PATH_DIR, '.env')

# Lee y guarda en un dict las variables de entorno
config = dotenv_values(PATH_ENV)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{config['USER_DB']}:{config['PASSW_DB']}@{config['HOST_DB']}/{config['NAME_DB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # no almacena las operaciones CRUD para luego procesarlas en paquete hasta la señal session.commit(). Desde la versión 3 está desactivado por defecto https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/config/#flask_sqlalchemy.config.SQLALCHEMY_TRACK_MODIFICATIONS 

db = SQLAlchemy(app=app) 
ma = Marshmallow(app)

###############################################################################
# API
###############################################################################
# Circular imports?: https://flask.palletsprojects.com/en/stable/patterns/packages/#simple-packages
from .API import endpoints








