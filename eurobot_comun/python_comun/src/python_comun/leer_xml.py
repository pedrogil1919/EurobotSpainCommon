"""
Created on 9 may 2024

Funciones para leer y guardar datos del archivo xml de configuración.

@author: pedrogil

"""
from tkinter import messagebox
from xml.etree import ElementTree


# Nombre del archivo xml, por si queremos modificar su contenido
nombre_xml = None
# Raíz del contenido del archivo xml
archivo_xml = None


###############################################################################
# FUNCIONES GENERALES
###############################################################################

# Definición de una función que emplearemos como decorator, para seguir la
# misma estrategia en todas las funciones de lectura del archivo xml en caso de
# error en el propio archivo xml.


def captura_error(funcion_leer_xml):
    """
    Función decorator

    Esta función realiza la llamada a la función de lectura de algún campo xml,
    capturando el error que genera el propio archivo, y sacando un mensaje por
    pantalla en caso de error en el archivo.

    """
    def control(*argumentos):
        try:
            # # Llamamos a la función de lectura del xml.
            # if len(argumentos) == 0:
            #     # NOTA: Si el argumento es None, se supone que estamos
            #     # realizando la llamada a una función que no acepta argumentos.
            #     res = funcion_leer_xml()
            # else:
            #     # Sin embargo, si no es None, es una función que acepta un
            #     # argumento.
            #     res = funcion_leer_xml(*argumentos)
            res = funcion_leer_xml(*argumentos)
            # Y devolvemos los datos leidos.
            return res
        except (AttributeError, KeyError):
            # Si hay algún error en el archivo xml, como que falta la clave o
            # el parámetro, mostramos un mensaje de error.
            messagebox.showerror(
                "Error configuración",
                "Error en el archivo de configuración %s. "
                "Revisar parámetros del elemento '%s'" %
                (nombre_xml, argumentos[0]))
            exit(1)
        except ValueError:
            # Si hay algún error en el archivo xml, como que falta la clave o
            # el parámetro, mostramos un mensaje de error.
            messagebox.showerror(
                "Error configuración",
                "Error en el archivo de configuración %s. "
                "Revisar parámetros del elemento '%s' / '%s'" %
                (nombre_xml, argumentos[0], argumentos[1]))
            exit(1)
    return control


def abrir_archivo_xml(archivo):
    """
    Abrir y guardar en el módulo el archivo xml de configuración.

    """
    global archivo_xml
    global nombre_xml
    try:
        archivo_xml = ElementTree.parse(archivo)
        nombre_xml = archivo
    except ElementTree.ParseError as error:
        raise RuntimeError("Error archivo XML %s: %s." % (archivo, error))


def txt2bool(valor):
    """
    Función para convertir el valor del xml a booleano

    """
    c = {
        "TRUE": True,
        "FALSE": False,
        "T": True,
        "F": False,
        "1": True,
        "0": False}
    valor = valor.upper()
    return c[valor]


def bool2txt(valor):
    """
    Función para convertir un bool en un texto para archivos xml

    """
    return "TRUE" if valor else "FALSE"


conversion_tipo = {
    's': lambda: None,
    'i': int,
    'f': float,
    'b': txt2bool}


def convertir_tipo(valor, formato):
    try:
        return conversion_tipo[formato](valor)
    except Exception:
        return valor


def convertir_tipo_inv(valor):
    if isinstance(valor, bool):
        return bool2txt(valor)
    if isinstance(valor, float):
        return "%f.1" % valor
    return str(valor)


def aux_atributos_xml(elemento, atributos, formatos):
    """
    Devuelve los atributos solicitados de un elemento.

    Argumentos:
    - elemento: ElementTree del elemento sobre el cual queremos obtener sus
      atributos.
    - atributos, formatos: ver función leer_atributos_xml

    """
    N = len(atributos)
    # Comprobamos el valor de la variable formato.
    if formatos is None:
        formatos = "s" * N
    if not isinstance(formatos, str):
        formatos = "s" * N
    if len(formatos) == 1:
        formatos = formatos * N
    if len(formatos) < N:
        formatos = formatos + "s" * (N - len(formatos))

    if not isinstance(atributos, (list, tuple)):
        # Sí solo nos piden uno, lo devolvemos como una única variable.
        valor = elemento.attrib[atributos]
        lista = convertir_tipo(valor, formatos[0])
    else:
        # Si nos piden más de un atributo, los colocamos en un diccionario.
        lista = {}
        for atributo, formato in zip(atributos, formatos):
            valor = elemento.attrib[atributo]
            valor = convertir_tipo(valor, formato)
            lista[atributo] = valor
    return lista


###############################################################################
# FUNCIONES DE LECTURA DE ARCHIVOS XML GENERALES
###############################################################################

