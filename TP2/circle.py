from utils import new_canvas,set_pixel,save_png 

def draw_circle(centerX,centerY,radio):
    points = []
    x = 0
    y = -radio
    yMid = y + 0.5
    decisionPoint = -radio
    while x < -y:
        if decisionPoint > 0:
            y+= 1
            decisionPoint += 2 * (x+y) + 1
        else:
            decisionPoint += 2 * x + 1
        points.append((centerX + x, centerY + y))
        points.append((centerX - x, centerY - y))
        points.append((centerX - x, centerY + y))
        points.append((centerX + x, centerY - y))
        points.append((centerX + y, centerY + x))
        points.append((centerX - y, centerY - x))
        points.append((centerX - y, centerY + x))
        points.append((centerX + y, centerY - x))
         
        x+=1
    return points

canvas = new_canvas(256,256)
circle = draw_circle(128,128,20)

for x,y in circle:
    set_pixel(x,y,canvas)

save_png("circle.png",canvas)



