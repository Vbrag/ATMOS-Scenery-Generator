'''
Created on 16.11.2023

@author: abdel
'''
import unittest
from Scenery_Model.scenery  import  *
import numpy as np

class TestStraightLine(unittest.TestCase):
    
    # def setUp(self):
    #     self.line = StraightLine()  # Create an instance of StraightLine for testing
    
    def test_XY2ST(self):
        
        line = StraightLine(10)

        
        # for x0 in np.arange(-10,10,1):
        #     for y0 in np.arange(-10,10,1):
        #         for hdg in np.arange(0,2*np.pi,.1):  
        #             # Test XY2ST method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
        X, Y, S0 = 1, 1, 0  # Example values
        
        S, T = line.XY2ST(x0, y0, hdg, X, Y, S0)
        
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(S, 1.414, places=3)  # Example expected value of S, rounded to 3 decimal places
        self.assertAlmostEqual(T, 0.0, places=3)  # Example expected value of T, rounded to 3 decimal places



    def test_XY2ST_ST2XY(self):
        
        line = StraightLine(50)

        
        for x0 in np.arange(-10,10,1):
            for y0 in np.arange(-10,10,1):
                for hdg in np.arange(0,2*np.pi,.1):  
                    # Test XY2ST method with some sample input
                        #x0, y0, hdg = 0, 0, np.pi / 4  # Example values
                        
 
                    X, Y, S0 = 1, 1, 0  # Example values
                    
                    S, T = line.XY2ST(x0, y0, hdg, X, Y, S0)
                    
                    X2,Y2 = line.ST2XY(x0, y0, hdg, S, S0, T)
                    
                    # Assert the expected values based on calculations or known answers
                    self.assertAlmostEqual(X, X2, places=3)  # Example expected value of S, rounded to 3 decimal places
                    self.assertAlmostEqual(Y, Y2, places=3)  # Example expected value of T, rounded to 3 decimal places



    def test_ST2XY_XY2ST(self):
        
        line = StraightLine(50)

        S0 = 0
        for S in np.arange(0,10,1):
            for T in np.arange(0,10,1):
                for hdg in np.arange(0,2*np.pi,.1):  
                    # Test XY2ST method with some sample input
                    x0, y0 = 0, 0 #, np.pi / 4  # Example values
                        
 
                    X, Y  = line.ST2XY(x0, y0, hdg, S, S0, T)
                    
                    S2, T2 = line.XY2ST(x0, y0, hdg, X, Y, S0)
                    
  
                    
                    # Assert the expected values based on calculations or known answers
                    self.assertAlmostEqual(S, S2, places=3)  # Example expected value of S, rounded to 3 decimal places
                    self.assertAlmostEqual(T, T2, places=3)  # Example expected value of T, rounded to 3 decimal places


    
    def test_ST2XY(self):
        
        line = StraightLine(10)
        # Test ST2XY method with some sample input
        
        for x0 in np.arange(-10,10,1):
            for y0 in np.arange(-10,10,1):
                for hdg in np.arange(0,2*np.pi,.1):                
                    #x0, y0, hdg = 0, 0, np.pi / 4  # Example values
                    S, S0, T = 1, 0, 0  # Example values
                    
                    x, y =  line.ST2XY(x0, y0, hdg, S, S0, T)
                    
                    # Assert the expected values based on calculations or known answers
                    self.assertAlmostEqual( x-x0 , S*np.cos(hdg), places=3)  # Example expected value of x, rounded to 3 decimal places
                    self.assertAlmostEqual( y-y0 , S*np.sin(hdg), places=3)  # Example expected value of y, rounded to 3 decimal places


    def test_ST2XY_2(self):
        
        line = StraightLine(10)
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
        S, S0, T = 10.001, 0, 0  # Example values
        
        x, y =  line.ST2XY(x0, y0, hdg, S, S0, T)
        
        # Assert the expected values based on calculations or known answers
        self.assertEqual(x, None )   
        self.assertEqual(y, None )   
    
    def test_get_endPoint(self):
        
        L = 10
        
        line = StraightLine(L)
        
        # Test get_endPoint method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
        
        x_end, y_end, hdg_end =  line.get_endPoint(x0, y0, hdg)
        
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x_end, L*np.cos(hdg), places=3)  # Example expected value of x_end, rounded to 3 decimal places
        self.assertAlmostEqual(y_end, L*np.sin(hdg), places=3)  # Example expected value of y_end, rounded to 3 decimal places
        self.assertAlmostEqual(hdg_end, np.pi / 4, places=3)  # Example expected value of hdg_end, rounded to 3 decimal places



 

