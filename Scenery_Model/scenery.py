'''
Created on 03.11.2023

@author: abdel
'''

from OSM_Interface import  osm_map as  osm_map

from OpenDRIVE_1_7_0 import  opendrive_17 as  opendrive
import os #, math
import ctypes, sys
#from pyproj import CRS, Transformer
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon , Rectangle
import matplotlib as mpl
import numpy as np
from math import isclose 
import random
 
import copy
from pickle import NONE
 

projection_fromGeographic_cash = dict()
clear = lambda: os.system('cls')


# def define_circle(p1, p2, p3):
#
#
#
#
#
#     x_start, y_start = p1
#     x_midel, y_midel = p2          
#     x_end  , y_end   = p3   
#
#     deltax1 = x_midel - x_start
#     deltax2 = x_end   - x_midel     
#
#     deltay1 = y_midel - y_start
#     deltay2 = y_end   - y_midel             
#
#
#
#
#
#     if deltax1  == 0:
#
#         if  deltay1 > 0:
#             hdg1 = np.pi/2
#         else:
#             hdg1 = -np.pi/2                    
#
#     else:
#
#         hdg1 =  np.arctan2( deltay1 ,deltax1 )
#
#
#     if deltax2  == 0:
#
#         if  deltay2 > 0:
#             hdg2 = np.pi/2
#         else:
#             hdg2 = -np.pi/2                    
#
#     else:
#
#         hdg2 =  np.arctan2( deltay2 ,deltax2 )    
#
#
#
#
#     temp = p2[0] * p2[0] + p2[1] * p2[1]
#     bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
#     cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
#     det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
#
#     if abs(det) < 1.0e-6:
#         return ((None,None), np.inf)
#
#     # Center of circle
#     cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
#     cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
#
#     radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
#
#     if hdg2 >hdg1     :
#
#         radius = -1.0 *radius
#         ###print(radius)    
#
#     return ((cx, cy), radius)
#
#
# # def spiral_interp_centre(distance, x, y, hdg, length, curvEnd):
# #     '''Interpolate for a spiral centred on the origin'''
# #     # s doesn't seem to be needed...
# #     theta = hdg                    # Angle of the start of the curve
# #     Ltot = length                  # Length of curve
# #     Rend = 1 / curvEnd             # Radius of curvature at end of spiral
# #
# #     # Rescale, compute and unscale
# #     a = 1 / np.sqrt(2 * Ltot * Rend)  # Scale factor
# #     distance_scaled = distance * a # Distance along normalised spiral
# #     deltay_scaled, deltax_scaled = fresnel(distance_scaled)
# #     deltax = deltax_scaled / a
# #     deltay = deltay_scaled / a
# #
# #     # deltax and deltay give coordinates for theta=0
# #     deltax_rot = deltax * np.cos(theta) - deltay * np.sin(theta)
# #     deltay_rot = deltax * np.sin(theta) + deltay * np.cos(theta)
# #
# #     # Spiral is relative to the starting coordinates
# #     xcoord = x + deltax_rot
# #     ycoord = y + deltay_rot
# #
# #     return xcoord, ycoord
#
#
# #import math
#
# # import matplotlib.pyplot as plt
# # import numpy as np
#
# def arcLength(XY):
#     return np.sum(np.hypot(np.diff(XY[:, 0]), np.diff(XY[:, 1])))
#
# def getAreaOfTriangle(XY, i, j, k):
#     xa, ya = XY[i, 0], XY[i, 1]
#     xb, yb = XY[j, 0], XY[j, 1]
#     xc, yc = XY[k, 0], XY[k, 1]
#     return abs((xa * (yb - yc) + xb * (yc - ya) + xc * (ya - yb)) / 2)
#
# def distance(XY, i, j):
#     return np.linalg.norm(XY[i, :] - XY[j, :])
#
# def getCurvatureUsingTriangle(XY, i, j, k):
#     fAreaOfTriangle = getAreaOfTriangle(XY, i, j, k)
#     AB = distance(XY, i, j)
#     BC = distance(XY, j, k)
#     CA = distance(XY, k, i)
#     fKappa = 4 * fAreaOfTriangle / (AB * BC * CA)
#     return fKappa
#
# def spiral_interp_centre(distances, arcLength, x_i, y_i, yaw_i, curvEnd ):
#     '''
#     :param arcLength: Desired length of the spiral
#     :param x_i: x-coordinate of initial point
#     :param y_i: y-coordinate of initial point
#     :param yaw_i: Initial yaw angle in radians
#     :param curvEnd: Curvature at the end of the curve.
#     :return:
#     '''
#     # Curvature along the Euler spiral is pi*t where t is the Fresnel integral limit.
#     # curvEnd = 1/R
#     # s = arcLength
#     # t = Fresnel integral limit
#     # Scalar a is used to find t such that (1/(a*R) = pi*t) and (a*s = t)
#     # ====> 1/(pi*a*R) = a*s
#     # ====> a^a*(pi*s*R)
#     # ====> a = 1/sqrt(pi*s*R)
#     # To achieve a specific curvature at a specific arc length, we must scale
#     # the Fresnel integration limit
#     scalar = np.pi
#     #distances = np.linspace(start=0.0, stop=arcLength, num=N)
#     R = np.abs( 1 / curvEnd ) # Radius of curvature at end of spiral
#     # Rescale, compute and unscale
#     a = 1 / np.sqrt(scalar *  arcLength  * R  +   np.finfo(float).eps) # Scale factor
#     scaled_distances = a * distances # Distance along normalized spiral
#     dy_scaled, dx_scaled = scipy.special.fresnel(scaled_distances)
#
#     dx = dx_scaled / a
#     dy = np.sign(curvEnd)* dy_scaled / a
#
#     # Rotate the whole curve by yaw_i
#     dx_rot = dx * np.cos(yaw_i) - dy * np.sin(yaw_i)
#     dy_rot = dx * np.sin(yaw_i) + dy * np.cos(yaw_i)
#
#     # Translate to (x_i, y_i)
#     x = x_i + dx_rot
#     y = y_i + dy_rot
#     return np.concatenate((x[:, np.newaxis], y[:, np.newaxis]), axis=1)

 

def projection_fromGeographic(latitude, longitude, referenceLat = 0 , referenceLon = 0):

 
        # crs_4326  = CRS.from_epsg(4326) # epsg 4326 is wgs84
        #
        # uproj = CRS.from_proj4("+proj=tmerc +lat_0={0} +lon_0={1} +x_0=0 +y_0=0 +ellps=GRS80 +units=m".format(referenceLat, referenceLon))
        # transformer = Transformer.from_crs(crs_4326, uproj)
        #
        # x,y = next(transformer.itransform([(latitude,longitude)]))
        #
        #     # radius = 6378137
    
    # see conversion formulas at
    # http://en.wikipedia.org/wiki/Transverse_Mercator_projection
    # and
    # http://mathworld.wolfram.com/MercatorProjection.html
     
    radius = 6378137
    k = 1
    
    self_lon =   referenceLon
    self_lat =   referenceLat
    self_latInRadians = np.radians(self_lat)
    lat = np.radians(latitude)
    lon = np.radians(longitude-self_lon)
    B = np.sin(lon) * np.cos(lat)
    x = 0.5 * k * radius * np.log((1+B)/(1-B))
    y = k * radius * ( np.arctan2(np.tan(lat),np.cos(lon)) - self_latInRadians )
    
    
    return (x,y)

class StraightLine():
    
 
    
    def __init__(self,    length=1):
        
 
        self.length = length
        
 
                 
    def XY2ST(self, x0 , y0 ,hdg , X , Y ,S0):
        
 
        
        deltaX= np.array(X - x0 ).astype(float)
        deltaY= np.array(Y - y0 ).astype(float)        
        S = deltaX * np.cos(2*np.pi-hdg) - deltaY * np.sin(2*np.pi-hdg) + S0
        T = deltaX * np.sin(2*np.pi-hdg) + deltaY * np.cos(2*np.pi-hdg)
         
             
        return  (S,T)               
        
        
        
        

 
    
    def ST2XY(self, x0 , y0 ,hdg,  S , S0 , T):
        
 
            
        delta_s = S - S0
        
        if delta_s > self.length:
            return (None ,None)
        
        else: 
 
                     
            deltaS= np.array(S - S0 ).astype(float)
            deltaT= np.array(T - 0 ).astype(float)        
            x = deltaS * np.cos( hdg) - deltaT * np.sin( hdg) + x0
            y = deltaS * np.sin( hdg) + deltaT * np.cos( hdg) + y0    
            
            return (x , y) 
 
    
    
    def get_endPoint(self, x0 , y0 ,hdg):
 
        
        x_end = x0 + self.length* np.cos( hdg)
        y_end = y0 + self.length* np.sin( hdg)        
        hdg_end = hdg
    
        return (x_end ,y_end , hdg_end )
     
class Spiral():

 


    
    def __init__(self, length=1 , CurvaturStart = 1 ,  CurvaturEnd = 1 ):
        
        self.length =length
        self.CurvaturStart = CurvaturStart
        self.CurvaturEnd = CurvaturEnd
        self._gamma = 1.0 * (-1*CurvaturEnd - -1*CurvaturStart) / length
        



    @classmethod
    def _calc(cls,gamma, s, x0=0, y0=0, kappa0=0, theta0=0 ):

 

        # Start
        C0 = x0 + 1j * y0
        
        kappa0 = -1*kappa0

        if gamma== 0 and kappa0 == 0:
            # Straight line
            Cs = C0 + np.exp(1j * theta0) * s

        elif gamma == 0 and kappa0 != 0:
            # Arc
            Cs = C0 + np.exp(1j * theta0) / kappa0 * (np.sin(kappa0 * s) + 1j * (1 - np.cos(kappa0 * s)))

        else:
            # Fresnel integrals
            Sa, Ca = fresnel((kappa0 + gamma * s) / np.sqrt(np.pi * np.abs(gamma)))
            Sb, Cb = fresnel(kappa0 / np.sqrt(np.pi * np.abs(gamma)))

            # Euler Spiral
            Cs1 = np.sqrt(np.pi / np.abs(gamma)) * np.exp(1j * (theta0 - kappa0**2 / 2 / gamma))
            Cs2 = np.sign(gamma) * (Ca - Cb) + 1j * Sa - 1j * Sb

            Cs = C0 + Cs1 * Cs2

        # Tangent at each point
        theta = gamma * s**2 / 2 + kappa0 * s + theta0

        return (Cs.real, Cs.imag, theta)
 
    def ST2XY(self, x0 , y0 ,hdg, S ,S0 ,T):
        
 
        
        theta0 = hdg  
 
        delta_s = S - S0 


        if delta_s > self.length:
            return (None ,None)
        
        else: 
        
            kappa0 = self.CurvaturStart
               
            xs , ys , hed = Spiral._calc(self._gamma, delta_s, x0, y0, kappa0, theta0)
     
     
            xs = xs + T*np.sin(np.pi  - hed )
            ys = ys + T*np.cos(np.pi  - hed )
               
            
            return (xs , ys) 
        
 

 
    
    def get_endPoint(self, x0 , y0 ,hdg):

 
        theta0 = hdg
        
        delta_s = self.length 
        
        kappa0 = self.CurvaturStart
           
        x_end ,y_end , hdg_end  = Spiral._calc(self._gamma,delta_s, x0, y0, kappa0, theta0)
         
    
        return (x_end ,y_end , hdg_end )
        
 
    def XY2ST(self, x0 , y0 ,hdg , X ,Y, S0):
 
 
        theta0 = hdg  
 
 
        
        kappa0 = self.CurvaturStart
        
        
        S_soll = 0
        T  = 1000000000000000000
        
        
        for delta_s in np.arange(0,self.length, 0.01):
           
            xs , ys , _ = self._calc(delta_s, x0, y0, kappa0, theta0)
            
            
            deltaX= np.array(X - xs ).astype(float)
            deltaY= np.array(Y - ys ).astype(float)
            L = np.sqrt(  deltaX * deltaX    + deltaY *deltaY  )
            
            if L < T:
                S_soll = delta_s
                T = L
                
                          
        
        
        if S_soll > self.length :
        
            return (None,None)  
              
        else:        
 
                
            S =  S_soll + S0
     
            return (S,T)

