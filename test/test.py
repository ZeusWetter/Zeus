import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import unittest
from backend.app.utility_scripts import haversine_distance, find_nearest_stations
import testdata

class TestFunctions(unittest.TestCase):

    def test_haversine_distance(self):
        # Tests the calculation of distances
        for lat1, lon1, lat2, lon2, expected in testdata.testdata_haversine:
            with self.subTest(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2): # Prevents an error from stopping all further tests
                result = haversine_distance(lat1, lon1, lat2, lon2)
                self.assertAlmostEqual(result, expected, delta=1, # Range of 1 km allowed to avoid roundig errors
                                       msg=f"Failed for input: ({lat1}, {lon1}) -> ({lat2}, {lon2}). Expected {expected} km, but got {result} km.")

    def test_find_stations_within_radius(self):
        # Tests if only stations within the radius are returned and if a maximum of 'max_stations' are returned
        for user_lat, user_lon, radius, max_stations, expected in testdata.testdata_nearest_station:
            with self.subTest(radius=radius, max_stations=max_stations):
                result = find_nearest_stations(user_lat, user_lon, radius, max_stations, testdata.testdata_stations)
                self.assertLessEqual(len(result), expected,
                                     f"Failed for given input. Expected {expected} stations, but got {len(result)} stations.")
    
    def test_stations_sorted_by_distance(self):
        # Tests if the returned stations are sorted by distance
        result = find_nearest_stations(48.0458, 8.4617, 100, 3, testdata.testdata_stations)
        distances = [station["Distance"] for station in result]
        self.assertEqual(distances, sorted(distances), "Stations are not sorted by distance.")
                         
if __name__ == "__main__":
    unittest.main()
