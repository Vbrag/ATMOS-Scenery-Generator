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
from scipy.optimize import minimize
from trio._path import classmethod_wrapper_factory

projection_fromGeographic_cash = dict()
clear = lambda: os.system('cls')

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
        # print(" ############## Building #################")
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["nodes_info"] = []
        
        
        
        
        for node in dictobj.get('nodes'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["nodes_info"].append(node)
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        return Building(Building_id, Floor_plan, tags, dictobj.get('nodes') )  
        
         
 
    
    def __init__(self ,Building_id , Floor_plan =[] , tags = dict(), nodes = []):
        
        self.object_id = Building_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        self.nodes =nodes
        
        
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
        # print(" ############## Building #################")
        
        
        
        
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
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
 
         
        return AreaSpace(ParkingSpace_id, Floor_plan, tags,  dictobj.get('nodes'))  
        
         
 
    
    def __init__(self ,ParkingSpace_id , Floor_plan =[] , tags = dict() ,nodes =[]):
        
        self.object_id = ParkingSpace_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        self.nodes =nodes        
        
    def draw_Space(self, fig , ax ):
        
        xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        ax.plot(xs,ys)
        
        facecolor = 'y'
        # if 'roof:colour' in self.tags.keys():
        #     facecolor = self.tags.get('roof:colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
            
        
        
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
 
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        #Floor_plan = [*Floor_plan  , Floor_plan[0]]
         
        return Waterway(waterway_id, Floor_plan, tags, dictobj.get('nodes'))  
        
         
 
    
    def __init__(self ,waterway_id , Floor_plan =[] , tags = dict(),nodes =[]):
        
        self.object_id = waterway_id
        self.Floor_plan = Floor_plan 
        
        # if self.Floor_plan[0] !=  self.Floor_plan[-1]:
        #     self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        self.nodes =nodes        
        
    def draw_Space(self, fig , ax ):
        
        # xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        # ax.plot(xs,ys)
        
        facecolor = 'b'
        # if 'roof:colour' in self.tags.keys():
        #     facecolor = self.tags.get('roof:colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
            
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
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        return Barrier_roadObject(barrier_id, Floor_plan, tags, dictobj.get('nodes'))  
        
         
 
    
    def __init__(self ,barrier_id , Floor_plan =[] , tags = dict() , nodes =[] ):
        
        self.object_id = barrier_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        self.nodes = nodes         
        
    def draw_Barrier(self, fig , ax ):
        
        # xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        # ax.plot(xs,ys)
        
        facecolor = 'g'
        if 'colour' in self.tags.keys():
            facecolor = self.tags.get('colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
            
        
        try:
            p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5) 
            
        except:
            facecolor = 'g'
            p = Polygon(self.Floor_plan, facecolor = facecolor, alpha=0.5)             
        ax.add_patch(p)
 
 
 
        
        
        


class StraightLine():
 
    @classmethod
    def func( cls,  x , x0, y0, hdg , opt_points_X , opt_points_Y):
        
        length= x[0] 
        
        line = StraightLine(length)
        
         
        
        X = np.array(opt_points_X)
        Y = np.array(opt_points_Y)
        
        refObj.get_endPoint()
        
        yhat= line.evalX(x0, y0, hdg, X)
        
        _  , yend , _ = line.get_endPoint(x0, y0, hdg)
        
    
        yhat= np.where(yhat  !=  None  , yhat , yend) 
    
        
        Y  = np.where(Y   !=  None  , Y  , yend) 
        
        eror = yhat - Y
        
        eror=  eror.astype(float)
    
        
        ls_error =   np.sum(  eror *eror    )
        
    
        return ls_error
    
    def __init__(self,    length=0):
        
 
        self.length = length
        

    def evalX(self, x0 , y0 ,hdg , X):
        
 
            
        if hdg != np.pi/2:
        
            y =   y0 + (X - x0)*np.tan(hdg)
        else:
            
            y =   y0
            
 
            
        deltaX= (X -x0 ).astype(float)
        deltaY= (y -y0 ).astype(float)
        
        lenght = np.sqrt(  deltaX * deltaX    + deltaY *deltaY  ) 
 
        
        return np.where(lenght   <=  self.length  , y , None)
        
 
                 
                
        
        
        
        

 
    
    def eval(self, x0 , y0 ,hdg,  S , S0 , T):
        
        
        hdg = hdg  
        
        
        delta_s = S - S0 
        
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
   
  
class Arc():

    @classmethod    
    def func( cls,  x , x0, y0, hdg , opt_points_X , opt_points_Y ):
        
        
        length=  x[0] 
        Radius=  x[1]  
        
        line = Arc(length, Radius)    
        X = np.array(opt_points_X)
        Y = np.array(opt_points_Y)
        print(Y)
        refObj.get_endPoint()
        
        yhat= line.evalX(x0, y0, hdg, X)
       
        #_  , yend , _ = line.get_endPoint(x0, y0, hdg)
    
        yhat= np.where(yhat  !=  None  , yhat , 0) 
           
        #Y  = np.where(Y   !=  None  , Y  , 0)         
         
        #print(yhat)
        
        eror = yhat - Y
        
        #print(eror)
        
        eror=  eror.astype(float)
        
        ls_error =   np.sum(  eror *eror)  
        
        return ls_error    

    
    def __init__(self, length=0 , Radius = 0 ):
        
        self.length =length
        self.Radius = Radius
 
 


    def eval(self, x0 , y0 ,hdg, S ,S0 ,T):
        
 

        alfa =   np.pi/2  - hdg  

        x_center = x0 + self.Radius * np.cos( alfa )
        y_center = y0 - self.Radius * np.sin( alfa )

        
        delta_s = S - S0 
        
        
        theta =  (delta_s /self.Radius )* (np.pi)
        
        hdg_end =    hdg-theta
 
        xs =  x_center + self.Radius*np.cos(np.pi - alfa -theta )    
        ys =  y_center + self.Radius*np.sin(np.pi - alfa -theta)   
        
        
        xs = xs + T*np.cos(np.pi/2.0  - hdg_end )
        ys = ys - T*np.sin(np.pi/2.0  - hdg_end )
           
        
        return (xs , ys) 
    
    
    def get_endPoint(self, x0 , y0 ,hdg):
        
        alfa =   np.pi/2  - hdg  

        x_center = x0 + self.Radius * np.cos( alfa )
        y_center = y0 - self.Radius * np.sin( alfa )

        
        delta_s = self.length
        
        
        theta =  (delta_s /self.Radius )* (np.pi)
 
        x_end =  x_center + self.Radius*np.cos(np.pi - alfa -theta )   
        y_end =  y_center + self.Radius*np.sin(np.pi - alfa -theta)
              
        hdg_end =    hdg-theta
    
        return (x_end ,y_end , hdg_end )
    
    
    def evalX(self, x0 , y0 ,hdg , X):
        
        alfa =   np.pi/2  - hdg  

        x_center = x0 + self.Radius * np.cos( alfa )
        y_center = y0 - self.Radius * np.sin( alfa )
        
        #try:
        theta =  -1*( np.arccos( (X - x_center)/self.Radius ) -np.pi +alfa) 
        
        y =  y_center + self.Radius*np.sin(np.pi - alfa -theta)
        
 
   
        lenght = theta /(np.pi) *self.Radius
        
 
        return np.where(lenght   <=  self.length  , y , None)
            
            # if (lenght  <=  self.length).all() :
            #     return y
            #
            # else:
            #     return None
            
        # except:
        #     return None

class RoadReferenceLine():


    @classmethod  
    def fitRoadReferenceLine(cls, points ):
        
 
        x0, y0 = points[0]
        x1, y1 = points[1]        
 
        hdg =  np.arctan2((y1 -y0 ) ,(x1 -x0 ) )
 
 
        geometry_elements = []
        
        
        refObj = RoadReferenceLine(x0, y0, hdg, geometry_elements)
        
 
        use_line  = False
        

        
        x0 , y0 , hdg  = refObj.get_endPoint()

        #point0 = points[0] 
        
        opt_points_X = [ ]
        opt_points_Y = [ ] 
        
        length0 = 0
        radius0 = 20

        for point in points:

            if point[0] is not None and point[1] is not None :
                opt_points_X.append( point[0]  )
                opt_points_Y.append( point[1]  )
                
                if len(opt_points_X) > 1:
                    x_end = point[0]
                    y_end = point[1]   
                    x_start = opt_points_X[-2]
                    y_start = opt_points_Y[-2]
                
                
                    deltaX = np.array( x_end - x_start ).astype(float)
                    deltaY = np.array( y_end - y_start ).astype(float)
                
                
                
                    length0  = length0 +  np.sqrt( deltaX*deltaX   +  deltaY *deltaY  )                
                    
 
        
        
        if use_line:
            bnds = ((0, None) )
            func = lambda x:StraightLine.func(x ,  x0, y0, hdg , opt_points_X , opt_points_Y)
            
            # if length == None:
            #     length0 = 1 
            #
            # else:
            #     length0 = length                    
        
        
            res = minimize(func, np.array([length0]), method='SLSQP', bounds=bnds , tol=1e-100, options={'maxiter':100 ,'gtol': 1e-100, 'disp': False})
            
            res_length = res.x[0]
            
        
            
            res_fun = res.fun
            
            print(res)
            print(res_fun)
        
            #if res_fun <= 0.001:
            
            #if length == None:
            length = res_length
            
            refObj.geometry_elements.append( StraightLine(length))
                
            # else:
            #     length = res_length
            #
            #     refObj.geometry_elements[-1].length =  length  
                    
            # else:
            #     length = None
            #     radius = None                    
            #     use_line = False
            #     x0 , y0 , hdg  = refObj.get_endPoint()
            #     opt_points_X = [point[0]]
            #     opt_points_Y = [point[1]]
                
        else :   
            bnds = ((0, None), (None, None))                                  
            func = lambda x : Arc.func(x  ,  x0, y0, hdg , opt_points_X , opt_points_Y) 
            
            # if length == None:
            #     length0 = 20.0
            # else:
            #     length0 = length   
            #
            # if radius == None:
            #     radius0 = 20 
            # else:
            #     radius0 = radius 
                  
                  
                  
            res = minimize(func, np.array([length0 ,radius0 ]) , method='SLSQP', bounds=bnds , tol=1e-100, options={'maxiter':100 ,'gtol': 1e-100, 'disp': False})
            
            res_length = res.x[0]
            res_radius = res.x[1]                
        
            
            res_fun = res.fun
            print(res)
            print(res_fun) 
 
            #if length == None:
            length = res_length
            radius =  res_radius  
                                    
            refObj.geometry_elements.append( Arc(length ,  radius     ))
            print("length0" ,length0 ,"radius0",radius0 )
                
            # else:
            #     length = res_length
            #     radius = res_radius                         
            #
            #
            #
            #     refObj.geometry_elements[-1].length =  length  
            #     refObj.geometry_elements[-1].radius =   radius                            
            # else:
            #     length = None
            #     radius = None                    
            #     use_line = True
            #     x0 , y0 , hdg  = refObj.get_endPoint()
            #     opt_points_X = [point[0]]
            #     opt_points_Y = [point[1]]                
                           
            
        return refObj
    
    def __init__(self, x0=0, y0=0 , hdg  = 0 , geometry_elements = [] ):
        
        self.x0 = x0 
        self.y0 = y0
        self.hdg = hdg
        self.geometry_elements = geometry_elements
        
    
    
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
 
    
    def eval(self, S ,T):

        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
        S0 = 0
        
        
        for ele in self.geometry_elements:
            
            if S - S0 < ele.length:
                
                return ele.eval(  x0 , y0 , hdg ,  S ,S0,T )
            
            else:
                
                x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )
                
                S0 = S0 + ele.length
            
        
        
        x_end , y_end , hdg  = self.get_endPoint()
        
        
        return ( x_end , y_end )
        
        
    def evalX(self, X):
    
        x0 = self.x0   
        y0 = self.y0   
        hdg = self.hdg   
    
        S0 = 0
    
        for ele in self.geometry_elements:
            
 
            
            Y = ele.evalX(  x0 , y0 ,hdg , X)
            
            
            if Y != None   :
                 
                return Y
    
            else:
    
                x0 , y0 , hdg = ele.get_endPoint(x0 ,y0 , hdg )
    
                S0 = S0 + ele.length
    
    
    
        return None       
        
    
 
 
      
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
            
            return Footway_Road(Road_id, points, tags, dictobj.get('nodes'))  
        
        
        elif (tags.get("highway") ==  "steps" ):
            return Footway_Road(Road_id, points, tags ,dictobj.get('nodes')) 
        
        elif ("bicycle" in tags_keys  and  tags.get("bicycle") =="yes")  or ( "highway" in tags_keys  and  tags.get("highway") =="cycleway" ) or ("bicycle" in tags_keys and  tags.get("bicycle") =="designated" ) :

            return Bicycle_Road(Road_id, points, tags , dictobj.get('nodes')) 
        
        
        elif "lanes" in tags_keys  or tags.get("highway") =="residential"   or  tags.get("highway") =="living_street"    or  tags.get("highway") == "construction"    :
            
            return Drivable_Road(Road_id, points, tags, dictobj.get('nodes'))
        
        
        elif "maxspeed" in tags_keys :
            return Drivable_Road(Road_id, points, tags , dictobj.get('nodes'))        
        
        
        elif tags.get("highway") =="busway"  :
            
            return Drivable_Road(Road_id, points, tags, dictobj.get('nodes'))           

        elif tags.get("highway") =="platform"  :
            
            return Drivable_Road(Road_id, points, tags, dictobj.get('nodes'))  

 
        elif tags.get("surface") =="asphalt"  :
            
            return Drivable_Road(Road_id, points, tags, dictobj.get('nodes'))  
        
        elif "railway" in tags_keys:

            return Railway_Road(Road_id, points, tags, dictobj.get('nodes')) 
            
        else:
            return Road(Road_id, points, tags, dictobj.get('nodes'))  
        
         
 
    
    def __init__(self ,Road_id , points =[] , tags = dict() , nodes =[]):
        
        self.object_id = Road_id
        self.points = points        
        self.tags = tags 
        self.nodes = nodes           
        
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
    
    
    def __init__(self, Road_id, points=[], tags=dict(), nodes=[]):
        Road.__init__(self, Road_id, points=points, tags=tags, nodes=nodes)
    
  
    
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
    
    def __init__(self, Road_id, points=[], tags=dict(), nodes=[]):
        Road.__init__(self, Road_id, points=points, tags=tags, nodes=nodes)    
    
    
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
    
    
    def __init__(self, Road_id, points=[], tags=dict(), nodes=[]):
        Road.__init__(self, Road_id, points=points, tags=tags, nodes=nodes)   
    
    
    def draw_Road(self, fig , ax ):   
                
        n_lans = int(self.tags.get("lanes" , 2))
        lane_width  = 3.5
        
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
        
                p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="k", alpha= .8)
        
                p.set_transform(t2)
        
                ax.add_patch(p)

        xs, ys = zip(*self.points) #create lists of x and y values
        ax.plot(xs,ys , color="k")     
        
        