class Arc():
 
    
    def __init__(self, length=1 , Curvatur = 1 ):
        
        self.length =length
        self.Curvatur = Curvatur
 
    def ST2XY(self, x0 , y0 ,hdg, S ,S0 ,T):

 
        ##print("============= ST2XY")
        
        Radius = 1.0/ (self.Curvatur )
        
        ##print("Radius ", Radius )
        Radius_abs = np.abs(Radius)
        ##print("Radius ", Radius_abs )
        x_center = 0
        y_center = Radius_abs
        
        delta_s = S - S0 

        if delta_s > self.length:
            return (None ,None)
        
        else: 
        
            ##print("delta_s ", delta_s )
            
            theta =  delta_s /  Radius_abs 
            
            ##print("theta ", theta )
    
    
            deltax =  x_center  +  Radius_abs*np.sin(  theta )    
            deltay =  y_center  -  Radius_abs*np.cos(  theta ) 
    
            
     
            
            if   Radius > 0 :
                 
                hdg_end =    hdg + theta 
                  
            else:
                deltay  = - deltay 
                hdg_end =  hdg - theta 
    
 
    
            # deltax and deltay give coordinates for theta=0
            deltax_rot = deltax * np.cos(hdg) - deltay * np.sin(hdg)
            deltay_rot = deltax * np.sin(hdg) + deltay * np.cos(hdg)
    
 
        
            # Spiral is relative to the starting coordinates
            xs = x0 + deltax_rot
            ys = y0 + deltay_rot
     
 
                
            xs = xs - T*np.sin(   hdg_end )
            ys = ys + T*np.cos(   hdg_end )     
               
 
            return (xs , ys) 
    
    def get_endPoint(self, x0 , y0 ,hdg):

 
        Radius = 1.0/ (self.Curvatur )
        
 
        Radius_abs = np.abs(Radius)
 
        x_center = 0
        y_center = Radius_abs
        
        delta_s = self.length
        
 
        
        theta =  delta_s /  Radius_abs 
 
        deltax =  x_center  +  Radius_abs*np.sin(  theta )    
        deltay =  y_center  -  Radius_abs*np.cos(  theta ) 

        
 
        if   Radius > 0 :
             
            hdg_end =    hdg + theta 
              
        else:
            deltay  = - deltay 
            hdg_end =  hdg - theta        


 
        # deltax and deltay give coordinates for theta=0
        deltax_rot = deltax * np.cos(hdg) - deltay * np.sin(hdg)
        deltay_rot = deltax * np.sin(hdg) + deltay * np.cos(hdg)

 
        # Spiral is relative to the starting coordinates
        xs = x0 + deltax_rot
        ys = y0 + deltay_rot
 
 
        x_end = xs  
        y_end = ys   

  


        if hdg_end < 0:
            hdg_end = np.pi*2 + hdg_end
            
        ##print("theta"  ,theta)
        if   hdg_end >=  2*np.pi:   
            hdg_end  = hdg_end - int(hdg_end/(2*np.pi) ) *2*np.pi  
        
 
        return (x_end ,y_end , hdg_end )
        
 
    def XY2ST(self, x0 , y0 ,hdg , X ,Y, S0):
 
        Radius = 1.0/ (self.Curvatur  )
        
 
        
        deltaX=  np.array(X - x0 ).astype(float) 
        deltaY=  np.array(Y - y0 ).astype(float) 
        
 
        deltax_rot = deltaX * np.cos(2*np.pi- hdg) - deltaY * np.sin( 2*np.pi - hdg)
        deltay_rot = deltaX * np.sin(2*np.pi- hdg) + deltaY * np.cos( 2*np.pi - hdg)

 
        Radius_abs = np.abs(Radius)
        x_center = 0
        y_center = Radius#Radius_abs       
 

        deltaXPointCenter= np.array( deltax_rot - x_center ).astype(float)
        deltaYPointCenter= np.array( deltay_rot - y_center ).astype(float)
        
 
        L = np.sqrt(  deltaXPointCenter * deltaXPointCenter    + deltaYPointCenter *deltaYPointCenter  )  

 
        
        if Radius > 0:
            if deltaXPointCenter  == 0:
            
                if  deltaYPointCenter > 0:
                    theta = np.pi/2
                else:
                    theta = 2*np.pi-np.pi/2                    
            
            else:
            
                theta  =    np.arctan2( deltaYPointCenter,deltaXPointCenter   )          
            ##print("theta"  ,theta)  
            theta = np.pi/2 + theta
        else:
            if deltaYPointCenter  == 0:
            
                if  deltaXPointCenter > 0:
                    theta = np.pi/2
                else:
                    theta = 2*np.pi-np.pi/2                    
            
            else:
            
                theta  =  np.arctan2( deltaXPointCenter , deltaYPointCenter    )      
 
        if theta < 0:
            theta = np.pi*2 + theta
 
        if   theta >=  2*np.pi:   
            theta  = theta - int(theta/(2*np.pi) ) *2*np.pi        
 
        
        
        L_circl = np.abs(  theta )  *Radius_abs
        
        if L_circl > self.length :
        
            return (None,None)  
              
        else:
 
            
            S =  L_circl + S0
            
 
            if Radius >   0:                     
                T =    Radius_abs - L  
            else:
                T =    L  - Radius_abs  
                     
 
     
            return (S,T)