@captura_error
def leer_atributos_xml(elementos, atributos, formatos=None):
    """
    Obtiene los atributos de un elemento, 

    Argumentos:
    - elementos: nombre del elemento del cual queremos obtener sus atributos.
      Si se trata de un elemento anidado, elementos debe ser una lista con
      todos los elementos que hay que atravesar, empezando por el de mayor
      nivel.
    - atributos: lista de atributos. Si esta variable sólo tiene un elemento,
      se devuelve su valor como una variable. Si tiene más elementos, se
      devuelve como un diccionario.
    - formatos: formatea el tipo de datos. Se trata de una cadena de caracteres, 
      cuyos valores pueden ser:
      - s: cadena de caracteres (no hacer conversión).
      - i: entero.
      - f: decimal.
      Si está vacio, no existe o es erréneo, no se hace ningún tipo de
      conversión.
      Si la cadena sólo tiene un carácter, se aplica el mismo formato a todos
      los elementos. Si tiene más caracteres, su longitud debe ser igual a la
      de la variable atributos.

###########################################################################
# Archivo prueba.xml
###########################################################################
<prueba>
    <elemento1 TAG1="24" TAG2="hola">
        <elemento2 TAG3="otro" TAG7="más">
            <elemento3>
                <elemento4 TAG4="prueba" TAG5="14.2" TAG6="otra">
                </elemento4>
            </elemento3>
        </elemento2>
    </elemento1>
</prueba>
###########################################################################

###########################################################################
# Archivo prueba.py
###########################################################################
from python_comun import abrir_archivo_xml
from python_comun import leer_atributos_xml

abrir_archivo_xml("prueba.xml")
t1 = leer_atributos_xml("elemento1", "TAG2")
print("t1: ", t1)
t2 = leer_atributos_xml("elemento1", "TAG1")
print("t2: ", t2, type(t2))
t3 = leer_atributos_xml("elemento1", "TAG1", "i")
print("t2: ", t3, type(t3))
t4 = leer_atributos_xml(
    ("elemento1", "elemento2", "elemento3", "elemento4"), 
    ("TAG4", "TAG5", "TAG6"), "sf")
print("t4: ", t4)
t5 = leer_atributos_xml(
    ("elemento1", "elemento2", "elemento3", "elemento4"), "TAG5", "f")
print("t5: ", t5, type(t5))
t6 = leer_atributos_xml(
    ("elemento1", "elemento2"), ("TAG3", "TAG7"))
print("t6: ", t6)
###########################################################################

    """
    raiz = archivo_xml.getroot()
    # Comprobamos si la raíz es una lista de etiquetas:
    if not isinstance(elementos, (list, tuple)):
        elementos = (elementos,)
    # Descendemos hasta el elemento del nivel indicado.
    for etiqueta in elementos:
        raiz = raiz.find(etiqueta)
    lista = aux_atributos_xml(raiz, atributos, formatos)
    return lista


@captura_error
def leer_lista_xml(elementos, nombre, atributo, formato="s"):
    """
    Lee todos los elmentos con el mismo nombre dentro de otro elemento.

    Argumentos:
    - elementos: ver función leer_atributos_xml
    - nombre: nombre del elemento del cual queremos generar la lista.
    - atributo: atributo a devolver de cada elemento anterior.

###########################################################################
# Archivo prueba.xml
###########################################################################
<prueba>
    <elemento1>
        <campo TAG="1"/>
        <campo TAG="2"/>
        <campo TAG="3"/>
        <campo TAG="4"/>
        <elemento2>
            <campo TAG2="A"/>
            <campo TAG2="B"/>
            <campo TAG2="C"/>
            <campo TAG1="D"/>
        </elemento2>
    </elemento1>
</prueba>
###########################################################################

###########################################################################
# Archivo prueba.py
###########################################################################
from python_comun import abrir_archivo_xml
from python_comun import leer_lista_xml

abrir_archivo_xml("prueba.xml")
l1 = leer_lista_xml("elemento1", "campo", "TAG")
print("l1: ", l1)
l2 = leer_lista_xml("elemento1", "campo", "TAG", "i")
print("l2: ", l2)
l3 = leer_lista_xml(("elemento1", "elemento2"), "campo", "TAG2")
print("l3: ", l3)
l4 = leer_lista_xml(("elemento1", "elemento2"), "campo", "TAG1")
print("l4: ", l4)
###########################################################################


    """
    raiz = archivo_xml.getroot()

    # Comprobamos si la raíz es una lista de etiquetas:
    if not isinstance(elementos, (list, tuple)):
        elementos = (elementos,)
    # Descendemos hasta el elemento del nivel indicado.
    for etiqueta in elementos:
        raiz = raiz.find(etiqueta)

    lista = ()
    # Obtenemos todos los elementos con el nombre solicitado.
    elementos_lista = raiz.findall(nombre)
    if len(elementos_lista) == 0:
        # Si no hay ningún elemento, se trata de un error.
        raise ValueError
    for campo in elementos_lista:
        try:
            # Comprobamos si existe el tag en dicho elemento.
            valor = campo.attrib[atributo]
        except KeyError:
            continue
        # Convertimos al formato indicado.
        valor = convertir_tipo(valor, formato)
        lista += (valor,)
    return lista


