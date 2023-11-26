'''
Created on 03.11.2023

@author: abdel
'''

from OSM_Interface import  osm_map as  osm_map
import os #, math
import ctypes, sys
from pyproj import CRS, Transformer
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon , Rectangle
import matplotlib as mpl
import numpy as np
from math import isclose 
import random
from scipy.optimize import minimize
from pickletools import optimize
 
import copy

projection_fromGeographic_cash = dict()
clear = lambda: os.system('cls')


def define_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    
    
    
    
    
    x_start, y_start = p1
    x_midel, y_midel = p2          
    x_end  , y_end   = p3   
    
    deltax1 = x_midel - x_start
    deltax2 = x_end   - x_midel     
    
    deltay1 = y_midel - y_start
    deltay2 = y_end   - y_midel             
            
    
 
    
    
    if deltax1  == 0:
        
        if  deltay1 > 0:
            hdg1 = np.pi/2
        else:
            hdg1 = -np.pi/2                    
        
    else:
    
        hdg1 =  np.arctan2( deltay1 ,deltax1 )
    
    
    if deltax2  == 0:
        
        if  deltay2 > 0:
            hdg2 = np.pi/2
        else:
            hdg2 = -np.pi/2                    
        
    else:
    
        hdg2 =  np.arctan2( deltay2 ,deltax2 )    
    
    
    
    
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    
    if abs(det) < 1.0e-6:
        return ((None,None), np.inf)
    
    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    
    if hdg2 >hdg1     :
 
        radius = -1.0 *radius
        #print(radius)    
        
    return ((cx, cy), radius)

def projection_fromGeographic(latitude, longitude, referenceLat = 0 , referenceLon = 0):
    
    # see conversion formulas at
    # http://en.wikipedia.org/wiki/Transverse_Mercator_projection
    # and
    # http://mathworld.wolfram.com/MercatorProjection.html
    
    # radius = 6378137
    # k = 1
    #
    # self_lon =   referenceLon
    # self_lat =   referenceLat
    # self_latInRadians = math.radians(self_lat)
    # lat = math.radians(latitude)
    # lon = math.radians(longitude-self_lon)
    # B = math.sin(lon) * math.cos(lat)
    # x1 = 0.5 * k * radius * math.log((1+B)/(1-B))
    # y1 = k * radius * ( math.atan(math.tan(lat)/math.cos(lon)) - self_latInRadians )
    
 
        # crs_4326  = CRS.from_epsg(4326) # epsg 4326 is wgs84
        #
        # uproj = CRS.from_proj4("+proj=tmerc +lat_0={0} +lon_0={1} +x_0=0 +y_0=0 +ellps=GRS80 +units=m".format(referenceLat, referenceLon))
        # transformer = Transformer.from_crs(crs_4326, uproj)
        #
        # x,y = next(transformer.itransform([(latitude,longitude)]))
        #
        #     # radius = 6378137
 
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




class Building():
 
    @classmethod
    def fromOSMdict(cls, dictobj , Building_id):
 
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
        
        
        
        for node in dictobj.get('nodes'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["nodes_info"].append(node)
              
 
         
        return Building(Building_id, Floor_plan, tags  )  
        
         
 
    
    def __init__(self ,Building_id , Floor_plan =[] , tags = dict() ):
        
        self.object_id = Building_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
 
        
        
    def draw_building(self, fig , ax ):
        
        xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        ax.plot(xs,ys)
        
        facecolor = 'gray'
        if 'roof:colour' in self.tags.keys():
            facecolor = self.tags.get('roof:colour')
            
        elif  'building:colour' in self.tags.keys():
            facecolor = self.tags.get('building:colour')
            
        elif  'colour' in self.tags.keys():
            facecolor = self.tags.get('colour')        
        
        
        
        try:
            p = Polygon(self.Floor_plan, facecolor = facecolor) 
            
        except:
            p = Polygon(self.Floor_plan, facecolor = 'gray')             
        ax.add_patch(p)
        

class AreaSpace():
 
    @classmethod
    def fromOSMdict(cls, dictobj , ParkingSpace_id ,  min_x, min_y ,max_x, max_y):
 
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
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
                
     
                
                if len(node.get("tags").keys()) > 0:
                    tags["nodes_info"].append(node)
              
 
        return AreaSpace(ParkingSpace_id, Floor_plan, tags )  
        
         
 
    
    def __init__(self ,ParkingSpace_id , Floor_plan =[] , tags = dict()  ):
        
        self.object_id = ParkingSpace_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
       
        
    def draw_Space(self, fig , ax ):
        
        xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        ax.plot(xs,ys)
        
        facecolor = 'y'
 
        
        p = Polygon(self.Floor_plan, facecolor = facecolor) 
        ax.add_patch(p)

class Waterway():
 
    @classmethod
    def fromOSMdict(cls, dictobj , waterway_id ,  min_x, min_y ,max_x, max_y):
 
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
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
                
     
                
                if len(node.get("tags").keys()) > 0:
                    tags["nodes_info"].append(node)
 
 
         
        return Waterway(waterway_id, Floor_plan, tags )  
        
         
 
    
    def __init__(self ,waterway_id , Floor_plan =[] , tags = dict() ):
        
        self.object_id = waterway_id
        self.Floor_plan = Floor_plan 
 
        self.tags = tags 
       
        
    def draw_Space(self, fig , ax ):
        
 
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

  
class Barrier_roadObject():
 
    @classmethod
    def fromOSMdict(cls, dictobj , barrier_id):
        # print(" ############## Building #################")
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
        for node in dictobj.get('nodes'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["nodes_info"].append(node)
              
 
         
        return Barrier_roadObject(barrier_id, Floor_plan, tags )  
        
         
 
    
    def __init__(self ,barrier_id , Floor_plan =[] , tags = dict()   ):
        
        self.object_id = barrier_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
          
    def draw_Barrier(self, fig , ax ):
        
 
        facecolor = 'g'
        if 'colour' in self.tags.keys():
            facecolor = self.tags.get('colour')
 
        try:
            p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5) 
            
        except:
            facecolor = 'g'
            p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5)             
        ax.add_patch(p)
 
 
 
        
        
        


