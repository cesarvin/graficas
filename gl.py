import struct

from obj import Obj

# Estructuras necesarias para construir el archivo
# Estructuras basadas en ejemplo realizado en clase
def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

BLACK = color(0,0,0)
WHITE = color(1,1,1)


class Render(object):
    def __init__(self):
        self.backcolor = BLACK
        self.pointcolor = WHITE
        

    def glInit(self):
        self.pixels =[]
    
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewPort(0, 0, width, height)

    def glViewPort(self, x, y, width, height):
        self.glViewPortWidth = width - 1
        self.glViewPortHeight = height - 1
        self.glViewPortX = x
        self.glViewPortY = y

    def glClear(self):
        self.pixels = [ [ self.backcolor for x in range(self.width)] for y in range(self.height) ]

    def glClearColor(self, r, g, b):
        self.backcolor = color(r, g, b) 
        self.pixels = [ [ self.backcolor for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y):
        glVertexX = ( x + 1 ) * ( self.glViewPortWidth / 2 ) + self.glViewPortX 
        glVertexY = ( y + 1 ) * ( self.glViewPortHeight / 2) + self.glViewPortY 
        #print (round(glVertexX))
        #print (round(glVertexY))
        self.pixels[round(glVertexY)][round(glVertexX)] = self.pointcolor

    def glColor(self, r, g, b):
        self.pointcolor = color(r, g, b)

    def glFinish(self, filename='out.bmp'):
        self.write(filename)        
    
    def write(self, filename):
        # Función write basada en ejemplo realizado en clase
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(char('B'))
        archivo.write(char('M'))

        #archivo.write(bytes('B'.encode('ascii')))
        #archivo.write(bytes('M'.encode('ascii')))

        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno

        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def point(self, x, y): 
        self.pixels[y][x] = self.pointcolor

    def glLine(self,x0, y0, x1, y1):
        '''
        posibles valores para las coordenadas de la función glLine(x0,y0,x1,y1)
        x0, y0 pos inicial
        x1, y1 pos final
        #
        (-1,1)         (0,1)         (1,1)
               +---------+---------+ 
               |         |         |
               |         |         |
        (-1,0) |       (0,0)       | (1,0)
               +---------+---------+ 
               |         |         |
               |         |         |
               |         |         |
               +---------+---------+ 
        (-1,-1)        (0,-1)        (1,-1)
        '''
        x0 = ( x0 + 1) * (self.glViewPortWidth  / 2 ) + self.glViewPortX
        y0 = ( y0 + 1) * (self.glViewPortHeight / 2 ) + self.glViewPortY
        x1 = ( x1 + 1) * (self.glViewPortWidth  / 2 ) + self.glViewPortX
        y1 = ( y1 + 1) * (self.glViewPortHeight / 2 ) + self.glViewPortY
        print(round(x1))
        print(round(y1))
        self.line(round(x0), round(y0), round(x1), round(y1))

    def line(self,x0, y0, x1, y1):
        #implementacion del algoritmo de bresenham para dibujar lineas
        #basado en el ejemplo de la clase
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        offset = 0
        limit = 0.5

        if dx != 0:
            m = dy/dx
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.point(y, x)
                else:
                    self.point(x, y)

                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def glLoadModel(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vc = len(face)

            for i in range(vc):
                v0 = model.vertices[ face[i][0] - 1 ]
                v1 = model.vertices[ face[(i + 1) % vc][0] - 1]

                self.line(round(v0[0] * scale[0]  + translate[0]), round(v0[1] * scale[1]  + translate[1]), round(v1[0] * scale[0]  + translate[0]), round(v1[1] * scale[1]  + translate[1]))

    