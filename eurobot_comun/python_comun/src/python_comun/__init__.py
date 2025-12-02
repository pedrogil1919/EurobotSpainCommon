'''
Created on 21 nov 2025

Módulo con funciones y objetos comunes en todos los proyectos. Las funciones
exportadas son:
- abrir_seleccion: abre un formulario que bloquea la ejecución del resto de
    programa. Permite seleccionar de entre varias opciones.
- Tabla: crea una tabla para mostrar resultados, por ejemplo de una consulta
    a una base de datos.
- Desplazamiento: Implementa un scroll para desplazar verticalmente cualquier
    objeto dentro de un canvas.

@author: pedrogil
'''

from .desplazamiento_tabla import Desplazamiento
from .formulario_seleccion import abrir_seleccion
from .funciones_comunes import maximizar_ventana
from .leer_xml import abrir_archivo_xml
from .leer_xml import leer_lista_xml, leer_atributos_xml, leer_lista_atributos_xml
from .leer_xml import leer_directorio_xml
from .tabla import Tabla
from .ventana_inicio import crear_ventana_inicio
