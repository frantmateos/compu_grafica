import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from utils import new_canvas, set_pixel, save_png
from bresenhamLine import bresenham_line
from middlePointCircle import middle_point_circle

WIDTH, HEIGHT = 400, 400 
COLOR = (255, 255, 255)  

canvas_data = new_canvas(WIDTH, HEIGHT, (0, 0, 0))  

root = tk.Tk()
root.title("Mini Paint Casero")

img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)) 
photo = ImageTk.PhotoImage(img)
label = tk.Label(root, image=photo)
label.pack()

mode = tk.StringVar(value="linea")
points = [] 
def redraw_canvas():
    global photo, img
    pixels = [pix for row in canvas_data for pix in row]
    img.putdata(pixels)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

def on_click(event):
    global points
    points.append((event.x, event.y))

    # --- Dibujar Línea ---
    if mode.get() == "linea" and len(points) == 2:
        linea = bresenham_line(points[0][0], points[0][1], points[1][0], points[1][1])
        for (x, y) in linea:
            set_pixel(canvas_data, x, y, COLOR)
        redraw_canvas()
        points = []

    # --- Dibujar Rectángulo ---
    elif mode.get() == "rect" and len(points) == 2:
        x0, y0 = points[0]
        x1, y1 = points[1]

        for p in bresenham_line(x0, y0, x1, y0):
            set_pixel(canvas_data, p[0], p[1], COLOR)
        for p in bresenham_line(x1, y0, x1, y1):
            set_pixel(canvas_data, p[0], p[1], COLOR)
        
        for p in bresenham_line(x1, y1, x0, y1):
            set_pixel(canvas_data, p[0], p[1], COLOR)
        for p in bresenham_line(x0, y1, x0, y0):
            set_pixel(canvas_data, p[0], p[1], COLOR)

        redraw_canvas()
        points = []

    # --- Dibujar Círculo ---
    elif mode.get() == "circle" and len(points) == 2:
        (cx, cy), (px, py) = points
        r = int(((px - cx) ** 2 + (py - cy) ** 2) ** 0.5)
        circulo = middle_point_circle(cx, cy, r)
        for (x, y) in circulo:
            set_pixel(canvas_data, x, y, COLOR)
        redraw_canvas()
        points = []

    # --- Dibujar Triángulo ---
    elif mode.get() == "tri" and len(points) == 3:
        for i in range(3):
            (x0, y0) = points[i]
            (x1, y1) = points[(i + 1) % 3]  
            for p in bresenham_line(x0, y0, x1, y1):
                set_pixel(canvas_data, p[0], p[1], COLOR)
        redraw_canvas()
        points = []

def save_image():
    filename = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
    if filename:
        save_png(filename, canvas_data)

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Línea", command=lambda: mode.set("linea")).pack(side=tk.LEFT)
tk.Button(frame, text="Rectángulo", command=lambda: mode.set("rect")).pack(side=tk.LEFT)
tk.Button(frame, text="Círculo", command=lambda: mode.set("circle")).pack(side=tk.LEFT)
tk.Button(frame, text="Triángulo", command=lambda: mode.set("tri")).pack(side=tk.LEFT)
tk.Button(frame, text="Guardar", command=save_image).pack(side=tk.LEFT)

label.bind("<Button-1>", on_click)

redraw_canvas()

root.mainloop()