class StraightLine():
    
 
    
    def __init__(self,    length=1):
        
 
        self.length = length
        
 
                 
    def XY2ST(self, x0 , y0 ,hdg , X , Y ,S0):
 
        deltaX= np.array(X - x0 ).astype(float)
        deltaY= np.array(Y - y0 ).astype(float)
        L = np.sqrt(  deltaX * deltaX    + deltaY *deltaY  ) 
        # if L > self.length*2:
        #     return (None , None)
        # else:
        alfa  =  np.arctan2(deltaY ,deltaX )
        theta = hdg  - alfa
        S = L*np.cos(theta) +S0
        T = L*np.sin(theta)   
             
        return  (S,T)               
        
        
        
        

 
    
    def ST2XY(self, x0 , y0 ,hdg,  S , S0 , T):
        
        
        hdg = hdg  
        delta_s = S - S0
        
        if delta_s > self.length:
            return (None ,None)
        
        else: 
            alfa = np.pi/2.0  - hdg  
            
            x =  x0 + delta_s*np.cos(hdg)  
            y =  y0 + delta_s*np.sin(hdg)     
        
            x = x + T*np.cos(alfa )
            y = y - T*np.sin(alfa )
                     
     
            
            return (x , y) 
 
    
    
    def get_endPoint(self, x0 , y0 ,hdg):
        
        x_end = x0 + self.length* np.cos( hdg)
        y_end = y0 + self.length* np.sin( hdg)        
        hdg_end = hdg
    
        return (x_end ,y_end , hdg_end )
    
    

    def EvalX( self,  x0 , y0 , hdg , X ):
        
        Y= y0 + (X - x0)*np.tan(hdg)
        return Y
   
    # @classmethod    
    # def fit( cls, x0, y0, hdg , opt_points_X , opt_points_Y ):
    #
    #     length=0   
    #
    #
    #     for index ,point_x in enumerate( opt_points_X[0:-1] ):
    #
    #         point_y = opt_points_Y[index]
    #
    #         x_end = opt_points_X[index+1]
    #         y_end = opt_points_Y[index+1]
    #
    #         deltaX = np.array( x_end - point_x ).astype(float)
    #         deltaY = np.array( y_end - point_y ).astype(float)
    #
    #         length  = length +  np.sqrt( deltaX*deltaX   +  deltaY *deltaY  ) 
    #
    #
    #     def cost_func(Radius , x0, y0, hdg , opt_points_X , opt_points_Y ):
    #
    #
    #         arc = Arc(length, Radius)    
    #         X = np.array(opt_points_X)
    #         Y = np.array(opt_points_Y)
    #
    #         refObj.get_endPoint()
    #         S0 = 0
    #         S ,T = arc.XY2ST(x0 , y0 ,hdg , X ,Y, S0)
    #
    #
    #         eror = T
    #
    #
    #
    #         eror=  eror.astype(float)
    #
    #         ls_error =   np.sum(  eror *eror)  
    #
    #         return   ls_error    
    #
    #
    #
    #     geometry_elements = []
    #
    #     refObj = RoadReferenceLine(x0, y0, hdg, geometry_elements)
    #     bnds = (  (None, None))                                  
    #     func = lambda x : cost_func(x  ,  x0, y0, hdg , opt_points_X , opt_points_Y) 
    #
    #     radius0 = 1
    #
    #     res = minimize(func, np.array([ radius0 ]) , method='SLSQP' , tol=1e-100, options={'maxiter':100 ,'gtol': 1e-100, 'disp': False})
    #
    #     res_radius = res.x[0]
    #
    #
    #
    #     ls_error = res.fun
    #     t(res)
    #     print(ls_error) 
    #
    #     #if length == None:
    #
    #     radius =  res_radius  
    #
    #     newele=  Arc(length ,  radius     ) 
    #     print( "radius0",radius )
    #
    #
    #     return newele , ls_error   
class Arc():




    
    def __init__(self, length=1 , Radius = 1 ):
        
        self.length =length
        self.Radius = Radius
 
 


    def ST2XY(self, x0 , y0 ,hdg, S ,S0 ,T):
        
        hdg = hdg - int(hdg/(2*np.pi) ) *2*np.pi

        alfa =   np.pi/2  - hdg
 
        x_center = x0 +self.Radius*np.sin( np.pi- hdg)
        y_center = y0 +self.Radius*np.cos( np.pi-  hdg)
        
        delta_s = S - S0 
        
        # if delta_s > self.length*2:
        #     return (None , None)
        # else:        
        
        theta =  (delta_s /(self.Radius + np.finfo(float).eps)) 
        theta  = theta - int(theta/(2*np.pi) ) *2*np.pi
        hdg_end =    hdg-theta
 
        xs =  x_center + self.Radius*np.cos( np.pi-  alfa -theta )    
        ys =  y_center + self.Radius*np.sin( np.pi- alfa - theta )   
        
        
        xs = xs + T*np.sin(np.pi  - hdg_end )
        ys = ys + T*np.cos(np.pi  - hdg_end )
           
        
        return (xs , ys) 

    def EvalX( self,  x0 , y0 , hdg , X ):
        hdg = hdg - int(hdg/(2*np.pi) ) *2*np.pi

        #alfa =   np.pi/2  - hdg
 
        x_center = x0 +self.Radius*np.sin( np.pi- hdg)
        y_center = y0 +self.Radius*np.cos( np.pi-  hdg)
        
        
        R = self.Radius
        
        
         
        Y = np.sqrt( R*R - (X - x_center)*(X - x_center) ) + y_center

        return Y
    
    def get_endPoint(self, x0 , y0 ,hdg):
        
        #if self.Radius > 0:
        
        hdg = hdg - int(hdg/(2*np.pi) ) *2*np.pi
        alfa =   np.pi/2  - hdg
 
        x_center = x0 +self.Radius*np.sin( np.pi- hdg)
        y_center = y0 +self.Radius*np.cos( np.pi-  hdg)

        
        delta_s = self.length
        
        
        theta =  (delta_s /(self.Radius + np.finfo(float).eps)) 
        
        try:    
        
            theta  = theta - int(theta/(2*np.pi) ) *2*np.pi
            
        except:
            print(theta)
            theta  = theta 
            
        
        x_end =  x_center + self.Radius*np.cos(np.pi - alfa -theta )   
        y_end =  y_center + self.Radius*np.sin(np.pi - alfa -theta)
              
        hdg_end =    hdg-theta
    
        return (x_end ,y_end , hdg_end )
        
 
    def XY2ST(self, x0 , y0 ,hdg , X ,Y, S0):
        

        hdg = hdg - int(hdg/(2*np.pi) ) *2*np.pi        
 
        x_center = x0 +self.Radius*np.sin( np.pi- hdg)
        y_center = y0 +self.Radius*np.cos( np.pi-  hdg)
        
        #print("x_center" , x_center)
        #print("y_center" , y_center)   
        
             
        deltaX= np.array( X - x_center ).astype(float)
        deltaY= np.array( Y - y_center ).astype(float)
        L = np.sqrt(  deltaX * deltaX    + deltaY *deltaY  )  
        
        #print("L" ,L)
        if self.Radius >   0:
 
            T =   self.Radius -L      
            
            alfa =   np.pi/2  - hdg
            
            gama  =  np.arctan2(deltaY ,deltaX ) 
     
            theta =      (np.pi  -  alfa   -  gama  )
        
            theta  = theta - int(theta/(2*np.pi) ) *2*np.pi
        
        else:
            T =   self.Radius +L      
            
            alfa =     hdg
            
            gama  =  np.pi/2  -np.arctan2( deltaY ,deltaX ) 
     
            theta =     (np.pi  -  alfa   -  gama  ) 
        
            theta  = np.abs(theta) - int(theta/(2*np.pi) ) *2*np.pi
        
        #print("T" ,T)
        # if theta < 0:
        #     theta  = 2*np.pi + theta
        
        #print("theta" , theta) 
        
        L_circl = theta   *np.abs( self.Radius)
        #print("L_circl" , L_circl)
        #print("self.length" , self.length)        
        
        # if L_circl > self.length:
        #     return (None , None)
        # else:
            
        S =  L_circl+ S0
 
        return (S,T)

