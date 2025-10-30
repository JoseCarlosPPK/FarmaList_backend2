from .. import BASE_API
from ... import app, db
from ...models import ListadoFarmaciasHospitalarias, Persona
from ...schemas import ListadoFarmaciasHospitalariasSchema
from flask_jwt_extended import jwt_required
from flask import request

Listado = ListadoFarmaciasHospitalarias
Schema = ListadoFarmaciasHospitalariasSchema
filter_to_column = {
        "nombre": Listado.nombre,
        "personas": Listado.personas,
        "correo": Listado.correo,
        "cp": Listado.cp,
        "direccion": Listado.direccion,
        "localidad": Listado.localidad,
        "provincia": Listado.provincia,
        "movil": Listado.movil,
        "telefono": Listado.telefono,
        "num_plazas": Listado.num_plazas,
    }

@app.get(f"{BASE_API}/listado-farmacias-hospitalarias/<int:id>")
@jwt_required()
def api_get_listado_farmacias_hospitalarias(id):
   # Using paginate() the following query strings are used:
   # - page, defaults to 1
   # - per_page, defaults to 20

   search_query = request.args.get("search", None)
   filter_query = request.args.get("filter", "nombre")
   columna = filter_to_column.get(filter_query, None)
   all_query = request.args.get("all", None)


   # Usamos try catch si columna es igual a None
   try:
      if all_query:
         listado = Listado.query.filter_by(id_convocatoria=id).all()
         total = len(listado)

      else:
         if search_query:
            if filter_query != "personas":
               pag_obj = Listado.query.filter_by(id_convocatoria=id).filter(columna.ilike(f'%{search_query}%')).paginate(count=True)
               
            else:
               pag_obj = db.session.query(Listado).filter_by(id_convocatoria=id).join(Listado.personas).filter(Persona.nombre.ilike(f'%{search_query}%')).distinct().paginate(count=True)     

         else:
               pag_obj = Listado.query.filter_by(id_convocatoria=id).paginate(count=True)
      
         listado = pag_obj.items
         total = pag_obj.total

   except Exception as e:
      listado = []
      total = 0
   

   return {
      "data": Schema(many=True).dump(listado),
      "total": total
   }