class RoadReferenceLine():

    @classmethod  
    def Connect3points(cls, x_start ,y_start , x_midel ,y_midel ,x_end ,y_end , R  ): 
        
        
        deltax0 = x_midel - x_start
        deltay0 = y_midel - y_start
        
        
        if deltax0  == 0:
        
            if  deltay0 > 0:
                hdg0 = np.pi/2
            else:
                hdg0 = 2*np.pi-np.pi/2                    
        
        else:
        
            hdg0 =  np.arctan2( deltay0 ,deltax0 )
                    
        
        deltax1 = x_end - x_midel
        deltay1 = y_end - y_midel
        
        
        if deltax1  == 0:
        
            if  deltay1 > 0:
                hdg1 = np.pi/2
            else:
                hdg1 = 2*np.pi -np.pi/2                    
        
        else:
        
            hdg1 =  np.arctan2( deltay1 ,deltax1 ) 
            
            
            
 
        
        if  isclose(hdg0, hdg1, abs_tol=1e-6)   : #  or   or 
            
            deltax = x_end - x_start
            deltay = y_end - y_start   
            
            length = np.sqrt( deltax*deltax   +  deltay *deltay  ) 
            ref = RoadReferenceLine( x0= x_start, y0 = y_start, hdg = hdg0, geometry_elements = [StraightLine(length) ])
            #line
 

        
        
        else:
            
            ref = RoadReferenceLine( x0= x_start, y0 = y_start, hdg = hdg0, geometry_elements = [])
            
            #arc
            length1 = np.sqrt( deltax0*deltax0   +  deltay0*deltay0  ) 
            length2 = np.sqrt( deltax1*deltax1   +  deltay1*deltay1  ) 
            #referenceLine.addStraightLine(length) 
            

            
            
            dist_inarc = min(R ,length1/5) 
            dist_inarc = min(dist_inarc ,length2/5)             
  
 
            
            length1 = length1 - dist_inarc
            length2 = length2 - dist_inarc            
            
 
            ref.addStraightLine(length1)                
            
            x0 , y0 , hdg0 = ref.get_endPoint()
            x_arc_start = x0
            y_arc_start = y0
            hed_arc_start = hdg0

            
            x_arc_End = x_midel + dist_inarc * np.cos(hdg1)
            y_arc_End = y_midel + dist_inarc * np.sin(hdg1)
            hed_arc_end= hdg1
            
            
 
            alfa =   np.pi/2  - hed_arc_start
            theta =  hed_arc_start - hed_arc_end  
            
 
            
            arc_Radius =   (x_arc_End - x_arc_start)/ ( np.sin( np.pi- hed_arc_start) +  np.cos(np.pi - alfa -theta ) ) 
        
            
 
            
            arc_length =  np.abs( theta  * arc_Radius  ) 
            
 
 
            ref.addArc(arc_length  , 1.0/- arc_Radius)
 
            ref.set_endPoint(x_arc_End, y_arc_End)
 
            ref.addStraightLine(length2)

                 
        
        return ref
  
    
    @classmethod  
    def fitRoadReferenceLine(cls, points ,x0 = None, y0 =None , hdg = None   ):
    
        
 
        x0_start = x0
        y0_start = y0        
        
        points = copy.deepcopy(points)
 
    
        if x0 is None or y0 is None:
            x0, y0 = points[0]
            x0_start = x0
            y0_start = y0
        
    
                    
        if len(points) < 2:
            
            geometry_elements =[]
            
            if hdg is None:
                hdg_start = 0
            
            else:
                hdg_start = hdg                
            return RoadReferenceLine(x0_start, y0_start, hdg_start, geometry_elements)    
 
        x1, y1 = points[1] 
    
    
        deltax = x1 -  x0_start
        deltay = y1 -  y0_start     
    
        if hdg is None:
            if deltax  == 0   :
    
                if  deltay > 0:
                    hdg = np.pi/2
                else:
                    hdg = 2*np.pi-np.pi/2                    
    
            else:
    
                hdg =  np.arctan2( deltay ,deltax ) 
    
        hdg_start = hdg
    
 
        geometry_elements =[]
    
    
        referenceLine = RoadReferenceLine(x0_start, y0_start, hdg_start, geometry_elements)
 

 
    
        for Point_index in range(0 , len(points),1):
 
            point_End = points[Point_index]
 
            x_end  , y_end   = point_End 

            ###print(Point_index)
            
            referenceLine.add_New_Point(x_end, y_end)
    
            referenceLine.set_endPoint(x_end, y_end)

                      
            
 
                
                

        endpoint = points[-1] 
        x_end  , y_end   = endpoint
        #referenceLine.cleanUp()
        referenceLine.set_endPoint(x_end, y_end)
        
        return referenceLine
            
 
    
    def __init__(self, x0=0, y0=0 , hdg  = 0 , geometry_elements = list() ):
        
        self.x0 = x0 
        self.y0 = y0
        self.hdg = hdg
        self.geometry_elements = geometry_elements
        
    
 
        
    
    def addStraightLine(self, length):
 
  
        if length > 0: 
        
            if len(self.geometry_elements )  ==0:
                self.geometry_elements.append(StraightLine(length)) 
                
            elif  isinstance(self.geometry_elements[-1], Arc):
 
                newline = StraightLine(length)
                
                self.geometry_elements.append(newline) 
                
     
                
            else:
                self.geometry_elements[-1].length  = self.geometry_elements[-1].length + length 
                        


    def addArc(self, length, Curvatur ):
        
        #Radius = 1.0/ (self.Curvatur +  np.finfo(float).eps)
        
        if length > 0 and Curvatur != np.nan and Curvatur != np.inf  :
        
            if len(self.geometry_elements )  ==0:
                self.geometry_elements.append(Arc(length, Curvatur) ) 
                
            elif not isinstance(self.geometry_elements[-1], Arc):
                
                
                self.geometry_elements.append(Arc(length, Curvatur)) 
            
            elif not    isclose(self.geometry_elements[-1].Curvatur, Curvatur, abs_tol=1e-5)  :
                self.geometry_elements.append(Arc(length, Curvatur))  
                
            elif Curvatur == 0:
                
                self.addStraightLine(length)
             
            else:
                self.geometry_elements[-1].length  = self.geometry_elements[-1].length + length 
            
            
    def addSpiral(self, length, CurvaturEnd):
 
 
        if length > 0: 
       
            if len(self.geometry_elements )  == 0   :
                self.geometry_elements.append(Spiral(length  = length, CurvaturStart  = 0, CurvaturEnd = CurvaturEnd))         
            
            elif isinstance(self.geometry_elements[-1], StraightLine):
            
                self.geometry_elements.append(Spiral(length  = length, CurvaturStart  = 0, CurvaturEnd = CurvaturEnd))       
                
            elif isinstance(self.geometry_elements[-1], Arc):
                CurvaturStart =   self.geometry_elements[-1].Curvatur
                self.geometry_elements.append(Spiral(length  = length, CurvaturStart  = CurvaturStart, CurvaturEnd = CurvaturEnd))                    
     
            elif isinstance(self.geometry_elements[-1], Spiral):
                CurvaturStart =   self.geometry_elements[-1].CurvaturEnd
                self.geometry_elements.append(Spiral(length  = length, CurvaturStart  = CurvaturStart, CurvaturEnd = CurvaturEnd)) 
     
    
    
    def add_New_Point(self , x_end , y_end):
    
 
        
        
        x0 , y0 , _  = self.get_endPoint() 
        
        #point_0 = (x0 ,y0)
        point_start =   (x0 , y0)
        point_End   =   (x_end , y_end)#points[index_1]
        
 
        
        
        x_start, y_start = point_start
        
        self.set_endPoint(x_start, y_start)
        
        x0 , y0 , hdg0  = self.get_endPoint()    
        
        
        x_end  , y_end   = point_End  
        
        
        
        deltax1 = x_end - x_start
        deltay1 = y_end - y_start
        
        
        if deltax1  == 0:
        
            if  deltay1 > 0:
                hdg1 = np.pi/2
            elif deltay1 < 0 :
                hdg1 = 2*np.pi-np.pi/2
            else:
                return                    
        
        else:
        
            hdg1 =  np.arctan2( deltay1 ,deltax1 ) 
            
 
 
        if  hdg0 < 0:
            hdg0 = hdg0 + 2*np.pi
            
                       
        if  hdg1 < 0:
            hdg1 = hdg1 + 2*np.pi
        
        
        if  isclose(hdg0, hdg1, abs_tol=1e-3)   : #  or   or 
            #line
            length = np.sqrt( deltax1*deltax1   +  deltay1 *deltay1  ) 
            self.addStraightLine(length) 
        
        
        
        else:
            
 
            
            
            x_midel = x0
            y_midel = y0

            last_ele = self.geometry_elements[-1]
            self.geometry_elements.remove(last_ele)
            
            x_start , y_start , hdg0  = self.get_endPoint()
            
                        
            refnew = RoadReferenceLine.Connect3points(x_start, y_start, x_midel, y_midel, x_end, y_end, R = 10 )
            
            self.geometry_elements = self.geometry_elements + refnew.geometry_elements
            self.set_endPoint(x_end, y_end)
 

 
    
    # def cleanUp(self):
    #
    #     indexList = []
    #     if len(self.geometry_elements )  >1:
    #         for index , ele in enumerate(self.geometry_elements ):
    #             if ele.length < 1:
    #                 indexList.append(index)
    #
    #     for index in indexList:
    #
    #         ele =  self.geometry_elements[index]
    #         if index >0:
    #             self.geometry_elements[index-1].length = self.geometry_elements[index-1].length  + ele.length
    #         else:
    #             self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length                    
    #     indexList.reverse()
    #     for index in indexList :
    #         ele =  self.geometry_elements[index]
    #         self.geometry_elements.remove(ele)
    #
    #
    #     indexList = []
    #     if len(self.geometry_elements )  >1:
    #         for index , ele in enumerate(self.geometry_elements[:-1] ):
    #             if  type(ele) == type(self.geometry_elements[index +1]):
    #                 indexList.append(index)
    #
    #
    #
    #     indexList_toremove = []
    #     for index in indexList:
    #
    #         ele =  self.geometry_elements[index]
    #
    #         if isinstance(ele, StraightLine):
    #             self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length 
    #             indexList_toremove.append(index)                
    #
    #             if  isclose(0 , ele.length, abs_tol=1e-3): 
    #                 indexList_toremove.append(index)  
    #
    #         elif isinstance(ele, Arc):
    #             if isclose(self.geometry_elements[index+1].Radius, ele.Radius, abs_tol=1e-1):
    #                 self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length 
    #
    #                 indexList_toremove.append(index)            
    #
    #             elif  isclose(0 , ele.Radius, abs_tol=1e-3): 
    #                 indexList_toremove.append(index)  
    #
    #             elif  isclose(0 , ele.length, abs_tol=1e-3): 
    #                 indexList_toremove.append(index)                                      
    #
    #
    #     indexList_toremove = list(set(indexList_toremove))            
    #     indexList_toremove.sort()
    #     indexList_toremove.reverse()
    #
    #
    #     if len(indexList_toremove) < len(self.geometry_elements):
    #
    #         for index in indexList_toremove :
    #             ele =  self.geometry_elements[index]
    #             self.geometry_elements.remove(ele)
    #
    #     else:
    #         self.addStraightLine(1)
            
                        
    
    def getLength(self):
        
        length  =0
        for ele in self.geometry_elements:
            length = length+ ele.length
            
        return length
             
    def get_endPoint(self):

        x0 = self.x0
        y0 = self.y0
        hdg =self.hdg         
 
        
        if len(self.geometry_elements) != 0:
            
            for ele in self.geometry_elements:
            
                x0 , y0 , hdg = ele.get_endPoint(x0 , y0 ,hdg)
            
 
            
        return x0 , y0 , hdg 
 
 
    def set_endPoint(self , X_end ,Y_end):
        
        (S,_) = self.XY2ST(X_end ,Y_end)
        
 
            
        if S is not None:   
        
            
            S0 = 0
             
            indextoremove = []
            index = 0
            
            allextra = False
            
            if len(self.geometry_elements ) > 1:
                for ele in self.geometry_elements[:-1]:
                    index = index +1 
                    if S0 + ele.length < S and not allextra:
                        
                        S0 = S0 + ele.length
                        
                    else:
                        indextoremove.append(index)
                        allextra = True
                        
                    
                    
                    
            
            ###print( S  )
            indextoremove.sort()
            indextoremove.reverse()
            for index in indextoremove:
                self.geometry_elements.remove(self.geometry_elements[index])
            
        
            if S is not None and len(self.geometry_elements ) >= 1 and  (S - S0 ) > 0:
                
                
                self.geometry_elements[-1].length = S - S0               
        
        
        
    def set_startPoint(self , xstart , ystart):
        
        geometry_elements_save = copy.deepcopy(self.geometry_elements ) 
        
        self.set_endPoint(xstart, ystart)
        
        xstrat , ystrat ,hed_start = self.get_endPoint()
        
        if len(self.geometry_elements) > 1:
            geometry_elements_save = geometry_elements_save[len(self.geometry_elements)-1: ]
        
        
        if len(self.geometry_elements) >= 1:    
            geometry_elements_save[0].length = geometry_elements_save[0].length - self.geometry_elements[-1].length
            
 
        self.x0 = xstrat
        self.y0 = ystrat 
        self.hdg = hed_start
               
        self.geometry_elements =   geometry_elements_save  
    
    def ST2XY(self, S ,T):

        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
        S0 = 0
        
        ele = None
        
        for ele in self.geometry_elements:
            
            if S - S0 <= ele.length:
                
                return ele.ST2XY(  x0 , y0 , hdg ,  S ,S0,T )
            
            else:
                
                x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )
                
                S0 = S0 + ele.length
            
        
        
        #x_end , y_end , hdg  = self.get_endPoint()
        
        
        if ele is not None:
        
            return ele.ST2XY(  x0 , y0 , hdg ,  S ,S0,T )
        
        else:
            return (S,T)
        
        
        
 
 
        
    def XY2ST(self, X , Y):
    
        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
    
        S0 = 0
        
        S_list =[]
        T_list =[]  
        
        if len(self.geometry_elements) >1:
            self.geometry_elements[-1].length = self.geometry_elements[-1].length*1.01
            
        
              
        for ele in self.geometry_elements:
            
 
            try:
                (S,T)= ele.XY2ST(  x0 , y0 ,hdg , X ,Y, S0)
            except:
                S = None
                T = None
            
            if  S is not None and S > 0:
            
                if (S >= 0)  and (S-S0) < ele.length:
                    S_list.append(S)
                    T_list.append(np.abs( T ))           
    
            x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )

            S0 = S0 + ele.length
 
 
        if len(self.geometry_elements) >1:
            self.geometry_elements[-1].length = self.geometry_elements[-1].length/1.01
 
        
        # ##print(S_list)
        # ##print(T_list)
        if len(T_list) >0:
            indexMinT = np.argmin(T_list)
     
            T =  T_list[indexMinT]   
            S =  S_list[indexMinT]
        
     
            return (S,T)
        # elif len(self.geometry_elements) > 0:
        #
        #     return (S,T)
        #

            
        else:
 
            return (None , None)
      
      
      
    def export2opendrive(self):
        

        geometry = []
        
        hdg = self.hdg
        s = 0
        x = self.x0
        y = self.y0
        for geo_ele in self.geometry_elements:
            
            length = geo_ele.length
            
            if isinstance(geo_ele, StraightLine):
            
                           
                
                geometry.append(opendrive.t_road_planView_geometry(hdg, length, s, x, y, line = opendrive.t_road_planView_geometry_line()) ) 
            
            elif  isinstance(geo_ele, Arc):
                
                curvature = geo_ele.Curvatur
                geometry.append(opendrive.t_road_planView_geometry(hdg, length, s, x, y,   arc = opendrive.t_road_planView_geometry_arc(curvature )) ) 
                
            elif isinstance(geo_ele, Spiral):
                
                curvStart = geo_ele.CurvaturStart
                curvEnd = geo_ele.CurvaturEnd
                geometry.append(opendrive.t_road_planView_geometry(hdg, length, s, x, y,   spiral= opendrive.t_road_planView_geometry_spiral(curvEnd, curvStart) ) ) 
                          
 
            s = s +   length
            
            x , y , hdg  =  geo_ele.get_endPoint(  x , y ,hdg)   
        
        planView = opendrive.t_road_planView(geometry )
        
        return planView

class RoadObject():

    @classmethod
    def fromOSMdict(cls, dictobj  ):
        pass

    def __init__(self ,  Floor_plan =list() , tags = dict() ):
        
        #
        self.Floor_plan = Floor_plan 
     
        self.tags = tags 
        
        
        Y = []
        X = []
    
        for point in self.Floor_plan:
            x, y = point
    
            if y != None:
                Y.append(y)
                X.append(x)
                
                
        self.x_center = np.average(X) 
        self.y_center = np.average(Y)
        
        
    def draw(self, fig , ax ):
 
        if len(self.Floor_plan ) > 0: 
            facecolor = 'g'
            if 'colour' in self.tags :
                index = self.tags.index("colour")
                facecolor = self.tags[index+1]
     
            try:
                p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5) 
                
            except:
                facecolor = 'g'
                p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5)             
            ax.add_patch(p)        

    
    
    def get_Center(self):
        
 
        
        return (self.x_center, self.y_center )       
            
class Building(RoadObject):
 
    @classmethod
    def fromOSMdict(cls, dictobj  ):
 
        Floor_plan = []
        tags = dictobj.get('tags')
 
        
        
        
        
        for node in dictobj.get('nodes'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags") ) > 0:
                tags = tags +node.get("tags")
                 
        dictobj["tags"] = tags
 
         
        return Building(  Floor_plan, tags  )  
        
 
 
    def draw(self, fig , ax ):


        if len(self.Floor_plan ) > 0:        
            xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
            ax.plot(xs,ys)
            
            facecolor = 'gray'
     
            if 'roof:colour' in self.tags :
                index = self.tags.index('roof:colour')
                facecolor =  self.tags[index+1]             
                
     
                
            elif  'building:colour' in self.tags:
     
    
                index = self.tags.index('building:colour')
            
                facecolor =  self.tags[index+1]  
    
                
            elif  'colour' in self.tags :
            
                index = self.tags.index('colour')
            
                facecolor =  self.tags[index+1]        
            
            
            try:
                p = Polygon(self.Floor_plan, facecolor = facecolor) 
                
            except:
                p = Polygon(self.Floor_plan, facecolor = 'gray')             
            ax.add_patch(p)
        
class AreaSpace(RoadObject):
 
    @classmethod
    def fromOSMdict(cls, dictobj ,    min_x, min_y ,max_x, max_y):
 
        Floor_plan = []
        tags = dictobj.get('tags')
 
        
        for node in dictobj.get('nodes'):

            x = node.get("x")
            y = node.get("y")
            
            if x >= min_x and  x <= max_x  and y >= min_y and  y <= max_y :
                if x < min_x:
                    x = min_x
                    
                if x > max_x:
                    x = max_x            
    
                if y < min_y:
                    y = min_y
                    
                if y > max_y:
                    y = max_y  
                Floor_plan.append((x ,y ))
                
     
                
                if len(node.get("tags") ) > 0:
                    tags = tags + node.get("tags")
        
        dictobj['tags']  =   tags
 
        return AreaSpace(  Floor_plan, tags )  
        
         
 
    
 
       
        
    def draw(self, fig , ax ):
        
        if len(self.Floor_plan ) > 0:
        
            xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
            ax.plot(xs,ys)
            
            facecolor = 'y'
     
            
            p = Polygon(self.Floor_plan, facecolor = facecolor) 
            ax.add_patch(p)

class Waterway(RoadObject):
 
    @classmethod
    def fromOSMdict(cls, dictobj ,    min_x, min_y ,max_x, max_y):
 
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags = []
        
        for node in dictobj.get('nodes'):

            x = node.get("x")
            y = node.get("y")
            
            
            if x >= min_x and  x <= max_x  and y >= min_y and  y <= max_y :
                if x < min_x:
                    x = min_x
                    
                if x > max_x:
                    x = max_x            
    
                if y < min_y:
                    y = min_y
                    
                if y > max_y:
                    y = max_y  
                Floor_plan.append((x ,y ))
                
     
     
                
                if len(node.get("tags") ) > 0:
                    tags = tags + node.get("tags")
 
         
        return Waterway(  Floor_plan, tags )  
        
         
 
        
    def draw(self, fig , ax ):
        
        if len(self.Floor_plan ) > 0: 
            facecolor = 'b'
     
                
            for index , point in enumerate(self.Floor_plan):
            
                if index <  len(self.Floor_plan) -1:
            
                    x_start , y_start  = point
                    x_end   , y_end    = self.Floor_plan[index+1]
                    
                    deltaX= (x_end -x_start ).astype(float)
                    deltaY= (y_end -y_start ) .astype(float)
                    
            
                    Road_lenght = np.sqrt( deltaX*deltaX   + deltaY *deltaY  )
            
                    Road_width = 2
            
            
                    angle= np.arctan2((y_end -y_start ) ,(x_end -x_start ) )
            
                    t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
            
                    p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="b", alpha= 1)
            
                    p.set_transform(t2)
            
                    ax.add_patch(p) 
                    
                    
            if self.Floor_plan[0] ==  self.Floor_plan[-1]:
                facecolor = 'b'
     
                p = Polygon(self.Floor_plan, facecolor = facecolor) 
                ax.add_patch(p)
 