class RoadReferenceLine():

    # @classmethod  
    # def fitRoadReferenceLine(cls, points ,x0 = None, y0 =None , hdg = None  , maxiter = 1000  ):
    #
    #
    #
    #
    #
    #
    #     #ls_error_max_error = 1.0/1000000 
    #     x0_start = x0
    #     y0_start = y0        
    #     hdg_start = hdg
    #
    #
    #     if x0 is None or y0 is None:
    #         x0, y0 = points[0]
    #         x0_start = x0
    #         y0_start = y0
    #
    #     x1, y1 = points[1] 
    #
    #
    #     deltax = x1 - x0_start
    #     deltay = y1   - y0_start     
    #
    #     if hdg is None:
    #         if deltax  == 0   :
    #
    #             if  deltay > 0:
    #                 hdg = np.pi/2
    #             else:
    #                 hdg = -np.pi/2                    
    #
    #         else:
    #
    #             hdg =  np.arctan2( deltay ,deltax ) 
    #
    #     hdg_start = hdg
    #
    #     point_0 = points[0]
    #
    #
    #     x_0  , y_0   = point_0  
    #
    #     opt_points_X.append( x_0 ) 
    #     opt_points_Y.append( y_0 )    
    #     L = 0
    #
    #     for Point_index in range(1 , len(points),1):
    #
    #         point_start = points[Point_index]
    #
    #         x_start  , y_start    = point_start
    #
    #         point_End = points[Point_index]
    #
    #
    #         x_end  , y_end   = point_End  
    #
    #
    #         deltaX= np.array( x_end - x_start ).astype(float)
    #         deltaY= np.array( y_end - y_start ).astype(float)
    #         L = L + np.sqrt(  deltaX * deltaX    + deltaY *deltaY  )
    #
    #         opt_points_X.append(x_end) 
    #         opt_points_Y.append(y_end)
    #
    #
    #
    #
    #     geometry_elements =[]
    #
    #
    #     referenceLine = RoadReferenceLine(x0_start, y0_start, hdg_start, geometry_elements)
    #
    #     f_result_old = None 
    #     for n_ele   in range(0,10):
    #
    #
    #
    #         referenceLine.addStraightLine(length = L/2)
    #         referenceLine.addArc(length = L/2, Radius = 100)
    #
    #         f_result = referenceLine.optimize(opt_points_X, opt_points_Y, maxiter)
    #
    #         #referenceLine.cleanUp()
    #
    #         f_result = referenceLine.optimize(opt_points_X, opt_points_Y, maxiter)
    #
    #         print("n_ele :" , n_ele , "F = " ,f_result )
    #
    #         if f_result_old is None:
    #             f_result_old = f_result
    #             referenceLine_save = copy.deepcopy(referenceLine)
    #
    #         elif f_result < f_result_old:
    #             referenceLine_save = copy.deepcopy(referenceLine)
    #
    #     return referenceLine_save
    
    @classmethod  
    def fitRoadReferenceLine(cls, points ,x0 = None, y0 =None , hdg = None  , maxiter = 500  ):
    
        
        avrag_dist_soll = 1
        
        print("dist ....")
        #while  min_dist >  avrag_dist_soll:
        x0_start = x0
        y0_start = y0        
 
        points = copy.deepcopy(points)
    
        if x0 is None or y0 is None:
            x0, y0 = points[0]
            x0_start = x0
            y0_start = y0
        
        
        
        
        for _ in range(0,10):
        
            for index in range(len(points)-2,-1 ,-1): 
        
                x_start , y_start  = points[index+1]
                x_end   , y_end    = points[index]
        
                deltaX= (x_end -x_start ).astype(float)
                deltaY= (y_end -y_start ) .astype(float)
        
        
                segmant_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
                
 
                
                if segmant_lenght > avrag_dist_soll:
                    
 
                    
                    angle= np.arctan2(deltaY ,deltaX)
            
                    x_new = x_start +  segmant_lenght/2.0*np.cos(angle) 
                    y_new = y_start +  segmant_lenght/2.0*np.sin(angle) 
            
                    points.insert(index+1, (x_new ,y_new ))    
                    
        if len(points) < 2:
            
            geometry_elements =[]
            
            if hdg is None:
                hdg_start = 0
            
            else:
                hdg_start = hdg                
            return RoadReferenceLine(x0_start, y0_start, hdg_start, geometry_elements)    
        #ls_error_max_error = 1.0/1000000 

    
        x1, y1 = points[1] 
    
    
        deltax = x1 - x0_start
        deltay = y1   - y0_start     
    
        if hdg is None:
            if deltax  == 0   :
    
                if  deltay > 0:
                    hdg = np.pi/2
                else:
                    hdg = -np.pi/2                    
    
            else:
    
                hdg =  np.arctan2( deltay ,deltax ) 
    
        hdg_start = hdg
    
    
        print("points ....")
    
        geometry_elements =[]
    
    
        referenceLine = RoadReferenceLine(x0_start, y0_start, hdg_start, geometry_elements)
    
        opt_points_X = [x0_start , x1 ]
        opt_points_Y = [y0_start , y1 ]
    

        opt_points_X_all = []
        opt_points_Y_all = [  ]    
    
        for Point_index in range(0 , len(points),3):
            point_End = points[Point_index]
            x_end  , y_end   = point_End 
            opt_points_X_all.append(x_end) 
            opt_points_Y_all.append(y_end)    
            
    
        print("profile ....")
    
        if len(points) == 2:
    
            length = np.sqrt( deltax*deltax   +  deltay*deltay  )  + 10
            referenceLine.addStraightLine(length) 
            x_end, y_end = x1 , y1
    
    
        for Point_index in range(0 , len(points)-2,1):
            index_1 = Point_index+1
            index_2 = Point_index+2
    
            #referenceLine_save = copy.deepcopy(referenceLine)   
    
    
            #point_0 = (x0 ,y0)
            point_start =   points[Point_index]
            point_midel = points[index_1]
            point_End = points[index_2]
    
    
    
    
            x_start, y_start = point_start
    
            referenceLine.set_endPoint(x_start, y_start)
    
            x0 , y0 , hdg0  = referenceLine.get_endPoint()    
    
            x_midel, y_midel = point_midel          
            x_end  , y_end   = point_End  
    
            opt_points_X.append(x_end) 
            opt_points_Y.append(y_end)
    
            deltax1 = x_midel - x_start
            deltay1 = y_midel - y_start
            
            # deltax2 = x_end   - x_midel 
            # deltay2 = y_end   - y_midel             
            # if deltax1  == 0:
            #
            #     if  deltay1 > 0:
            #         hdg1 = np.pi/2
            #     else:
            #         hdg1 = -np.pi/2                    
            #
            # else:
            #
            #     hdg1 =  np.arctan2( deltay1 ,deltax1 )    
            #
            #
            #
            # if deltax1  == 0:
            #
            #     if  deltay1 > 0:
            #         hdg1 = np.pi/2
            #     else:
            #         hdg1 = -np.pi/2                    
            #
            # else:
            #
            #     hdg1 =  np.arctan2( deltay1 ,deltax1 )
            #
            #
            # if deltax2  == 0:
            #
            #     if  deltay2 > 0:
            #         hdg2 = np.pi/2
            #     else:
            #         hdg2 = -np.pi/2                    
            #
            # else:
            #
            #     hdg2 =  np.arctan2( deltay2 ,deltax2 )                   
    
             
    
            #
            # if        isclose(hdg0, hdg1, abs_tol=1e-3) and isclose(hdg2, hdg0, abs_tol=1e-3) and isclose(hdg1, hdg2, abs_tol=1e-6)    : #  or   or 
            #     #line
            #
            #     referenceLine.addStraightLine(length) 
            #
            #
            #
            # else:
            #     #arc   
            (cx, cy), Radius = define_circle(point_start, point_midel, point_End)
 
            if Radius != np.inf:
                
                
                
                hdg0 = hdg0 - int(hdg0/(2*np.pi) ) *2*np.pi        
   
                deltaX= np.array( x_midel - cx ).astype(float)
                deltaY= np.array( y_midel - cy ).astype(float)
  
                
                #print("L" ,L)
                if Radius >   0:
         
     
                    
                    alfa =   np.pi/2  - hdg0
                    
                    gama  =  np.arctan2(deltaY ,deltaX ) 
             
                    theta =      (np.pi  -  alfa   -  gama  )
                
                    theta  = theta - int(theta/(2*np.pi) ) *2*np.pi
                
                else:
     
                    
                    alfa =     hdg0
                    
                    gama  =  np.pi/2  -np.arctan2( deltaY ,deltaX ) 
             
                    theta =     (np.pi  -  alfa   -  gama  ) 
                
                    theta  = np.abs(theta) - int(theta/(2*np.pi) ) *2*np.pi
                
 
                
                L_circle = theta   *np.abs(  Radius)
                
 

                referenceLine.addArc(L_circle, Radius) 


            else:
                length = np.sqrt( deltax1*deltax1   +  deltay1 *deltay1  ) 
                referenceLine.addStraightLine(length)    
    
    
    
    
            referenceLine.set_endPoint(x_midel, y_midel)
    
        print("optimize ....")            
    
        F_end0 = referenceLine.optimize(opt_points_X, opt_points_Y, maxiter)



        if F_end0 >  1e-2    :

            print("###########################################################################################")
            print("###########################################################################################")
            print("###########################################################################################")
            print("###########################################################################################")
            print("###########################################################################################")

            F_end_clc= 0
            for Point_index in range(0 , len(points),1):
                point = points[Point_index]
                x , y = point
                
                _,T = referenceLine.XY2ST(x, y)
                
                F_end_clc = F_end_clc +T*T*10
                
                if F_end_clc >  1e-2 :
                    Point_index  = Point_index - 1
                    
                    end_point = points[Point_index]
                    X_end , Y_end = end_point
                    referenceLine.set_endPoint(X_end, Y_end)
                    
                    referenceLine.get_endPoint()
                    
                    X_end, Y_end = points[ Point_index]
 
                    x0_start , y0_start ,hdg_start =  referenceLine.get_endPoint()
                    
                    part2 = points[Point_index: ] 
                    print("part2")
                
                    ref_part2 = RoadReferenceLine.fitRoadReferenceLine(points = part2,  x0 = x0_start, y0  =y0_start, hdg =  hdg_start,   maxiter = maxiter)    
                    
                    referenceLine.geometry_elements = referenceLine.geometry_elements + ref_part2.geometry_elements 
                    
                    F_end0 = referenceLine.optimize(opt_points_X, opt_points_Y, maxiter)
                    
                    break                    
                    
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            # if len(points) > 15:
            #
            #     Point_index = int( len(points) /3)
            #     part1 = points[0:Point_index]
            #     part2 = points[Point_index:2*Point_index]            
            #     part3 = points[2*Point_index:] 
            #
            #     #referenceLine_save = copy.deepcopy(referenceLine)
            #     print("part1")            
            #
            #     ref_part1 = RoadReferenceLine.fitRoadReferenceLine(points = part1, x0 = x0_start, y0  =y0_start, hdg =  hdg_start, maxiter = maxiter)
            #     X_end, Y_end = points[ Point_index]
            #     ref_part1.set_endPoint(X_end, Y_end)
            #     X0 , Y0 ,Hdg0 =  ref_part1.get_endPoint()
            #
            #     print("part2")
            #
            #     ref_part2 = RoadReferenceLine.fitRoadReferenceLine(points = part2,   maxiter = maxiter)    
            #
            #     X_end, Y_end = points[ 2*Point_index]
            #     ref_part2.set_endPoint(X_end, Y_end)
            #
            #     X0 , Y0 ,Hdg0 =  ref_part2.get_endPoint()   
            #
            #     print("part3")
            #
            #     ref_part3 = RoadReferenceLine.fitRoadReferenceLine(points = part3,   maxiter = maxiter)  
            #     X_end, Y_end = points[ -1]
            #     ref_part3.set_endPoint(X_end, Y_end)    
            #
            #     referenceLine.geometry_elements = ref_part1.geometry_elements + ref_part2.geometry_elements + ref_part3.geometry_elements 
            #
            # else:
            #     Point_index = int( len(points) /2)
            #     part1 = points[0:Point_index]
            #     part2 = points[Point_index: ]            
            #
            #
            #     #referenceLine_save = copy.deepcopy(referenceLine)
            #     print("part1")            
            #
            #     ref_part1 = RoadReferenceLine.fitRoadReferenceLine(points = part1,  maxiter = maxiter)
            #     X_end, Y_end = points[ Point_index]
            #     ref_part1.set_endPoint(X_end, Y_end)
            #     X0 , Y0 ,Hdg0 =  ref_part1.get_endPoint()               
            #
            #
            #     print("part2")
            #
            #     ref_part2 = RoadReferenceLine.fitRoadReferenceLine(points = part2,   maxiter = maxiter)                    
            #     X_end, Y_end = points[ -1]
            #     ref_part2.set_endPoint(X_end, Y_end) 
            #
            #     referenceLine.geometry_elements = ref_part1.geometry_elements + ref_part2.geometry_elements  
                    
                
        if len(referenceLine.geometry_elements) == 0:
            
            print("******************************************************************")
            print("******************************************************************")
            print("*************************XXXXXXXXXXXXXXX**************************")
            
                        
            referenceLine.addStraightLine(1)
            referenceLine.addArc(1, 1)
            referenceLine.addStraightLine(1)
            referenceLine.addArc(1, 1)
            referenceLine.addStraightLine(1)
            referenceLine.addArc(1, 1)
            referenceLine.addStraightLine(1)
                        
            referenceLine.optimize(opt_points_X, opt_points_Y, maxiter)
                    
                
        if not ( F_end0 <  1e-2) :  
            
            print("-------------->final opt<--------------------")
            endpoint = points[-1] 
            x_end  , y_end   = endpoint
            referenceLine.set_endPoint(x_end, y_end)            
            F_end = referenceLine.optimize(opt_points_X , opt_points_Y , maxiter *10)
            
            referenceLine_save = copy.deepcopy(referenceLine)
            referenceLine.cleanUp()
            
            
            F_end2=  referenceLine.optimize(opt_points_X , opt_points_Y , maxiter*10)
            
     
            
            if F_end < F_end2:
                referenceLine = referenceLine_save
                
        referenceLine.set_endPoint(x_end, y_end)
        
        return referenceLine
                #reset
    
    
                      
            
 
 
    
    def __init__(self, x0=0, y0=0 , hdg  = 0 , geometry_elements = [] ):
        
        self.x0 = x0 
        self.y0 = y0
        self.hdg = hdg
        self.geometry_elements = geometry_elements
        
    
    
    def optimize(self,opt_points_X ,opt_points_Y,  maxiter = 1000):
            
            # self.x0 = opt_points_X[0]
            # self.y0 = opt_points_Y[0]  
            
        return 0
            
        
        F_end = None   
        if len(self.geometry_elements) > 0:
            
            x0 =[]
    
            bnds = ()
            index = 0
            for obj in self.geometry_elements:
    
                objectIndex  = []
                objectvalues  = []
    
                for key in obj.__dict__.keys():
    
                    objectIndex.append(index)
                    x0_ele = obj.__dict__.get(key)
                    objectvalues.append(x0_ele)
    
                    index =index +1
    
                    if key == "length":
                        bnds = bnds + ( (0,x0_ele*2), )
                    elif key == "Radius":
                        bnds = bnds + ((-100,100),)
    
 
                x0 =x0 + objectvalues
    
            #print(excludIndex)     
            # print(x0)            
            # print(bnds)
    
            def cost_func(opt_paramter ,   opt_points_X , opt_points_Y ):
    
 
                index = 0           
                for obj in self.geometry_elements:
                    for key in obj.__dict__.keys():
                        setattr(obj, key, opt_paramter[index])
                        index =index +1
    
    
    
                eror = []
    
                for index in  range( 0 , len(opt_points_X) ):
                    X = opt_points_X[index]
                    Y = opt_points_Y[index]           
                    _ ,T = self.XY2ST(  X ,Y )
                    
 
                    eror.append( T*T )
    
                
                
                x_end =opt_points_X[-1] 
                y_end =opt_points_Y[-1] 
                
                x_end_ist , y_end_ist , hdg = self.get_endPoint()
                
                eror.append( (x_end -x_end_ist )*(x_end -x_end_ist) *100)
                eror.append( (y_end -y_end_ist )*(y_end -y_end_ist) *100)                
    
                eror = np.array( eror )
    
                eror=  eror.astype(float)
                ls_error =   np.sum(  eror )  
                return   ls_error 
    
    
            func = lambda x : cost_func(x  ,  opt_points_X , opt_points_Y) 
            #x0_save = x0.copy()
            
            
            
            
    
            res = minimize(func, x0 , method='SLSQP',   bounds= bnds  , tol=1e-20,options={'maxiter':maxiter   , 'disp': True} )#,   bounds= bnds 
            print(res)
            
            status = res.status
            F_end = res.fun
            if status == 9 and F_end > 0.01:
                x0 = res.x
                res = minimize(func, x0 , method='SLSQP' ,   bounds= bnds , tol=1e-20 ,  options={'maxiter':maxiter   , 'disp': True}) # bounds= bnds,
                print(res)
                
            

            x_end = opt_points_X[-1] 
            y_end   = opt_points_Y[-1] 
            self.set_endPoint(x_end, y_end)

            
        return F_end
        
    
    def addStraightLine(self, length):
        
        if len(self.geometry_elements )  ==0:
            self.geometry_elements.append(StraightLine(length)) 
            
        elif not isinstance(self.geometry_elements[-1], StraightLine):
            self.geometry_elements.append(StraightLine(length)) 
        else:
            self.geometry_elements[-1].length  = self.geometry_elements[-1].length + length 
                        


    def addArc(self, length, Radius ):
        
        if len(self.geometry_elements )  ==0:
            self.geometry_elements.append(Arc(length, Radius) ) 
            
        elif not isinstance(self.geometry_elements[-1], Arc):
            self.geometry_elements.append(Arc(length, Radius)) 
        elif not    isclose(self.geometry_elements[-1].Radius, Radius, abs_tol=1e-1)  :
            self.geometry_elements.append(Arc(length, Radius))  
        elif Radius == np.inf:
            
            self.addStraightLine(length)
         
        else:
            self.geometry_elements[-1].length  = self.geometry_elements[-1].length + length 
    
    
    
    def cleanUp(self):
        
        indexList = []
        if len(self.geometry_elements )  >1:
            for index , ele in enumerate(self.geometry_elements ):
                if ele.length < 1:
                    indexList.append(index)
                    
        for index in indexList:
            
            ele =  self.geometry_elements[index]
            if index >0:
                self.geometry_elements[index-1].length = self.geometry_elements[index-1].length  + ele.length
            else:
                self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length                    
        indexList.reverse()
        for index in indexList :
            ele =  self.geometry_elements[index]
            self.geometry_elements.remove(ele)
        
            
        indexList = []
        if len(self.geometry_elements )  >1:
            for index , ele in enumerate(self.geometry_elements[:-1] ):
                if  type(ele) == type(self.geometry_elements[index +1]):
                    indexList.append(index)
                    
       
        
        indexList_toremove = []
        for index in indexList:
            
            ele =  self.geometry_elements[index]
            
            if isinstance(ele, StraightLine):
                self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length 
                indexList_toremove.append(index)                
                
                if  isclose(0 , ele.length, abs_tol=1e-3): 
                    indexList_toremove.append(index)  
               
            elif isinstance(ele, Arc):
                if isclose(self.geometry_elements[index+1].Radius, ele.Radius, abs_tol=1e-1):
                    self.geometry_elements[index+1].length = self.geometry_elements[index+1].length  + ele.length 

                    indexList_toremove.append(index)            
                    
                elif  isclose(0 , ele.Radius, abs_tol=1e-3): 
                    indexList_toremove.append(index)  
                    
                elif  isclose(0 , ele.length, abs_tol=1e-3): 
                    indexList_toremove.append(index)                                      
                      
        
        indexList_toremove = list(set(indexList_toremove))            
        indexList_toremove.sort()
        indexList_toremove.reverse()
        
            
        if len(indexList_toremove) < len(self.geometry_elements):
        
            for index in indexList_toremove :
                ele =  self.geometry_elements[index]
                self.geometry_elements.remove(ele)
                
        else:
            self.addStraightLine(1)
            
                        
    
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
                    
                
                
                
        
        #print( S  )
        indextoremove.sort()
        indextoremove.reverse()
        for index in indextoremove:
            self.geometry_elements.remove(self.geometry_elements[index])
            
        
        if S is not None and len(self.geometry_elements ) >= 1 and  (S - S0 ) > 0:
            
            
            self.geometry_elements[-1].length = S - S0               
        
        
            
    
    def ST2XY(self, S ,T):

        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
        S0 = 0
        
        ele = None
        
        for ele in self.geometry_elements:
            
            if S - S0 < ele.length:
                
                return ele.ST2XY(  x0 , y0 , hdg ,  S ,S0,T )
            
            else:
                
                x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )
                
                S0 = S0 + ele.length
            
        
        
        #x_end , y_end , hdg  = self.get_endPoint()
        
        
        if ele is not None:
        
            return ele.ST2XY(  x0 , y0 , hdg ,  S ,S0,T )
        
        else:
            return (S,T)
        
        
        
    def EvalX(self, X):

        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
        S0 = 0
        
        ele = None
        
        Y =[]
        
        for ele in self.geometry_elements:
                
                
                
                y = ele.EvalX(  x0 , y0 , hdg , X )
                
 
                if  not np.isnan(y)   : 
                    Y.append(y )
               
                else:
                    Y.append(X )
                    
         
        return np.array(Y)  
        
 
        
    def XY2ST(self, X , Y):
    
        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
    
        S0 = 0
        
        S_list =[]
        T_list =[]  
        
              
        for ele in self.geometry_elements:
            
 
            
            (S,T)= ele.XY2ST(  x0 , y0 ,hdg , X ,Y, S0)
            
            if  S is not None:
            
                if (S >= 0):
                    S_list.append(S)
                    T_list.append(np.abs( T ))           
    
            x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )

            S0 = S0 + ele.length
        
        # print(S_list)
        # print(T_list)
        if len(T_list) >0:
            indexMinT = np.argmin(T_list)
     
            T =  T_list[indexMinT]   
            S =  S_list[indexMinT]
        
     
            return (S,T)
        elif len(self.geometry_elements) > 0:
            
            return (S,T)
            
            
        else:
 
            return (X , Y)
      
