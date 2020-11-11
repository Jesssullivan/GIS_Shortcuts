import numpy as np # np.array functions and for stl
from PIL import Image # to iterate over a raster
from stl import mesh
from scipy.spatial import distance # calucate pairwise distances
import time # for time eval

timerBegin = time.clock()

file = "sample2.jpeg"
output = "SampleOut.stl"

img = Image.open(file)
loadedPix = img.load()
width, height = img.size

pointCloud = []
# "points"
for w in range(width):
    for h in range(height):
        zvalue = loadedPix[w,h][0]
        pointCloud.append([w,h,zvalue])

points = np.array(pointCloud)

timerpointCloud = time.clock()
print(timerpointCloud - timerBegin, "time elapsed to generate pointCloud")


# "faces" (nearest point) - Computation heavy
D = distance.squareform(distance.pdist(points))

timerPairwise = time.clock()
print(timerPairwise - timerpointCloud, "time elapsed to generate pairwise distances for pointCloud")

# Also a computation heavy process
closest = np.argsort(D)

print("Clostest calcuation is working...")
k = 3
faces = closest[:, 1:k+1]


timerClosest = time.clock()
print(timerPairwise - timerClosest, "time elapsed to sort pairwise distances",
    " by nearest neighbor, ")
# mesh
shape = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        shape.vectors[i][j] = points[f[j],:]

timerShapeForm = time.clock()
print(timerShapeForm - timerPairwise, "time elapsed to mesh triangles")

# Write the mesh to file "cube.stl"
shape.save(output)
