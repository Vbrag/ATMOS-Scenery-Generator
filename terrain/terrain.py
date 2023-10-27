'''
Created on 24.10.2023

@author: abdel
'''
import requests 
import  gzip 
import struct
import os , math
import numpy as  np


savePath = "C:\\Users\\abdel\\Documents\\OpenStreetMaps\\"

terrainDir  = os.path.join(savePath , "terrain")



def getSrtmIntervals(x1, x2):
    """
    Split (x1, x2) into SRTM intervals. Examples:
    (31.2, 32.7) => [ (31.2, 32), (32, 32.7) ]
    (31.2, 32) => [ (31.2, 32) ]
    """
    _x1 = x1
    intervals = []
    while True:
        _x2 = math.floor(_x1 + 1)
        if (_x2>=x2):
            intervals.append((_x1, x2))
            break
        else:
            intervals.append((_x1, _x2))
            _x1 = _x2
    return intervals


def getHgtFileName(lat, lon):
    
    if lat>= 0:
        prefixLat = "N"  
    else: 
        prefixLat = "S"


    if lon>= 0:
        prefixLon = "E"  
    else :
        prefixLon = "W"       
 
    return "{}{:02d}{}{:03d}.hgt.gz".format(prefixLat, abs(lat), prefixLon, abs(lon))


 
def get_url(lat, lon):
 
    HgtFileName = getHgtFileName(lat, lon)
    
    terrainUrl = "https://s3.amazonaws.com/elevation-tiles-prod/skadi/{}/{}".format(HgtFileName[0:3]  ,HgtFileName )
 
    return terrainUrl
    


def download_url(url, save_path, chunk_size=128):

    print("download : " +  url)
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

 
def get_sample(filename, n, e):
 
    i = 1201 - int(round(n / 3, 0))
    j = int(round(e / 3, 0))
    with open(filename, "rb") as f:
        f.seek(((i - 1) * 1201 + (j - 1)) * 2)  # go to the right spot,
        buf = f.read(2)  # read two bytes and convert them:
        print(buf)
        val = struct.unpack('>h', buf)  # ">h" is a signed two byte integer
        if not val == -32768:  # the not-a-valid-sample value
            return val
        else:
            return None


def gbs_Degrees2Decimal(gps_arrey):
    
    if not isinstance(gps_arrey, list):
        return  gps_arrey
        
    
    if len(gps_arrey)  == 3:
        
        return gps_arrey[0] + gps_arrey[1]/60.0  + gps_arrey[2]/3600.0
        
    elif len(gps_arrey)  == 2:
        
        return gps_arrey[0] + gps_arrey[1]/60.0  
    
    elif len(gps_arrey)  == 1:
         
        return gps_arrey[0]
    else:
         
        return gps_arrey

def gbs_Decimal2Degrees(gps):
    
    Degrees = int(gps)
    Minutes_Seconds =  gps - Degrees
    
    if Minutes_Seconds < 0:
        Minutes_Seconds = -1*Minutes_Seconds
    
    
    Minutes = int(60.0000000000*Minutes_Seconds)
    
    Seconds = int(3600.0*(Minutes_Seconds - Minutes/60.00000000000000000000000000000))
    
    
    
    return [Degrees ,Minutes ,Seconds  ]
    
     