class Road():
    
    
   
    
 
    @classmethod
    def fromOSMdict(cls, dictobj , Road_id ,    min_x, min_y ,max_x, max_y):
        #print(" ############## Road #################")
 
        points = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
 
        
        for node in dictobj.get('nodes'):
            
            x = node.get("x")
            y = node.get("y")
            
            if x >= min_x and x <= max_x and y >= min_y and y <= max_y: 
 
                points.append((node.get("x") ,node.get("y") ))
                
                if len(node.get("tags").keys()) > 0:
                    tags["nodes_info"].append(node)
                    
 
              
        # print(Road_id)     
        # print(points) 
        # print(tags) 
        
        tags_keys =  tags.keys()
        if ("service" in tags_keys  and  tags.get("service") =="parking_aisle") or (  tags.get("highway") =="pedestrian"   )  or (  tags.get("highway") =="footway"   )  or ( "foot" in tags_keys and  tags.get("foot") =="designated"    )  or (   tags.get("highway") =="path" )  or ( tags.get("highway") =="service"  )  :
            
            return Footway_Road(Road_id, points, tags )  
        
        
        elif (tags.get("highway") ==  "steps" ):
            return Footway_Road(Road_id, points, tags  ) 
        
        elif ("bicycle" in tags_keys  and  tags.get("bicycle") =="yes")  or ( "highway" in tags_keys  and  tags.get("highway") =="cycleway" ) or ("bicycle" in tags_keys and  tags.get("bicycle") =="designated" ) :

            return Bicycle_Road(Road_id, points, tags  ) 
        
        
        elif "lanes" in tags_keys  or tags.get("highway") =="residential"   or  tags.get("highway") =="living_street"    or  tags.get("highway") == "construction"    :
            
            
            
            return Drivable_Road(Road_id, points, tags )
        
        
        elif "maxspeed" in tags_keys :
            return Drivable_Road(Road_id, points, tags  )        
        
        
        elif tags.get("highway") =="busway"  :
            
            return Drivable_Road(Road_id, points, tags )           

        elif tags.get("highway") =="platform"  :
            
            return Drivable_Road(Road_id, points, tags )  

 
        elif tags.get("surface") =="asphalt"  :
            
            return Drivable_Road(Road_id, points, tags )  
        
        elif "railway" in tags_keys:

            return Railway_Road(Road_id, points, tags ) 
            
        else:
            return Road(Road_id, points, tags  )  
        
         
 
    
    def __init__(self ,Road_id , points =[] , tags = dict()  ):
        
        self.object_id = Road_id
        self.points = points        
        self.tags = tags 
   
        self.ReferenceLine = None     
        
    def __add__(self, other):
        
        #print("**************************************************************ADD**********************************************************************")
        # if other.points[0] in  self.points:
        #     self.points = self.points + other.points[1:]         
        # else:
        self.points = self.points + other.points 
        
        
         
        
        
        self.tags = {**self.tags, **other.tags}  #+ other.tags
        
        
        
        
        
        
        #print("**************************************************************ADD**********************************************************************")
 
        #self.nodes =   self.nodes  +other.nodes
                 
            
        # for node in self.nodes:
        #
        #     x = node.get("x")
        #     y = node.get("y")
        #
        #     self.points.append((x ,y ))

           
        return self
    
    
    def update_ReferenceLine(self ):
    
        if len(self.points ) >=2:
        
            self.ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(self.points , maxiter= 100000   )
            print("New ReferenceLine OK")
        else:
      
            self.ReferenceLine = None        
        
        
        
    
        
    def draw_Road(self, fig , ax ):
        
 
        xs, ys = zip(*self.points) #create lists of x and y values
        ax.plot(xs,ys)
        
        print("######### draw raod ###########")
        
        print(self.points)
        
        for key in self.tags:
            print(key , " ---> ",self.tags.get(key))
        
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
    
