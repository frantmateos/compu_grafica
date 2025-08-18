import random


def bressenham_line(x1, y1, x2, y2, canvas):

    point = []
    deltaX = x2-x1
    deltaY = y2-y1

    stepx = 1 if deltaX >= 0 else -1
    stepy = 1 if deltaY >= 0 else -1

    err =  deltaX - deltaY

    while x1 != x2 or y1 != y2:
        point.append((x1, y1))
        e2 = 2 * err
        if e2 > -deltaY:
            err -= deltaY
            x1 += stepx
        if e2 < deltaX:
            err += deltaX
            y1 += stepy
    
    for x, y in point:
        set_pixel(int(x), int(y), canvas)


def save_ppm_p3(filename,canvas):
    height = len(canvas)
    width = len(canvas[0])
    with open(filename,"w",encoding="utf-8") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for row in canvas:
            line = []
            for (r,g,b) in row:
                line.append(f"{r} {g} {b}")
            f.write(" ".join(line) + "\n")

            f.write("\n")
        f.close()


def draw_line(x1, y1, x2, y2, canvas):
    point = []
    deltaX = x2-x1
    deltaY = y2-y1

    step = max(abs(deltaX), abs(deltaY))

    if deltaX >= 0:
        stepx = deltaX / step
        stepy = deltaY / step
        for i in range(step + 1):
            point.append((round(x1+i * stepx), round(y1+i * stepy)))

        for x, y in point:
            set_pixel(int(x), int(y), canvas)





def new_canvas(width,height,background_color = (0, 0, 0)):
    return [[background_color for _ in range(width) ]for _ in range(height)]


def set_pixel(x,y,canvas):
    color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    if 0 <= x < len(canvas[0]) and 0 <= y < len(canvas):
        canvas[y][x] = color

def print_canvas(canvas):
    for row in canvas:
        print("|".join(row))


canvas = new_canvas(80, 80)
#draw_line(0, 0, 0, 9, canvas)
#set_pixel(2, 3, canvas)
bressenham_line(12, 23, 67, 43, canvas)
bressenham_line(5, 2, 79, 78, canvas)
bressenham_line(34, 10, 60, 77, canvas)
bressenham_line(1, 1, 79, 79, canvas)
#print_canvas(canvas)
save_ppm_p3("primeralinea.ppm", canvas)