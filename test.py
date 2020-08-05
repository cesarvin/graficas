from gl import Render, color, V2, V3
from obj import Obj 

import random

r = Render()
r.glCreateWindow(1200,800)

r.glLoadModel( './models/Tiger.obj',  V3(600,50,0), V3(1,1,1))

#r.glFinish('Tiger.bmp')
r.glZBuffer('Tiger_zbuffer.bmp')

