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
    
    intensity = ((normal.x * render.light.x) + (normal.y * render.light.y) + (normal.z * render.light.z))

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0


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