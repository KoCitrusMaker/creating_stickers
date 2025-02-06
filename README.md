# Sticker Generator from PNG Images

This script allows you to edit PNG images to expand them, add borders, and save them as stickers.

## Requirements
The script is fully written in Python and requires the following libraries:

```bash
pip install opencv-python numpy pillow tk tktooltip
```

## Instructions
1. **Execution**:  
   Run the `main.py` file to start the program.

2. **Main Files**:  
   - **`expandir_imagen.py`**  
     This file expands the image. It uses the function:  
     ```python
     generate_expanded_image(image_path, expand_pixels)
     ```  
     Where:  
     - `image_path`: Path to the image you want to expand.  
     - `expand_pixels`: Number of pixels to expand.

   - **`stickers_generador.py`**  
     This file detects the largest contour of the image, expands it, paints it white, and then overlays the original image. It returns a `.png` file with the function:  
     ```python
     generate_sticker(image_path, contour_expand)
     ```  
     Where:  
     - `image_path`: Path to the original image.  
     - `contour_expand`: Amount of expansion for the contour.

## Example
Below is an example showing the input image and the resulting sticker with a 10-pixel border:

<p align="center">
  <img src="input.png" alt="Input Image" width="200" style="margin-right: 10px;"> ➡️ <img src="output.png" alt="Resulting Sticker" width="200">
</p>

With this script, turning your images into personalized stickers is simple and quick!


### Resulting Sticker
![Resulting Sticker](output.png)

With this script, turning your images into personalized stickers is simple and quick!
