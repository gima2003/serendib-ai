import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from backend.agents.planner.route.data_cleaner import (
    clean_roads_data,
    clean_bus_fares_data,
    clean_scenic_places_data,
    clean_text_series
)

class TestDataCleaner(unittest.TestCase):
    def test_clean_text_series(self):
        series = pd.Series(["  Colombo  ", " ", "NaN", "None", "Kandy", ""])
        cleaned = clean_text_series(series)
        self.assertEqual(cleaned.iloc[0], "Colombo")
        self.assertTrue(pd.isna(cleaned.iloc[1]))
        self.assertTrue(pd.isna(cleaned.iloc[2]))
        self.assertTrue(pd.isna(cleaned.iloc[3]))
        self.assertEqual(cleaned.iloc[4], "Kandy")
        self.assertTrue(pd.isna(cleaned.iloc[5]))
        
    def test_clean_roads_data(self):
        data = {
            'road_name': ['A1 ', ' A2', 'A1 '],
            'length_km': ['10.5', 'invalid', '10.5'],
            'road_condition': ['GOOD', '  Poor ', 'GOOD'],
            'geometry': ['LINESTRING(1 1)', None, 'LINESTRING(1 1)']
        }
        df = pd.DataFrame(data)
        cleaned = clean_roads_data(df)
        
        # Deduplication
        self.assertEqual(len(cleaned), 2)
        
        # Text cleaning and lowercasing
        self.assertEqual(cleaned['road_name'].iloc[0], 'A1')
        self.assertEqual(cleaned['road_condition'].iloc[1], 'poor')
        
        # Numeric conversion
        self.assertEqual(cleaned['length_km'].iloc[0], 10.5)
        self.assertTrue(np.isnan(cleaned['length_km'].iloc[1]))
        
        # Geometry validation
        self.assertTrue(cleaned['geometry_valid'].iloc[0])
        self.assertFalse(cleaned['geometry_valid'].iloc[1])
        
    def test_clean_bus_fares_data(self):
        data = {
            'Route_ID': ['R1', 'R2', 'R1'],
            'From': ['Colombo', 'Kandy', 'Colombo'],
            'Fare (LKR)': ['100.5', 'Rs 6000', '100.5']
        }
        df = pd.DataFrame(data)
        cleaned = clean_bus_fares_data(df)
        
        # Deduplication
        self.assertEqual(len(cleaned), 2)
        
        # Numeric conversion and suspicious flags
        self.assertEqual(cleaned['Fare (LKR)'].iloc[0], 100.5)
        self.assertEqual(cleaned['Fare (LKR)'].iloc[1], 6000.0)
        
        self.assertTrue(cleaned['fare_valid'].iloc[0])
        self.assertFalse(cleaned['fare_valid'].iloc[1]) # > 5000 is flagged suspicious
        
    def test_clean_scenic_places_data(self):
        data = {
            'osm_id': [1, 2, 3, 1],
            'name': ['Sigiriya ', 'Fake Place', 'Galle Fort', 'Sigiriya '],
            'latitude': ['7.957', '1.0', '6.033', '7.957'], # Fake place has lat 1.0 (invalid for LK)
            'longitude': ['80.760', '80.0', '80.217', '80.760'],
            'category': ['Heritage', 'None', 'Heritage', 'Heritage']
        }
        df = pd.DataFrame(data)
        cleaned = clean_scenic_places_data(df)
        
        # Deduplication and rejection of invalid coordinates
        self.assertEqual(len(cleaned), 2)
        
        self.assertEqual(cleaned['name'].iloc[0], 'Sigiriya')
        self.assertEqual(cleaned['category'].iloc[0], 'heritage')
        
        # Fake Place should be dropped
        self.assertNotIn('Fake Place', cleaned['name'].values)

if __name__ == '__main__':
    unittest.main()
