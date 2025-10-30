from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet
from datetime import datetime, timedelta
import os

PATH_DIR = os.path.dirname(__file__)

# Diccionario para traducir un mes numérico a texto
meses =  {
    1:"enero",
    2:"febrero",
    3:"marzo",
    4:"abril",
    5:"mayo",
    6:"junio",
    7:"julio",
    8:"agosto",
    9:"septiembre",
    10:"octubre",
    11:"noviembre",
    12:"diciembre"
}

def cabecera_excel(worksheet:Worksheet, titulo_listado:str, titulo_encabezado:dict, encabezado:dict, curso_academico:str, actualizado_format: Format):
   """
   Escribe la cabecera (específica) en una hoja de excel. La cabecera tiene:
   * Un título encuadrado en un rectángulo morado, centrado.
   * Dos logos (imágenes) a los lados del título. Un logo es el de la UGR (izquierda)
   y otro el de la Facultad de Farmacia (derecha). Las posiciones de ambos logos
   limitan el tamaño de la tabla.
   * Encabezado de la tabla:
      * Título que ocupa todo el ancho de la tabla
      * Encabezado de cada columna

   Args:
      worksheet (Worksheet): Hoja del excel donde se va a escribir la cabecera
      titulo_listado (str): indica el tipo de listado que es
      titulo_encabezado (dict): {'contenido': str, 'format':Format}
      encabezado (dict): {'contenido':list con los encabezados/colummnas , 'format':Format}
      curso_academico (str): formato yyyy-yyyy
      actualizado_format (Format): 
   """
   path_logos = os.path.join(PATH_DIR, "img")
   logo_ugr = f"{path_logos}/logo_ugr.png"
   logo_farmacia = f"{path_logos}/logo_farmacia.png"
   fecha_actual = datetime.now().strftime("%d/%m/%Y") # fecha para poner el actualizado

   image_format = {
      'x_scale': 1,
      'y_scale': 1
   }

   worksheet.insert_image('A1', logo_ugr, image_format)
   worksheet.insert_image('F1', logo_farmacia, image_format)
   worksheet.merge_range('E5:F5', f"Actualizado {fecha_actual}", actualizado_format)
   worksheet.merge_range('A6:I6', titulo_encabezado['msg'], titulo_encabezado['format'])
   # Establecer el alto de la fila. El índice empiza en 0. El valor de 30 (altura)
   # se ha sacado probando
   worksheet.set_row(5, 30) 
   
   worksheet.write_row('A7', encabezado['contenido'], encabezado['format'])
   worksheet.set_row(6, 30)

   # Rectángulo morado
   # Será un textbox en vez de un dibujo (rectángulo)
   # Los valores numéricos han sido escogidos probando
   format = {
      'width': 400,
      'height': 60,
      'x_offset': 300,
      'y_offset': 0,
      "align": {"vertical": "middle", "horizontal": "center", "text": "center"},
      'font': {'color': 'white',
               'size': 14,
               'bold': True},
      'fill': {'color': 'purple'},
   }

   worksheet.insert_textbox('B2', f"Listado de {titulo_listado} - Grado en Farmacia\nCurso académico {curso_academico}", format)



def worksheet_horizontal(worksheet:Worksheet):
   """
   Pone una hoja de excel en horizontal
   
   Args:
      worksheet (Worksheet): Hoja del excel que se va a poner en horizontal
   """
   
   worksheet.set_landscape()



def get_titulo_format(workbook: Workbook, color:str) -> Format:
   """
   Crea el formato para el título de la tabla

   Args:
      workbook (Workbook): referencia del excel para crear el formato
      color (str): cadena que representa un color. El formato debe ser uno válido
      para el módulo xlsxwriter

   Returns:
      Format: formato del título de la tabla
   """
   return workbook.add_format({
      'align': 'center',
      'valign': 'vcenter',
      'bold': True,
      'border': 1,
      'bg_color': color,
      'font_size': 14
   })



def get_encabezados_format(workbook:Workbook) -> Format:
   """
   Crea el formato para los encabezados de la tabla

   Args:
      workbook (Workbook): excel para crear los formatos

   Returns:
      Format: formato de los encabezados
   """
   return workbook.add_format({
      'align': 'center',
      'valign': 'vcenter',
      'bold': True,
      'border': 1,
      'bg_color': '#B9CDE5',
      'font_size': 14
   })



def get_tabla_format_par(workbook):
   return get_tabla_format(workbook, 'D9D9D9')


def get_tabla_format_impar(workbook):
   return get_tabla_format(workbook, 'white')


def get_tabla_format(workbook, color):
   return workbook.add_format({
      'align': 'center',
      'valign': 'vcenter',
      'bg_color': color,
      'font_size': 13,
      'border': 1
   })

def get_encabezados_farmacia():
   return [
      'Nº',
      'Nombre de la farmacia',
      'Dirección del centro colaborador',
      'Localidad',
      'Provincia',
      'Código Postal',
      'Tutores',
      'E-mail',
      'Teléfono',
      'Nº plazas'
   ]

def get_encabezados_hospitales():
   return [
      'Nº',
      'Nombre del hospital',
      'Dirección',
      'Localidad',
      'Provincia',
      'Código Postal',
      'Tutores',
      'E-mail',
      'Teléfono',
      'Nº plazas'
   ]


def cambia_factor_escala(worksheet, factor):
   # Configurar la escala de la página
   worksheet.set_print_scale(factor)