class TestArc(unittest.TestCase):
    
 
    
    def test_ST2XY(self):
    
        
        Radius = 15
        L = 2*np.pi*Radius
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.pi*Radius, 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        
        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0    , places=3)  # Example expected value of y, rounded to 3 decimal places


        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        hdg = 2*np.pi    


 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
 
    def test_ST2XY_1(self):
    
        
        Radius = 15
        L = 2*np.pi*Radius
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.pi*Radius, 0, 1  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,  0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius+1     , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        
        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius -1 , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0   , places=3)  # Example expected value of y, rounded to 3 decimal places


        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius-1    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        hdg = 2*np.pi    


 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,  0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius+1     , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        
 
    def test_XY2ST(self):
    
        
        Radius = 15
        L = 2*np.pi*Radius+0.1
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.pi*Radius, 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        
        hdg = 2*np.pi    

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places       
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places


    def test_XY2ST_2(self):
    
        
        Radius = 15
        L = 2*np.pi*Radius 
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.pi*Radius /2, 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -1* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,   Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, -1* Radius   , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,    Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        
        hdg = 2*np.pi    

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -1* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places       
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places



                
    def test_get_endPoint(self):
        L = 10
        R = 10
    
        arc = Arc(L ,R) 
        # Test get_endPoint method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
    
        x_end, y_end, hdg_end =  arc.get_endPoint(x0, y0, hdg)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x_end, 9.200651963458439, places=3)  # Example expected value of x_end, rounded to 3 decimal places
        self.assertAlmostEqual(y_end, 2.699544827129283, places=3)  # Example expected value of y_end, rounded to 3 decimal places
        self.assertAlmostEqual(hdg_end, -0.21460183660255172, places=3)  # Example expected value of hdg_end, rounded to 3 decimal places
    
    def test_XY2ST_3(self):
        L = 10
        R = 10
    
        arc = Arc(L ,R) 
        # Test XY2ST method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
        X, Y, S0 = 1, 1, 0  # Example values
    
        S, T =  arc.XY2ST(x0, y0, hdg, X, Y, S0)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(S, 1.4048970175352027, places=3)  # Example expected value of S, rounded to 3 decimal places
        self.assertAlmostEqual(T, -0.09950493836207741, places=3)  # Example expected value of T, rounded to 3 decimal places


    def test_ST2XY_XY2ST(self):
    
        Radius = 15
        L = 2*np.pi*Radius
        arc = Arc(L ,Radius)
        T = 0
        S0 = 0
        for S in np.arange(0,10,1):
            for T in np.arange(0,10,1):
                for hdg in np.arange(0,2*np.pi,.1):  
                    # Test XY2ST method with some sample input
                    x0, y0 = 0, 0 #, np.pi / 4  # Example values
                    
                    print("hdg" , hdg)
                    print("S",S,"T", T)
                    X, Y  = arc.ST2XY(x0, y0, hdg, S, S0, T)
                    
                    print("X",X,"Y", Y)
                    
                    print(X, Y)
                    S2, T2 = arc.XY2ST(x0, y0, hdg, X, Y, S0)
    
                    print("S2",S2,"T2", T2)
    
                    # Assert the expected values based on calculations or known answers
                    self.assertAlmostEqual(S, S2, places=3)  # Example expected value of S, rounded to 3 decimal places
                    self.assertAlmostEqual(T, T2, places=3)  # Example expected value of T, rounded to 3 decimal places


    def test_XY2ST_ST2XY(self):
    
        Radius = 15
        L = 2*np.pi*Radius
        arc = Arc(L ,Radius)
    
 
    
    
        for x0 in np.arange(-3,3,1):
            for y0 in np.arange(-3,3,1):
                for hdg in np.arange(0, np.pi,.1):  
                    # Test XY2ST method with some sample input
                    #x0, y0, hdg = 0, 0, 0# np.pi / 4  # Example values
                    
                    print("X0",x0,"y", y0)
                    
                    X, Y, S0 = 1 + x0  , 1 +y0  , 0  # Example values

                    print("X",X,"Y", Y)

                    
                    S, T = arc.XY2ST(x0, y0, hdg, X, Y, S0)
                    print("S",S,"T", T)
                    
                    
                    X2,Y2 = arc.ST2XY(x0, y0, hdg, S, S0, T)
                    
                    print("hdg" , hdg)
                    

                    print("X2",X2,"Y2", Y2)
                    
                    # Assert the expected values based on calculations or known answers
                    self.assertAlmostEqual(X, X2, places=3)  # Example expected value of S, rounded to 3 decimal places
                    self.assertAlmostEqual(Y, Y2, places=3)  # Example expected value of T, rounded to 3 decimal places 




