'''
Created on 03.11.2023

@author: abdel
'''

from OSM_Interface import  osm_map as  osm_map
import os , math
import ctypes, sys
from pyproj import CRS, Transformer
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon , Rectangle
import matplotlib as mpl

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
    
    
 
    crs_4326  = CRS.from_epsg(4326) # epsg 4326 is wgs84

    uproj = CRS.from_proj4("+proj=tmerc +lat_0={0} +lon_0={1} +x_0=0 +y_0=0 +ellps=GRS80 +units=m".format(referenceLat, referenceLon))
    transformer = Transformer.from_crs(crs_4326, uproj)
    
    x,y = next(transformer.itransform([(latitude,longitude)]))
    
 
    
    return (x,y)




class Building():
 
    @classmethod
    def fromOSMdict(cls, dictobj , Building_id):
        # print(" ############## Building #################")
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["noads_info"] = []
        
        for node in dictobj.get('noads'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["noads_info"].append(node)
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        return Building(Building_id, Floor_plan, tags)  
        
         
 
    
    def __init__(self ,Building_id , Floor_plan =[] , tags = dict()):
        
        self.Building_id = Building_id
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
        
        p = Polygon(self.Floor_plan, facecolor = facecolor) 
        ax.add_patch(p)
        

class ParkingSpace():
 
    @classmethod
    def fromOSMdict(cls, dictobj , ParkingSpace_id):
        # print(" ############## Building #################")
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["noads_info"] = []
        
        for node in dictobj.get('noads'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["noads_info"].append(node)
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        return ParkingSpace(ParkingSpace_id, Floor_plan, tags)  
        
         
 
    
    def __init__(self ,ParkingSpace_id , Floor_plan =[] , tags = dict()):
        
        self.ParkingSpace_id = ParkingSpace_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        
        
    def draw_ParkingSpace(self, fig , ax ):
        
        xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        ax.plot(xs,ys)
        
        facecolor = 'b'
        # if 'roof:colour' in self.tags.keys():
        #     facecolor = self.tags.get('roof:colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
            
        
        
        p = Polygon(self.Floor_plan, facecolor = facecolor) 
        ax.add_patch(p)
 
 
class Barrier_roadObject():
 
    @classmethod
    def fromOSMdict(cls, dictobj , barrier_id):
        # print(" ############## Building #################")
        
        
        
        
        Floor_plan = []
        tags = dictobj.get('tags')
        tags["noads_info"] = []
        
        for node in dictobj.get('noads'):
 
            Floor_plan.append((node.get("x") ,node.get("y") ))
            
            if len(node.get("tags").keys()) > 0:
                tags["noads_info"].append(node)
              
        # print(Building_id)     
        # print(Floor_plan) 
        # print(tags)  
         
        return Barrier_roadObject(barrier_id, Floor_plan, tags)  
        
         
 
    
    def __init__(self ,barrier_id , Floor_plan =[] , tags = dict()):
        
        self.barrier_id = barrier_id
        self.Floor_plan = Floor_plan 
        
        if self.Floor_plan[0] !=  self.Floor_plan[-1]:
            self.Floor_plan.append(self.Floor_plan[0])
               
        self.tags = tags 
        
        
    def draw_Barrier(self, fig , ax ):
        
        xs, ys = zip(* self.Floor_plan ) #create lists of x and y values
        ax.plot(xs,ys)
        
        facecolor = 'g'
        if 'colour' in self.tags.keys():
            facecolor = self.tags.get('colour')
        #
        # elif  'building:colour' in self.tags.keys():
        #     facecolor = self.tags.get('building:colour')
            
        
        
        p = Polygon(self.Floor_plan, facecolor = facecolor) 
        ax.add_patch(p)

          
class Road():
 
    @classmethod
    def fromOSMdict(cls, dictobj , Road_id ,    min_x, min_y ,max_x, max_y):
        #print(" ############## Road #################")
 
        points = []
        tags = dictobj.get('tags')
        tags["noads_info"] = []
        
        for node in dictobj.get('noads'):
            
            x = node.get("x")
            y = node.get("y")
            
            if x > min_x and x < max_x and y > min_y and y < max_y: 
 
                points.append((node.get("x") ,node.get("y") ))
                
                if len(node.get("tags").keys()) > 0:
                    tags["noads_info"].append(node)
              
        # print(Road_id)     
        # print(points) 
        # print(tags)  
         
        return Road(Road_id, points, tags)  
        
         
 
    
    def __init__(self ,Road_id , points =[] , tags = dict()):
        
        self.Road_id = Road_id
        self.points = points        
        self.tags = tags 
        
        
    def draw_Road(self, fig , ax ):
        
        
        tags_keys = self.tags.keys()
        if "lanes" in tags_keys:
            
            # xs, ys = zip(*self.points) #create lists of x and y values
            # ax.plot(xs,ys ,color="r" )            
            # print(self.points)
            #
            # for key in self.tags:
            #     print(key , " ---> ",self.tags.get(key))
            
            n_lans = int(self.tags.get("lanes"))
            lane_width  = 3.5
 
            for index , point in enumerate(self.points):
                
                if index <  len(self.points) -1:
                    
                    x_start , y_start  = point
                    x_end   , y_end    = self.points[index+1]
                    
                    Road_lenght = math.sqrt( (x_end -x_start ) *(x_end -x_start )    +(y_end -y_start ) *(y_end -y_start )  )
                    
                    Road_width = n_lans*lane_width
                    
                    
                    angle= math.atan2((y_end -y_start ) ,(x_end -x_start ) )
                    
                    t2 = mpl.transforms.Affine2D().rotate_around(x_start, y_start, angle) + ax.transData
                    
                    p = Rectangle((x_start  ,y_start - Road_width / 2.0 ), Road_lenght, Road_width, color="k", alpha=1)
                    
                    p.set_transform(t2)
  
                    ax.add_patch(p)
             
        
        else:
            xs, ys = zip(*self.points) #create lists of x and y values
            ax.plot(xs,ys)
 
            print("######### draw raod ###########")
            
            print(self.points)
            
            for key in self.tags:
                print(key , " ---> ",self.tags.get(key))
            
            
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

class Scenery():
    
    @classmethod
    def from_Osm(cls, filepath):
        
        Roads =[]
        Buildings = []
        ParkingSpaces = []
        Barriers = []
        
        
        osmObj = osm_map.parse(filepath, silence = True , print_warnings = True)
        
        
        bound = osmObj.bounds[0]
        
        minlat =  float(bound.minlat )
        minlon =  float(bound.minlon  )      
        maxlat = float( bound.maxlat )
        maxlon =  float(bound.maxlon )
        
        
        min_x, min_y = projection_fromGeographic(minlat, minlon, minlat ,minlon )
        max_x, max_y = projection_fromGeographic(maxlat, maxlon, minlat ,minlon )
        
        
        delta_x = max_x  - min_x
        delta_y = max_y  - min_y        
        
        
        max_x = max_x + delta_x/2
        max_y = max_y + delta_y/2        
        
        min_x = min_x - delta_x/2
        min_y = min_y - delta_y /2       
        
        
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
        
            nodsdict[node_id] = {"x": x , "y" : y , "tags" : tags}
            #print(node)
            #print(nodsdict[node_id])
            
        
         
        waysdict = dict()
            
        for way in tqdm(osmObj.way):
            
            way_id = way.id
            visible = (way.visible == "true")
            noads = []
            for nd in way.nd:
                noads.append(nodsdict.get(nd.ref, None))
                
            tags = dict()
        
            for tag  in way.tag:
                tags[tag.k] = tag.v            
            
            waysdict[way_id] = {"visible": visible , "noads" : noads , "tags" : tags}            
            
            #print(waysdict[way_id])
            
            tagkeys =  tags.keys()
            
            
            if "historic" in tagkeys  or "boundary"  in tagkeys or len(tagkeys) == 0 or ( "landuse" in tagkeys   and tags.get("landuse") ==  "retail" ):
                
                pass
            
            elif "building" in tagkeys  :
                building = Building.fromOSMdict(waysdict[way_id] , way_id)
                
                Buildings.append(building)
 
 
            elif "parking" in tagkeys   or ("leisure"  in tagkeys  and  tags.get("leisure") ==  "park") :
 
                parking = ParkingSpace.fromOSMdict(waysdict[way_id] , way_id   )
                
                ParkingSpaces.append(parking)


            elif "barrier" in tagkeys   or ( "landuse" in tagkeys   and tags.get("landuse") ==  "village_green" ) or "natural" in tagkeys   or ( "amenity" in tagkeys   and tags.get("amenity") ==  "fountain" ) : #  or "natural" in tagkeys   or "amenity" in tagkeys 
 
                barrier = Barrier_roadObject.fromOSMdict(waysdict[way_id] , way_id   )
                
                Barriers.append(barrier)
                
                
            elif "highway" in tagkeys:
                #print(way)
                road = Road.fromOSMdict(waysdict[way_id] , way_id ,  min_x, min_y ,max_x, max_y )
                
                Roads.append(road)                 
            else:
 
                print(way)
                
                
                 
            
            
        return Scenery(metaData ,Roads, Buildings, ParkingSpaces , Barriers)
    
    
    def __init__(self, metaData = dict(), Roads = [] ,Buildings = [] ,  ParkingSpaces = []  , Barriers = []  ):
        
        
        self.metaData =metaData
        self.Roads = Roads
        self.Buildings = Buildings 
        self.ParkingSpaces =ParkingSpaces 
        self.Barriers = Barriers     
        
        
    
    
    
    
    def draw_scenery(self):
        fig, ax = plt.subplots(figsize=(1, 1), facecolor='lightskyblue', layout='constrained')
        plt.axis('equal')
        
        for Building in self.Buildings:
            Building.draw_building(  fig , ax)
            
           

        for parkingSpace in self.ParkingSpaces:
            parkingSpace.draw_ParkingSpace(  fig , ax)


        for Barrier_roadObject in self.Barriers:
            Barrier_roadObject.draw_Barrier(  fig , ax)
            
            
         
        for road in self.Roads:
 
            road.draw_Road(  fig , ax )
            
        plt.show() 
            
 

if __name__ == '__main__':
    
    
    filepath = os.path.abspath("C:\\Users\\abdel\\Documents\\GitHub\\ATMOS-Scenery-Generator\\OSM_Interface\\westerntor.osm")
    sceneryObj = Scenery.from_Osm(filepath)
    
 
    
    sceneryObj.draw_scenery() 
    