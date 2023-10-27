'''
Created on 27.10.2023

@author: abdel
'''
import unittest
from terrain.terrain import  *

class TestGBSDegrees2Decimal(unittest.TestCase):
    def test_degrees_minutes_seconds_conversion(self):
        coordinates = [45, 30, 30]
        decimal_degrees = gbs_Degrees2Decimal(coordinates)
        self.assertAlmostEqual(decimal_degrees, 45.50833333333333, places=7)

    def test_degrees_minutes_conversion(self):
        coordinates = [35, 15]
        decimal_degrees = gbs_Degrees2Decimal(coordinates)
        self.assertAlmostEqual(decimal_degrees, 35.25, places=7)

    def test_invalid_input(self):
        invalid_input = 42
        result = gbs_Degrees2Decimal(invalid_input)
        self.assertEqual(result, 42)

    def test_empty_input(self):
        empty_input = []
        result = gbs_Degrees2Decimal(empty_input)
        self.assertEqual(result, [])



class TestGBSDecimal2Degrees(unittest.TestCase):
    def test_decimal_to_degrees_minutes_seconds(self):
        decimal_degrees = 45.50833333333334
        result = gbs_Decimal2Degrees(decimal_degrees)
        self.assertEqual(result, [45, 30, 30])

    def test_negative_decimal_to_degrees_minutes_seconds(self):
        decimal_degrees = -120.72555555555556
        result = gbs_Decimal2Degrees(decimal_degrees)
        self.assertEqual(result, [-120, 43, 32])

    def test_large_decimal_to_degrees_minutes_seconds(self):
        decimal_degrees = 100.987654321
        result = gbs_Decimal2Degrees(decimal_degrees)
        self.assertEqual(result, [100, 59, 15])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main() 