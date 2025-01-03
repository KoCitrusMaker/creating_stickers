import cv2
import numpy as np

class StickerGenerator:
    def __init__(self):
        pass

    @staticmethod
    def read_image(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    @staticmethod
    def extract_alpha_channel(img):
        if img.shape[2] < 4:
            raise ValueError("The input image does not have an alpha channel.")
        return img[:, :, 3]

    @staticmethod
    def get_largest_contour(alpha_channel):
        smoothed = cv2.GaussianBlur(alpha_channel, (15, 15), 0)
        contours = cv2.findContours(smoothed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        if not contours:
            raise ValueError("No contours found in the alpha channel.")
        big_contour = max(contours, key=cv2.contourArea)
        peri = cv2.arcLength(big_contour, True)
        return cv2.approxPolyDP(big_contour, 0.001 * peri, True)

    @staticmethod
    def draw_filled_contour_on_black_background(big_contour, shape):
        contour_img = np.zeros(shape, dtype=np.uint8)
        cv2.drawContours(contour_img, [big_contour], 0, 255, -1)
        return contour_img

    @staticmethod
    def apply_dilation(img,border_size):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (border_size,border_size))
        return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)

    @staticmethod
    def apply_overlays(canvas, img, dilate):
        white_background = np.ones_like(canvas) * 255
        white_background[:, :, 3] = 0

        white_background[dilate == 255, :3] = [255, 255, 255]
        white_background[dilate == 255, 3] = 255

        alpha = img[:, :, 3] / 255.0
        canvas[:, :, :3] = (
            img[:, :, :3] * alpha[..., None] + white_background[:, :, :3] * (1 - alpha[..., None])
        )
        canvas[:, :, 3] = np.maximum(img[:, :, 3], white_background[:, :, 3])
        return canvas

    def create_sticker(self, img_path, border_size):
       # img = self.read_image(img_path)
        img = img_path
        alpha = self.extract_alpha_channel(img)
        big_contour = self.get_largest_contour(alpha)
        contour_img = self.draw_filled_contour_on_black_background(big_contour, alpha.shape)
        dilate = self.apply_dilation(contour_img,border_size)

        canvas = np.zeros(img.shape, dtype=np.uint8)
        canvas = self.apply_overlays(canvas, img, dilate)

        return canvas.astype(np.uint8)

# Función para usar en tu proyecto
def generate_sticker(img_path, border_size):
    """Genera un sticker a partir de una imagen con fondo transparente."""
    """_summary_

    Args:
        img_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    generator = StickerGenerator()
    return generator.create_sticker(img_path,border_size)
