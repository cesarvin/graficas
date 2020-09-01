import struct

from obj import Obj
from collections import namedtuple
from gl_aux import *

#import numpy as np
#from numpy import matrix, cos, sin

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z','w'])

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


def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B.y - C.y)*(P.x - C.x) + (C.x - B.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        v = ( ((C.y - A.y)*(P.x - C.x) + (A.x - C.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

BLACK = color(0,0,0)
WHITE = color(1,1,1)


class Render(object):
    def __init__(self):
        self.backcolor = BLACK
        self.pointcolor = WHITE
        self.light = V3(0,0,1)
        self.active_texture = None
        self.active_shader = None

    def glInit(self):
        self.pixels =[]
    
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewPort(0, 0, width, height)
        self.createViewMatrix()
        self.createProjectionMatrix()

    def glViewPort(self, x, y, width, height):
        self.glViewPortWidth = width - 1
        self.glViewPortHeight = height - 1
        self.glViewPortX = x
        self.glViewPortY = y
        self.viewportMatrix = matrix([[width/2,        0,   0,  x + width/2],
                                      [      0, height/2,   0, y + height/2],
                                      [      0,        0, 0.5,          0.5],
                                      [      0,        0,   0,            1]])

    def glClear(self):
        self.pixels = [ [ self.backcolor for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glClearColor(self, r, g, b):
        self.backcolor = color(r, g, b) 
        self.pixels = [ [ self.backcolor for x in range(self.width)] for y in range(self.height) ]
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

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

    def point(self, x, y, color = None):
        if x < self.glViewPortX or x >= self.glViewPortX + self.glViewPortWidth or y < self.glViewPortY or y >= self.glViewPortY + self.glViewPortHeight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.pointcolor
        except:
            pass

    def glLine(self,x0, y0, x1, y1, color = None):
        x0 = ( x0 + 1) * (self.glViewPortWidth  / 2 ) + self.glViewPortX
        y0 = ( y0 + 1) * (self.glViewPortHeight / 2 ) + self.glViewPortY
        x1 = ( x1 + 1) * (self.glViewPortWidth  / 2 ) + self.glViewPortX
        y1 = ( y1 + 1) * (self.glViewPortHeight / 2 ) + self.glViewPortY
        v0 = V2(round(x0), round(y0))
        v1 = V2(round(x1), round(y1))

        self.line(v0, v1, color)

    def line(self, v0, v1, color = None):
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

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
                    self.point(y, x, color)
                else:
                    self.point(x, y, color)

                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def glLoadModel_poli(self, filename, translate, scale):
        model = Obj(filename)

        for face in model.faces:
            vc = len(face)

            for i in range(vc):
                v0 = model.vertices[ face[i][0] - 1 ]
                v1 = model.vertices[ face[(i + 1) % vc][0] - 1]

                lv0 = V2(round(v0[0] * scale[0]  + translate[0]), round(v0[1] * scale[1]  + translate[1]))
                lv1 = V2(round(v1[0] * scale[0]  + translate[0]), round(v1[1] * scale[1]  + translate[1]))    
                self.line(lv0 , lv1)

    def glLoadModel_flat(self, filename, translate = V3(0,0,0), scale = V3(1,1,1)):
        model = Obj(filename)

        light = V3(0,0,1)

        for face in model.faces:

            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1 ]
            v1 = model.vertices[ face[1][0] - 1 ]
            v2 = model.vertices[ face[2][0] - 1 ]

            v0 = self.transform_original(v0,translate, scale)
            v1 = self.transform_original(v1,translate, scale)
            v2 = self.transform_original(v2,translate, scale)

            s1 = V3((v1.x - v0.x), (v1.y - v0.y), (v1.z - v0.z))
            s2 = V3((v2.x - v0.x), (v2.y - v0.y), (v2.z - v0.z))
            
            normal = V3(((s1.y * s2.z)- (s2.y * s1.z)), -((s1.x * s2.z)- (s2.x * s1.z)), ((s1.x * s2.y)- (s2.x * s1.y)))
            
            try:
                norm_normal = ( abs(normal.x)**2 + abs(normal.y)**2 + abs(normal.z)**2 )**(1/2)
                normal = V3((normal.x / norm_normal), (normal.y / norm_normal), (normal.z / norm_normal))
                intensity = ((normal.x * light.x) + (normal.y * light.y) + (normal.z * light.z))

                if intensity >=0:
                    self.triangle_bc_flat(v0,v1,v2, color(intensity, intensity, intensity))

                if vertCount > 3: 
                    v3 = model.vertices[ face[3][0] - 1 ]
                    v3 = self.transform_original(v3,translate, scale)
                    if intensity >=0:
                        self.triangle_bc_flat(v0,v2,v3, color(intensity, intensity, intensity))
            except:
                pass

    def glLoadModel_texture(self, filename, translate = V3(0,0,0), scale = V3(1,1,1), texture = None):
        model = Obj(filename)

        light = V3(0,0,1)

        for face in model.faces:

            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1 ]
            v1 = model.vertices[ face[1][0] - 1 ]
            v2 = model.vertices[ face[2][0] - 1 ]
            if vertCount > 3:
                v3 = model.vertices[ face[3][0] - 1 ]

            v0 = self.transform_original(v0,translate, scale)
            v1 = self.transform_original(v1,translate, scale)
            v2 = self.transform_original(v2,translate, scale)
            if vertCount > 3:
                v3 = self.transform_original(v3,translate, scale)

            if texture:
                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                vt0 = V2(vt0[0], vt0[1])
                vt1 = V2(vt1[0], vt1[1])
                vt2 = V2(vt2[0], vt2[1])
                if vertCount > 3:
                    vt3 = model.texcoords[face[3][1] - 1]
                    vt3 = V2(vt3[0], vt3[1])
            else:
                vt0 = V2(0,0) 
                vt1 = V2(0,0) 
                vt2 = V2(0,0) 
                vt3 = V2(0,0) 

            s1 = V3((v1.x - v0.x), (v1.y - v0.y), (v1.z - v0.z))
            s2 = V3((v2.x - v0.x), (v2.y - v0.y), (v2.z - v0.z))
                
            normal = V3(((s1.y * s2.z)- (s2.y * s1.z)), -((s1.x * s2.z)- (s2.x * s1.z)), ((s1.x * s2.y)- (s2.x * s1.y)))

            try:
                norm_normal = ( abs(normal.x)**2 + abs(normal.y)**2 + abs(normal.z)**2 )**(1/2)
            
                normal = V3((normal.x / norm_normal), (normal.y / norm_normal), (normal.z / norm_normal))

                intensity = (normal.x * light.x) + (normal.y * light.y) + (normal.z * light.z)
 
                if intensity >=0:
                    self.triangle_bc_texture(v0,v1,v2, texture = texture, texcoords = (vt0,vt1,vt2), intensity = intensity )
                    if vertCount > 3: 
                        v3 = model.vertices[ face[3][0] - 1 ]
                        v3 = self.transform_original(v3,translate, scale)
                        self.triangle_bc_texture(v0,v2,v3, texture = texture, texcoords = (vt0,vt2,vt3), intensity = intensity)
            except:
                pass

    def transform_original(self, vertex, translate=V3(0,0,0), scale=V3(1,1,1)):
        return V3(round(vertex[0] * scale.x + translate.x),
                  round(vertex[1] * scale.y + translate.y),
                  round(vertex[2] * scale.z + translate.z))

    def transform(self, vertex, vMatrix):
        
        augVertex = V4( vertex[0], vertex[1], vertex[2], 1)
        transVertex = self.viewportMatrix @ self.projectionMatrix @ self.viewMatrix @ vMatrix @ augVertex

        transVertex = transVertex.tolist()[0]

        transVertex = V3(transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])
        #print(transVertex)
        return transVertex

    def dirTransform(self, vertex, vMatrix):
        augVertex = V4( vertex[0], vertex[1], vertex[2], 0)
        transVertex = vMatrix @ augVertex
        transVertex = transVertex.tolist()[0]
        transVertex = V3(transVertex[0],transVertex[1],transVertex[2])

        return transVertex
    
    def glLoadModel_shaders(self, filename, translate = V3(0,0,0), scale = V3(1,1,1)):
        model = Obj(filename)

        #light = V3(0,0,1)

        for face in model.faces:

            vertCount = len(face)
            v0 = model.vertices[ face[0][0] - 1 ]
            v1 = model.vertices[ face[1][0] - 1 ]
            v2 = model.vertices[ face[2][0] - 1 ]
            if vertCount > 3:
                v3 = model.vertices[ face[3][0] - 1 ]

            v0 = self.transform_original(v0,translate, scale)
            v1 = self.transform_original(v1,translate, scale)
            v2 = self.transform_original(v2,translate, scale)
            if vertCount > 3:
                v3 = self.transform_original(v3,translate, scale)

            if self.active_texture:
                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                vt0 = V2(vt0[0], vt0[1])
                vt1 = V2(vt1[0], vt1[1])
                vt2 = V2(vt2[0], vt2[1])
                if vertCount > 3:
                    vt3 = model.texcoords[face[3][1] - 1]
                    vt3 = V2(vt3[0], vt3[1])
            else:
                vt0 = V2(0,0) 
                vt1 = V2(0,0) 
                vt2 = V2(0,0) 
                vt3 = V2(0,0) 
            
            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]
                

            if vertCount > 3:
                vn3 = model.normals[face[3][2] - 1]
            try:
                self.triangle_bc(v0,v1,v2, texcoords = (vt0,vt1,vt2), normals = (vn0,vn1,vn2))
                if vertCount > 3:
                    self.triangle_bc(v0,v2,v3, texcoords = (vt0,vt2,vt3), normals = (vn0,vn2,vn3))
            except:
                pass
    
    def glLoadModel(self, filename, translate = V3(0,0,0), scale = V3(1,1,1), rotate=V3(0,0,0)):
        model = Obj(filename)

        mMatrix = modelMatrix(translate, scale, rotate)
        rMatrix = rotationMatrix(rotate)

        for face in model.faces:

            vertCount = len(face)
            v0 = model.vertices[ face[0][0] - 1 ]
            v1 = model.vertices[ face[1][0] - 1 ]
            v2 = model.vertices[ face[2][0] - 1 ]
            if vertCount > 3:
                v3 = model.vertices[ face[3][0] - 1 ]

            v0 = self.transform(v0, mMatrix)
            v1 = self.transform(v1, mMatrix)
            v2 = self.transform(v2, mMatrix)
            if vertCount > 3:
                v3 = self.transform(v3, mMatrix)

            if self.active_texture:
                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                vt0 = V2(vt0[0], vt0[1])
                vt1 = V2(vt1[0], vt1[1])
                vt2 = V2(vt2[0], vt2[1])
                if vertCount > 3:
                    vt3 = model.texcoords[face[3][1] - 1]
                    vt3 = V2(vt3[0], vt3[1])
            else:
                vt0 = V2(0,0) 
                vt1 = V2(0,0) 
                vt2 = V2(0,0) 
                vt3 = V2(0,0) 
            
            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]

            vn0 = self.dirTransform(vn0, rMatrix)
            vn1 = self.dirTransform(vn1, rMatrix)
            vn2 = self.dirTransform(vn2, rMatrix)

            if vertCount > 3:
                vn3 = model.normals[face[3][2] - 1]
                vn3 = self.dirTransform(vn3, rMatrix)

            try:
                self.triangle_bc(v0,v1,v2, texcoords = (vt0,vt1,vt2), normals = (vn0,vn1,vn2))
                if vertCount > 3:
                    self.triangle_bc(v0,v2,v3, texcoords = (vt0,vt2,vt3), normals = (vn0,vn2,vn3))
            except:
                pass

    def triangle(self, A, B, C, color = None):
        
        def flatBottomTriangle(v1,v2,v3):
            for y in range(v1.y, v3.y + 1):
                xi = round( v1.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v1.y))
                xf = round( v2.x + (v3.x - v2.x)/(v3.y - v2.y) * (y - v2.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x,y, color or self.pointcolor)

        def flatTopTriangle(v1,v2,v3):
            for y in range(v1.y, v3.y + 1):
                xi = round( v2.x + (v2.x - v1.x)/(v2.y - v1.y) * (y - v2.y))
                xf = round( v3.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v3.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x,y, color or self.pointcolor)

        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        if A.y == C.y:
            return

        if A.y == B.y: 
            flatBottomTriangle(A,B,C)
        elif B.y == C.y: 
            flatTopTriangle(A,B,C)
        else: 
            x4 = A.x + (C.x - A.x)/(C.y - A.y) * (B.y - A.y)
            D = V2( round(x4), B.y)
            flatBottomTriangle(D,B,C)
            flatTopTriangle(A,B,D)

    def triangle_bc_flat(self, A, B, C, color = None):
        minX = min(A.x, B.x, C.x)
        minY = min(A.y, B.y, C.y)
        maxX = max(A.x, B.x, C.x)
        maxY = max(A.y, B.y, C.y)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))
                if u >= 0 and v >= 0 and w >= 0:
                    z = A.z * u + B.z * v + C.z * w

                    if z > self.zbuffer[y][x]:
                        self.point(x, y, color)
                        self.zbuffer[y][x] = z
    
    def triangle_bc_texture(self, A, B, C,  _color = WHITE, texture = None, texcoords = (), intensity = 1):
        minX = min(A.x, B.x, C.x)
        minY = min(A.y, B.y, C.y)
        maxX = max(A.x, B.x, C.x)
        maxY = max(A.y, B.y, C.y)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = baryCoords(A, B, C, V2(x, y))
                if u >= 0 and v >= 0 and w >= 0:
                    z = A.z * u + B.z * v + C.z * w

                    if z > self.zbuffer[y][x]:
                        b, g , r = _color
                        b /= 255
                        g /= 255
                        r /= 255

                        b *= intensity
                        g *= intensity
                        r *= intensity

                        if texture:
                            ta, tb, tc = texcoords
                            tx = ta.x * u + tb.x * v + tc.x * w
                            ty = ta.y * u + tb.y * v + tc.y * w

                            texColor = texture.getColor(tx, ty)
                            b *= texColor[0] / 255
                            g *= texColor[1] / 255
                            r *= texColor[2] / 255
                        
                        #print(r,g,b)
                        self.point(x, y, color(r,g,b))
                        self.zbuffer[y][x] = z

    
    def triangle_bc(self, A, B, C, texcoords = (), normals = (), _color = None):
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = baryCoords(A, B, C, V2(x, y))
                if u >= 0 and v >= 0 and w >= 0:
                    z = A.z * u + B.z * v + C.z * w

                    # if z > self.zbuffer[y][x]:
                    #print('Holi........')
                    if z > self.zbuffer[y][x]: #and z <= 1 and z >= -1:
                    
                        if self.active_shader:
                            r, g, b = self.active_shader(
                                self,
                                verts=(A,B,C),
                                baryCoords=(u,v,w),
                                texCoords=texcoords,
                                normals=normals,
                                color = _color or self.pointcolor)
                        else: 
                            b, g, r = _color or self.pointcolor

                        self.point(x, y, color(r,g,b))
                        self.zbuffer[y][x] = z

    
    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
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

        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                
                if (maxZ - minZ) > 0:
                    depth = (depth - minZ) / (maxZ - minZ)
                else:
                    depth = (depth - minZ)

                archivo.write(color(depth,depth,depth))
                

        archivo.close()

    def createViewMatrix(self, camPosition = V3(0,0,0), camRotation = V3(0,0,0)):
        self.viewMatrix = viewMatrix(camPosition, camRotation)

    def lookAt(self, eye, camPosition = V3(0,0,0)):
        self.viewMatrix = look(eye, camPosition)

    def createProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        self.projectionMatrix =projectionMatrix(n, f, fov, self.glViewPortWidth, self.glViewPortHeight)

