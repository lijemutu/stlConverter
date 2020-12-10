import pyvista

mesh = pyvista.PolyData('E13_inner_wall.stl')
mesh.plot()