class Railway_Road(Road):
    
    
    def __init__(self, Road_id, points=[], tags=dict(), nodes=[]):
        Road.__init__(self, Road_id, points=points, tags=tags, nodes=nodes)
    
    
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
            
            
        return Scenery(metaData , nodsdict ,Roads, Buildings, Spaces , Barriers)
    
    
    def __init__(self, metaData = dict(), nodsdict =dict(), Roads = [] ,Buildings = [] ,  Spaces = []  , Barriers = []  ):
        
        
        self.metaData =metaData
        self.nodsdict =nodsdict
        self.Roads = Roads
        self.Buildings = Buildings 
        self.Spaces =Spaces 
        self.Barriers = Barriers     
        
        
    
    
    def onclick(self, event):
        #global ix, iy
        clear()
        ix, iy = event.xdata, event.ydata
        
        print("***********************************************************")
        print("***********************************************************")
        print("***********************************************************")
        print("***********************************************************")
        print (f'x = {ix}, y = {iy}')
        
        
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
        

        
        fig, ax = plt.subplots(figsize=(1, 1), facecolor='lightskyblue', layout='constrained')
        plt.axis('equal')
        onclick = self.onclick
        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        
        for space in  self.Spaces:
            space.draw_Space(  fig , ax)
        
        for Building in self.Buildings:
            Building.draw_building(  fig , ax)
 
        for Barrier_roadObject in self.Barriers:
            Barrier_roadObject.draw_Barrier(  fig , ax)
            
 
        for road in self.Roads:
            
            if isinstance(road ,Drivable_Road):
            
                road.draw_Road(  fig , ax )
                
                
        for road in self.Roads:
            
            if not isinstance(road ,Drivable_Road):
            
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
    
    
    # filepath = os.path.abspath("..\\OSM_Interface\\WesternTor_2.osm")
    # sceneryObj = Scenery.from_Osm(filepath)    
    # sceneryObj.draw_scenery() 
    
    x0 = 0
    y0 = 0
    hdg =  np.pi/4
    
    length = 20.0
    Radius = 50.0
    geometry_elements = [ Arc(length, Radius) ] # , StraightLine(length) ,, Arc(length, Radius)  , StraightLine(length) ,  Arc(length,- Radius), StraightLine(length) ,  Arc(length,  Radius) 
    refObj = RoadReferenceLine(x0, y0, hdg, geometry_elements)
    
    
    S = np.arange(0.0,refObj.getLength() *3,0.001  )
    # xy = []
    # #
    # # T = 0
    # #
    # # for ele in S:
    # #     xy.append(refObj.eval(ele,T))
    # #
    # # plt.plot(*zip(*xy))
    #
    # xy = []
    #
    # T = 1
    #
    # for ele in S:
    #     xy.append(refObj.eval(ele,T))
    #
    # plt.plot(*zip(*xy))
    #
    # xy = []
    #
    # T = -1
    #
    # for ele in S:
    #     xy.append(refObj.eval(ele,T))
    #
    # plt.plot(*zip(*xy))    
    #
    #
    #
    points =[]
    
    X = np.arange(0.0,70,1.0)    
    Y = []
    for x in X:
        y = refObj.evalX(x)
        Y.append(y)
        points.append((x, y))
    
    plt.scatter(X,Y) 
    
 
    ReferenceLine =  RoadReferenceLine.fitRoadReferenceLine(points)  
    
    
    
    print(ReferenceLine.geometry_elements[0].length )
    print(ReferenceLine.geometry_elements[0].Radius )
    xy = []
    for ele in S:
        xy.append(ReferenceLine.eval(ele,0))
    
    plt.plot(*zip(*xy))
    

    plt.show()      
    