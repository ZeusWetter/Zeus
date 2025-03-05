import numpy as np

testdata_haversine = [
    # (lat1, lon1, lat2, lon2, expected)
    (52.5200, 13.4050, 48.1351, 11.5820, 504.4), # Berlin -> Muenchen, 504.4 km expected
    (52.5200, 13.4050, 52.5200, 13.4050, 0) # Same coordinates, 0 km expected
]

testdata_stations = [
    # Sample data to test the find_nearest_stations function
    {"ID": "GME00129634", "Latitude": 48.0458, "Longitude": 8.4617}, # Villingen-Schwenningen
    {"ID": "GME00122458", "Latitude": 48.0242, "Longitude": 7.8353}, # Freiburg
    {"ID": "GME00129490", "Latitude": 48.5206, "Longitude": 9.0525}, # Tuebingen
    {"ID": "GME00129442", "Latitude": 48.3142, "Longitude": 9.2481}, # Trochtelfingen
    {"ID": "GME00127850", "Latitude": 52.5331, "Longitude": 13.3831} # Berlin-Mitte
]

testdata_inventory = {
    "GME00129634": {"TMAX": (1947, 2024), "TMIN": (1947, 2024)},
    "GME00122458": {"TMAX": (1881, 2024), "TMIN": (1881, 2024)},
    "GME00129490": {"TMAX": (1950, 1982), "TMIN": (1950, 1982)},
    "GME00129442": {"TMAX": (1947, 1973), "TMIN": (1947, 1973)},
    "GME00127850": {"TMAX": (1956, 1964), "TMIN": (1956, 1964)}
}

testdata_nearest_station = [
    # (user_lat, user_lon, radius, max_stations, start_year, end_year)
    {
        "input": [48.0458, 8.4617, 100, 5, 1956, 1964],
        "expected_ids": ["GME00129634", "GME00122458", "GME00129490", "GME00129442"] # Villingen-Schwenningen, 100 km radius, max 5 stations, 4 stations expected
    },
    {
        "input": [48.0458, 8.4617, 100, 3, 1956, 1964],
        "expected_ids": ["GME00129634", "GME00122458", "GME00129442"] # Villingen-Schwenningen, 100 km radius, max 3 stations, 3 stations expected
    },
    {
        "input": [47.3759, -31.2243, 1, 5, 1956, 1964],
        "expected_ids": [] # Remote location, 1 km radius, 0 stations expected
    }
]

testdata_download_weather = {
    "station_id": "GME00129634",  # Villingen-Schwenningen
    "start_year": 2020,
    "end_year": 2021,
    "example_date": "2020-01-01"
}

testdata_calculate_means = {
    "weather_data": {
        "2024-01-01": {"TMAX": 10.0, "TMIN": 3.0},
        "2024-01-02": {"TMAX": 12.0, "TMIN": 4.0},
        "2024-01-03": {"TMAX": 8.0, "TMIN": 2.0}
    },
    "first_year": 2023,
    "last_year": 2024,
    "latitude": 48.0458,
    "expected_result": {
        "entire_year": {
            2024: {"TMAX": np.float64(10.0), "TMIN": np.float64(3.0)}
        },
        "winter": {
            2024: {"TMAX": np.float64(10.0), "TMIN": np.float64(3.0)}
        },
        "spring": {},
        "summer": {},
        "autumn": {}
    }
}