import apiworks
import gpsconnect
import serial

#import requests
import webbrowser
import time
#import polyline
from time import sleep
import math
import os.path
from os import path
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface




serial2 = i2c(port=1, address=0x3C)
percent= 48
testtime = "1:10"
pace = "3:30"
segname = 'Walkup'
speed = '14.4'
#substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial2)

    
f = apiworks.api(True)
#f.refresh()
g = gpsconnect.gps()
#f.findSegments((42.2321,-88.3622))
lat,long = g.getall()[0]

mode = 'outseg'
initaltime = time.time()
segtime = 0
lastsegfind = time.time()
nearbySegs = []
currentpath = 0
lastfinish = 0




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
    percent = 100 *  (1.0 * segArray.index(closestLoc)+1)/len(segArray)
    #print(percent)
    return percent


def distanceMiles(dist):
    #print(dist)
    a = math.sqrt(dist)*69.0
    #print(a)
    return a
nearbySegs = f.importStar()

def cT(t):
    out = ''
    out +=(str(int(t/60)))
    out +=(':')
    out +=str(int(t%60))
    return out
while True:

    with canvas(device) as d:  
        #if time.time()-lastsegfind > 5:
            #nearbySegs = f.importStar(g.getll())
            #lastsegfind = time.time()
            #print('latest segs found')
        if mode == 'outseg':
            #print('displaying outseg')
            (lat,lon),speed,sats = g.getall()
            #print(speed)
            #d.text((1,1), "Not on segment", fill = True,spacing = 1)
            d.text((1,1), "Segments tracked: " + str(len(nearbySegs)), fill = True,spacing = 1)
            #d.arc((50,35),start = 0,end=360,outline="white")
            d.text((1,30), "Speed        " +str(speed)+ "mph" , fill=True,spacing = 1)
            d.text((1,20), "Time Riding   " +cT(time.time()-initaltime) , fill=True,spacing = 1)
            d.text((1,40), "Last seg finish " + cT(lastfinish),fill = True,spaceing = 1)
            d.text((1,50),"sats:"+sats,fill =True,spacing = 1)
            #lat,lon = g.getll()
            #print(lat,lon)
            for i in nearbySegs:
                if distanceMiles(squareDistance(i[1],(lat,lon))) < .05:
                    print('on a segment')
                    #print(i)
                    mode = 'inseg'
                    segtime = time.time()
                    segname = i[3]
                    currentpath = i[2]
        if mode =='inseg':
            (lat,lon),speed,sats = g.getall()
            #print(lat,long)
            percent = int(closest(currentpath,(lat,lon)))
            d.rectangle([(1,1),(101,15)],outline = "white")
            d.rectangle([(1,1),(1+percent,15)],fill=True)
            d.text((108,4), str(percent ) + "%", fill=True,spacing = 1)
            d.text((1,17), segname , fill=True,spacing = 1)
            d.text((1,25),    "Time         " + cT(time.time()-segtime) , fill=True,spacing = 1)
            d.text((1,25+10), "Est Finish   " +cT((time.time()-segtime)/(percent*.01)) , fill=True,spacing = 1)
            d.text((1,25+20), "Speed        " +str(speed) , fill=True,spacing = 1)
            d.text((1,55),"sats:"+sats,fill =True,spacing = 1)

            if percent > 95:
                mode = 'outseg'
                lastfinish = time.time()-segtime
                
            

        