# @captura_error
def leer_lista_atributos_xml(elementos, nombre, atributos, formatos=None):
    """
    Similar a leer_lista_xml, pero solicitando más de un atributo.

    Se devuelve una lista, donde cada elemento es un diccionario con los
    atributos solicitados. Solo se incluyen los elementos que tengan todos
    los atributos indicados. 

###########################################################################
# Archivo prueba.xml
###########################################################################
<prueba>
    <elemento1>
        <campo TAG1="1" TAG2="A"/>
        <campo TAG1="2" TAG2="B"/>
        <campo TAG1="3"/>
        <campo TAG1="4" TAG2="C"/>
        <elemento2>
            <campo TAG2="A"/>
            <campo TAG2="B"/>
            <campo TAG2="C"/>
            <campo TAG1="D"/>
        </elemento2>
    </elemento1>
</prueba>
###########################################################################

###########################################################################
# Archivo prueba.py
###########################################################################
from python_comun import abrir_archivo_xml
from python_comun import leer_lista_atributos_xml

abrir_archivo_xml("prueba.xml")
l1 = leer_lista_atributos_xml("elemento1", "campo", "TAG1")
print("l1: ", l1)
l2 = leer_lista_atributos_xml("elemento1", "campo", ("TAG1", "TAG2"))
print("l2: ", l2)
l3 = leer_lista_atributos_xml("elemento1", "campo", ("TAG1", "TAG2"), "is")
print("l3: ", l3)

l4 = leer_lista_atributos_xml(("elemento1", "elemento2"), "campo", "TAG2")
print("l4: ", l4)
l5 = leer_lista_atributos_xml( ("elemento1", "elemento2"), "campo", ("TAG2", "TAG1") )
print("l5: ", l5)


    """
    raiz = archivo_xml.getroot()

    # Comprobamos si la raíz es una lista de etiquetas:
    if not isinstance(elementos, (list, tuple)):
        elementos = (elementos,)
    # Descendemos hasta el elemento del nivel indicado.
    for etiqueta in elementos:
        raiz = raiz.find(etiqueta)

    lista = ()
    elementos_lista = raiz.findall(nombre)
    if len(elementos_lista) == 0:
        raise ValueError
    for campo in elementos_lista:
        try:
            valores = aux_atributos_xml(campo, atributos, formatos)
        except KeyError:
            continue
        lista += (valores,)
    return lista


# @captura_error
def leer_directorio_xml(elementos, tag):
    """
    Construye un directorio a partir de varios elementos anidados.

    El directorio se construye con todos los elementos que tengan el tag
    tag. Si un elmento no lo tiene, pero alguno de los elementos que
    están dentro de el sí, no es ningún error, simplemente se ignora este
    elemento y se sigue construyendo a partir de su descendiente.

    elementos es una lista de todos los elementos, en sentido descendente, que
    hay que recorrer. Por ejemplo:
###########################################################################
# Archivo prueba.xml
###########################################################################
<prueba>
    <elemento1 DIRECTORIO="dir1/">
        <elemento2 OTRO_TAG="otro">
            <elemento3 DIRECTORIO="dir3/">
                <elemento4 DIRECTORIO="dir4/">
                </elemento4>
            </elemento3>
        </elemento2>
    </elemento1>
</prueba>
###########################################################################

###########################################################################
# Archivo prueba.py
###########################################################################
from python_comun import abrir_archivo_xml
from python_comun import leer_directorio_xml
abrir_archivo_xml("prueba.xml")
var = leer_directorio_xml(
    ("elemento1", "elemento2", "elemento3", "elemento4" ),
    "DIRECTORIO")
print("Directorio: ", var)
###########################################################################
>> dir1/dir3/dir4/

    """
    raiz = archivo_xml.getroot()
    # Comprobamos si la raíz es una lista de etiquetas:
    if not isinstance(elementos, (list, tuple)):
        elementos = (elementos,)

    # Construimos el directorio en esta variable.
    directorio = ""
    for elemento in elementos:
        # Avanzamos hasta el siguiente elemento.
        raiz = raiz.find(elemento)
        try:
            # Comprobamos si el elemento tiene el tag
            d = raiz.attrib[tag]
            # Si lo tiene, lo añadimos al directorio.
            directorio += d
        except KeyError:
            pass
    return directorio


# def guardar_atributos_xml(elementos, atributos, valores):
#
#     raiz = archivo_xml.getroot()
#     # Comprobamos si la raíz es una lista de etiquetas:
#     if not isinstance(elementos, (list, tuple)):
#         elementos = (elementos,)
#     for etiqueta in elementos:
#         raiz = raiz.find(etiqueta)
#
#     if len(atributos) != len(valores):
#         raise ValueError
#     N = len(atributos)
#     for n in range(N):
#         raiz[atributos[n]] = convertir_tipo_inv(valores[n])
#     archivo_xml.write(nombre_xml)