class Barrier(RoadObject):
 
    @classmethod
    def fromOSMdict(cls, dictobj  ):
 
        
        Floor_plan = []
        tags = dictobj.get('tags')
 
        
        for node in dictobj.get('nodes'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags") ) > 0:
                tags = tags +node.get("tags")
                 
        dictobj["tags"] = tags
        
        return Barrier(  Floor_plan, tags )  
 
class Road():
    
    
   
    
 
    @classmethod
    def fromOSMdict(cls, dictobj ,      min_x, min_y ,max_x, max_y):
        ###print(" ############## Road #################")
 
        points = []
        tags = dictobj.get('tags')
        #tags["nodes_info"] = []
        
 
        
        for node in dictobj.get('nodes'):
            
            x = node.get("x")
            y = node.get("y")
            
            if x >= min_x and x <= max_x and y >= min_y and y <= max_y: 
 
                points.append((node.get("x") ,node.get("y") ))
                
                if len(node.get("tags") ) > 0:
                    tags = tags + node.get("tags")
                    
        dictobj['tags'] = tags
              
        # ##print(Road_id)     
        # ##print(points) 
        # ##print(tags) 
        
        tags_keys =  tags 


        if "railway" in tags_keys:

            return Railway_Road(  points, tags )         
 
        elif "maxspeed" in tags_keys :
            return Drivable_Road(  points, tags  )  
        
 

        elif "driveway" in tags_keys :
            return Drivable_Road(  points, tags  ) 


        elif "lanes" in tags_keys  or  "residential"  in tags_keys or   "living_street"   in tags_keys or    "construction"  in tags_keys  :#or 'asphalt'  in tags_keys
 
            return Drivable_Road(  points, tags )
        
        
        
        elif 'motor_vehicle:conditional' in tags_keys :
            
            return Drivable_Road(  points, tags )        
        
        elif ("service" in tags_keys  and   "parking_aisle" in tags_keys) or (   "pedestrian"  in tags_keys )  or (   "footway" in tags_keys  )  or ( "foot" in tags_keys and   "designated" in tags_keys   )  or (    "path"  in tags_keys)  or (  "service" in tags_keys )  :
            
            return Footway_Bicycle_Road(  points, tags )  
        
        
        elif (  "steps" in tags_keys ):
            return Footway_Bicycle_Road(  points, tags  ) 
        
        elif ("bicycle" in tags_keys  and   "yes" in tags_keys)  or ( "highway" in tags_keys  and   "cycleway" in tags_keys) or ("bicycle" in tags_keys and  "designated" in tags_keys ) :

            return Footway_Bicycle_Road(  points, tags  ) 
        
        
        elif "lanes" in tags_keys  or  "residential"  in tags_keys or   "living_street"   in tags_keys or    "construction"  in tags_keys  :
      
            return Drivable_Road(  points, tags )
 
        
        elif  "busway"  in tags_keys:
            
            return Drivable_Road(  points, tags )           

        elif  "platform" in tags_keys :
            
            return Drivable_Road(  points, tags )  

 
        elif  "asphalt" in tags_keys :
            
            return Drivable_Road(  points, tags )  
        

            
        else:
            return Road(  points, tags  )  
        
         
 
    
    def __init__(self ,  points =list()  , tags = list()   ):
        
        self.points = []
        for point in points:
            x ,y = point
            if x is not None and y is not None:
                self.points.append(point)
                
            
        
            
                
        self.tags = tags 
   
        self.ReferenceLine = None 
        
        self.update_ReferenceLine()
        

        
    def __add__(self, other):
        
        ###print("**************************************************************ADD**********************************************************************")
        if other.points[0] in  self.points:
            self.points = self.points + other.points[1:]         
        else:
            self.points = self.points + other.points 
        
        
         
        
        
        self.tags =  self.tags + other.tags  #+ other.tags
        
        self.update_ReferenceLine()
        
        
 
        return self
    
    
    def update_ReferenceLine(self ):
    
        if len(self.points ) >=2:
        
            self.ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(self.points     )
            ###print("New ReferenceLine OK")
        else:
      
            self.ReferenceLine = None        
        
        
        
    
        
    def draw_Road(self, fig , ax ):
        
        if len(self.points ) > 0: 
            xs, ys = zip(*self.points) #create lists of x and y values
            #ax.plot(xs,ys)
            plt.scatter(xs,ys)
    
            # for space in  self.Spaces:
            #     space.draw(  fig , ax)
            #
            # for Building in self.Buildings:
            #     Building.draw(  fig , ax)
            #
            # for Barrier in self.Barriers:
            #     Barrier.draw(  fig , ax)
            
            #print("######### draw raod ###########")
            
            #print(self.points)
            
            # for key in self.tags:
            #     print(key , " ---> " )
            
        return False
        # facecolor = 'k'
        # if 'roof:colour' in self.tags.keys():
        #     facecolor = self.tags.get('roof:colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
        #
        #
        #
        # p = Polygon(self.Floor_plan, facecolor = facecolor) 
        # ax.add_patch(p)
    
    
    def export2opendrive(self):
        
        
        
 
        junction  =None
        
        if self.ReferenceLine  is not None:
            length = self.ReferenceLine.getLength()
            planView = self.ReferenceLine.export2opendrive()
            
        else:
            
            length = 0
            planView = None        
        
        return opendrive.t_road(id = self.object_id, junction = junction, length = length,   planView = planView )
 
class Junction():
 
 
    @classmethod
    def fromRoads(cls, RoadsList , junctionRadius = 25  ):
        
        junction = Junction(JunctionRoads = list())
        
        RoadsList = copy.copy(RoadsList)
        
        Y = []
        X = []
        
        # for road in RoadsList:
        #     if road.ReferenceLine is not None:
        #         junctionRadius = min(junctionRadius ,road.ReferenceLine.getLength()/2 )
                
 
 
        # for road in RoadsList:
        #
        #     if "lanes" in road.tags:
        #         index = road.tags.index("lanes")
        #
        #         n_lans = int(road.tags[index+1])
        #     else:
        #         n_lans = 2 
        #
        #     if n_lans <2:
        #         n_lans = 2            
        #
        #     lane_width  = 3.5 
        #
        #     roadwidth = lane_width*n_lans
        #     junctionRadius = max(junctionRadius , roadwidth *1.5)                
        
        
        for road in RoadsList:
            for otherRoad in RoadsList:
                if road != otherRoad :
 
                    if road.ReferenceLine is not None:
                    
                        x1 = road.ReferenceLine.x0 
                        y1 = road.ReferenceLine.y0
             
                        x2 , y2 , _ = road.ReferenceLine.get_endPoint()     
                        
                    else:
                        RoadStart = road.points[0]
                        RoadEnd = road.points[-1]   
                        x1 , y1 = RoadStart
                        x2 , y2 = RoadEnd                                       


                    if otherRoad.ReferenceLine is not None: 
                        x3 = otherRoad.ReferenceLine.x0 
                        y3 = otherRoad.ReferenceLine.y0
             
                        x4 , y4 , _ = otherRoad.ReferenceLine.get_endPoint() 
 
                    else:                    
                        otherRoadStart = otherRoad.points[0]
                        otherRoadEnd = otherRoad.points[-1] 
                        x3 , y3 = otherRoadStart
                        x4 , y4 = otherRoadEnd
                    
                    Px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1-x2)*(x3*y4 - y3*x4) ) / ( (x1 - x2)*(y3 -y4) - (y1 -y2)*(x3 -x4) ) 
                    
 
                    Py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1-y2)*(x3*y4 - y3*x4 )) / ( (x1 - x2)*(y3 -y4) - (y1 -y2)*(x3 -x4) )                
            
                    X.append(Px)
                    Y.append(Py)            
            
        x_center = np.average(X) 
        y_center = np.average(Y)  
        
                     
        
        #print( "Junction center", x_center , y_center)
        
        #for i in range(0,5):
        
        
        roadpointdict = dict()
        
        # for index in range( len(RoadsList)-1 , -1 , -1):
        #     road = RoadsList[index]
        #     road_length = road.ReferenceLine.getLength()
        #
        #     if road_length <  junctionRadius :
        #         RoadsList.remove(road)
                
                
                
            
            
            
            
        

        for road in RoadsList:
            
            if road.ReferenceLine is   None:
            
                road.update_ReferenceLine()
            
            if road.ReferenceLine is not None:
                RoadStart_X = road.ReferenceLine.x0 
                RoadStart_Y = road.ReferenceLine.y0
     
                RoadEnd_X , RoadEnd_Y , _ = road.ReferenceLine.get_endPoint()
                
                
                deltaX= (RoadStart_X - x_center ).astype(float)
                deltaY= (RoadStart_Y - y_center ) .astype(float)
        
        
        
                d1 = np.sqrt( deltaX *deltaX    + deltaY *deltaY )
                
                deltaX= (RoadEnd_X - x_center ).astype(float)
                deltaY= (RoadEnd_Y - y_center ) .astype(float)
     
                d2 = np.sqrt( deltaX *deltaX    + deltaY *deltaY ) 
                road_length = road.ReferenceLine.getLength()
                
                if d2 < d1:
    
                    junctionRadiussub = min(junctionRadius ,road.ReferenceLine.getLength()/2 )
                    if d2 < junctionRadiussub   :
                        xend , yend =  road.ReferenceLine.ST2XY(road_length -junctionRadiussub , 0 )
                        
                        xmid , ymid =  road.ReferenceLine.ST2XY(road_length -3*junctionRadiussub/4 , 0 )
                        
                        
                        road.ReferenceLine.set_endPoint(xend , yend)
                        xend , yend , _ = road.ReferenceLine.get_endPoint()
                        roadpointdict[str(road)] = [(xmid , ymid ) ,(xend , yend)  ]
                        roadpointdict[str(road) +"_dir"] =   "End"  
                else:
                    junctionRadiussub = min(junctionRadius ,road.ReferenceLine.getLength()/2 )
                    if d1 < junctionRadiussub  :
                        xstart , ystart  =  road.ReferenceLine.ST2XY( junctionRadiussub , 0 )
                        
                        xmid , ymid =  road.ReferenceLine.ST2XY( junctionRadiussub/4 , 0 )
                        
                        road.ReferenceLine.set_startPoint(xstart , ystart) 
                        
                        
                        
                                  
                        roadpointdict[str(road)] =   [(xstart , ystart) , (xmid , ymid)  ]
                         
                        roadpointdict[str(road) +"_dir"] =   "Strat"
        
        
        #print(roadpointdict.keys())
        for road_index in  range(0  , len(RoadsList)):
            
            road = RoadsList[road_index]
            
            for otherRoad in RoadsList[road_index+1:]:
                if road != otherRoad  and road.ReferenceLine is not None and otherRoad.ReferenceLine is not None:
                    
                                                                    
                    
                    pointsStart= roadpointdict.get(str(road), None ) 
                    pointsEnd = roadpointdict.get(str(otherRoad) , None )
                    
                    if pointsStart is not None and pointsEnd is not None:
                    
                        if roadpointdict[str(road) +"_dir"] ==  "End":
                            pointsStart = copy.deepcopy(pointsStart)
                            pointsStart.reverse()
                            
                         
                        
                        if roadpointdict[str(otherRoad) +"_dir"] ==  "Strat":
                            pointsEnd = copy.deepcopy(pointsEnd)
                            pointsEnd.reverse()
                                                
 
                        points = pointsStart + [ (x_center ,y_center ) ] + pointsEnd
                        
                        if isinstance(road, Drivable_Road) and isinstance(otherRoad, Drivable_Road): 
                        
                            newroad = Drivable_Road(points = points )
                        
                        else:
                             
                            newroad = Footway_Bicycle_Road(points = points )                    
 
                        junction.JunctionRoads.append(newroad) 
                
                                      
                                
        
        return junction
    
    def __init__(self, JunctionRoads = list() ):
        
        self.JunctionRoads = JunctionRoads
    
    
    def draw(  self, fig , ax):
        #print("JunctionRoads" , len(self.JunctionRoads))
        
        for road in self.JunctionRoads:

            road.draw_Road(  fig , ax )    
          
