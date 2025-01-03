import cv2
from expandir_imagen import generate_expanded_image
from stickers_generador import generate_sticker
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, StringVar
from tktooltip import ToolTip
import os

class InterfazGeneradorSticker:
    def __init__(self):
        self.ventana = tk.Tk()
        self.archivos = AdministradorArchivos()
        self.configurar_ventana()
        self.crear_widgets()

    def configurar_ventana(self):
        """Configura la ventana principal."""
        self.ventana.title("Generador de Sticker")
        self.ventana.geometry("300x200")
        self.ventana.resizable(False, False)
        self.ventana.config(bg="white")

    def crear_widgets(self):
        """Crea y organiza los widgets dentro de la ventana."""
        frame_archivos = tk.Frame(self.ventana, bg="white")
        frame_archivos.pack(pady=5)
        self.carpetas(frame_archivos)

        frame_contorno = tk.Frame(self.ventana, bg="white")
        frame_contorno.pack(pady=5)
        self.contorno_imagen(frame_contorno)

        frame_iniciar = tk.Frame(self.ventana, bg="white")
        frame_iniciar.pack(pady=5)
        self.iniciar_boton(frame_iniciar)

        # Agregar barra de progreso
        frame_progress = tk.Frame(self.ventana, bg="white")
        frame_progress.pack(pady=5)
        tk.Label(frame_progress, text="Progreso", anchor="w", bg="white").pack(side="left", fill="x")
        self.progreso = ttk.Progressbar(frame_progress, orient="horizontal", length=200, mode="determinate")
        self.progreso.pack(side="left", padx=5)
        
        frame_version = tk.Frame(self.ventana, bd=1, relief="sunken")
        frame_version.pack(side="bottom", fill="x")
        self.version(frame_version)

    def carpetas(self, frame):
        """Crea los botones para seleccionar archivo o carpeta."""
        tk.Label(frame, text="Selecciona las rutas de acceso", bg="white").pack(side="left")
        self.ruta_archivo = tk.Button(frame, text="Abrir carpeta", command=self.archivos.abrir_carpeta)
        self.ruta_archivo.pack(pady=5, side="left", padx=5)

        ToolTip(self.ruta_archivo, "Selecciona una imagen para convertir a sticker")

    def contorno_imagen(self, frame):
        tk.Label(frame, text="Tamaño del contorno", bg="white").pack(side="left")
        self.contorno = StringVar()
        contorno_input = tk.Entry(frame, textvariable=self.contorno)
        contorno_input.pack(pady=5, side="left", padx=5)

        ToolTip(contorno_input, "Ingresa el tamaño del contorno en pixeles")     

    def iniciar_boton(self, frame):
        def control():
            if self.archivos.control() == False:
                tk.messagebox.showerror("Error", "No se han seleccionado archivos")
            else:
                self.sticker_generado()

        tk.Button(frame, text="Iniciar", command=control).pack(side="top")

    def sticker_generado(self):
        """Muestra el sticker generado."""
        img_path = self.archivos.archivo  # Obtener la ruta desde el objeto AdministradorArchivos
        self.file_path = self.archivos.guardar_carpeta()
        if not os.path.isdir(img_path):
            print(f"La ruta {img_path} no es válida.")
            tk.messagebox.showerror("Error", "La ruta no es válida.")
            return

        print(f"Ruta de la imagen: {img_path}")  # Depuración: imprimir la ruta

        # Obtener el número total de imágenes para configurar la barra de progreso
        total_imagenes = len([imagen for imagen in os.listdir(img_path) if imagen.lower().endswith('.png')])

        self.progreso["maximum"] = total_imagenes  # Establecer el máximo de la barra de progreso
        self.progreso["value"] = 0  # Establecer el valor inicial de la barra de progreso

        for index, imagen in enumerate(os.listdir(img_path)):
            try:
                ruta_imagen = os.path.join(img_path, imagen)
                if os.path.isfile(ruta_imagen) and imagen.lower().endswith('.png'):
                    print(f"Procesando la imagen: {ruta_imagen}")  # Depuración: ruta de cada imagen
                    nombre_archivo = imagen
                    contorno = int(self.contorno.get())
                    expanded_img = generate_expanded_image(ruta_imagen, contorno + 5)
                    sticker = generate_sticker(expanded_img, contorno)

                    ruta_completa = os.path.join(self.file_path, nombre_archivo.split('.')[0] + "_sticker.png")
                    cv2.imwrite(ruta_completa, cv2.cvtColor(sticker, cv2.COLOR_RGBA2BGRA))

                    # Actualizar la barra de progreso
                    self.progreso["value"] = index + 1
                    self.ventana.update_idletasks()

            except FileNotFoundError as e:
                print(f"Error: El archivo {imagen} no se encontró. Detalles: {e}")
            except cv2.error as e:
                print(f"Error al procesar la imagen {imagen}. Detalles: {e}")
            except Exception as e:
                print(f"Se ha producido un error inesperado con la imagen {imagen}. Detalles: {e}")

        # Finalizar con el mensaje de completado
        tk.messagebox.showinfo("Proceso completado", "Se han generado los stickers correctamente.")

    def progreso_bar(self, total):
        self.progreso["maximum"] = total
        self.progreso["value"] = 0
        self.progreso.pack(pady=5)
    
    def version(self,frame):

        # Etiquetas dentro del Frame, lado a lado
        tk.Label(frame, text="Versión 1.0", anchor="w").pack(side="left", fill="x")
        tk.Label(frame, text="SrBolillo Studios", anchor="w").pack(side="right", fill="x")


    def iniciar(self):
        """Inicia el bucle principal de la interfaz."""
        self.ventana.mainloop()

