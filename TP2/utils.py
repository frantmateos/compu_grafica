import random
from PIL import Image


def new_canvas(width,height,background_color = (0, 0, 0)):
    return [[background_color for _ in range(width) ]for _ in range(height)]

def save_png(filename, canvas):
    """Guarda la imagen en PNG usando Pillow.""" # Texto descriptivo para una función, esto es muy útil
    h = len(canvas)
    w = len(canvas[0])
    im = Image.new("RGB", (w, h))
    # Flatten de la lista de listas
    pixels_flat = [pixel for row in canvas for pixel in row] # recorre cada fila de img y dentro de cada fila recorre cada pixel para guardarlo en una sola lista.
    im.putdata(pixels_flat)
    im.save(filename, "PNG")


def set_pixel(x,y,canvas):

    color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    if 0 <= x < len(canvas[0]) and 0 <= y < len(canvas):
        canvas[y][x] = color