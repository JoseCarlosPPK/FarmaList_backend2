from . import BASE_API
from .convocatorias import api_get_convocatoria
from .. import app
from ..schemas import ConvocatoriaSchema
from ..excel import rellena_workbook
from  flask import send_file, request
import xlsxwriter
import io
import zipfile
import requests

@app.get(f"{BASE_API}/excel")
def get_excel_convocatoria():

    id_query_param = request.args.get('id')
    list_id = [] 

    if (id_query_param):
        list_id = list(map(lambda id: int(id) ,id_query_param.split(',')))

    # Cogemos la información de la convocatoria
    response = api_get_convocatoria(list_id[0])

    if (isinstance(response, tuple)):
        return response
    
    convocatoria = ConvocatoriaSchema().load(response['data'])

    ###########################################################################
    # Excel
    ###########################################################################
    # Creamos un espacio de memoria para escribir en él
    # En vez de tener ficheros en disco, lo hacemos todo en memoria,
    # lo que supone no tener ficheros temporales
    mem_output_farmacias = io.BytesIO()
    mem_output_farmacias_hospitalarias = io.BytesIO()

    workbooks = [xlsxwriter.Workbook(mem_output_farmacias), xlsxwriter.Workbook(mem_output_farmacias_hospitalarias)]

    datos_farmacias = requests.get(f'http://localhost:5000/api/listado-farmacias/{convocatoria.id}?all=True', cookies=request.cookies).json()

    datos_farmacias_hospitalarias = requests.get(f'http://localhost:5000/api/listado-farmacias-hospitalarias/{convocatoria.id}?all=True', cookies=request.cookies).json()

    # Ordenamos los centros por localidad y provincia
    datos_farmacias["data"] = sorted(datos_farmacias['data'], key=lambda x: (x['provincia'], x['localidad']))

    datos_farmacias_hospitalarias["data"] = sorted(datos_farmacias_hospitalarias['data'], key=lambda x: (x['provincia'], x['localidad']))


    rellena_workbook(workbooks[0], "farmacias", convocatoria, datos_farmacias['data'])
    rellena_workbook(workbooks[1], "hospitales", convocatoria, datos_farmacias_hospitalarias['data'])


    # Cerrar el libro de trabajo para guardar los cambios.
    for workbook in workbooks:
        workbook.close()

    mem_output_farmacias.seek(0)
    mem_output_farmacias_hospitalarias.seek(0)

    # Para el nombre de los archivos añadimos la fecha de la convocatoria
    fecha_convocatoria_formateada = f"{convocatoria.fecha_ini.day}_{convocatoria.fecha_ini.month}_{convocatoria.fecha_ini.year}"

    # Crear un archivo ZIP en memoria
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f'farmacias_{fecha_convocatoria_formateada}.xlsx', mem_output_farmacias.getvalue())
        zip_file.writestr(f'farmacias_hospitalarias{fecha_convocatoria_formateada}.xlsx', mem_output_farmacias_hospitalarias.getvalue())


    zip_buffer.seek(0)

    return send_file(zip_buffer, download_name=f"convocatoria_{fecha_convocatoria_formateada}.zip", as_attachment=True)
