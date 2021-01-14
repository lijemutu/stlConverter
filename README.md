# Avizo to .STL converter 3D models

Given the ASCII Avizo vertex and triangle info it can be converted through the following algorithm

Avizo file:

```
Vertices 304
	6.399997 5.060000 6.949996
	6.399997 5.510000 6.949996 
  ...
  
Triangles 456
  1 2 3
  2 4 3
  4 5 3
  5 6 3
  7 8 2
 ....
  ```
  
  STL ASCII format uses blocks with a normal vector and the vertex on the given face:
  
  ```
  facet normal 0.0019457999999997985  0.0  0.06537689999999999
  outer loop
   vertex 6.109851  6.11  6.933861
   vertex 6.254716  6.56  6.945672
   vertex 6.254716  6.11  6.945672
  endloop
 endfacet
  ```
  
  We just need to compute the normal vector of the given Avizo triangle 
  That is standard finding normal to plane problem and its fully detailed [here](https://web.ma.utexas.edu/users/m408m/Display12-5-4.shtml)
  
 ```
  p1 = np.array((self.vertex[triangle[0]-1]))
  p2 = np.array((self.vertex[triangle[1]-1]))
  p3 = np.array((self.vertex[triangle[2]-1]))

  p1p2 = p1-p2
  p3p2 = p3-p2

  normalVector = np.cross(p1p2,p3p2)
 ```
 
 Then its properyly formatted using .stl ASCII format and print out
