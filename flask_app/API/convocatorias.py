import marshmallow.exceptions
from .. import app, db
from ..models import Convocatoria, Listado
from ..schemas import ConvocatoriaSchema, TIPOS_LISTADO_SCHEMAS
from . import BASE_API
from flask_jwt_extended import jwt_required
from flask import request
import sqlalchemy
import marshmallow

# SqlAlchemy OperationalError and IntegrityError bug
# https://github.com/PyMySQL/mysqlclient/issues/535


@app.get(f"{BASE_API}/convocatorias")
@jwt_required()
def api_get_convocatorias():
   # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html#order-by
   paginate_obj = Convocatoria.query.order_by(Convocatoria.fecha_ini.desc()).paginate(count=True, per_page=20)

   return { 
      "data": ConvocatoriaSchema(many=True).dump(paginate_obj.items),
      "total": paginate_obj.total
      }



@app.get(f"{BASE_API}/convocatorias/<int:id>")
@jwt_required()
def api_get_convocatoria(id):
   convocatoria = Convocatoria.query.get(id)

   if (not convocatoria):
      return {"error": f"No hay ninguna convocatoria con id {id}"}, 404
   
   return { "data": ConvocatoriaSchema().dump(convocatoria) }


@app.delete(f"{BASE_API}/convocatorias/<int:id>")
@jwt_required()
def api_delete_convocatoria(id):
   a_borrar = Convocatoria.query.get(id)

   if (not a_borrar):
      return {"error": f"No hay ninguna convocatoria con id {id}"}, 404

   try:
      db.session.delete(a_borrar)
      db.session.commit()
   except Exception as e:
      return {"error": f"Fallo del servidor al realizar el borrado de la convocatoria con id {id}"}, 500

   return {"msg": f"Centro con id {id} borrado"}, 200 # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods/DELETE



@app.post(f"{BASE_API}/convocatorias")
@jwt_required()
def api_add_convocatoria():
   # Obtengo del JSON la fecha inicial y final.
   # Creo la convocatoria.
   # Cojo los IDs de los centros que me han pasado.
   # Cojo los centros a partir de sus IDs
   # Añado los centros al listado

   data_json = request.json

   try:
      convocatoria = ConvocatoriaSchema().load(data_json["convocatoria"])
   except marshmallow.exceptions.ValidationError as e:
      # En e.messages se muestran los errores por cada atributo. Por ejemplo:
      # { 'nombre': falta y es obligatorio }
      return e.messages, 400


   # Intentamos añadir la convocatoria
   # Puede haber errores como incumplir restriciones de la BD
   try:
      db.session.add(convocatoria)
      db.session.flush()
   except sqlalchemy.exc.SQLAlchemyError as e:
      return {'error': e._message()}, 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


   for tipo_listado_schema in TIPOS_LISTADO_SCHEMAS:
      listado_json = data_json.get(tipo_listado_schema.key_json, []) # Estado inicial [] para que no haya problemas
      listado_centros = []

      for obj in listado_json:
         centro = tipo_listado_schema.model_center.query.get(obj["id"])

         if (not centro):
            db.session.rollback()
            return {'error': f"Centro con id {obj['id']} no encontrado"}, 404

         # Preparamos al centro para el formato de listado
         centro.id_centro = obj["id"]
         centro.num_plazas = obj["num_plazas"]
         centro.id_convocatoria = convocatoria.id

         listado_centros.append(centro)

      listado_centros = tipo_listado_schema(many=True).load(tipo_listado_schema(many=True).dump(listado_centros))

      db.session.add_all(listado_centros)
     

   # Intentamos guardar los cambios
   # Puede haber errores como incumplir restriciones de la BD
   try:
      db.session.commit()
   except sqlalchemy.exc.SQLAlchemyError as e:
      db.session.rollback()
      return {'error': e._message()}, 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8

   return { 
      "convocatoria": ConvocatoriaSchema().dump(convocatoria)
   }, 201



@app.put(f"{BASE_API}/convocatorias/<int:id>")
@jwt_required()
def api_update_convocatoria(id):
   convocatoria = Convocatoria.query.get(id)

   if (not convocatoria):
      return {"error": f"No hay ninguna convocatoria con id {id}"}, 404

   data_json = request.json

   try:
      convocatoria = ConvocatoriaSchema().load(data_json["convocatoria"], instance=convocatoria)
   except marshmallow.exceptions.ValidationError as e:
      # En e.messages se muestran los errores por cada atributo. Por ejemplo:
      # { 'nombre': falta y es obligatorio }
      return e.messages, 400


   # Intentamos actualizar la convocatoria
   # Puede haber errores como incumplir restriciones de la BD
   try:
      db.session.flush()
   except sqlalchemy.exc.SQLAlchemyError as e:
      return {'error': e._message()}, 409
   

   Listado.query.filter_by(id_convocatoria=id).delete()
   

   for tipo_listado_schema in TIPOS_LISTADO_SCHEMAS:
      listado_json = data_json.get(tipo_listado_schema.key_json, []) # Estado inicial [] para que no haya problemas
      listado_centros = []

      for obj in listado_json:
         centro = tipo_listado_schema.model_center.query.get(obj["id"])

         if (not centro):
            db.session.rollback()
            return {'error': f"Centro con id {obj['id']} no encontrado"}, 404

         # Preparamos al centro para el formato de listado
         centro.id_centro = obj["id"]
         centro.num_plazas = obj["num_plazas"]
         centro.id_convocatoria = convocatoria.id

         listado_centros.append(centro)

      listado_centros = tipo_listado_schema(many=True).load(tipo_listado_schema(many=True).dump(listado_centros))

      db.session.add_all(listado_centros)   


   # Intentamos guardar los cambios
   # Puede haber errores como incumplir restriciones de la BD
   try:
      db.session.commit()
   except sqlalchemy.exc.SQLAlchemyError as e:
      db.session.rollback()
      return {'error': e._message()}, 409 # https://datatracker.ietf.org/doc/html/rfc7231#section-6.5.8


   return {
      "convocatoria": ConvocatoriaSchema().dump(convocatoria)
   }, 200