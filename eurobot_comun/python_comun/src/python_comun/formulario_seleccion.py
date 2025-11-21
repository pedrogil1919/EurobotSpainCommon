'''
Created on 6 may 2024

Formulario general para seleccionar elementos de una lista. El formulario se 
divide en tres zonas:
- Cabecera, praa mostrar un logo o similar.
- Zona de selección, donde se muestran las opciones en forma de checkboxes.
- Zona de botones, con el botón guardar y cancelar.

Para emplear este formulario, debemos realizar la llamada a la función
abrir_seleccion. Esta función bloquea la ejecución del código hasta que la
ventana sea cerrada. Devuelve True si el usuario pulsa el botón Guardar, y
False si Cancelar. Las modificaciones realizadas por el usuario, se actualizan
sobre la misma lista de elementos pasada como argumento en la función anterior.

@author: pedrogil
'''

from PIL import Image, ImageTk
from functools import partial
import tkinter


class FormularioSeleccion:

    def __init__(self, ventana, logo_cabecera):
        """
        Crea el formulario de selección genérico.

        Argumentos:
        - ventana: ventana llamante, para poder crear una nueva ventana 
          dependiente de esta ventana principal.
        - logo_cabecera: nombre del archivo con la imagen para mostrar en la 
          parte superior del formulario.

        """

        # Creamos un formulario dependiente de la ventana principal.
        self.__formulario = tkinter.Toplevel(ventana)
        # Y hacemos que esta ventana siempre esté encima de la principal.
        self.__formulario.transient(ventana)
        # Hacemos desaparecer la nueva ventana hasta que no la tengamos
        # completamente construida, para evitar efectos raros.
        self.__formulario.withdraw()

        # Impedimos que el usuario pueda redimensionar la venana, es decir, su
        # tamaño es fijo una vez se crean todos los elementos dentro de la
        # ventana:
        # NOTA: El tamaño final es dependiente de los checkboxs que añadamos,
        # tanto en altura (númro de elementos a añadir) como en anchura
        # (longitud del elemento con el texto más largo).
        self.__formulario.resizable(False, False)

        # Creamos la cabezera con el logo.
        # Creamos un marco que será el que colocemos en el grid del formulario
        # principal.
        cabecera = tkinter.Frame(self.__formulario, padx=20, pady=40)
        # Abrimos la imagen para la cabecera.
        # NOTA: La imagen debe guardarse como un miembro de la clase, si no,
        # al finalizar el constructor desaparece y no se representa en la
        # ventana.

        self.__imagen = ImageTk.PhotoImage(Image.open(logo_cabecera))
        cabecera_logo = tkinter.Label(cabecera, image=self.__imagen)

        # Creamos un marco donde pondremos los checkboxes para marcar los
        # equipos.
        marco_checks = tkinter.Frame(self.__formulario, padx=10)
        # Y sobre éste añadimos otro marco que será el que contenga a los
        # checkbox de los equipos y el mensaje para el usuario.
        self.__marco_checks = tkinter.Frame(marco_checks)
        self.__marco_checks.pack()

        # Creamos los botones para cerrar el formulario.
        self.__boton_guardar = tkinter.Button(

            self.__formulario, command=self.cerrar, text="Guardar", width=8)
        self.__boton_cancelar = tkinter.Button(
            self.__formulario, command=self.cancelar, text="Cancelar", width=8)
        # Control del botón guardar del formulario. Sólo se habilita una vez
        # se produzca alguna modificación en algún checkbox.
        self.__modificado = False
        self.__boton_guardar.config(state="disabled")

        # Creamos la estructura del formulario mediante grid.
        self.__boton_guardar.grid(row=3, column=1)
        self.__boton_cancelar.grid(row=3, column=3)
        marco_checks.grid(row=1, column=0, sticky="EW", columnspan=5)
        cabecera.grid(row=0, column=0, sticky="NSEW", columnspan=5)
        cabecera_logo.pack(
            expand=True, fill=tkinter.BOTH, anchor=tkinter.CENTER)

        # Y configuramos la geometría para que los huecos que se redimensionen
        # para ajustarse al tamaño necesario sean:
        # Verticalmente hay que agrandar la fila que contiene los checkboxes.
        self.__formulario.rowconfigure(0, minsize=7)
        self.__formulario.rowconfigure(1, weight=1)
        self.__formulario.rowconfigure(2, minsize=20)
        self.__formulario.rowconfigure(4, minsize=7)
        # Horizontalmente agrandamos los margenes del formulario.
        self.__formulario.columnconfigure(0, weight=1, minsize=20)
        self.__formulario.columnconfigure(2, minsize=20)
        self.__formulario.columnconfigure(4, weight=1, minsize=20)

        # Asiganmos los atajos del teclado:
        self.__boton_guardar.bind("<Return>", partial(self.cerrar))
        self.__boton_guardar.bind("<KP_Enter>", partial(self.cerrar))
        # self.__boton_guardar.bind("<Button-1>", partial(self.cerrar))

        self.__boton_cancelar.focus_set()
        self.__boton_cancelar.bind("<Return>", partial(self.cancelar))
        self.__boton_cancelar.bind("<KP_Enter>", partial(self.cancelar))
        # self.__boton_cancelar.bind("<Button-1>", partial(self.cancelar))
        self.__formulario.bind("<Escape>", partial(self.cancelar))
        self.__formulario.protocol("WM_DELETE_WINDOW", self.cancelar)

    def abrir(self, titulo, mensaje, datos):
        """
        Abre el formulario de selección y deshabilita la ventana principal
        hasta que el usuario cierre esta ventana:

        Argumentos. Ver función abrir_seleccion

        """
        self.__formulario.title(titulo)

        # Creamos un diccionario donde almacenaremos los valores de los check.
        # NOTA: No hay otra forma de hacer esto en tkinter.
        # self.__check_var = {}
        # Guardamos la lista de elementos, ya que será aquí donde reflejemos
        # los cambios introducidos por el usuario.
        self.__datos = datos
        # Añadimos una etiqueta con las instrucciones.
        etiqueta_info = tkinter.Label(
            self.__marco_checks, justify="left", wraplength=400,
            text=mensaje, font=("sans-serif", 14, "bold"), pady=10)
        etiqueta_info.pack()
        # Construimos los elementos que van dentro del marco con los checkbox
        # de los equipos.
        for dato in self.__datos:
            # Añadimos un elemento más al diccionario, que es la variable con
            # la que relacionamos el estado del checkbox.
            dato["var"] = tkinter.IntVar()
            dato["var"].set(dato["valor"])
            check = tkinter.Checkbutton(
                self.__marco_checks, variable=dato["var"],
                command=self.habilitar_guardar, text=dato["titulo"])
            check.pack(pady=5, anchor=tkinter.W)
        # Hacemos visible la ventana.
        self.__formulario.deiconify()

        # Deshabilitar la ventana principal.
        # NOTA: Si hacemos el bloqueo desde esta misma función, puede dar
        # error, ya que es posible que no se haya terminado de visualizar la
        # ventana. Si hacemos una espera antes de bloquearla, no salta el
        # error. En este caso, la ventana principal estaría sin bloquear el
        # tiempo en ms indicado en la función after.
        # ATENCIÓN: Si salta un error en esta función, es porque esta ventana
        # no ha terminado de mostrarse en la pantalla. Si es así, aumentar el
        # tiempo indicado en la llamada a "after".
        self.__formulario.after(1, self.__formulario.grab_set)

        return self.__formulario

    def cerrar(self, __=None):
        """
        Cierra la ventana, guardando los cambios si los ha habido.

        """
        if self.__modificado:
            # Actualizamos los valores de la lista de elementos que nos pasaron
            # al inicio.
            for dato in self.__datos:
                dato["valor"] = dato["var"].get()
                del dato["var"]
        self.__formulario.destroy()

    def cancelar(self, __=None):
        """
        Cerrar la ventana, cancelando cualquier cambio realizado.

        """
        self.__modificado = False
        self.cerrar()

    def habilitar_guardar(self):
        """
        Habilitar el botón guardar la primera vez que haya un cambio.

        """
        self.__modificado = True
        self.__boton_guardar.config(state="normal")

    def get_modificado(self):
        return self.__modificado
    modificado = property(get_modificado, None, None, None)