class Footway_Road(Road):
    
    
    def __init__(self, Road_id, points=[], tags=dict() ):
        Road.__init__(self, Road_id, points=points, tags=tags )
    
  
    
    def draw_Road(self, fig , ax ):
        
 
        n_lans = 1
        lane_width  = 2
           
        for index , point in enumerate(self.points):
        
            if index <  len(self.points) -1:
        
                x_start , y_start  = point
                x_end   , y_end    = self.points[index+1]
                
                
                deltaX= (x_end -x_start ).astype(float)
                deltaY= (y_end -y_start ) .astype(float)
                
                
        
                Road_lenght = np.sqrt( deltaX *deltaX    + deltaY *deltaY )
        
                Road_width = n_lans*lane_width
        
        
                angle= np.arctan2(deltaY ,deltaX)
        
                t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        
                p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="gray", alpha=1)
        
                p.set_transform(t2)
        
                ax.add_patch(p)  
  
class Bicycle_Road(Road):
    
    def __init__(self, Road_id, points=[], tags=dict() ):
        Road.__init__(self, Road_id, points=points, tags=tags )    
    
    
    def draw_Road(self, fig , ax ):    
    
        n_lans = 1
        lane_width  =   float(self.tags.get("cycleway:width" , 2.5 ) )
        
        
                        
        for index , point in enumerate(self.points):
        
            if index <  len(self.points) -1:
        
                x_start , y_start  = point
                x_end   , y_end    = self.points[index+1]


                
                deltaX= (x_end -x_start ).astype(float)
                deltaY= (y_end -y_start ) .astype(float)
                
        
                Road_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
        
                Road_width = n_lans*lane_width
        
        
                angle= np.arctan2(deltaY ,deltaX )
        
                t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        
                p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="y", alpha= 0.5)
        
                p.set_transform(t2)
        
                ax.add_patch(p)     
                