if __name__ == '__main__':
    
    L1 = 8.7455
    L2 = 8.7633
    
    W1 = 51.7145
    W2 = 51.7237   
    
    minLon = min(L1 , L2)
    maxLon = max(L1 , L2)    
    
    minLat = min(W1 , W2)
    maxLat = max(W1 , W2)    
    
     
 
    
 
    latIntervals = list(reversed(getSrtmIntervals( minLat,  maxLat)))
    lonIntervals = getSrtmIntervals(minLon, maxLon)
    
 
    
    vertices = []
    
    # for latInterval in latIntervals:
    #     for lonInterval in lonIntervals:
    #
    #         print(latInterval)
    #         print(lonInterval)
    #         lat = int(latInterval[0])
    #         lon = int(lonInterval[0])
    #         filename  = getHgtFileName(lat, lon)
    #
    #
    #         filepath  = os.path.join(terrainDir , filename)
    #
    #         if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
    #             print("downloading -> " + filename)  
    #             terrainUrl = get_url(lat, lon)     
    #             download_url(url = terrainUrl, save_path =filepath )
    #
    #         # with gzip.open(filepath, "rb") as f:
    #         #     print(1)
    #         #     reslution = 10000.0
    #         #
    #         #     for latitude in np.arange( latInterval[0]  , latInterval[1] ,  1.0/reslution ):    
    #         #
    #         #         for longitude  in np.arange( lonInterval[0]  ,  lonInterval[1] ,  1.0/reslution    ): 
    #         #
    #         #             [latitude_Degrees,latitude_Minute,latitude_Second  ] = gbs_Decimal2Degrees(latitude  )
    #         #             [longitude_Degrees  , longitude_Minute ,longitude_Second   ] = gbs_Decimal2Degrees(longitude  )
    #         #             n = latitude_Minute * 60 + latitude_Second
    #         #             e =  longitude_Minute* 60 + longitude_Second
    #         #
    #         #             i = 1201 - int(round(n / 3, 0))
    #         #             j = int(round(e / 3, 0))
    #         #             f.seek(((i - 1) * 1201 + (j - 1)) * 2)  # go to the right spot,
    #         #             buf = f.read(2)  # read two bytes and convert them:
    #         #
    #         #             val = struct.unpack('>h', buf)[0]  # ">h" is a signed two byte integer
    #         #             if not val == -32768:  # the not-a-valid-sample value
    #         #                 val =  val
    #         #             else:
    #         #                 val = None                                
    #         #
    #         #             vtrx = (gbs_Degrees2Decimal([latitude_Degrees,latitude_Minute,latitude_Second  ])  , gbs_Degrees2Decimal([longitude_Degrees  , longitude_Minute ,longitude_Second   ] ),  val)
    #         #
    #         #             print(vtrx)
    #         #             vertices.append(vtrx)
            
            
    minHeight = 32767
    maxHeight = -32767
    maxLon = 0
    maxLat = 0
    
    vertsCounter = 0
    
    # we have an extra row for the first latitude interval
    firstLatInterval = 1
    
    # initialize the array of vertCounter values
    lonIntervalVertsCounterValues = []
    for lonInterval in lonIntervals:
        lonIntervalVertsCounterValues.append(None)
    
    for latInterval in latIntervals:
        # latitude of the lower-left corner of the SRTM tile
        _lat = math.floor(latInterval[0])
        # vertical indices that limit the active SRTM tile area
        y1 = math.floor( 3600 * (latInterval[0] - _lat) )
        y2 = math.ceil( 3600 * (latInterval[1] - _lat) ) + firstLatInterval - 1
        
        # we have an extra column for the first longitude interval
        firstLonInterval = 1
        
        for lonIntervalIndex,lonInterval in enumerate(lonIntervals):
            # longitude of the lower-left corner of the SRTM tile
            _lon = math.floor(lonInterval[0])
            # horizontal indices that limit the active SRTM tile area
            x1 = math.floor( 3600 * (lonInterval[0] - _lon) ) + 1 - firstLonInterval 
            x2 = math.ceil( 3600 * (lonInterval[1] - _lon) )
            xSize = x2-x1
            
            filename  = getHgtFileName(lat, lon)
    
    
            filepath  = os.path.join(terrainDir , filename)
    
            if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                print("downloading -> " + filename)  
                terrainUrl = get_url(lat, lon)     
                download_url(url = terrainUrl, save_path =filepath )
            
            with gzip.open(srtmFileName, "rb") as f:
                for y in range(y2, y1-1, -1):
                    # set the file object position at y, x1
                    f.seek( 2*((self.size-y)*(self.size+1) + x1) )
                    for x in range(x1, x2+1):
                        lat = _lat + y/self.size
                        lon = _lon + x/self.size
                        xy = self.projection.fromGeographic(lat, lon)
                        # read two bytes and convert them
                        buf = f.read(2)
                        # ">h" is a signed two byte integer
                        z = struct.unpack('>h', buf)[0]
                        if z==self.voidValue:
                            z = self.voidSubstitution
                        if z<minHeight:
                            minHeight = z
                        elif z>maxHeight:
                            maxHeight = z
                            maxLon = lat
                            maxLat = lon
                        # add a new vertex to the verts array
                        verts.append((xy[0], xy[1], z))
                        if not firstLatInterval and y==y2:
                            topNeighborIndex = lonIntervalVertsCounterValues[lonIntervalIndex] + x - x1
                            if x!=x1:
                                if self.primitiveType == "quad":
                                    indices.append((vertsCounter, topNeighborIndex, topNeighborIndex-1, vertsCounter-1))
                                else: # self.primitiveType == "triangle"
                                    indices.append((vertsCounter-1, topNeighborIndex, topNeighborIndex-1))
                                    indices.append((vertsCounter, topNeighborIndex, vertsCounter-1))
                            elif not firstLonInterval:
                                leftNeighborIndex = prevLonIntervalVertsCounter - (y2-y1)*(prevXsize+1)
                                leftTopNeighborIndex = topNeighborIndex-prevYsize*(x2-x1+1)-1
                                if self.primitiveType == "quad":
                                    indices.append((vertsCounter, topNeighborIndex, leftTopNeighborIndex, leftNeighborIndex))
                                else: # self.primitiveType == "triangle"
                                    indices.append((leftNeighborIndex, topNeighborIndex, leftTopNeighborIndex))
                                    indices.append((vertsCounter, topNeighborIndex, leftNeighborIndex))
                        elif not firstLonInterval and x==x1:
                            if y!=y2:
                                leftNeighborIndex = prevLonIntervalVertsCounter - (y-y1)*(prevXsize+1)
                                topNeighborIndex = vertsCounter-xSize-1
                                leftTopNeighborIndex = leftNeighborIndex-prevXsize-1
                                if self.primitiveType == "quad":
                                    indices.append((vertsCounter, topNeighborIndex, leftTopNeighborIndex, leftNeighborIndex))
                                else: # self.primitiveType == "triangle"
                                    indices.append((leftNeighborIndex, topNeighborIndex, leftTopNeighborIndex))
                                    indices.append((vertsCounter, topNeighborIndex, leftNeighborIndex))
                        elif x>x1 and y<y2:
                            topNeighborIndex = vertsCounter-xSize-1
                            leftTopNeighborIndex = vertsCounter-xSize-2
                            if self.primitiveType == "quad":
                                indices.append((vertsCounter, topNeighborIndex, leftTopNeighborIndex, vertsCounter-1))
                            else: # self.primitiveType == "triangle"
                                indices.append((vertsCounter-1, topNeighborIndex, leftTopNeighborIndex))
                                indices.append((vertsCounter, topNeighborIndex, vertsCounter-1))
                        vertsCounter += 1
            
            if firstLonInterval:
                # we don't have an extra column anymore
                firstLonInterval = 0
            # remembering vertsCounter value
            prevLonIntervalVertsCounter = vertsCounter - 1
            lonIntervalVertsCounterValues[lonIntervalIndex] = prevLonIntervalVertsCounter - xSize
            # remembering xSize
            prevXsize = xSize
        if firstLatInterval:
            firstLatInterval = 0
        # remembering ySize
        prevYsize = y2-y1            
            
            
    from mpl_toolkits.mplot3d import Axes3D  
    # Axes3D import has side effects, it enables using projection='3d' in add_subplot
    import matplotlib.pyplot as plt
    import random
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
 
    X = []
    Y= []
    Z= []
    
    for vtrx in vertices:
        X.append(vtrx[0])
        Y.append(vtrx[1])    
        Z.append(vtrx[2])    
    
    ax.plot_trisurf(np.array(X),  np.array(Y) , np.array(Z))
    
    
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    
    plt.show()
    