class Footway_Bicycle_Road(Road):
    
    
    def __init__(self,   points=[], tags = []  ):
        Road.__init__(self,   points=points, tags=tags )
    
  
    
    def draw_Road(self, fig , ax ):
        
        # for space in  self.Spaces:
        #     space.draw(  fig , ax)
        #
        # for Building in self.Buildings:
        #     Building.draw(  fig , ax)
        #
        # for Barrier in self.Barriers:
        #     Barrier.draw(  fig , ax)
             
        # n_lans = 1
        # lane_width  = 2
        #
        # for index , point in enumerate(self.points):
        #
        #     if index <  len(self.points) -1:
        #
        #         x_start , y_start  = point
        #         x_end   , y_end    = self.points[index+1]
        #
        #
        #         deltaX= (x_end -x_start ).astype(float)
        #         deltaY= (y_end -y_start ) .astype(float)
        #
        #
        #
        #         Road_lenght = np.sqrt( deltaX *deltaX    + deltaY *deltaY )
        #
        #         Road_width = n_lans*lane_width
        #
        #
        #         angle= np.arctan2(deltaY ,deltaX)
        #
        #         t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        #
        #         p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="gray", alpha=.5)
        #
        #         p.set_transform(t2)
        #
        #         ax.add_patch(p)  
        
        if len(self.points ) > 0: 
            xs, ys = zip(*self.points) #create lists of x and y values
        
            plt.scatter(xs,ys) 
            
            if self.ReferenceLine is not None:
                
                
                xs = []
                ys = []
                for s in np.arange(0, self.ReferenceLine.getLength(),.1):
                    
                    
                    
                    x, y = self.ReferenceLine.ST2XY(s, 0)
                    xs.append(x)
                    ys.append(y)
     
                    #xs, ys = zip(*self.points) #create lists of x and y values
                    
                    
                    
                    
                ax.plot(xs , ys , color="g")   
    
                
            else:
                raise ValueError("wtf")
                #print("wtf")
            #print(self) 
            #print(self.points)   
 
class Drivable_Road(Road):
    
    
    def __init__(self,  points=[], tags=dict()   ):
        
        
        
        
        Road.__init__(self,   points=points, tags=tags ) 
        

          
        
        # ##print("New Drivable_Road")
        # if len(points ) >=2:
        #
        #     self.ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(points , optimize=   False  )
        #
        # else:
        #     ##print(points)
        #     self.ReferenceLine = None        
        #
        #
        # ##print("New Drivable_Road OK")

    def draw_Road(self, fig , ax ):   
 
        #print("draw_Road")
        # for space in  self.Spaces:
        #     space.draw(  fig , ax)
        #
        # for Building in self.Buildings:
        #     Building.draw(  fig , ax)
        #
        # for Barrier in self.Barriers:
        #     Barrier.draw(  fig , ax)
            

                
                #plt.show() 
                
        # for road in self.Footway_Bicycle_Roads:
        #
        #     road.draw_Road(  fig , ax ) 
 
        
        # ###print( self.tags)
        # if "lanes" in self.tags:
        #     index = self.tags.index("lanes")
        #
        #     n_lans =  int(self.tags[index+1])  
        # else:
        #     n_lans =  2  
        #
        #
        #
        # #n_lans = int(self.tags.get("lanes" , 2))
        # lane_width  = 3.5
        # #coler = random.choice(["b" , "y" , "k" , "r"  ]) 
        # for index , point in enumerate(self.points):
        #
        #     if index <  len(self.points) -1:
        #
        #         x_start , y_start  = point
        #         x_end   , y_end    = self.points[index+1]
        #
        #         deltaX= (x_end -x_start ).astype(float)
        #         deltaY= (y_end -y_start ) .astype(float)
        #
        #
        #         Road_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
        #
        #         Road_width = n_lans*lane_width
        #
        #
        #         angle= np.arctan2(deltaY ,deltaX )
        #
        #         t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        #
        #         p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="k", alpha= .5)
        #
        #         p.set_transform(t2)
        #
        #         ax.add_patch(p)
        #coler = random.choice(["b" , "y" , "k" , "r" , "w"]) 
        # xs, ys = zip(*self.points) #create lists of x and y values
        # ax.plot(xs,ys , color="k")    
 
        
        if len(self.points ) > 0:  
            xs, ys = zip(*self.points) #create lists of x and y values
        
            plt.scatter(xs,ys) 
            
            if self.ReferenceLine is not None:
            
                ##print("Length:" , self.ReferenceLine.getLength())
                xs = []
                ys = []
                for s in np.arange(0, self.ReferenceLine.getLength(),.1):
            
            
            
                    x, y = self.ReferenceLine.ST2XY(s, 0)
                    xs.append(x)
                    ys.append(y)
            
    
            
            
                ax.plot(xs , ys, color="k"  )   #
            
    
                
            else:
                raise ValueError("wtf")
            
            
    def export2opendrive(self):        
 
        junction  ="-1"
        
        if self.ReferenceLine  is not None:
            length = self.ReferenceLine.getLength()
            planView = self.ReferenceLine.export2opendrive()
            
        else:
            
            length = 0
            planView = None 
        

        if "lanes" in self.tags:
            
            #print(self.tags)
            
            index = self.tags.index("lanes")
 
            n_lans = int(self.tags[index+1])
        else:
            n_lans = 2 
            
        if n_lans <2:
            n_lans = 2            
            
        lane_width  = 3.5  
        
        roadwidth = lane_width*n_lans 
                 
        laneSection = [] 
 
        roadMark_lane = opendrive.t_road_lanes_laneSection_lcr_lane_roadMark(color = opendrive.e_roadMarkColor.WHITE,
                                                                                    laneChange = opendrive.e_road_lanes_laneSection_lcr_lane_roadMark_laneChange.NONE, 
                                                                                    material = "standard",
                                                                                    sOffset = "0",
                                                                                    type__attr = opendrive.e_roadMarkType.BROKEN ,
                                                                                    weight = opendrive.e_roadMarkWeight.STANDARD,
                                                                                    width = "1.1999999731779099e-01"  )
        
        
        center_lane = opendrive.t_road_lanes_laneSection_center_lane(level = "false", type_ = "none",   id = 0 , roadMark = [roadMark_lane])
        center = opendrive.t_road_lanes_laneSection_center([center_lane])
        left_lane = []
        
        nleft = int(n_lans/2)

        roadMark_sidewalk_curb = opendrive.t_road_lanes_laneSection_lcr_lane_roadMark(color = opendrive.e_roadMarkColor.STANDARD,
                                                                                    laneChange = opendrive.e_road_lanes_laneSection_lcr_lane_roadMark_laneChange.NONE, 
                                                                                    material = "standard",
                                                                                    sOffset = "0",
                                                                                    type__attr = opendrive.e_roadMarkType.NONE ,
                                                                                    weight = opendrive.e_roadMarkWeight.STANDARD,
                                                                                    width = "0"  )        
        
        
        #sidewalk        
        width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = 2, b = 0, c = 0, d  =0 ) ]
        link = None#opendrive.t_road_link( successor  =  opendrive.t_road_lanes_laneSection_lcr_lane_link_predecessorSuccessor(id = nleft+2))
        
        lanetype = opendrive.e_laneType.SIDEWALK
        level = "false"
        
        left_lane.append(opendrive.t_road_lanes_laneSection_left_lane(level = level, type_ = lanetype, link = link,   width = width ,  id = nleft+2 , roadMark = [roadMark_sidewalk_curb]))
        #curb
        
        width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = "1.5239999999999998e-01", b = 0, c = 0, d  =0 ) ]
        link = None#opendrive.t_road_link( successor  =  opendrive.t_road_lanes_laneSection_lcr_lane_link_predecessorSuccessor(id = nleft+1))
        
        lanetype = opendrive.e_laneType.CURB
        level = "false"
        left_lane.append(opendrive.t_road_lanes_laneSection_left_lane(level = level, type_ = lanetype, link = link,   width = width ,  id = nleft+1 , roadMark = [roadMark_sidewalk_curb]))
        
        
        
        
        for i in range(nleft,0,-1):
             
            level = "false"
            width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = lane_width, b = 0, c = 0, d  =0 ) ]
            link = None#opendrive.t_road_link( successor  =  opendrive.t_road_lanes_laneSection_lcr_lane_link_predecessorSuccessor(id = i))
            lanetype="driving"
            left_lane.append(opendrive.t_road_lanes_laneSection_left_lane(level = level, type_ = lanetype, link = link,   width = width ,  id = i , roadMark = [roadMark_lane]))
        
        
        
        
        
        left = opendrive.t_road_lanes_laneSection_left(left_lane )
        
        
        nright = n_lans -nleft
        
        right_lane = []
        
        for i in range( -1,-1*nright-1,-1):
             
            level = "false"
            width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = lane_width, b = 0, c = 0, d  =0 ) ]
            link = None#opendrive.t_road_link( )
            lanetype="driving"
            right_lane.append(opendrive.t_road_lanes_laneSection_right_lane(level = level, type_ = lanetype, link = link,   width = width ,  id = i , roadMark = [roadMark_lane]))
        
        #curb
        
        width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = "1.5239999999999998e-01", b = 0, c = 0, d  =0 ) ]
        link = None#opendrive.t_road_link( successor  =  opendrive.t_road_lanes_laneSection_lcr_lane_link_predecessorSuccessor(id =-( nleft+1)))
        
        lanetype = opendrive.e_laneType.CURB
        level = "false"
        right_lane.append(opendrive.t_road_lanes_laneSection_left_lane(level = level, type_ = lanetype, link = link,   width = width ,  id =   i-1 , roadMark = [roadMark_sidewalk_curb]))
        
       
        #sidewalk
        width = [opendrive.t_road_lanes_laneSection_lr_lane_width(a = 2, b = 0, c = 0, d  =0 ) ]
        link = None#opendrive.t_road_link( successor  =  opendrive.t_road_lanes_laneSection_lcr_lane_link_predecessorSuccessor(id = -(nleft+2)))
        
        lanetype = opendrive.e_laneType.SIDEWALK
        level = "false"
        
        right_lane.append(opendrive.t_road_lanes_laneSection_left_lane(level = level, type_ = lanetype, link = link,   width = width ,  id = i-2 , roadMark = [roadMark_sidewalk_curb]))





        right = opendrive.t_road_lanes_laneSection_right(right_lane )        
        lansec = opendrive.t_road_lanes_laneSection(s = 0, singleSide = False, left = left, center = center, right  = right)
            
        laneSection.append(lansec)
        laneOffset = [opendrive.t_road_lanes_laneOffset(a = 0, b= 0, c = 0, d = 0, s = 0)    ]  
        lanes =  opendrive.t_road_lanes(laneOffset = laneOffset, laneSection  =laneSection)
        
        superelevation = [opendrive.t_road_lateralProfile_superelevation(a= 0, b= 0, c= 0, d = 0, s = 0)]
        
        
        shape = [opendrive.t_road_lateralProfile_shape(a= 0, b= 0, c= 0, d= 0, s= 0, t = -roadwidth)]
        lateralProfile = opendrive.t_road_lateralProfile(superelevation, shape )
        
        elevation = [ opendrive.t_road_elevationProfile_elevation(a= 0, b= 0, c= 0, d= 0, s = 0)]
        elevationProfile = opendrive.t_road_elevationProfile(elevation )
        
        rule = opendrive.e_trafficRule.RHT
        type_ = opendrive.e_roadType.TOWN
        country = opendrive.e_countryCode_deprecated.GERMANY
        
        
        
        if "maxspeed" in self.tags:
            
            
            index = self.tags.index("maxspeed")
            try:
                maxspeed = int(self.tags[index+1])
            except:
                
                if self.tags[index+1] == 'none':
                
                    maxspeed =  130
                else:
                    maxspeed =  35
                               
        else:
            maxspeed = 35       
        
        
        
        
        speed = opendrive.t_road_type_speed(max = maxspeed, unit  =  opendrive.e_unitSpeed.KMH)
        s = 0
        type_ = [opendrive.t_road_type(country, s   , type_, speed )]
        return opendrive.t_road(id = None, junction = junction, length = length,   planView = planView , lanes = lanes , elevationProfile= elevationProfile ,  lateralProfile = lateralProfile , rule = rule , type_ = type_ )          
   