class Drivable_Road(Road):
    
    
    def __init__(self, Road_id, points=[], tags=dict() ):
        Road.__init__(self, Road_id, points=points, tags=tags )   
        
        # print("New Drivable_Road")
        # if len(points ) >=2:
        #
        #     self.ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(points , optimize=   False  )
        #
        # else:
        #     print(points)
        #     self.ReferenceLine = None        
        #
        #
        # print("New Drivable_Road OK")
    def draw_Road(self, fig , ax ):   
        
        self.update_ReferenceLine( )
                
        n_lans = int(self.tags.get("lanes" , 2))
        lane_width  = 3.5
        coler = random.choice(["b" , "y" , "k" , "r"  ]) 
        for index , point in enumerate(self.points):
        
            if index <  len(self.points) -1:
        
                x_start , y_start  = point
                x_end   , y_end    = self.points[index+1]
        
                deltaX= (x_end -x_start ).astype(float)
                deltaY= (y_end -y_start ) .astype(float)
                
        
                Road_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
        
                Road_width = n_lans*lane_width
        
        
                angle= np.arctan2(deltaY ,deltaX )
        
                t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        
                p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color=coler, alpha= .8)
        
                p.set_transform(t2)
        
                ax.add_patch(p)
        #coler = random.choice(["b" , "y" , "k" , "r" , "w"]) 
        # xs, ys = zip(*self.points) #create lists of x and y values
        # ax.plot(xs,ys , color="k")    
        
        if self.ReferenceLine is not None:
            
            
            xs = []
            ys = []
            for s in np.arange(0, self.ReferenceLine.getLength(),10):
                
                
                
                x, y = self.ReferenceLine.ST2XY(s, 0)
                xs.append(x)
                ys.append(y)
 
                #xs, ys = zip(*self.points) #create lists of x and y values
                
                
                
                
            ax.plot(xs , ys , color="k")                
                
                
             
        
        
class Railway_Road(Road):
    
    
    def __init__(self, Road_id, points=[], tags=dict() ):
        Road.__init__(self, Road_id, points=points, tags=tags )
    
    
    def draw_Road(self, fig , ax ):   
                
 
         
        for index , point in enumerate(self.points):
        
            if index <  len(self.points) -1:
        
                x_start , y_start  = point
                x_end   , y_end    = self.points[index+1]
        
                deltaX= (x_end -x_start ).astype(float)
                deltaY= (y_end -y_start ) .astype(float)
                
        
                Road_lenght = np.sqrt( deltaX *deltaX    + deltaY*deltaY  )
        
                Road_width = 6
        
        
                angle= np.arctan2(deltaY ,deltaX)
        
                t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
        
                p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="r", alpha= .8)
        
                p.set_transform(t2)
        
                ax.add_patch(p)

        xs, ys = zip(*self.points) #create lists of x and y values
        ax.plot(xs,ys , color="r")               
                