class AdministradorArchivos:
    def __init__(self):
        self.archivo = None
        self.carpeta = None
        self.respuesta = False
        self.downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def guardar_carpeta(self):
        self.carpeta = filedialog.askdirectory(initialdir=self.downloads_folder,title="Seleccionar carpeta")
        if self.carpeta:
            print("Archivo seleccionado fue: ", self.carpeta)
            self.respuesta = True
            self.carpeta.encode('utf-8').decode('utf-8')
            return self.carpeta
        else:
            messagebox.showerror("Error", "No se seleccionó ningún archivo")

    def abrir_carpeta(self):
        self.archivo = filedialog.askdirectory(initialdir=self.downloads_folder,title="Seleccionar carpeta")
        if self.archivo:
            print("Carpeta seleccionada fue: ", self.archivo)
            self.respuesta = True
            self.archivo.encode('utf-8').decode('utf-8')
            return self.archivo
        else:
            messagebox.showerror("Error", "No se encontró ninguna carpeta")

    def control(self):
        return self.respuesta
def img_generator(img_path):
    # Paso 1: Expansión de la imagen
    img_path = "pechocho.png"
    border_size = 30

    # Expandir la imagen
    expanded_img = generate_expanded_image(img_path, border_size)

    # Mostrar la imagen expandida
    cv2.imshow("Expanded Image", cv2.cvtColor(expanded_img, cv2.COLOR_RGBA2BGRA))

    # Guardar la imagen expandida
    cv2.imwrite("expanded_image.png", cv2.cvtColor(expanded_img, cv2.COLOR_RGBA2BGRA))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Paso 2: Generación del sticker
    img_path = "expanded_image.png"
    sticker = generate_sticker(img_path)

    # Mostrar la imagen del sticker
    cv2.imshow("Sticker", cv2.cvtColor(sticker, cv2.COLOR_RGBA2BGRA))

    # Guardar la imagen del sticker
    cv2.imwrite("sticker5.png", cv2.cvtColor(sticker, cv2.COLOR_RGBA2BGRA))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Iniciar la interfaz
if __name__ == "__main__":
    interfaz = InterfazGeneradorSticker()
    interfaz.iniciar()
