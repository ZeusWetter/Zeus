import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import unittest
from unittest.mock import patch, MagicMock, mock_open
from backend.app.utility_scripts import load_stations_data, load_stations_from_file, load_station_inventory, load_inventory_from_file, haversine_distance, find_nearest_stations, download_weather_data, calculate_means
import testdata

class TestLoadStationsData(unittest.TestCase):

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_load_stations_data_success(self, mock_get):
        """Tests if the function loads and saves weather station data correctly"""
        # Simulate response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = testdata.testdata_load_stations["mock_response_text"]
        mock_get.return_value = mock_response

        # Check if data directory exists
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        os.makedirs(data_dir, exist_ok=True)

        result = load_stations_data()

        # Check if the file has been saved
        stations_path = os.path.join(data_dir, "stations.json")
        self.assertTrue(os.path.exists(stations_path), f"File {stations_path} not found.")
        self.assertTrue(result)

        # Check if the content has been saved correctly
        with open(stations_path, "r") as f:
            data = json.load(f)
            self.assertEqual(data[0]["ID"], "GME00129634", f"Failed. Expected: GME00129634, but got: {data[0]['ID']}.")
            self.assertEqual(data[0]["Latitude"], 48.0458, f"Failed. Expected: 48.0458, but got: {data[0]['Latitude']}.")
            self.assertEqual(data[0]["Longitude"], 8.4617, f"Failed. Expected: 8.4617, but got: {data[0]['Longitude']}.")

        # Delete file after test
        os.remove(stations_path)

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_load_stations_data_failure(self, mock_get):
        """Tests the behavior if the Website is not available"""
        mock_get.return_value.status_code = 404  # Simulate error

        result = load_stations_data()

        # Check if the function returns False if the download fails
        self.assertFalse(result, f"Failed. Expected: False, but got: {result}.")