class Scenery():
    
    @classmethod
    def from_Osm(cls, filepath):
        
        Roads =[]
        Buildings = []
        Spaces = []
        Barriers = []
        
        
        osmObj = osm_map.parse(filepath, silence = True , print_warnings = True)
        
        
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
        
        
        metaData = {"minlat":minlat ,"minlon" : minlon , "maxlat": maxlat  , "maxlon" : maxlon }
        
                
        print(metaData)
        
        
        nodsdict = dict()
        
        for node in tqdm(osmObj.node):
            #print(node)
            node_id = node.id
            latitude =  float( node.lat )
            longitude = float( node.lon )
            x ,y = projection_fromGeographic(latitude, longitude, minlat ,minlon )
        
            tags = dict()
        
            for tag  in node.tag:
                tags[tag.k] = tag.v
        
            nodsdict[node_id] = {"x": x , "y" : y , "tags" : tags  ,"latitude":latitude  , "longitude":longitude , "node_id" : node_id}
            #print(node)
            #print(nodsdict[node_id])
            
        
         
        waysdict = dict()
            
        for way in tqdm(osmObj.way):
            
            way_id = way.id
            visible = (way.visible == "true")
            nodes = []
            for nd in way.nd:
                nodes.append(nodsdict.get(nd.ref, None))
                
            tags = dict()
        
            for tag  in way.tag:
                tags[tag.k] = tag.v            
            
            waysdict[way_id] = {"visible": visible , "nodes" : nodes , "tags" : tags}            
            
            #t(waysdict[way_id])
            
            tagkeys =  tags.keys()
            
            
            if "historic" in tagkeys  or "roof:edge" in tagkeys or "boundary"  in tagkeys or len(tagkeys) == 0 or ( "landuse" in tagkeys   and tags.get("landuse") ==  "retail"   or    tags.get("landuse") ==  "residential"  or    tags.get("landuse") ==  "construction"  or    tags.get("landuse") ==  "industrial"):
                
                # area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y )
                #
                # Spaces.append(area)
                pass

            elif "highway" in tagkeys  and  tags.get("highway") ==  "elevator" :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)

            
            elif "highway" in tagkeys   or  "railway" in tagkeys      :
                #print(way)
                road = Road.fromOSMdict(waysdict[way_id] , way_id ,  min_x, min_y ,max_x, max_y )
                
                Roads.append(road)          
    
            
            elif "building" in tagkeys   or  "building:material" in tagkeys  or  "demolished:building" in tagkeys   or  "building:levels" in tagkeys  or "building:part" in tagkeys or ( "amenity" in tagkeys   and tags.get("amenity") ==  "kindergarten"   or tags.get("amenity") ==  "school"    ):
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
                
                
            elif "power" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)                  
                
            elif "roof:ridge" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)      
                
                
            elif "roof:shape" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)            

            elif "indoor" in tagkeys   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
                
                
                
 
            elif "man_made" in tagkeys  and  tags.get("man_made") ==  "bridge" :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)  
 
                
            elif "source" in tagkeys   :              
            
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building) 

            elif "amenity" in tagkeys and  tags.get("amenity") ==  "college"   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
                
                
            elif "amenity" in tagkeys and  tags.get("amenity") ==  "hospital"   :              
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
                
                
            elif "landuse" in tagkeys  and tags.get("landuse") ==  "railway":                  
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building) 
 
            elif "leisure" in tagkeys  and tags.get("leisure") ==  "swimming_pool":                  
                
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
 
 
            elif "parking" in tagkeys   or ("leisure"  in tagkeys  and  tags.get("leisure") ==  "park"  )   or ("area" in tagkeys and  tags.get("area") ==  "yes")   or  ("amenity"  in tagkeys  and  tags.get("amenity") ==  "bicycle_parking")   :
 
                parking = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(parking)
                
            elif "motor_vehicle:conditional" in tagkeys:
            
                parking = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
            
                Spaces.append(parking)
                
                
                
                                
                
            elif "amenity" in tagkeys  and ( tags.get("amenity") ==  "parking" or tags.get("amenity") ==  "parking_space")   or  "parking_space" in tagkeys :                 
                parking = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(parking)
                
                
                                
                
            elif "name" in tagkeys  and  "public_transport" in tagkeys  :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area) 
                


            elif "man_made" in tagkeys  and tags.get("man_made") ==  "courtyard" :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)



                
            elif "man_made" in tagkeys  and  "public_transport" in tagkeys  :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area) 
                
                
                
            elif "leisure" in tagkeys    :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)                

 


            elif "landuse" in tagkeys  and  tags.get("landuse") ==  "brownfield"   :                
                
                area = AreaSpace.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(area)  
                               
                
            elif ( "landuse" in tagkeys   and tags.get("landuse") ==  "grass" )   or ( "landuse" in tagkeys   and tags.get("landuse") ==  "greenfield" )   or   ( "leisure" in tagkeys   and tags.get("leisure") ==  "playground" ) or ("leisure"  in tagkeys  and  tags.get("leisure") ==  "garden"  )   :
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)
                
                
                
            elif ( "landuse" in tagkeys   and tags.get("landuse") ==  "orchard" ) :                
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)                
                


            elif ( "landuse" in tagkeys   and tags.get("landuse") ==  "cemetery" ) :                
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)     
                
            elif ( "leisure" in tagkeys   and tags.get("leisure") ==  "outdoor_seating" ) :                
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)                  

            elif ( "bench" in tagkeys    ) :                
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)

                           

            elif ( "attraction" in tagkeys   ) :                
                
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)


                
            elif ( "stairwell" in tagkeys     ) :               
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier) 


            elif "man_made" in tagkeys  and  tags.get("man_made") ==  "pier"   :
   
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier) 
                
                
            elif "shelter" in tagkeys  and  "public_transport" in tagkeys  :
   
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)  
                
                
            elif "amenity" in tagkeys  and  tags.get("amenity") ==  "shelter"    :
   
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)  
                                                                              
   
            elif "playground" in tagkeys    :
   
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)     




   
            elif "amenity" in tagkeys  and  tags.get("amenity") ==  "bench"  :
   
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier) 
                
                
                
            elif "waterway" in tagkeys :
                                
 
                
                waterway = Waterway.fromOSMdict(waysdict[way_id] , way_id  ,  min_x, min_y ,max_x, max_y  )
                
                Spaces.append(waterway)

            elif "barrier" in tagkeys   or ( "landuse" in tagkeys   and tags.get("landuse") ==  "village_green" ) or "natural" in tagkeys   or ( "amenity" in tagkeys   and tags.get("amenity") ==  "fountain" ) : #  or "natural" in tagkeys   or "amenity" in tagkeys 
 
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)
                
                
               
            else:
                print("***********************************************************************")
                print(way)
                # road = Road.fromOSMdict(waysdict[way_id] , way_id ,  min_x, min_y ,max_x, max_y )
                # fig, ax = plt.subplots(figsize=(1, 1), facecolor='lightskyblue', layout='constrained')
                # plt.axis('equal')
                # road.draw_Road(  fig , ax )
                # plt.show() 
            
        Roads =  Scenery.organize_Roads(Roads)  
        return Scenery(metaData , nodsdict ,Roads, Buildings, Spaces , Barriers)
    
    
    def __init__(self, metaData = dict(), nodsdict =dict(), Roads = [] ,Buildings = [] ,  Spaces = []  , Barriers = []  ):
        
        
        self.metaData =metaData
        self.nodsdict =nodsdict
        self.Roads = Roads
        self.Buildings = Buildings 
        self.Spaces =Spaces 
        self.Barriers = Barriers     
        
    @classmethod        
    def organize_Roads(cls ,Roads ):
        
        rods_dict  = dict()
        
        rods_iD_dict  = dict()
        
        for road in Roads:
            class_name= str(road.__class__.__name__)
            
            rods_iD_dict[road.object_id] = road
            
            if rods_dict.get(class_name, None) is None:
                rods_dict[class_name] = []
            
            
            rods_dict[class_name].append(road) 
        
        #print(rods_dict)
        
        nameslist = list(rods_dict.keys())
        nameslist.reverse()
        for class_name in nameslist:
            # print(class_name)
            #
            # if "Drivable_Road" == class_name:
            #     print("relavent")
            
            
            class_name_roads_list = rods_dict.get(class_name)
            
            #roads_start_end  = {}
            pints_of_intest = dict()
            
            for road in class_name_roads_list:
                
                Road_id = road.object_id
                
                start = road.points[0]
                
                end = road.points[-1]
 
                
                
                for other_road in class_name_roads_list:
                    
                    if other_road != road:
                    
                        other_Road_id = other_road.object_id
                        
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
                #print(mergelist) 
                
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
                    
                    #print(road.points.count(road.points[index]))
                    road.points.remove(road.points[index])
                    
            if len(road.points) <2:
                Roads.remove(road)
                


        #add midel point
        
        
        
                
        
                                  
        
        return Roads
            
        
         
    
    def onclick(self, event):
        #global ix, iy
        clear()
        ix, iy = event.xdata, event.ydata
        
        # print("***********************************************************")
        # print("***********************************************************")
        # print("***********************************************************")
        # print("***********************************************************")
        # print (f'x = {ix}, y = {iy}')
        
        
        dist = 20
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
                
                closet_node.append( node_id )
                
            
            
        
        
        #print( closet_node  )
        
        results = []
        for space in  self.Spaces:
            for node in space.nodes: 
                if node["node_id"]  in closet_node:
                    
                    if space not in results:
                        results.append(space)
                    
 
        for Building in  self.Buildings:
            for node in Building.nodes: 
                if node["node_id"]  in closet_node:
                    if Building not in results:
                        results.append(Building)


        for Road in  self.Roads:
            for node in Road.nodes: 
                if node["node_id"]  in closet_node:
                    if Road not in results:
                        results.append(Road)
            

        for Barrier in  self.Barriers:
            for node in Barrier.nodes: 
                if node["node_id"]  in closet_node:
                    if Barrier not in results:
                        results.append(Barrier)

             
        for result in results:
            print(f"#############################{result.__class__.__name__}############################")
            
            print(f"#############################{result.object_id}############################")            
            
            
            for key in result.tags.keys():
                
                print(key, "--->" , result.tags.get(key))
                
            
            
            
               
             
        
            
    
    
    
    def draw_scenery(self):
        

        #for road in self.Roads:
        fig, ax = plt.subplots(figsize=(1, 1), facecolor='lightskyblue', layout='constrained')
        plt.axis('equal')
        #onclick = self.onclick
        #cid = fig.canvas.mpl_connect('button_press_event', onclick)

        
        for space in  self.Spaces:
            space.draw_Space(  fig , ax)
        
        for Building in self.Buildings:
            Building.draw_building(  fig , ax)
        
        for Barrier_roadObject in self.Barriers:
            Barrier_roadObject.draw_Barrier(  fig , ax)
            

                
                #plt.show() 
                
        for road in self.Roads:
        
            if not isinstance(road ,Drivable_Road):
        
                road.draw_Road(  fig , ax ) 


 
        for road in self.Roads:
            
            if isinstance(road ,Drivable_Road):
            
                road.draw_Road(  fig , ax )
            
        plt.show() 



    # global coords
    # coords.append((ix, iy))
    #
    # if len(coords) == 2:
    #     fig.canvas.mpl_disconnect(cid)
    #
    # return coords


