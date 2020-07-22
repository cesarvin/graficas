from gl import Render

r = Render()

r.glInit() # funcion que inicia el render para generar el archivo
r.glCreateWindow(800,600) # crea el area sobre la que se trabaja la imagen
r.glViewPort(100,100, 600, 400)
r.glClearColor(0,0.5,1)
r.glColor(1,1,1)

# posibles valores para las coordenadas de la función glLine(x0,y0,x1,y1) para dibujar las lineas dentro del viewport
# x0, y0 pos inicial
# x1, y1 pos final
#
# (-1,1)        (0,1)        (1,1)
#        +--------+--------+ 
#        |        |        |
#        |        |        |
# (-1,0) |      (0,0)      | (1,0)
#        +--------+--------+ 
#        |        |        |
#        |        |        |
#        |        |        |
#        +--------+--------+ 
# (-1,-1)       (0,-1)       (1,-1)

r.glLine(0,0,1,1) #crea una linea del centro del viewport hacia la esquina superior izquierda
r.glLine(0,0,-1,1) #crea una linea del centro del viewport hacia la esquina superior derecha
r.glLine(-1,0,1,0) #crea una linea en el centro del viewport

r.glColor(0,0.5,1) #cambia el color de la linea


r.glFinish()