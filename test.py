from gl import Render

r = Render()

r.glInit() 
r.glCreateWindow(800,800) 
r.glColor(0.5,1,0.6)

#camión
r.glLoadModel('./models/truck.obj', (400,100 ), (150,150) )
r.glFinish('truck.bmp')
 

r.glCreateWindow(1200,800) 

#tigre
r.glLoadModel('./models/Tiger.obj', (600,50 ), (1,1) )
r.glFinish('tiger.bmp')