if __name__ == '__main__':
    

    
    #
    # center, radius = define_circle((0,1), (1,0), (0,-1))
    # if center is not None:
    #     plt.figure(figsize=(10, 10))
    #     circle = plt.Circle(center, radius)
    #     plt.gcf().gca().add_artist(circle)    
    #     plt.show()

    
    filepath = os.path.abspath("..\\OSM_Interface\\WesternTor_2.osm")
    sceneryObj = Scenery.from_Osm(filepath)    
    
    
    
    
    #sceneryObj.draw_scenery()
    
    
    #fig, ax = plt.subplots(figsize=(1, 1)) #, facecolor='lightskyblue', layout='constrained'
    #plt.axis('equal')
    #onclick = self.onclick
    #cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    
    # for space in  sceneryObj.Spaces:
    #     space.draw_Space(  fig , ax)
    #
    # for Building in sceneryObj.Buildings:
    #     Building.draw_building(  fig , ax)
    #
    # for Barrier_roadObject in sceneryObj.Barriers:
    #     Barrier_roadObject.draw_Barrier(  fig , ax)
    #
    #
    #
    #         #plt.show() 
    #
    # for road in self.Roads:
    #
    #     if not isinstance(road ,Drivable_Road):
    #
    #         road.draw_Road(  fig , ax ) 
    
    i= 0
    
    for road in sceneryObj.Roads:
        
        if isinstance(road ,Drivable_Road):
            i = i +1 
            
            if i > 0:
                fig, ax = plt.subplots(figsize=(10, 10))
                #road.draw_Road(  fig , ax )
                
                points = road.points
                
                
                
    
                         
     
                
                new_points = points.copy()
                #points = new_points
                
                Y = []
                X = []
                
                for point in points:
                    x, y = point
                
                    if y != None:
                        Y.append(y)
                        X.append(x)
       
                
                plt.scatter(X,Y) 
                
                opt_points_X = X
                opt_points_Y = Y
                
                ax.plot(X , Y , color="k")
                
                #points.reverse()
                print(points)
                
                #new_points.remove(new_points[7])
                #new_points.remove(new_points[8])
                
                ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(new_points  )
    
     
                print("#############################################")
                for ele in ReferenceLine.geometry_elements:
                    print("ele : " , ele.__class__.__name__)
                    print("length", ele.length )
            
                    try:
                        print("Radius" , ele.Radius )
            
                    except:
                        pass
    
                
                #F_end = ReferenceLine.optimize(opt_points_X, opt_points_Y)
                
                #print(F_end)
                
                S = ReferenceLine.getLength()
    
                xy = []
                for ele in np.arange(0,S,0.1):
                    xy.append(ReferenceLine.ST2XY(ele,0))
                plt.plot(*zip(*xy))

            
        #plt.show()
        plt.savefig(f"./{i}.png")
    
    
    
    
    
    
    
    
    
    
    
    
    
     
    
    # x0 = 0
    # y0 = 0
    # hdg =   np.pi/4
    #
    # length = 20.0
    # Radius = 50.0
    # geometry_elements = [ StraightLine(length) ,  Arc(5*length,   -Radius) ,StraightLine(length),  Arc(length,    -Radius),  Arc(2*length,   Radius) ,StraightLine(3*length)] #) , StraightLine(length) ,  Arc(length,  -  Radius) , , StraightLine(length) ,Arc(length,   Radius)  , StraightLine(length) Arc(length,   Radius), StraightLine(length) ,   Arc(length,   Radius)  ,     StraightLine(length) ,  Arc(length,  Radius ),  Arc(length,  Radius),  ,,   )  , StraightLine(length) ,  Arc(length,  Radius )
    # refObj = RoadReferenceLine(x0, y0, hdg, geometry_elements)
    #
    #
    # S = np.arange(0.0,refObj.getLength() ,10 )
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
    # ReferenceLine =   RoadReferenceLine.fitRoadReferenceLine(points , x0 , y0  , hdg )
    #
    #
    #
    # print(x0 , y0  , hdg )
    #
    # print(ReferenceLine.__dict__)
    #
    #
    # for ref in [refObj ,ReferenceLine ]:
    #     print("#############################################")
    #     for ele in ref.geometry_elements:
    #         print("ele : " , ele.__class__.__name__)
    #         print("length", ele.length )
    #
    #         try:
    #             print("Radius" , ele.Radius )
    #
    #         except:
    #             pass
    # xy = []
    # for ele in S:
    #     xy.append(ReferenceLine.ST2XY(ele,0))
    # plt.plot(*zip(*xy))
    #
    #
    # plt.show()      
    

    
    
    
