import tkinter as tk
from PIL import Image, ImageTk
from menu import create_menu
import os


def create_main_window():
    root = tk.Tk()
    root.title('Sistema de Auscultación en Instrumentación de Presas - "Represas Condor Cliff"')
    root.configure(bg='red')

    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill='both', expand=True)

    # Ruta a la imagen de fondo
    ruta_imagen = os.path.join(os.path.dirname(__file__), '..', 'Imagenes', 'instrumentos.jpg')
    imagen = Image.open(ruta_imagen)
    imagen_fondo = ImageTk.PhotoImage(imagen)
    imagen_ancho, imagen_alto = imagen.size

    # Mantener una referencia a la imagen
    canvas.imagen_fondo_original = imagen_fondo

    # Función para centrar y ajustar la imagen de fondo
    def centrar_ajustar_imagen(event):
        canvas.delete("all")
        canvas_ancho = event.width
        canvas_alto = event.height

        ratio = min(canvas_ancho / imagen_ancho, canvas_alto / imagen_alto)
        if ratio > 1:
            ratio = 1  # Evitar que la imagen se redimensione más allá de su tamaño original
        new_width = int(imagen_ancho * ratio)
        new_height = int(imagen_alto * ratio)

        imagen_resized = imagen.resize((new_width, new_height), Image.LANCZOS)
        imagen_fondo_resized = ImageTk.PhotoImage(imagen_resized)

        x = (canvas_ancho - new_width) // 2
        y = (canvas_alto - new_height) // 2
        canvas.create_image(x, y, image=imagen_fondo_resized, anchor='nw')

        # Mantener la referencia a la imagen
        canvas.imagen_fondo = imagen_fondo_resized

    canvas.bind('<Configure>', centrar_ajustar_imagen)

    footer_label = tk.Label(root, text="Sistema desarrollado por Ing. Jorge Gaspar Accardi", bg='lightblue', anchor='e')
    footer_label.pack(side='bottom', fill='x')

    return root, canvas

def run_app():
    root, canvas = create_main_window()
    create_menu(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
