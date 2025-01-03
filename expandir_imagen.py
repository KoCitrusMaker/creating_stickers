import cv2
import numpy as np

def generate_expanded_image(img_path, border_size):
    """Amplía una imagen expandiendo los bordes con transparencia."""
    """_summary_

    Args:
        img_path (_type_): _description_
        border_size (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Leer la imagen
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    # Obtener el tamaño original
    original_height, original_width = img.shape[:2]
    
    # Calcular el nuevo tamaño
    new_width = original_width + 2 * border_size
    new_height = original_height + 2 * border_size
    
    # Crear una nueva imagen con transparencia (RGBA)
    expanded_img = np.zeros((new_height, new_width, 4), dtype=np.uint8)
    
    # Calcular las coordenadas para centrar la imagen original
    y_start = border_size
    y_end = y_start + original_height
    x_start = border_size
    x_end = x_start + original_width
    
    # Copiar la imagen original al centro del nuevo lienzo
    expanded_img[y_start:y_end, x_start:x_end] = img
    
    return expanded_img

# Ejemplo de uso
if __name__ == "__main__":
    img_path = "patata.png"  # Ruta de la imagen original
    border_size = 30  # Tamaño del borde adicional en píxeles
    
    # Llamar a la función para generar la imagen expandida
    expanded_img = generate_expanded_image(img_path, border_size)
    
    # Mostrar y guardar la imagen expandida
    cv2.imshow("Expanded Image", cv2.cvtColor(expanded_img, cv2.COLOR_RGBA2BGRA))
    cv2.imwrite("guardado.png", cv2.cvtColor(expanded_img, cv2.COLOR_RGBA2BGRA))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
