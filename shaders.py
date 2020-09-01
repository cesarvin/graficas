from gl import *

import random

def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)
    
    intensityA = ((na.x * render.light.x) + (na.y * render.light.y) + (na.z * render.light.z))
    intensityB = ((nb.x * render.light.x) + (nb.y * render.light.y) + (nb.z * render.light.z))
    intensityC = ((nc.x * render.light.x) + (nc.y * render.light.y) + (nc.z * render.light.z))

    colorA = (r * intensityA, g * intensityA, b * intensityA)
    colorB = (r * intensityB, g * intensityB, b * intensityB)
    colorC = (r * intensityC, g * intensityC, b * intensityC)

    b = colorA[2] * u + colorB[2] * v + colorC[2] * w
    g = colorA[1] * u + colorB[1] * v + colorC[1] * w
    r = colorA[0] * u + colorB[0] * v + colorC[0] * w

    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b

    return r, g, b


def toon(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)
    
    intensity = ((normal.x * render.light.x) + (normal.y * render.light.y) + (normal.z * render.light.z))

    if (intensity > 0.95):
        intensity = 1
    if (intensity > 0.85):
        intensity = 0.94        
    elif (intensity > 0.75):
        intensity = 0.84
    elif (intensity > 0.50):
        intensity = 0.74
    elif (intensity > 0.25):
        intensity = 0.49
    else:
        intensity = 0.24

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def static_matrix(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = [0,255,14]
    
    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255
    
    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)
    
    intensity = ((normal.x * render.light.x) + (normal.y * render.light.y) + (normal.z * render.light.z))
    
    b *= intensity
    g *= intensity
    r *= intensity
    
    if intensity >=0.80 and random.randint(1, 2) % 2 == 0:
        return r, g, b
    elif intensity >= 0.74 and random.randint(1, 3) % 3 == 0:
        return r, g, b
    elif intensity >= 0.49 and random.randint(1, 4) % 4 == 0:
        return r, g, b
    elif intensity >= 0.24 and random.randint(1, 5) % 5 == 0:
        return r, g, b
    else:
        return 0,0,0

def negative(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    b, g, r = kwargs['color']

    b /= 255 
    g /= 255 
    r /= 255 

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    return 1-r, 1-g, 1-b    

def phong(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    normal = V3(nx, ny, nz)
    
    intensity = ((normal.x * render.light.x) + (normal.y * render.light.y) + (normal.z * render.light.z))

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0


def greyScale(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)
    
    intensity = ((normal.x * render.light.x) + (normal.y * render.light.y) + (normal.z * render.light.z))

    b *= intensity
    g *= intensity
    r *= intensity

    prom = b + g + r / 3.0

    if intensity > 0:
        return prom, prom, prom
    else:
        return 0,0,0