testdata_haversine = [
    # (lat1, lon1, lat2, lon2, expected)
    (52.5200, 13.4050, 48.1351, 11.5820, 504.4), # Berlin -> Muenchen, 504.4 km expected
    (52.5200, 13.4050, 52.5200, 13.4050, 0) # Same coordinates, 0 km expected
]

testdata_stations = [
    # Sample data to test the find_nearest_stations function
    {"Station": "GME00129634", "Latitude": 48.0458, "Longitude": 8.4617}, # Villingen-Schwenningen
    {"Station": "GME00122458", "Latitude": 48.0242, "Longitude": 7.8353}, # Freiburg
    {"Station": "GME00129490", "Latitude": 48.5206, "Longitude": 9.0525}, # Tuebingen
    {"Station": "GME00129442", "Latitude": 48.3142, "Longitude": 9.2481}, # Trochtelfingen
    {"Station": "GME00127850", "Latitude": 52.5331, "Longitude": 13.3831} # Berlin-Mitte
]

testdata_nearest_station = [
    # (user_lat, user_lon, radius, max_stations, expected)
    (48.0458, 8.4617, 100, 5, 4), # Villingen-Schwenningen, 100 km radius, max 5 stations, 4 stations expected
    (48.0458, 8.4617, 100, 3, 3), # Villingen-Schwenningen, 100 km radius, max 3 stations, 3 stations expected
    (48.0452, 8.3716, 1, 5, 0) # Remote location, 1 km radius, 0 stations expected
]