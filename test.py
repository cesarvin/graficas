from gl import Render, color, V2, V3
from obj import Obj, Texture

r = Render()
r.glCreateWindow(1000,1000)
r.glClearColor(0.4,0.6,0.5)
t = Texture('./models/model.bmp')
r.glLoadModel('./models/model.obj',V3(500,500,0), V3(300,300,300), t)

r.glFinish('output.bmp')

