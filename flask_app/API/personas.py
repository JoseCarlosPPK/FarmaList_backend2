from .. import app
from ..models import Persona
from ..schemas import PersonaSchema
from . import BASE_API
from flask import jsonify, request
from flask_jwt_extended import jwt_required

@app.get(f"{BASE_API}/personas")
@jwt_required()
def api_get_personas():
    name = request.args.get("name", None)

    if name:
        paginate_obj = Persona.query.filter(Persona.nombre.ilike(f'%{name}%')).paginate(count=True)

    else:
        paginate_obj = Persona.query.paginate(count=True)

    return jsonify(
        {
            "data": PersonaSchema(many=True).dump(paginate_obj.items),
            "total": paginate_obj.total
        }
    )