def abrir_seleccion(ventana, titulo, cabecera, mensaje, datos):
    """
    Función principal.

    Argumentos:
    - ventana: ventana llamante, para poder situar el formulario sobre ésta.
    - titulo: título del formulario de selección.
    - cabecera: nombre del archivo con la imagen para la parte superior del
      formulario.
    - mensaje: instrucciones para el usuario.
    - datos: lista con los datos a mostrar para que el usuario seleccione. 
      Cada elemento de la lista es un diccionario con las siguientes
      claves:
      - "titulo": texto a mostrar al lado del checkbox.
      - "valor": booleano, indicando si el elemento está seleccionado o no.
      La lista de datos debe venir inicializada con los valores actuales de
      los elementos de la lista. Si el usuario realiza alguna modificación,
      dicha modificación se registra sobre el propio diccionario, por lo
      que debemos revisar esta lista para comprobar la selección realizada.

    Devuelve True si ha habido alguna modificación y el usuario ha pulsado la
    tecla Guardar.

    """
    # Crear formulario de selección.
    seleccion = FormularioSeleccion(ventana, cabecera)
    # Abrir el formulario con los datos a seleccionar.
    formulario = seleccion.abrir(titulo, mensaje, datos)
    # Bloquear la ejecución del código hasta que se cierre la ventana.
    ventana.wait_window(formulario)

    return seleccion.modificado
