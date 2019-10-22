# Ein Spirograph
# https://de.wikipedia.org/wiki/Spirograph_(Spielzeug)
from PIL import Image, ImageDraw
from math import pi,sin,cos

R = 100 #Radius des großen Kreises

def spiro_curve(n,m,a,t):
    c = R/(1+(n/m))
    return ( (c* cos(t) + a*cos(m/n*t)), (c*sin(t) - a * sin(m/n * t)))

def spiro(n,m,a):
    T = 2*n
    h = 100
    interval = [t/h for t in range(0,h*T)]
    return [spiro_curve(n,m,a,t*pi) for t in interval]

def ggT(a,b):
    if b == 0:
        return a
    return ggT(b,a%b)

def spiro_image(n,m,f,colour):
    # m,n bestimmen Verhältnis der Radien s.d.
    # n*pi die Periode der Kurve angibt.
    # Vermutung: n+m = Anzahl der Zacken
    #f: Position des Stiftes im kleinen Kreis
    #0 = Mitte, 1 = Rand
    d = ggT(n,m)
    m = m//d
    n = n//d

    r = R/(1+m/n) # Radius des kleinen Kreises
    a = f * r
    im = Image.new('RGBA',(2*R,2*R))
    (oldx,oldy) = spiro_curve(n,m,a,0*pi)
    old = (oldx+R,oldy+R)
    draw = ImageDraw.Draw(im)
    for pixel in spiro(n,m,a):
        (x,y) = pixel
        x = round(x)+R
        y = round(y)+R
        #im.putpixel((x+R,y+R), colour+(255,))
        draw.line(old + (x,y), fill = colour+(255,))
        old = (x,y)
    return im

im = Image.new('RGBA',(2*R,2*R))
#params = [(10,7,0.3,(0,255,255)), (2,1,0.5,(255,0,255)), (5,3,0.7,(255,255,0))]
params = [(3,1,1,(255,0,0)), (1,1,0,(0,255,0))]
for (n,m,f,colour) in params:
    im2 = spiro_image(n,m,f,colour)
    im = Image.alpha_composite(im,im2)

im.show()
im.save('spirale.png', 'PNG')
