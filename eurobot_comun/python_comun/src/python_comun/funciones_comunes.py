'''
Created on 25 nov 2025

Repositorio de funciones comunes.

@author: pedrogil
'''

import sys


def maximizar_ventana(ventana):
    """
    Maximizar la ventana principal en función del sistema operativo.

    """
    # Iniciamos la ventana completamente maximizada. Tener en cuenta que esto
    # depende del sistema operativo.
    if sys.platform == "linux" or sys.platform == "linux2":
        ventana.attributes("-zoomed", True)
    elif sys.platform == "darwin":
        raise RuntimeError("Aplicación no diseñada para MAC")
    elif sys.platform == "win32":
        ventana.state('zoomed')
