from gl import Render, color, V2, V3
from obj import Obj, Texture
from shaders import *


import random

r = Render()
r.glCreateWindow(1000,1000)

r.active_texture = Texture('./models/model.bmp')

r.active_shader = gourad
#r.glLoadModel('./models/earth.obj', V3(500,500,0), V3(1,1,1))
r.glLoadModel('./models/model.obj',V3(500,500,0), V3(300,300,300))
r.glFinish('gourad.bmp')
print('gourad.bmp creado')
r.glClear()

r.active_shader = toon
r.glLoadModel('./models/model.obj',V3(500,500,0), V3(300,300,300))
r.glFinish('toon.bmp')
print('toon.bmp creado')
r.glClear()

r.active_shader = static_matrix
r.glLoadModel('./models/model.obj',V3(500,500,0), V3(300,300,300))
print('static_matrix.bmp creado')
r.glFinish('static_matrix.bmp')
r.glClear()

r.active_shader = negative
r.glLoadModel('./models/model.obj',V3(500,500,0), V3(300,300,300))
print('negative.bmp creado')
r.glFinish('negative.bmp')
r.glClear()
