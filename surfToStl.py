import numpy as np
import os

class surf:
    """
    Class for handling .surf files with this particular header
    # HyperSurface 0.1 ASCII

    Parameters {
    Materials {
        Exterior {
            id 0
        }
        Interior {
            id 1
        }
    }
    BoundaryIds {
        name "BoundaryConditions"
    }
    Filename "/gpfs/home/cxl503/work/research/mesh/E17_conv_outer_wall.stl"
    }
    """
    
    def __init__(self,surfFile):
        self.file = surfFile
        # Read file
        with open(self.file,"r") as surfFile:
            readLines = surfFile.readlines()
            # Cycle through all the lines
            for i, lines in enumerate(readLines):
                # To find vertices lines it will look to the word Vertices
                if 'Vertices' in lines.split():
                    # The next number besides Vertices is the number of vertices
                    self.numberOfVertices = int(lines.split()[1])
                    self.vertex = readLines[i+1:i+self.numberOfVertices+1]
                    self.vertex = list(map(lambda x:x.strip(),self.vertex))
                    self.vertex = list(map(lambda x:x.split(),self.vertex))
                    self.vertex = list(map(lambda x: [float(i)  for i in x] ,self.vertex))
                if 'Triangles' in lines:
                    self.numberOfTriangles = int(lines.split()[1])
                    self.triangles = readLines[i+1:i+self.numberOfTriangles+1]
                    self.triangles = list(map(lambda x:x.strip(),self.triangles))
                    self.triangles = list(map(lambda x:x.split(),self.triangles))
                    self.triangles = list(map(lambda x: [int(i) for i in x] ,self.triangles))
        self.getNormalVectors()
        

    def getNormalVectors(self):

        self.normalVectors = []
        for triangle in self.triangles:
            # Use numpy array to do sum-wise and cross product
            p1 = np.array((self.vertex[triangle[0]-1]))
            p2 = np.array((self.vertex[triangle[1]-1]))
            p3 = np.array((self.vertex[triangle[2]-1]))

            p1p2 = p1-p2
            p3p2 = p3-p2

            normalVector = np.cross(p1p2,p3p2)
            # Go back to list not np
            self.normalVectors.append(normalVector.tolist())

    def writeSTL(self):
        stlFile = os.path.splitext(self.file)[0] + '.stl'
        with open(stlFile,'w') as stl:
            stl.write("solid ascii\n")
            faceCounter = 0
            for faces in self.triangles:
                # Write face normal vector eliminating '[' ']' and ','
                stl.write(" facet normal {normalVector}\n" .format(normalVector=str(self.normalVectors[faceCounter])\
                    .replace('[','').replace(']','').replace(',',' ')))
                stl.write("  outer loop\n")
                stl.write("   vertex {vertex1}\n" .format(vertex1=str(self.vertex[faces[0]-1])\
                    .replace('[','').replace(']','').replace(',',' ')))
                stl.write("   vertex {vertex2}\n" .format(vertex2=str(self.vertex[faces[1]-1])\
                    .replace('[','').replace(']','').replace(',',' ')))
                stl.write("   vertex {vertex3}\n" .format(vertex3=str(self.vertex[faces[2]-1])\
                    .replace('[','').replace(']','').replace(',',' ')))
                stl.write("  endloop\n")


                stl.write(" endfacet\n")
            stl.write("endsolid ascii")
        
        
                

for files in os.listdir():
    if files.endswith(".surf"):
        
        fileSurf = surf(files)
        fileSurf.writeSTL()