class TestLoadStationsFromFile(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=testdata.testdata_load_stations["read_data"])
    def test_load_stations_success(self, mock_file):
        """Tests the successful loading of weather station data from the JSON file"""
        result = load_stations_from_file()

        # Check if the data was loaded correctly
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["ID"], "GME00129634", f"Failed. Expected: GME00129634, but got: {result[0]['ID']}.")
        self.assertEqual(result[0]["Latitude"], 48.0458, f"Failed. Expected: 48.0458, but got: {result[0]['Latitude']}.")
        self.assertEqual(result[0]["Longitude"], 8.4617, f"Failed. Expected: 8.4617, but got: {result[0]['Longitude']}.")

        # Check if the file was opened
        mock_file.assert_called_with("data/stations.json", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_stations_file_not_found(self, mock_file):
        """Tests the behavior if the JSON file does not exist"""
        result = load_stations_from_file()

        # Check if {} is returned if the file is missing
        self.assertEqual(result, {}, f"Failed. Expected: {{}}, but got: {result}.")

class TestLoadStationInventory(unittest.TestCase):

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_load_station_inventory_success(self, mock_get):
        """Tests if the function loads and saves inventory data correctly"""
        # Simulate response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = testdata.testdata_load_inventory["mock_response_text"]
        mock_get.return_value = mock_response

        # Check if data directory exists
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
        os.makedirs(data_dir, exist_ok=True)

        result = load_station_inventory()

        # Check if the file has been saved
        inventory_path = os.path.join(data_dir, "inventory.json")
        self.assertTrue(os.path.exists(inventory_path), f"File {inventory_path} not found.")
        self.assertTrue(result)

        # Check if the content has been saved correctly
        with open(inventory_path, "r") as f:
            data = json.load(f)
            self.assertIn("GME00129634", data, f"Failed. Expected: GME00129634, but got: {data}.")
            self.assertIn("TMAX", data["GME00129634"], f"Failed. Expected: TMAX, but got: {data['GME00129634']}.")
            self.assertIn("TMIN", data["GME00129634"], f"Failed. Expected: TMIN, but got: {data['GME00129634']}.")
            self.assertEqual(data["GME00129634"]["TMAX"], [1947, 2025],
                             f"Failed. Expected: [1947, 2025], but got: {data['GME00129634']['TMAX']}.")
            self.assertEqual(data["GME00129634"]["TMIN"], [1947, 2025],
                             f"Failed. Expected: [1947, 2025], but got: {data['GME00129634']['TMIN']}.")

        # Delete file after test
        os.remove(inventory_path)

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_load_station_inventory_failure(self, mock_get):
        """Tests the behavior if the Website is not available"""
        mock_get.return_value.status_code = 404  # Simulate error

        result = load_station_inventory()

        # Check if the function returns False if the download fails
        self.assertFalse(result, f"Failed. Expected: False, but got: {result}.")

class TestLoadInventoryFromFile(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=testdata.testdata_load_inventory["read_data"])
    def test_load_inventory_success(self, mock_file):
        """Tests the successful loading of inventory data from the JSON file"""
        result = load_inventory_from_file()

        # Check if the data was loaded correctly
        self.assertIsInstance(result, dict)
        self.assertIn("GME00129634", result, f"Failed. Expected: GME00129634, but got: {result}.")
        self.assertIn("TMAX", result["GME00129634"], f"Failed. Expected: TMAX, but got: {result['GME00129634']}.")
        self.assertIn("TMIN", result["GME00129634"], f"Failed. Expected: TMIN, but got: {result['GME00129634']}.")
        self.assertEqual(result["GME00129634"]["TMAX"], [1947, 2024],
                         f"Failed. Expected: [1947, 2024], but got: {result['GME00129634']['TMAX']}.")
        self.assertEqual(result["GME00129634"]["TMIN"], [1947, 2024],
                         f"Failed. Expected: [1947, 2024], but got: {result['GME00129634']['TMIN']}.")

        # Check if the file was opened
        mock_file.assert_called_with("data/inventory.json", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_inventory_file_not_found(self, mock_file):
        """Tests the behavior if the JSON file does not exist"""
        result = load_inventory_from_file()

        # Check if {} is returned if the file is missing
        self.assertEqual(result, {}, f"Failed. Expected: {{}}, but got: {result}.")

class TestHaversineDistance(unittest.TestCase):

    def test_haversine_distance(self):
        """Tests the calculation of distances"""
        for lat1, lon1, lat2, lon2, expected in testdata.testdata_haversine:
            with self.subTest(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2):  # Prevents an error from stopping the further tests
                result = haversine_distance(lat1, lon1, lat2, lon2)
                self.assertAlmostEqual(result, expected, delta=1,  # Range of 1 km allowed to avoid roundig errors
                                       msg=f"Failed for input: ({lat1}, {lon1}) -> ({lat2}, {lon2}). Expected {expected} km, but got {result} km.")

class TestFindNearestStations(unittest.TestCase):

    @patch("backend.app.utility_scripts.load_stations_from_file", return_value=testdata.testdata_stations)
    @patch("backend.app.utility_scripts.load_inventory_from_file", return_value=testdata.testdata_inventory)
    def test_find_nearest_stations(self, mock_stations, mock_inventory):
        """Tests if the expected stations are returned"""
        for case in testdata.testdata_nearest_station:
            user_lat, user_lon, radius, max_stations, start_year, end_year = case["input"]
            expected_ids = set(case["expected_ids"])

            with self.subTest(user_lat=user_lat, user_lon=user_lon, radius=radius, max_stations=max_stations):
                result = find_nearest_stations(user_lat, user_lon, radius, max_stations, start_year, end_year)

                # Extract station IDs
                result_ids = {station["ID"] for station in result}

                # Check the expected station IDs
                self.assertEqual(result_ids, expected_ids, 
                                 f"Failed. Expected: {expected_ids}, but got: {result_ids}.")

                # Check if a maximum of "max_stations" are returned
                self.assertLessEqual(len(result), max_stations, 
                                     f"Maximum number of stations exceeded: {len(result)} stations instead of {max_stations} stations.")

                # Check if the returned stations are sorted by distance
                distances = [station["Distance"] for station in result]
                self.assertEqual(distances, sorted(distances), 
                                 "The stations are not correctly sorted by distance.")
                
class TestDownloadWeatherData(unittest.TestCase):

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_download_weather_data_success(self, mock_get):
        """Tests if weather data is successfully downloaded and saved"""
        # Simulate response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = testdata.testdata_download_weather["mock_response_text"]
        mock_get.return_value = mock_response

        result = download_weather_data("GME00129634", 2020, 2021)

        # Check if the weather data has been processed correctly
        self.assertIsInstance(result, dict)
        self.assertIn("data", result, "Key 'data' is missing in the weather data.")

        # Check if example date is in the data
        self.assertEqual(result["data"]["2021-01-01"]["TMAX"], 0.8)
        self.assertEqual(result["data"]["2021-01-01"]["TMIN"], -2.4)

    @patch("backend.app.utility_scripts.requests.get")  # Mocks GET request
    def test_download_weather_data_failure(self, mock_get):
        """Tests the behavior if the Website is not available"""
        mock_get.return_value.status_code = 404  # Simulate error

        # Check if the function raises a ValueError if the website is not available
        with self.assertRaises(ValueError, msg="Failed. ValueError not raised."):
            download_weather_data("GME00129634", 2020, 2021)

class TestCalculateMeans(unittest.TestCase):

    def test_calculate_means(self):
        """Tests the correct calculation of mean values for weather data"""
        station_weather_data = {"data": testdata.testdata_calculate_means["weather_data"]}
        first_year = testdata.testdata_calculate_means["first_year"]
        last_year = testdata.testdata_calculate_means["last_year"]
        latitude = testdata.testdata_calculate_means["latitude"]
        expected_result = testdata.testdata_calculate_means["expected_result"]

        result = calculate_means(station_weather_data, first_year, last_year, latitude)

        self.assertEqual(result, expected_result, f"Failed. Expected {expected_result}, but got {result}.")

if __name__ == "__main__":
    unittest.main()
