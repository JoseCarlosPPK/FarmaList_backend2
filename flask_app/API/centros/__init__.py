from flask_restful import Api
from .. import app,BASE_API
from .farmacia import Farmacia
from .farmacia_hospitalaria import FarmaciaHospitalaria

api = Api(app)

# Registro de las APIs 
api.add_resource(Farmacia, f"{BASE_API}/farmacias", f"{BASE_API}/farmacias/<int:id>")
api.add_resource(FarmaciaHospitalaria, f"{BASE_API}/farmacias-hospitalarias", f"{BASE_API}/farmacias-hospitalarias/<int:id>")