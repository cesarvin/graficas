from gl import Render, color, V2, V3
from obj import Obj, Texture
from shaders import *

r = Render()
r.glCreateWindow(500,500)

r.active_texture = Texture('./models/model.bmp')
r.active_shader = gourad

posModel = V3( 0, 3, 0)
r.lookAt(posModel, V3(0,0,-5))
r.glLoadModel('./models/model.obj', posModel, V3(2,2,2), V3(0,0,0))
r.glFinish('high_angle.bmp')

r.glClear()

posModel = V3( 0, -3, 0)
r.lookAt(posModel, V3(0,0,-5))
r.glLoadModel('./models/model.obj', posModel, V3(2,2,2), V3(0,0,0))
r.glFinish('low_angle.bmp')

r.glClear()

posModel = V3( 0, 0, 0)
r.lookAt(posModel, V3(0,0,-5))
r.glLoadModel('./models/model.obj', posModel, V3(2,2,2), V3(0,0,0))
r.glFinish('medium_angle.bmp')


r.glClear()

posModel = V3( 0, 0, 0)
r.lookAt(posModel, V3(-3,-3,-0.5))
r.glLoadModel('./models/model.obj', posModel, V3(2,2,2), V3(0,90,0))
r.glFinish('dutch_angle.bmp')