########################################################################
    
    def test_ST2XY_negativR(self):
    
        
        Radius = -15
        L = np.abs(2*np.pi*Radius)
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.abs(np.pi*Radius ), 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        
        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0    , places=3)  # Example expected value of y, rounded to 3 decimal places


        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        hdg = 2*np.pi    


 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
    
    

    def test_ST2XY_1__negativR(self):
    
        
        Radius = -15
        L = np.abs(2*np.pi*Radius)
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.abs(np.pi*Radius ), 0, 1  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,  0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius+1     , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        
        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius -1 , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0   , places=3)  # Example expected value of y, rounded to 3 decimal places


        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius-1    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        hdg = 2*np.pi    


 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,  0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius+1     , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        

    def test_XY2ST__negativR(self):
    
        
        Radius = -15
        L = np.abs(2*np.pi*Radius+0.1)
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.abs(np.pi*Radius ), 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 2* Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  0    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        
        hdg = 2*np.pi    

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x, 0  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -2* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places       
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places


    def test_XY2ST_2_negativR(self):
    
        
        Radius = -15
        L = np.abs( 2*np.pi*Radius )
        arc = Arc(L ,Radius) 
    
        # Test ST2XY method with some sample input
        x0, y0, hdg = 0, 0,  0  #np.pi / 4  # Example values
        S, S0, T = np.abs( np.pi*Radius /2), 0, 0  # Example values
    
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,np.abs( Radius)  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -1* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)
        
 
        
        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        
        hdg = np.pi /2  

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,   Radius  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,  np.abs( Radius )   , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        hdg = np.pi    

 
 
 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,   Radius   , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y,    Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places

        

        
        hdg = 2*np.pi    

 
        x, y =  arc.ST2XY(x0, y0, hdg, S, S0, T)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x,np.abs( Radius)  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(y, -1* Radius    , places=3)  # Example expected value of y, rounded to 3 decimal places
        
        S2 ,T2 = arc.XY2ST(x0, y0, hdg, x, y, S0)

        self.assertAlmostEqual(S, S2  , places=3)  # Example expected value of x, rounded to 3 decimal places
        self.assertAlmostEqual(T2, 0    , places=3)  # Example expected value of y, rounded to 3 decimal places



                
    def test_get_endPoint_negativR(self):
        L = 10
        R = -10
    
        arc = Arc(L ,R) 
        # Test get_endPoint method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
    
        x_end, y_end, hdg_end =  arc.get_endPoint(x0, y0, hdg)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(x_end, 2.699544827129282, places=3)  # Example expected value of x_end, rounded to 3 decimal places
        self.assertAlmostEqual(y_end, 9.200651963458435, places=3)  # Example expected value of y_end, rounded to 3 decimal places
        self.assertAlmostEqual(hdg_end, 1.7853981633974483, places=3)  # Example expected value of hdg_end, rounded to 3 decimal places
   
    def test_XY2ST_3_negativR(self):
        L = 10
        R = -10
    
        arc = Arc(L ,R) 
        # Test XY2ST method with some sample input
        x0, y0, hdg = 0, 0, np.pi / 4  # Example values
        X, Y, S0 = 1, 1, 0  # Example values
    
        S, T =  arc.XY2ST(x0, y0, hdg, X, Y, S0)
    
        # Assert the expected values based on calculations or known answers
        self.assertAlmostEqual(S, 1.4048970175352027, places=3)  # Example expected value of S, rounded to 3 decimal places
        self.assertAlmostEqual(T, 0.09950493836207741, places=3)  # Example expected value of T, rounded to 3 decimal places


    # def test_ST2XY_XY2ST_negativR(self):
    #
    #     Radius = -15
    #     L = np.abs(3*np.pi*Radius)
    #     arc = Arc(L ,Radius)
    #     T = 0
    #     S0 = 0
    #     for S in np.arange(0,10,1):
    #         for T in np.arange(0,10,1):
    #             for hdg in np.arange(0,2*np.pi,.1):  
    #                 # Test XY2ST method with some sample input
    #                 x0, y0 = 0, 0 #, np.pi / 4  # Example values
    #
    #                 print("hdg" , hdg)
    #                 print("S",S,"T", T)
    #                 X, Y  = arc.ST2XY(x0, y0, hdg, S, S0, T)
    #
    #                 print("X",X,"Y", Y)
    #
    #                 print(X, Y)
    #                 S2, T2 = arc.XY2ST(x0, y0, hdg, X, Y, S0)
    #
    #                 print("S2",S2,"T2", T2)
    #
    #                 # Assert the expected values based on calculations or known answers
    #                 self.assertAlmostEqual(S, S2, places=3)  # Example expected value of S, rounded to 3 decimal places
    #                 self.assertAlmostEqual(T, T2, places=3)  # Example expected value of T, rounded to 3 decimal places
    #
    #
    # def test_XY2ST_ST2XY_negativR(self):
    #
    #     Radius = -15
    #     L = np.abs(2*np.pi*Radius)
    #     arc = Arc(L ,Radius)
    #
    #
    #
    #
    #     for x0 in np.arange(-3,3,1):
    #         for y0 in np.arange(-3,3,1):
    #             for hdg in np.arange(0, np.pi,.1):  
    #                 # Test XY2ST method with some sample input
    #                 #x0, y0, hdg = 0, 0, 0# np.pi / 4  # Example values
    #
    #                 print("X0",x0,"y", y0)
    #
    #                 X, Y, S0 = 1 + x0  , 1 +y0  , 0  # Example values
    #
    #                 print("X",X,"Y", Y)
    #
    #
    #                 S, T = arc.XY2ST(x0, y0, hdg, X, Y, S0)
    #                 print("S",S,"T", T)
    #
    #
    #                 X2,Y2 = arc.ST2XY(x0, y0, hdg, S, S0, T)
    #
    #                 print("hdg" , hdg)
    #
    #
    #                 print("X2",X2,"Y2", Y2)
    #
    #                 # Assert the expected values based on calculations or known answers
    #                 self.assertAlmostEqual(X, X2, places=3)  # Example expected value of S, rounded to 3 decimal places
    #                 self.assertAlmostEqual(Y, Y2, places=3)  # Example expected value of T, rounded to 3 decimal places 
    #




 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()