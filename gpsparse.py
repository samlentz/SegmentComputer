import apiworks
import requests
import webbrowser
import pickle
import time
import polyline
import matplotlib.pyplot as plt
import random

#f = apiworks.api()
#f.refresh()
def squareDistance(pt1,pt2):
    x1,y1 = pt1
    x2,y2 = pt2
    return (x2-x1)**2 + (y2-y1)**2

def closest(segArray, point):
    closestLoc = (0,0)
    closestDist = 100000000000
    for i in segArray:
        if(squareDistance(i,point) < closestDist):
            closestLoc = i
            closestDist = squareDistance(i,point)
    percent = 100 * (1 - (1.0 * segArray.index(closestLoc)/len(segArray)))
    return closestLoc,percent
#array = f.getSegment(24430025)
array = [(42.23601, -88.34016), (42.2361, -88.34023), (42.23619, -88.34041), (42.23629, -88.34044), (42.23636, -88.34052), (42.23643, -88.34056), (42.23656, -88.34073), (42.23671, -88.34085), (42.23674, -88.34092), (42.23672, -88.34093), (42.23663, -88.34112), (42.2366, -88.34114), (42.23646, -88.34136), (42.23647, -88.34141), (42.23641, -88.34151), (42.23636, -88.34163), (42.23625, -88.342), (42.23614, -88.34208), (42.23607, -88.34217), (42.23603, -88.34228), (42.23606, -88.3423), (42.23606, -88.34241), (42.23609, -88.34251), (42.23614, -88.34256), (42.23633, -88.34262), (42.23635, -88.34267), (42.23642, -88.34275), (42.23647, -88.34277), (42.23643, -88.34283), (42.23647, -88.34288), (42.23661, -88.34299), (42.2367, -88.3431), (42.23673, -88.34314), (42.23676, -88.34324), (42.23676, -88.34338), (42.2367, -88.34353), (42.23669, -88.3436), (42.23655, -88.34369), (42.23654, -88.34374), (42.2365, -88.34379), (42.2365, -88.34391), (42.23647, -88.34394), (42.23648, -88.34403), (42.23626, -88.34456), (42.23629, -88.34466), (42.23642, -88.34492), (42.23646, -88.34495), (42.23663, -88.34512), (42.2369, -88.34527), (42.23699, -88.34538), (42.23695, -88.34542), (42.23706, -88.34545), (42.2371, -88.34549), (42.23714, -88.34554), (42.23715, -88.34559), (42.23733, -88.34568), (42.23729, -88.34585), (42.23725, -88.34591), (42.23724, -88.34623), (42.2372, -88.34646), (42.2372, -88.34658), (42.23723, -88.34676), (42.23723, -88.34723), (42.23722, -88.34745), (42.2372, -88.3475), (42.23725, -88.34755), (42.23723, -88.34771), (42.23718, -88.34781), (42.23717, -88.34802)]
print(array)
lats= []
longs= []
noiselats = []
noiselongs = []
noisepts = []
count = 0
for i in array:
    x,y = i
    lats.append(x)
    longs.append(y)
    if count%5 == 0:
        x = x+(random.random()*.0001) - .00005
        y = y+(random.random()*.0001)- .00005
        noiselats.append(x)
        noiselongs.append(y)
        noisepts.append((x,y))
    count+=1

fig, ax = plt.subplots()
ax.plot(lats,longs)
ax.plot(noiselats,noiselongs)
print(noisepts[1])
for i in noisepts:
    z,percent = closest(array,i)
    x,y=z
    ax.plot(x,y,marker = 'o')
    ax.annotate(str(int(percent)),(x,y))
ax.set_aspect('equal')
plt.show()
