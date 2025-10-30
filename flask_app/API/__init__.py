from flask_cors import CORS
from .. import app

BASE_API = "/api"
# https://corydolphin.com/flask-cors/
CORS(app, supports_credentials=True, resources=f'{BASE_API}/*')