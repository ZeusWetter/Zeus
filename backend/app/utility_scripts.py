import requests, math
import pandas as pd
from io import StringIO

# in folgender Funktion werden die Daten der
# Wetterstationen in eine JSON Datei eingelesen
def load_stations_data():
    url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
    # file_path = "data/stations.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("Datenzugriff war erfolgreich")
        # Die einzelnen Spalten benennen
        columns = ["ID", "Latitude", "Longitude", "Elevation", "State", "Name"]
        # Start- und Endpositionen der Spalten im Fixed-Width Format angeben
        colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
        # Daten in einem Data Frame speichern
        stations = pd.read_fwf(StringIO(response.text), colspecs=colspecs, header=None, names=columns)

        # Die Daten optional in eine JSON-Datei speichern
        # stations.to_json(file_path, orient="records", indent=4)
        # print(f"Daten erfolgreich in {file_path} gespeichert")

        return stations
    else:
        print(f"Fehler beim Herunterladen der Datei: {response.status_code}")
        return None


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    lat1: Breitengrad Punkt 1
    lon1: Längengrad Punkt 1
    lat2: Breitengrad Punkt 2
    lon2: Längengrad Punkt 2
    """
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
    """
    user_lat: Eingabe Breitengrad des Users
    user_lon: Eingabe Längengrad des Users
    radius: Eingabe radius des Users
    max_stations: Anzahl anzuzeigender Stationen. Eingabe des Users
    json_data: JSON Daten der Stationen
    """
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

    nearby_stations.sort(key=lambda x: x["Distance"]) # Das lambda gibt an, dass die Liste nach dem Wert des Schlüssels "Distance" in jedem Dictionary sortiert wird.
    result = nearby_stations[:max_stations]
    return result

def download_weather_data(station_id, start_year, end_year):
    """"
    station_id: ID der Wetterstation. Beispiel Villingen-Schwenningen = "GME00129634"})
    start_year: Startjahr im Format "YYYY"
    end_year: Endjahr im Format "YYYY"
    """
    url = f"https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/{station_id}.dly"
    
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise ValueError(f"Fehler beim Herunterladen der Datei: {url}")
    
    weather_data = {"station": station_id, "data": {}} # Datenstruktur wird erstellt

    # Typumwandlungen für Vergleich
    start_year = int(start_year)
    end_year = int(end_year)

    # Direkt aus dem Stream lesen, ohne die Datei zu speichern
    for line in response.iter_lines(decode_unicode=True):
        if line:  # Stelle sicher, dass die Zeile nicht leer ist
            year = line[11:15]  # YYYY
            month = line[15:17]  # MM
            element = line[17:21]  # Wettervariable (TMAX, TMIN)

            if start_year <= int(year) <= end_year and element in ["TMAX", "TMIN"]:
                for day in range(1, 32):  # Maximal 31 Tage pro Monat
                    pos = 21 + (day - 1) * 8 # Erster Tag ist an der 21 Stelle. Jeder Tag Inklusive Flag ist 8 Zeichen breit
                    if pos + 5 <= len(line):  # Sicherstellen, dass der Index existiert
                        value = int(line[pos:pos+5]) # extrahiert Daten aus der Zeile (5 Buchstaben pro Tag)
                        if value == -9999:
                            value = None
                        else: 
                            value = value /10
                        date = f"{year}-{month}-{day:02d}" # 02d stellt sicher dass der Tag immer zweistellig ist 1 -> 01
                        
                        if date not in weather_data["data"]:
                            weather_data["data"][date] = {"TMAX": None, "TMIN": None} 
                        
                        weather_data["data"][date][element] = value
    return weather_data

if __name__ == "__main__":
    try:
        load_stations_data()
    except Exception as e:
        print(e)