def centra_tabla_horizontal_al_imprimir(worksheet):
   # Configurar la hoja de trabajo para centrar horizontalmente al imprimir
   worksheet.center_horizontally()


def repite_filas_al_imprimir(worksheet, first, last):
   worksheet.repeat_rows(first, last)



def columnas_format(worksheet):
   worksheet.set_column('A:A', 5)
   worksheet.set_column('B:B', 40)
   worksheet.set_column('C:C', 40)
   worksheet.set_column('D:D', 30)
   worksheet.set_column('E:E', 15)
   worksheet.set_column('F:F', 20)
   worksheet.set_column('G:J', None, None, {'hidden':1})


def set_margenes(worksheet):
   worksheet.set_margins(0.2, 0.2, 0.2, 0.2)



def rellena_workbook(workbook, tipo, convocatoria, datos):
   # Crea las hojas/pestañas (worksheets) del excel
   worksheet = workbook.add_worksheet("listado")

   worksheets = [worksheet]

   # Creamos los formatos
   titulo_format_11 = get_titulo_format(workbook, '#FDEADA')
   encabezados_format = get_encabezados_format(workbook)
   tabla_format = {
      'par': get_tabla_format_par(workbook),
      'impar': get_tabla_format_impar(workbook)
   }
   actualizado_format = workbook.add_format({
      'align': "right"
   })

   if tipo == "farmacias":
      principio_titulo_msg = "Farmacias"
      encabezados_contenido = get_encabezados_farmacia()
      contenido_excel = contenido_excel_farmacias

   elif tipo == "hospitales":
      principio_titulo_msg = "Farmacias hospitalarias"
      encabezados_contenido = get_encabezados_hospitales()
      contenido_excel = contenido_excel_hospitales


  
   fecha_ini = convocatoria.fecha_ini
   fecha_fin = convocatoria.fecha_fin

   fechas_11a = (
      f"{fecha_ini.day} de {meses[fecha_ini.month]}",
      f"{fecha_fin.day} de {meses[fecha_fin.month]}"
   )

   curso_academico = f"{0}/{1}"


   titulo_11a_msg = f"{principio_titulo_msg} que se ofertan para el periodo comprendido entre el {fechas_11a[0]} al {fechas_11a[1]}"


   titulo_11a = {
      'msg': titulo_11a_msg,
      'format': titulo_format_11
   }


   columnas = {
      'contenido': encabezados_contenido,
      'format': encabezados_format
   }
   
   cabecera_excel(worksheet, tipo, titulo_11a, columnas, curso_academico, actualizado_format)


   contenido_excel(worksheet, datos, tabla_format)


   for w in worksheets:
      worksheet_horizontal(w)
      cambia_factor_escala(w, 65)
      centra_tabla_horizontal_al_imprimir(w)
      repite_filas_al_imprimir(w, 0, 6)
      columnas_format(w)
      set_margenes(w)


def contenido_excel_farmacias(worksheet, centros, format):
   i = 1
   ROW_HEIGH = 30 # 

   for centro in centros:
      if centro['telefono'] != "" and centro['movil'] != "":
         contacto = f"{centro['telefono']}/{centro['movil']}"
      elif centro['telefono'] != "":
         contacto = centro['telefono']
      else:
         contacto = centro['movil']

      tutores = ''
      for persona in centro['personas']:
         tutores += persona['nombre'] + '\n'

      tutores = tutores.rstrip()

      factor_mult = 1
      # num_tutores = len(centro['personas'])
      # if num_tutores > 1:
      #    factor_mult = 0.2 * num_tutores + 1

      fila_datos = [
         i,
         centro['nombre'],
         centro['direccion'],
         centro['localidad'],
         centro['provincia'],
         centro['cp'],
         tutores,
         centro['correo'],
         contacto,
         centro['num_plazas']
      ]

      
      if i % 2 == 0:
         format_escogido = format['par']
      else:
         format_escogido = format['impar']

      worksheet.write_row(f'A{7+i}', fila_datos, format_escogido)
      worksheet.set_row(6+i, ROW_HEIGH * factor_mult) # Establecer el alto de la fila
      i += 1


def contenido_excel_hospitales(worksheet, centros, format):
   i = 1
   ROW_HEIGH = 30

   for centro in centros:
      if centro['telefono'] != "" and centro['movil'] != "":
         contacto = f"{centro['telefono']}/{centro['movil']}"
      elif centro['telefono'] != "":
         contacto = centro['telefono']
      else:
         contacto = centro['movil']

      tutores = ''
      for persona in centro['personas']:
         tutores += persona['nombre'] + '\n'

      tutores = tutores.rstrip()

      factor_mult = 1
      # num_tutores = len(centro['personas'])
      # if num_tutores > 1:
      #    factor_mult = 0.2 * num_tutores + 1

      fila_datos = [
         i,
         centro['nombre'],
         centro['direccion'],
         centro['localidad'],
         centro['provincia'],
         centro['cp'],
         tutores,
         centro['correo'],
         contacto,
         centro['num_plazas']
      ]

      if i % 2 == 0:
         format_escogido = format['par']
      else:
         format_escogido = format['impar']

      worksheet.write_row(f'A{7+i}', fila_datos, format_escogido)
      worksheet.set_row(6+i, ROW_HEIGH * factor_mult) # Establecer el alto de la fila
      i += 1