class Railway_Road(Road):
    
    
    def __init__(self,   points=[], tags=dict() ):
        Road.__init__(self,  points=points, tags=tags )
    
    
    def draw_Road(self, fig , ax ):   
                
 
        
        if len(self.points ) > 0:          
            # for index , point in enumerate(self.points):
            #
            #     if index <  len(self.points) -1:
            #
            #         x_start , y_start  = point
            #         x_end   , y_end    = self.points[index+1]
            #
            #         deltaX= (x_end -x_start ).astype(float)
            #         deltaY= (y_end -y_start ) .astype(float)
            #
            #
            #         Road_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
            #
            #         Road_width = 6
            #
            #
            #         angle= np.arctan2(deltaY ,deltaX)
            #
            #         t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
            #
            #         p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="r", alpha= .5)
            #
            #         p.set_transform(t2)
            #
            #         ax.add_patch(p)
    
            xs, ys = zip(*self.points) #create lists of x and y values
            ax.plot(xs,ys , color="r")               
            if self.ReferenceLine is not None:
                
                
                xs = []
                ys = []
                for s in np.arange(0, self.ReferenceLine.getLength(),.1):
                    
                    
                    
                    x, y = self.ReferenceLine.ST2XY(s, 0)
                    xs.append(x)
                    ys.append(y)
     
                    #xs, ys = zip(*self.points) #create lists of x and y values
                    
                    
                    
                    
                ax.plot(xs , ys , color="r") 
                
            else:
                raise ValueError ("wtf")                 

