# Carga un archivo OBJ

class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.read()

    def read(self):
        for line in self.lines:
            if line:
                if len(line) > 0 :
                    if line[0] != '#' :
                        prefix, value = line.split(' ', 1)
                        value = value.strip().replace('//','/').replace('  ',' ')

                        if prefix == 'v':
                            self.vertices.append(list(map(float,value.split(' '))))
                        elif prefix == 'f':
                            nvalue = value.strip()
                            self.faces.append([list(map(int, face.split('/'))) for face in nvalue.split(' ')])
