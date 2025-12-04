from python_comun import abrir_archivo_xml
from python_comun import leer_atributos_xml

abrir_archivo_xml("prueba.xml")
t1 = leer_atributos_xml("elemento1", "TAG2")
print("t1: ", t1)
t11 = leer_atributos_xml("elemento1", ("TAG1",))
print("t11: ", t11)
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