class Scenery():
    
    @classmethod
    def from_Osm(cls, filepath):
        
        Roads =[]
        Buildings = []
        Spaces = []
        Barriers = []
        
        
        osmObj = osm_map.parse(filepath, silence = True ,  print_warnings = True)
        
        
        bound = osmObj.bounds[0]
        
        minlat =  float(bound.minlat )
        minlon =  float(bound.minlon  )      
        maxlat = float( bound.maxlat )
        maxlon =  float(bound.maxlon )
        
        
        min_x, min_y = projection_fromGeographic(minlat, minlon, minlat ,minlon )
        max_x, max_y = projection_fromGeographic(maxlat, maxlon, minlat ,minlon )
        
        
        # delta_x = max_x  - min_x
        # delta_y = max_y  - min_y        
        #
        #
        # max_x = max_x + delta_x/2
        # max_y = max_y + delta_y/2        
        #
        # min_x = min_x - delta_x/2
        # min_y = min_y - delta_y /2       
        
        
        metaData = {"minlat":minlat ,"minlon" : minlon , "maxlat": maxlat  , "maxlon" : maxlon  , "min_x" : min_x , "min_y" : min_y , "max_x" : max_x , "max_y" :max_y }
        
                
        ###print(metaData)
        
        
        nodsdict = dict()
        
        for node in tqdm(osmObj.node):
            ###print(node)
            node_id = node.id
            latitude =  float( node.lat )
            longitude = float( node.lon )
            x ,y = projection_fromGeographic(latitude, longitude, minlat ,minlon )
        
            tags = []#dict()
        
            for tag  in node.tag:
                #tags[tag.k] = tag.v
                tags.append(tag.k)
                tags.append(tag.v)                
                
            nodsdict[node_id] = {"x": x , "y" : y , "tags" : tags  ,"latitude":latitude  , "longitude":longitude , "node_id" : node_id}
            ###print(node)
            ###print(nodsdict[node_id])
            
        
         
        waysdict = dict()
            
        for way in tqdm(osmObj.way):
            
            way_id = way.id
            visible = (way.visible == "true")
            nodes = []
            for nd in way.nd:
                nodes.append(nodsdict.get(nd.ref, None))
                
            tags = []# dict()
        
            for tag  in way.tag:
                #tags[tag.k] = tag.v            
                tags.append(tag.k)
                tags.append(tag.v)
                
                
            waysdict[way_id] = {"visible": visible , "nodes" : nodes , "tags" : tags}            
            
            #t(waysdict[way_id])
            
            tagkeys =  tags#.keys()
            
            

                

            if    "elevator"  in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] )
                
                Buildings.append(building)

            
            elif "highway" in tagkeys         :
                ###print(way)
                road = Road.fromOSMdict(waysdict[way_id] ,    min_x, min_y ,max_x, max_y )
                
                Roads.append(road)          

            elif "cycleway" in tagkeys         :
                ###print(way)
                road = Road.fromOSMdict(waysdict[way_id] ,    min_x, min_y ,max_x, max_y )
                
                Roads.append(road) 

    
    
            elif "historic" in tagkeys  or "roof:edge" in tagkeys or "boundary"  in tagkeys or len(tagkeys) == 0   or ( "landuse" in tagkeys   and   "retail"  in tagkeys    or       "residential" in tagkeys     or     "construction"  in tagkeys    or      "industrial" in tagkeys   ):
                
                #area = AreaSpace.fromOSMdict(waysdict[way_id] ,    min_x, min_y ,max_x, max_y )
                
                #Spaces.append(area)
                pass
            elif   "railway" in tagkeys      :
                ###print(way)
                road = Road.fromOSMdict(waysdict[way_id] ,    min_x, min_y ,max_x, max_y )
                
                Roads.append(road)    
            
            
            elif "building" in tagkeys   or  "building:material" in tagkeys  or  "demolished:building" in tagkeys   or  "building:levels" in tagkeys  or "building:part" in tagkeys or ( "amenity" in tagkeys    and   "kindergarten"  in tagkeys    or   "school"  in tagkeys     ):
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)
                
                
            elif "power" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)                  
                
            elif "roof:ridge" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)      
                
                
            elif "roof:shape" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] )
                
                Buildings.append(building)            

            elif "indoor" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)
                
                
                
 
            elif "man_made" in tagkeys  and     "bridge" in tagkeys    :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)  
 
                
            elif "source" in tagkeys   :              
            
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building) 

            elif "amenity" in tagkeys and    "college"  in tagkeys     :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)
                
                
            elif "amenity" in tagkeys and     "hospital"  in tagkeys     :              
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)
                
                
            elif "landuse" in tagkeys  and   "railway" in tagkeys   :                  
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building) 
 
            elif "leisure" in tagkeys  and   "swimming_pool" in tagkeys   :                  
                
                building = Building.fromOSMdict(waysdict[way_id]  )
                
                Buildings.append(building)
 
 
            elif "parking" in tagkeys   or ("leisure"  in tagkeys  and    "park"  in tagkeys    )   or ("area" in tagkeys and     "yes" in tagkeys   )   or  ("amenity"  in tagkeys  and     "bicycle_parking" in tagkeys   )   :
 
                parking = AreaSpace.fromOSMdict(waysdict[way_id]   ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(parking)
                
            elif "motor_vehicle:conditional" in tagkeys:
            
                parking = AreaSpace.fromOSMdict(waysdict[way_id]    ,  min_x, min_y ,max_x, max_y  )
            
                Spaces.append(parking)
                
                
                
                                
                
            elif "amenity" in tagkeys  and (   "parking" in tagkeys    or   "parking_space" in tagkeys     or  "parking_space" in tagkeys ):                 
                parking = AreaSpace.fromOSMdict(waysdict[way_id]    ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(parking)
                
                
                                
                
            elif "name" in tagkeys  and  "public_transport" in tagkeys  :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id]    ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area) 
                


            elif "man_made" in tagkeys  and    "courtyard"  in tagkeys   :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id]   ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)



                
            elif "man_made" in tagkeys  and  "public_transport" in tagkeys  :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id]   ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area) 
                
                
                
            elif "leisure" in tagkeys    :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id]  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)                

 


            elif "landuse" in tagkeys  and  "brownfield"  in tagkeys     :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id]    ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)  
                               
                
            elif ( "landuse" in tagkeys   and   "grass"  in tagkeys   )   or ( "landuse" in tagkeys   and   "greenfield" in tagkeys    )   or   ( "leisure" in tagkeys   and   "playground" in tagkeys    ) or ("leisure"  in tagkeys  and    "garden"  in tagkeys    )   :
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]     )
                
                Barriers.append(barrier)
                
                
                
            elif ( "landuse" in tagkeys   and    "orchard"  in tagkeys   ) :                
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]    )
                
                Barriers.append(barrier)                
                


            elif ( "landuse" in tagkeys   and   "cemetery"  in tagkeys   ) :                
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]     )
                
                Barriers.append(barrier)     
                
            elif ( "leisure" in tagkeys   and   "outdoor_seating" in tagkeys    ) :                
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]    )
                
                Barriers.append(barrier)                  

            elif ( "bench" in tagkeys    ) :                
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]     )
                
                Barriers.append(barrier)

                           

            elif ( "attraction" in tagkeys   ) :                
                
                barrier = Barrier.fromOSMdict(waysdict[way_id]    )
                
                Barriers.append(barrier)


                
            elif ( "stairwell" in tagkeys     ) :               
                barrier = Barrier.fromOSMdict(waysdict[way_id]   )
                
                Barriers.append(barrier) 


            elif "man_made" in tagkeys  and    "pier"  in tagkeys     :
   
                barrier = Barrier.fromOSMdict(waysdict[way_id]   )
                
                Barriers.append(barrier) 
                
                
            elif "shelter" in tagkeys  and   tagkeys in tagkeys    :
   
                barrier = Barrier.fromOSMdict(waysdict[way_id]   )
                
                Barriers.append(barrier)  
                
                
            elif "amenity" in tagkeys  and   "shelter"  in tagkeys     :
   
                barrier = Barrier.fromOSMdict(waysdict[way_id]     )
                
                Barriers.append(barrier)  
                                                                              
   
            elif "playground" in tagkeys    :
   
                barrier = Barrier.fromOSMdict(waysdict[way_id]    )
                
                Barriers.append(barrier)     




   
            elif "amenity" in tagkeys  and    "bench" in tagkeys    :
   
                barrier = Barrier.fromOSMdict(waysdict[way_id]    )
                
                Barriers.append(barrier) 
                
                
                
            elif "waterway" in tagkeys :
                                
 
                
                waterway = Waterway.fromOSMdict(waysdict[way_id] ,    min_x, min_y ,max_x, max_y  )
                
                Spaces.append(waterway)

            elif "barrier" in tagkeys   or ( "landuse" in tagkeys   and   "village_green"  in tagkeys   ) or "natural" in tagkeys   or ( "amenity" in tagkeys   and    "fountain"  in tagkeys   ) : #  or "natural" in tagkeys   or "amenity" in tagkeys 
 
                barrier = Barrier.fromOSMdict(waysdict[way_id]     )
                
                Barriers.append(barrier)
                
                
               
            else:
                print("***********************************************************************")
                print(way)
                area = AreaSpace.fromOSMdict(waysdict[way_id]    ,  min_x, min_y ,max_x, max_y  )
                Spaces.append(area)  
                # road = Road.fromOSMdict(waysdict[way_id] , way_id ,  min_x, min_y ,max_x, max_y )
                # fig, ax = plt.subplots(figsize=(1, 1), facecolor='lightskyblue', layout='constrained')
                # plt.axis('equal')
                # road.draw_Road(  fig , ax )
                # plt.show() 
   
        Roads =  Scenery.organize_Roads(Roads )  
        Junctions = []#Roads ,Junctions  = Scenery.organize_junctions(Roads ) 
        
        toremove = []
        for road in Roads:
            if road.ReferenceLine.getLength() < 1 :
                toremove.append(road)
                
        for road in   toremove:
            Roads.remove(road)
            
                
        
        return Scenery(metaData , nodsdict ,Roads,   Buildings, Spaces , Barriers , Junctions)
    
    
    def __init__(self, metaData = dict(), nodsdict =dict(), Roads = list()  , Buildings = list() , Spaces = list() , Barriers= list() , Junctions = list(), name = "Database name" ):
        
        self.name = name
        self.metaData =metaData
        self.nodsdict =nodsdict
        self.Roads = Roads
 
        self.Buildings = Buildings 
        self.Spaces =Spaces 
        self.Barriers = Barriers          
        self.Junctions = Junctions 


    @classmethod        
    def organize_junctions(cls ,Roads ): #, Buildings, Spaces , Barriers 
        
        rods_iD_dict  = dict()
        
 
        
        class_name_roads_list = []
        
        for road in Roads:
            
            if isinstance(road, Drivable_Road) or isinstance(road, Footway_Bicycle_Road):
                class_name_roads_list.append(road) 
                rods_iD_dict[str(road)] = road
 
 
 
        
        
        #roads_start_end  = {}
        pints_of_intest = dict()
        
        for road in class_name_roads_list:
            
            Road_id = str(road)#.object_id
            
            start = road.points[0]
            
            end = road.points[-1]
        
            
            
            for other_road in class_name_roads_list:
                
                if other_road != road:
                
                    other_Road_id = str(other_road)#.object_id
                    
                    other_start = other_road.points[0]
                    
                    other_end = other_road.points[-1]
                    
                    point = None
                    if other_start == end:
                        point = str(end) 
                        
                    elif other_end == start: 
                        point = str(start) 
                    # elif other_start == start:  
                    #     point = str(start)  
                    # elif  other_end == end:
                    #     point = str( end )  
                    
                    
                    if point is not None:
                        if pints_of_intest.get(point, None) is None:
                            pints_of_intest[point] = []
                            
                        if not Road_id in pints_of_intest[point]:
                            pints_of_intest[point].append(Road_id) 
                            
                        if not other_Road_id in pints_of_intest[point]:
                            pints_of_intest[point].append(other_Road_id)
                        
        
        junctions = []                 
                            
        for point in pints_of_intest.keys():
            
            pints_of_intest[point] = list(set(pints_of_intest[point]))
            
            if len(pints_of_intest[point]) >=  2:
                
                #print(point)
                
                junc_list =pints_of_intest[point] 
                
                junc_list = list(set(junc_list))
                
                roadlist =[]
                for road in junc_list:
                    
                    road = rods_iD_dict.get(road)
                    
                    roadlist.append(road)
                    start =  road.points[0]
                    end =  road.points[-1]            
                    #print("start" , start , "end"  , end)                     
                 
                 
                #print("N Roads" ,  len(roadlist))  
                
                junctionRadius = 0
                
                for road in roadlist:
                    junctionRadius = junctionRadius + road.ReferenceLine.getLength()/4
                    
                junctionRadius = junctionRadius/len(roadlist)   
                
                for road in roadlist:
                
                    if "lanes" in road.tags:
                        index = road.tags.index("lanes")
                
                        n_lans = int(road.tags[index+1])
                    else:
                        n_lans = 2 
                
                    if n_lans <2:
                        n_lans = 2            
                
                    lane_width  = 3.5 
                
                    roadwidth = lane_width*n_lans
                    junctionRadius = max(junctionRadius , roadwidth *1.5)  
                
                
                 
                junction = Junction.fromRoads(roadlist, junctionRadius)
                #print("N Roads junction" ,  len(junction.JunctionRoads)) 
                junctions.append(junction)
                    
        return Roads , junctions
        
        
        
    @classmethod        
    def organize_Roads(cls ,Roads ): #, Buildings, Spaces , Barriers 
        
        rods_dict  = dict()
        
        rods_iD_dict  = dict()
        
        for road in Roads:
            class_name= str(road.__class__.__name__)
            
            # if class_name == "Drivable_Road"  or class_name == "Footway_Bicycle_Road" :
            #
            #     class_name = "Drivable_Road"
                
            rods_iD_dict[str(road)] = road
            
            if rods_dict.get(class_name, None) is None:
                rods_dict[class_name] = []
            
            
            rods_dict[class_name].append(road) 
        
        ###print(rods_dict)
        
        nameslist = list(rods_dict.keys())
        nameslist.reverse()
        for class_name in nameslist:
            # ##print(class_name)
            #
            # if "Drivable_Road" == class_name:
            #     ##print("relavent")
            
            
            class_name_roads_list = rods_dict.get(class_name)
            
            #roads_start_end  = {}
            pints_of_intest = dict()
            
            for road in class_name_roads_list:
                
                
                if len(road.points) > 2:
                
                    Road_id = str(road)#.object_id
                    
                    start = road.points[0]
                    
                    end = road.points[-1]
     
                    
                    
                    for other_road in class_name_roads_list:
                        
                        if other_road != road  and len(other_road.points) > 2:
                        
                            other_Road_id = str(other_road)#.object_id
                            
                            other_start = other_road.points[0]
                            
                            other_end = other_road.points[-1]
                            
                            point = None
                            if other_start == end:
                                point = str(end) 
                                
                            elif other_end == start: 
                                point = str(start) 
                            # elif other_start == start:  
                            #     point = str(start)  
                            # elif  other_end == end:
                            #     point = str( end )  
                            
                            
                            if point is not None:
                                if pints_of_intest.get(point, None) is None:
                                    pints_of_intest[point] = []
                                    
                                if not Road_id in pints_of_intest[point]:
                                    pints_of_intest[point].append(Road_id) 
                                    
                                if not other_Road_id in pints_of_intest[point]:
                                    pints_of_intest[point].append(other_Road_id)
                            
 
            mergelists = []                  
                                
            for point in pints_of_intest.keys():
                
                pints_of_intest[point] = list(set(pints_of_intest[point]))
                
                if len(pints_of_intest[point]) == 2:
                           
                    road_Id1 = pints_of_intest[point][0]
                    
                    road_Id2 = pints_of_intest[point][1] 
                     
                    found = False
                    for mergelist in mergelists:
                        if road_Id1 in mergelist or road_Id2 in mergelist:
                            found = True
                            
                            if not road_Id2 in mergelist:
                                mergelist.append(road_Id2)
                            if not road_Id1 in mergelist:
                                mergelist.append(road_Id1)
                            
                            break
                            
                    if not  found:
                        newlist = [road_Id1 ,road_Id2 ]
                                                                           
                        mergelists.append(newlist)
                    
            
            mergelists_updated= []
            
            removedLists = []
            for mergelist in mergelists: 
                reultList = mergelist
                
                for road_id in mergelist:
                
                    for other_mergelist in mergelists: 
                        
                        if other_mergelist != mergelist and road_id in other_mergelist:
                            reultList = reultList + other_mergelist 
                            removedLists.append(other_mergelist)
                
                if mergelist not in removedLists:
                    
                    reultList = list(set(reultList))
                    
                    mergelists_updated.append(reultList)   
                
                
                
                          
            mergelists =  mergelists_updated  
            
        
            for mergelist in mergelists:
                ###print(mergelist) 
                
                roadsList = []
                for road_id in mergelist:
                    road = rods_iD_dict.get(road_id)
                    roadsList.append(road)
                    
                roadsListSorted = []
                
                while  len(roadsListSorted) < len(roadsList):
                    for road in roadsList:
                        if not road in roadsListSorted:
                            start = road.points[0]
                            end = road.points[-1] 
                            
                            index = 0
                            
                            for other_road  in roadsListSorted:
                                other_road_start = other_road.points[0]
                                other_road_end = other_road.points[-1]                                                    
                                
                                if start ==  other_road_end:
                                    index = roadsListSorted.index(other_road) + 1
                                    
                                elif  end == other_road_start:
                                    
                                    index = roadsListSorted.index(other_road) 
                                    
                            roadsListSorted.insert(index, road)                                       
                
                
                roadsList = roadsListSorted
                
 

                nTotal = 0
                for other in roadsList:
                    nTotal = nTotal + len(other.points)

                
                result = roadsList[0]
                
                i =0 
                while  len(result.points) <  nTotal:
                    
                    
                    i = i +1
                    
                    for other in roadsList[1:]:
                        
    
                        start = result.points[0]
                        end = result.points[-1] 
                        
     
                        other_road_start = other.points[0]
                        other_road_end = other.points[-1] 
                        
                        if end == other_road_start  :
     
                            result =  result + other 
                        
                        elif  other_road_end == start  :
                            result =   other  + result                       
                      
                                        
                    if i > 10:
                        break  
                        
                for other in roadsList[1:]:
                    other_start = other.points[0]
                    other_End = other.points[-1]  
                
                    if   other_start in   result.points and     other_End in   result.points and other in Roads :
                        Roads.remove(other)
                        

                        
                    
                        

                if result not in Roads  and result is not None :
                    Roads.append(result)
                    

 


        for road in Roads:
            for index in range(len(road.points)-1,0 ,-1):
                
                
                if road.points[index] == road.points[index-1]:
 
                    road.points.remove(road.points[index])
                    
                elif  road.points.count(road.points[index]) > 1: 
                    
                    ###print(road.points.count(road.points[index]))
                    road.points.remove(road.points[index])
                    
            if len(road.points) <2:
                Roads.remove(road)
                
                
        indextoremove = []        
                
        for index in range(0, len(Roads)):
            road1 = Roads[index]
            
            for other_road in Roads:
                
                if road1 != other_road:
                    
                    
                    
                    if len(road1.points) > 2 and len(other_road.points) > 2 and  road1.points[0] in other_road.points and  road1.points[-1] in other_road.points:
                        indextoremove.append(index)
                        
                    elif len(road1.points) <2:
                        indextoremove.append(index)
                        
                        
                    
                    
        indextoremove = list(set(indextoremove))            
                    
        indextoremove.sort()
        indextoremove.reverse()
        
        for index in  indextoremove:
            
            Roads.remove(Roads[index])
            
                   
        
        
        # Buildings, Spaces , Barriers 
        
        # Drivable_Road_List= [] 
        #
        # for road in  Roads:
        #
        #     if isinstance(road, Drivable_Road):
        #
        #         Drivable_Road_List.append(road) 
        #
        #
        #
        #
 
        # for  Building in tqdm( Buildings ):
        #     xc , yc = Building.get_Center()
        #     T_min = 1000
        #     RoadNear =None            
        #     for road in Roads:
        #
        #         S, T = road.ReferenceLine.XY2ST(xc , yc)
        #
        #         if S is not None and T is not None  and S < road.ReferenceLine.getLength() and np.abs(T) < T_min:
        #                 T_min = np.abs(T) 
        #                 RoadNear = road
        #
        #     if RoadNear is not None:
        #         RoadNear.Buildings.append(Building)
        #     else:
        #         raise ValueError("yalahowy")
        #
        #
        #
        # for  Space in tqdm( Spaces ):
        #     xc , yc = Space.get_Center()
        #     T_min = 1000
        #     RoadNear =None            
        #     for road in Roads:
        #
        #         S, T = road.ReferenceLine.XY2ST(xc , yc)
        #
        #         if S is not None and T is not None  and S < road.ReferenceLine.getLength() and np.abs(T) < T_min:
        #                 T_min = np.abs(T) 
        #                 RoadNear = road
        #
        #     if RoadNear is not None:
        #         RoadNear.Spaces.append(Space)            
        #
        # for  Barrier in tqdm( Barriers ):
        #     xc , yc = Barrier.get_Center()
        #     T_min = 50
        #     RoadNear =None            
        #     for road in Roads:
        #
        #         S, T = road.ReferenceLine.XY2ST(xc , yc)
        #
        #         if S is not None and T is not None  and S < road.ReferenceLine.getLength() and np.abs(T) < T_min:
        #                 T_min = np.abs(T) 
        #                 RoadNear = road
        #
        #     if RoadNear is not None:
        #         RoadNear.Barriers.append(Barrier)        
                                  
        
        return Roads
            
        
         
    
    def onclick(self, event):
        #global ix, iy
        
        ix, iy = event.xdata, event.ydata
        
        ##print("***********************************************************")
        ##print("***********************************************************")
        ##print("***********************************************************")
        ##print("***********************************************************")
        
        clear()
 
        try:
        
            dist = 1000
            closet_node= []
            
            
            for node_id in self.nodsdict.keys():
                node = self.nodsdict.get(node_id)
                node_x = node["x"]
                node_y =  node["y"]
    
    
                deltaX= (ix -node_x ).astype(float)
                deltaY= (iy -node_y ) .astype(float)
                
                new_dist =  np.sqrt( deltaX *deltaX   +deltaY*deltaY  )
                
                
                if new_dist < dist:
                    dist = new_dist
                    
                    closet_node = (node_x ,node_y)
                    
                
                
            
            
            ##print( str(closet_node ) )
            
            results = []
            
            # for space in  self.Spaces:
            #     if closet_node in space.Floor_plan:
            #         results.append(space)
                    
                
            # for node in space.nodes: 
            #     if node["node_id"]  in closet_node:
            #
            #         if space not in results:
            #             results.append(space)
                        
     
            # for Building in  self.Buildings:
            #
            #
            #
            #     if closet_node in Building.Floor_plan:
            #         results.append(Building)
    
    
            for Road in  self.Roads:
                if closet_node in Road.points:
                    results.append(Road)
                
    
            # for Barrier in  self.Barriers:
            #     if closet_node in Barrier.Floor_plan:
            #         results.append(Barrier)
                 
            
            for result in results:
                print(f"#############################{result.__class__.__name__}############################")
                
                ###print(f"#############################{result.object_id}############################")            
                
                
                print(result)
                print(result.tags)
            
        except:
            
            pass    
            


    def export2opendrive(self, save_path):
        
        east = self.metaData.get('max_x')
        north = self.metaData.get('max_y')
        west = self.metaData.get('min_x')
        south = self.metaData.get('min_y')
        
 
        referenceLat = self.metaData.get('minlat')
        referenceLon = self.metaData.get('minlon')
        
        
        geo =  "<![CDATA[+proj=tmerc +lat_0=0.002049196191879877 +lon_0=4.513789469769987 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +geoidgrids=egm96_15.gtx +vunits=m +no_defs ]]>"
 
 
        
        geoReference = opendrive.t_header_GeoReference(  valueOf_=  geo   )
        
        header = opendrive.t_header(  east  = east, name = self.name, north = north, revMajor = 1, revMinor = 7, south =south, vendor = "OSM", version  =1, west = west, geoReference =geoReference)
        
        
        
        
        road = []
        i= 0
        for roadObj in self.Roads:
            
            if isinstance(roadObj, Drivable_Road)  :
                 
                roadXml = roadObj.export2opendrive()
                roadXml.id = i
                road.append( roadXml)
            
                i = i+1
        
        
        
        controller = []
        junction = []
        junctionGroup =[]
        station =[]
        dataQuality =None
        include= None
        userData = None
        gds_collector_ = None 
        opendrive_object = opendrive.OpenDRIVE(header, road, controller, junction, junctionGroup, station, dataQuality, include, userData, gds_collector_)
        
        
  
        with open(save_path, 'w') as outfile:
            
            
            outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            opendrive_object.export(outfile = outfile ,  level = 0 ,  pretty_print  =True)
 
             
        
            
    
    
    
    def draw_scenery(self, savepath = None , size = (25,25)):
        

        #for road in self.Roads:
        fig, ax = plt.subplots(figsize=size, facecolor='lightskyblue', layout='constrained')
        plt.axis('equal')
        onclick = self.onclick
        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        for space in  self.Spaces:
 
            space.draw(  fig , ax)
        
        for Building in self.Buildings:
            Building.draw(  fig , ax)
        
        for Barrier in self.Barriers:
            Barrier.draw(  fig , ax)


        for junction in self.Junctions:
            junction.draw(  fig , ax)

 
        for road in self.Roads:
        
            road.draw_Road(  fig , ax )
            
        #plt.show() 
        if savepath is NONE:
            savepath = f"..\\Data\\scenery"
            
        
        plt.savefig(savepath + ".png")
        plt.savefig(savepath + ".svg" )
 


