'''
Created on 28.10.2023

@author: abdelmaw
'''

import osm_map   as osm_map

if __name__ == '__main__':
    
    map =  osm_map.parse("map_osm.xml",  silence=True )
    
    
    print("node:")
    
    for ele in map.node:
        print(ele)
    