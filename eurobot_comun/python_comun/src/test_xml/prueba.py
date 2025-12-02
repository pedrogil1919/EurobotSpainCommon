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
l5 = leer_lista_atributos_xml( ("elemento1", "elemento2"), "campo", "TAG1")
print("l5: ", l5)
l6 = leer_lista_atributos_xml( ("elemento1", "elemento2"), "campo", ("TAG1", "TAG2") )
print("l6: ", l6)