if __name__ == '__main__':
    






    # #import numpy as np
    # from scipy.special import fresnel
    # #import matplotlib.pyplot as plt
    #
    # t = np.linspace(0, 5.0, 201)
    # ss, cc = fresnel(t / np.sqrt(np.pi / 2))
    # scaled_ss = np.sqrt(np.pi / 2) * ss
    # scaled_cc = np.sqrt(np.pi / 2) * cc
    # plt.plot(t, scaled_cc, 'g--', t, scaled_ss, 'r-', linewidth=2)
    # plt.grid(True)
    # plt.show()
    #

    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.set_aspect('equal')
    # R = 20.0
    # for arcLength in range(0, 400, 20):
    #
    #     distances = np.linspace(start=-arcLength, stop=arcLength, num=300)
    #     XY = spiral_interp_centre(distances,arcLength, 50, 100, np.radians(45), 1/R )
    #     ax.plot(XY[:, 0], XY[:, 1])
    #     ###print('d={:.3f}, dd={:.3f}, R={:.3f}, RR={:.3f}'.format(d, arcLength(XY), R, 1/getCurvatureUsingTriangle(XY, 299, 298, 297)))
    #
    # R = -20.0
    # for arcLength in range(0, 400, 20):
    #
    #     distances = np.linspace(start=-arcLength, stop=arcLength, num=300)
    #     XY = spiral_interp_centre(distances,arcLength, 50, 100, np.radians(45), 1/R )
    #     ax.plot(XY[:, 0], XY[:, 1])
    #     ###print('d={:.3f}, dd={:.3f}, R={:.3f}, RR={:.3f}'.format(d, arcLength(XY), R, 1/getCurvatureUsingTriangle(XY, 299, 298, 297)))        
    #
    # plt.show()
    
    #
    # center, radius = define_circle((0,1), (1,0), (0,-1))
    # if center is not None:
    #     plt.figure(figsize=(10, 10))
    #     circle = plt.Circle(center, radius)
    #     plt.gcf().gca().add_artist(circle)    
    #     plt.show()
    
    
    # x_start = -10
    # y_start =  10  
    #
    #
    # x_midel = 0
    # y_midel = 10  
    #
    #
    # x_end = -10
    # y_end = -20  
    #
    #
    # Rmax  = 15
    #
    # Rmin  = 5
    #
    # ref = RoadReferenceLine.Connect3points(x_start, y_start, x_midel, y_midel, x_end, y_end, Rmax, Rmin)
    #
    #
    # for ele in ref.geometry_elements:
    #     #print("ele : " , ele.__class__.__name__)
    #     #print("length", ele.length )
    #
    #     try:
    #         #print("Curvatur" , ele.Curvatur )
    #
    #     except:
    #         pass
    #
    #     try:
    #         #print("CurvaturStart" , ele.CurvaturStart )
    #         #print("CurvaturEnd" , ele.CurvaturEnd )
    #     except:
    #         pass  
    #
    #
    #
    #
    # fig, ax = plt.subplots(figsize=(10, 10))
    # S = ref.getLength()
    #
    # X =[x_start ,x_midel ,x_end  ]
    # Y =[y_start ,y_midel ,y_end  ]
    #
    # plt.scatter(X,Y) 
    #
    # xy = []
    # for ele in np.arange(0,S  +0.1,0.1):
    #     xy.append(ref.ST2XY(ele,0))
    # plt.plot(*zip(*xy))
    #
    #
    # plt.show()
    # #plt.savefig(f"./road_{i}.png")


    
    
    filepath = os.path.abspath("..\\Data\\WesternTor_2.osm")
    sceneryObj = Scenery.from_Osm(filepath)    
    sceneryObj.export2opendrive("..\\Data\\WesternTor_2.xodr")
    sceneryObj.draw_scenery("..\\Data\\WesternTor_2" , (50,50))
    
    # for road in sceneryObj.Roads:
    #
    #     #if isinstance(road, Drivable_Road):
    #     fig, ax = plt.subplots(figsize=(10, 10))
    #     road.draw_Road(  fig , ax )    
    #     plt.show()
    
    # i= 0
    #
    # for road in sceneryObj.Roads:
    #     i = i +1
    #     fig, ax = plt.subplots(figsize=(10, 10))
    #     #road.draw_Road(  fig , ax )
    #
    #     points = road.points
    #
    #
    #
    #
    #
    #
    #
    #     new_points = points.copy()
    #     #points = new_points
    #
    #     Y = []
    #     X = []
    #
    #     for point in points:
    #         x, y = point
    #
    #         if y != None:
    #             Y.append(y)
    #             X.append(x)
    #
    #
    #     plt.scatter(X,Y) 
    #
    #     opt_points_X = X
    #     opt_points_Y = Y
    #
    #     ax.plot(X , Y , color="k")
    #
    #     #points.reverse()
    #     ##print(points)
    #
    #     #new_points.remove(new_points[7])
    #     #new_points.remove(new_points[8])
    #
    #     ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(new_points  )
    #
    #
    #     ##print("#############################################  " , i)
    #     for ele in ReferenceLine.geometry_elements:
    #         #print("ele : " , ele.__class__.__name__)
    #         #print("length", ele.length )
    #
    #         try:
    #             #print("Curvatur" , ele.Curvatur )
    #
    #         except:
    #             pass
    #
    #         try:
    #             #print("CurvaturStart" , ele.CurvaturStart )
    #             #print("CurvaturEnd" , ele.CurvaturEnd )
    #         except:
    #             pass
    #
    #
    #     #F_end = ReferenceLine.optimize(opt_points_X, opt_points_Y)
    #
    #     ###print(F_end)
    #
    #     S = ReferenceLine.getLength()
    #
    #     xy = []
    #     for ele in np.arange(0,S  +0.1,0.1):
    #         xy.append(ReferenceLine.ST2XY(ele,0))
    #     plt.plot(*zip(*xy))
    #
    #
    #     #plt.show()
    #     plt.savefig(f"./road_{i}.png")
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    # x0 = 0
    # y0 = 0
    # hdg =   -np.pi  
    #
    # length = 200.0
    # Radius = 50.0
    # geometry_elements = [ StraightLine(length) , Spiral(length/3, CurvaturStart = 0, CurvaturEnd = 1/Radius)  ,   Arc( length/3,  1/ Radius) , Spiral(length/3, CurvaturStart = 1/Radius, CurvaturEnd =0 )   ,StraightLine(length) ]
    # #) , StraightLine(length) ,  Arc(length,  -  Radius) , , StraightLine(length) ,Arc(length,   Radius)  , StraightLine(length) Arc(length,   Radius), StraightLine(length) ,   Arc(length,   Radius)  ,     StraightLine(length) ,  Arc(length,  Radius ),  Arc(length,  Radius),  ,,   )  , StraightLine(length) ,  Arc(length,  Radius )
    # refObj = RoadReferenceLine(x0, y0, hdg, geometry_elements)
    #
    #
    # S = np.arange(0.0,refObj.getLength() ,1)
    #
    # points =[]
    #
    #
    # Y = []
    # X = []
    #
    # for s in S:
    #     x, y = refObj.ST2XY(s,0)
    #
    #     if y != None:
    #         Y.append(y)
    #         X.append(x)
    #         points.append((x, y))
    #
    # plt.scatter(X,Y) 
    #
    # opt_points_X = X
    # opt_points_Y = Y
    #
    #
    #
    # ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(points )
    #
    #
    #
    # ##print(x0 , y0  , hdg )
    #
    # ##print(ReferenceLine.__dict__)
    #
    #
    # for ref in [refObj ,ReferenceLine ]:
    #     ##print("#############################################")
    #     for ele in ref.geometry_elements:
    #         ##print("ele : " , ele.__class__.__name__)
    #         ##print("length", ele.length )
    #
    #         try:
    #             ##print("Curvatur" , ele.Curvatur )
    #
    #         except:
    #             pass
    #
    #         try:
    #             ##print("CurvaturStart" , ele.CurvaturStart )
    #             ##print("CurvaturEnd" , ele.CurvaturEnd )
    #         except:
    #             pass
    #
    #
    # xy = []
    # for ele in S:
    #     xy.append(ReferenceLine.ST2XY(ele,0))
    # plt.plot(*zip(*xy))
    #
    #
    # plt.show()      
    

    
    
    
