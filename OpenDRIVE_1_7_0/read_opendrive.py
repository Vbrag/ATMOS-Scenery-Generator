
'''
Created on 28.10.2023

@author: abdelmaw
'''

import  OpenDRIVE_1_7_0.opendrive_17   as opendrive

if __name__ == '__main__':
    
    map =  opendrive.parse("output.xodr",  silence=True )
    
    print(type(map))
    print("road:")
    
    for ele in map.road:
        print(type(ele))