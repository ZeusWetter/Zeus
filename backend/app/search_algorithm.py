import math
import json

def haversine_distance(lat1, lon1, lat2, lon2):
    # Diese Funktion berechnet den Abstand zwischen 2 Punkten mit der Haversine-Formel.
    earth_radius = 6371.0 # Radius der Erde in km

# sin() und cos() erwarten die Werte in Radiant und nicht in Grad
    lat1_rad = math.radians(lat1) 
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

# Differenzen lat und lon werden berechnet
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine-Formel anwenden
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Entfernung berechnen
    distance = earth_radius * c
    return distance

# erstmal auslassen und Perfomance ohne testen: def calculate_bounds(lat, lon, radius):

def find_nearest_stations(user_lat, user_lon, radius, max_stations):
    json_file ="backend/app/data/stations.json"

    # Auf die JSON Datei wird im Lesemodus zugegriffen und in der neuen Variable stations gespeichert -> Liste mit Dictionaries
    with open(json_file, "r") as file:
        stations = json.load(file)
    
    nearby_stations = [] # Liste für die n nächsten Stationen

    # Iteration über alle Stationen in der Liste stations um den Abstand zu berechnen. Dies geschieht über die haversine_distance Funktion
    for station in stations:
        station_lat = station["Latitude"]
        station_lon = station["Longitude"]
        distance = haversine_distance(user_lat, user_lon, station_lat, station_lon)
        if distance <= radius:
            station_copy = station.copy()
            station_copy["Distance"] = distance
            nearby_stations.append(station_copy)

    nearby_stations.sort(key=lambda x: x["Distance"])# Das lambda gibt an, dass die Liste nach dem Wert des Schlüssels "Distance" in jedem Dictionary sortiert wird.
    result = nearby_stations[:max_stations]
    
    # Ergebnis in einer neuen JSON-Datei speichern
    output_file = "backend/app/data/nearest_stations.json"
    with open(output_file, "w") as outfile:
        json.dump(result, outfile, indent=4)

    return json.dumps(result, indent=4)

if __name__ == "__main__":

    user_lat = 48.0594 # Koordinaten von Villingen-Schwenningen
    user_lon = 8.4641
    search_radius = 100  # Radius in Kilometern
    max_stations = 5  # Maximale Anzahl der nächsten Stationen

    results_json = find_nearest_stations(user_lat, user_lon, search_radius, max_stations)
    print("Nächste Stationen innerhalb des Radius als JSON:")
    print(results_json)

