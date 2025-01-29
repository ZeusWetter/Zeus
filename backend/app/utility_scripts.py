import requests, math
import pandas as pd
from io import StringIO

# in folgender Funktion werden die Daten der
# Wetterstationen in eine JSON Datei eingelesen
def load_stations_data():
    url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
    file_path = "data/stations.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("Datenzugriff war erfolgreich")
        # Die einzelnen Spalten benennen
        columns = ["ID", "Latitude", "Longitude", "Elevation", "State", "Name"]
        # Start- und Endpositionen der Spalten im Fixed-Width Format angeben
        colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
        # Daten in einem Data Frame speichern
        stations = pd.read_fwf(StringIO(response.text), colspecs=colspecs, header=None, names=columns)
        # Die Daten in eine JSON-Datei speichern
        stations.to_json(file_path, orient="records", indent=4)
        print(f"Daten erfolgreich in {file_path} gespeichert")
        return stations
    else:
        print(f"Fehler beim Herunterladen der Datei: {response.status_code}")
        return None


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


def find_nearest_stations(user_lat, user_lon, radius, max_stations, json_data):
    stations = json_data
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
    return result

if __name__ == "__main__":
    try:
        load_stations_data()
    except Exception as e:
        print(e)
