from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
import marshmallow
import sqlalchemy
from ... import db
from ...models import Centro as CentroModel, Persona
from ...schemas import CentroSchema

class Centro(Resource):
    model = CentroModel
    schema = CentroSchema
    filter_to_column = {
        "nombre": model.nombre,
        "personas": model.personas,
        "correo": model.correo,
        "cp": model.cp,
        "direccion": model.direccion,
        "localidad": model.localidad,
        "provincia": model.provincia,
        "movil": model.movil,
        "telefono": model.telefono
    }


    @jwt_required()
    def get(self):
        # El método paginate usa los siguientes query params por defecto
        # - page = 1
        # - per_page = 20
        # - max_per_page = None
        # Ver: https://flask-sqlalchemy.readthedocs.io/en/stable/pagination/

        search_query = request.args.get("search", None)
        filter_query = request.args.get("filter", "nombre")
        columna = self.filter_to_column.get(filter_query, None)

        # Usamos try catch si columna es igual a None
        try:
            if search_query:
                if filter_query != "personas":
                    pag_obj = self.model.query.filter(columna.ilike(f'%{search_query}%')).paginate(count=True)
                    
                else:
                    pag_obj = db.session.query(self.model).join(self.model.personas).filter(Persona.nombre.ilike(f'%{search_query}%')).distinct().paginate(count=True)     

            else:
                pag_obj = self.model.query.paginate(count=True)

            farmacias = pag_obj.items
            total = pag_obj.total
            
        except Exception as e:
            farmacias = []
            total = 0


        return {
                "data": self.schema(many=True).dump(farmacias),
                "total": total
            }
    

    @jwt_required()
    def post(self):
        centro_schema = self.schema()

        # Con load se validan los datos
        try:
            centro = centro_schema.load(request.json)
        except marshmallow.ValidationError as e:
            # En e.messages se muestran los errores por cada atributo. Por ejemplo:
            #{ 'nombre': falta y es obligatorio }
            return e.messages, 400


        # Intentamos añadir y guardar el centro en la BD.
        # Puede haber errores como incumplir restricciones de la BD
        try:            
            db.session.add(centro)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return {'error': e._message()}, 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


        return {'msg': 'Centro creado', 'centro': centro_schema.dump(centro)}, 201



    @jwt_required()
    def put(self, id):
        centro_schema = self.schema(partial=True)
        centro = self.model.query.get(id)

        if (not centro):
            return {'error': f"Centro con id {id} no encontrado"}, 404

        # Con load se validan los datos
        try:
            centro = centro_schema.load(request.json, instance=centro)
        except marshmallow.ValidationError as e:
            # En e.messages se muestran los errores por cada atributo. Por ejemplo:
            #{ 'nombre': falta y es obligatorio }
            return e.messages, 400


        # Intentamos editar guardando la farmacia en la BD.
        # https://flask-sqlalchemy.readthedocs.io/en/stable/queries/#insert-update-delete
        # Puede haber errores como incumplir restricciones de la BD
        try:            
            # Para hacer update no es necesario hacer add()
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return {'error': e._message()}, 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


        return {'msg': 'Centro editado', 'centro': centro_schema.dump(centro)}, 201


    @jwt_required()
    def delete(self, id):
        a_borrar = self.model.query.get(id)
    
        if (not a_borrar):
            return {"error": f"No hay ningún centro con id {id}"}, 404

        try:
            db.session.delete(a_borrar)
            db.session.commit()
        except Exception as e:
            return {"error": f"Fallo del servidor al realizar el borrado del centro con id {id}"}, 500

        return {"msg": f"Centro con id {id} borrado"}, 200 # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/DELETE