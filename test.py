from gl import Render

r = Render()

r.glInit() # funcion que inicia el render para generar el archivo
r.glCreateWindow(600,800) # crea el area sobre la que se trabaja la imagen


r.glClearColor(0.3,0.8,0.46)

r.glColor(0,0,0)

r.glVertex(0,0)


r.glFinish()