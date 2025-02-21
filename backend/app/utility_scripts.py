import requests, math
import pandas as pd
import numpy as np
import json
import os
from io import StringIO
from collections import OrderedDict

# in folgender Funktion werden die Daten der
# Wetterstationen in eine JSON Datei eingelesen
def load_stations_data():
    """
    Lädt die Stationsdaten herunter und speichert sie in einer JSON unter data/stations.json

    Rückgabe: True / False im Bezug auf erolgreiche Durchführung
    """
    url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
    file_path = "data/stations.json"

    # Verzeichnis prüfen und erstellen, falls es nicht existiert
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    response = requests.get(url)
    if response.status_code == 200:
        # Die einzelnen Spalten benennen
        columns = ["ID", "Latitude", "Longitude", "Elevation", "State", "Name"]
        # Start- und Endpositionen der Spalten im Fixed-Width Format angeben
        colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
        # Daten in einem Data Frame speichern
        stations = pd.read_fwf(StringIO(response.text), colspecs=colspecs, header=None, names=columns)
        # Die Daten in eine JSON-Datei speichern
        stations.to_json(file_path, orient="records", indent=4)
        return True # Funktion gibt True zurück wenn die Daten erfolgreich gespeichert werden konnten
    else:
        print(f"Fehler beim Herunterladen der Datei: {response.status_code}")
        return False # False signalisiert hier, dass die Daten nicht erfolgreich gespeichert werden konnten

def load_stations_from_file():
    """
    Diese Funktion öffnet die JSON Datei stations.json und gibt diese als Dictionary zurück.

    Rückgabe: Dictionary mit den Stationsdaten
    """
    file_path = "data/stations.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)  # JSON in ein Dictionary umwandeln
    except FileNotFoundError:
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return {}

def load_station_inventory():
    """
    Lädt die Inventardaten der Stationen herunter und speichert sie in einer JSON unter data/inventory.json

    Rückgabe: True / False im Bezug auf erolgreiche Durchführung
    """
    url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt"
    response = requests.get(url)
    file_path = "data/inventory.json"
        
    if response.status_code != 200:
        print("Fehler beim Laden der Inventardatei")
        return False # Zeigt an dass die Daten nicht gespeichert werden konnten

    inventory = {}
        
    # Datei Zeile für Zeile verarbeiten
    for line in response.text.splitlines():
        station_id = line[:11].strip()  # Station ID
        element = line[31:35].strip()   # Wettervariable (z.B. TMAX, TMIN)
        start_year = int(line[36:40])   # Erstes Jahr mit Daten
        end_year = int(line[41:45])     # Letztes Jahr mit Daten

        # Nur TMAX oder TMIN relevant
        if element in ["TMAX", "TMIN"]:
            if station_id not in inventory:
                inventory[station_id] = {}

            # Speichere Start- und Endjahr für TMAX und TMIN getrennt
            if element in inventory[station_id]:
                # Aktualisiere den frühesten Start und spätesten Endzeitpunkt
                inventory[station_id][element] = (
                    min(inventory[station_id][element][0], start_year),
                    max(inventory[station_id][element][1], end_year)
                )
            else:
                inventory[station_id][element] = (start_year, end_year)

    # Verzeichnis prüfen und erstellen, falls nicht vorhanden
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Speichern als JSON-Datei
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(inventory, json_file, indent=4)

    return True # True gibt an dass die Daten erfolgreich gespeichert wurden

def load_inventory_from_file():
    """
    Diese Funktion öffnet die JSON Datei inventory.json und gibt diese als Dictionary zurück.

    Rückgabe: Dictionary mit Inventardaten der Stationen
    """
    file_path = "data/inventory.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)  # JSON in ein Dictionary umwandeln
    except FileNotFoundError:
        print(f"Fehler: Datei {file_path} nicht gefunden.")
        return {}
    
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    lat1: Breitengrad Punkt 1
    lon1: Längengrad Punkt 1
    lat2: Breitengrad Punkt 2
    lon2: Längengrad Punkt 2

    Rückgabe: Entfernung der Koordinaten in km
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


def find_nearest_stations(user_lat, user_lon, radius, max_stations, start_year, end_year):
    """
    Sucht die nächsten Wetterstationen basierend auf Koordinaten und prüft,
    ob die Station Daten für das Start- und Endjahr enthält.

    user_lat: Breitengrad des Users
    user_lon: Längengrad des Users
    radius: Maximaler Suchradius in km
    max_stations: Maximale Anzahl zurückzugebender Stationen
    start_year: Startjahr der Wetterdaten
    end_year: Endjahr der Wetterdaten

    Rückgabe: Dictionary mit den X nächstgelegensten Stationen
    """
    stations = load_stations_from_file()
    inventory = load_inventory_from_file()
    nearby_stations = [] # Liste für die n nächsten Stationen

    # Iteration über alle Stationen in der Liste stations um den Abstand zu berechnen. Dies geschieht über die haversine_distance Funktion
    for station in stations:
        station_lat = station["Latitude"]
        station_lon = station["Longitude"]
        station_id = station["ID"]
        
        
        # Prüfen ob die Station in der Inventardatei enthalten ist
        if station_id in inventory:
            station_data = inventory[station_id]

            # Prüfen ob die Station TMIN und TMAX für den Zeitraum hat
            if "TMAX" in station_data and "TMIN" in station_data:
                tmax_start, tmax_end = station_data["TMAX"]
                tmin_start, tmin_end = station_data["TMIN"]
                # Prüfen, ob beide Variablen den Zeitraum abdecken
                if tmax_start <= start_year and tmax_end >= end_year and tmin_start <= start_year and tmin_end >= end_year:
                    distance = haversine_distance(user_lat, user_lon, station_lat, station_lon)

                    if distance <= radius:
                        station_copy = station.copy()
                        station_copy["Distance"] = distance
                        nearby_stations.append(station_copy)

    nearby_stations.sort(key=lambda x: x["Distance"])# Das lambda gibt an, dass die Liste nach dem Wert des Schlüssels "Distance" in jedem Dictionary sortiert wird.
    result = nearby_stations[:max_stations]
    return result

def download_weather_data(station_id, start_year, end_year):
    """"
    station_id: ID der Wetterstation. Beispiel Villingen-Schwenningen = "GME00129634"})
    start_year: Startjahr im Format "YYYY"
    end_year: Endjahr im Format "YYYY"

    Rückgabe: Wetterdaten einer einzelnen Station
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
                        date = f"{year}-{month}-{day:02d}" #02d stellt sicher dass der Tag immer zweistellig ist 1 -> 01
                        
                        if date not in weather_data["data"]:
                            weather_data["data"][date] = {"TMAX": None, "TMIN": None} 
                        
                        weather_data["data"][date][element] = value
    return weather_data

def calculate_means(station_weather_data, first_year, last_year, latitude):
    """
    Berechnet die durchschnittlichen Maximal- und Minimaltemperaturen
    für das gesamte Jahr sowie für jede Jahreszeit basierend auf den übergebenen Wetterdaten.
    Berücksichtigt dabei, dass der Dezember eines Jahres zur Winterperiode
    des folgenden Jahres gezählt wird. Ignoriert die ersten 11 Monate des ersten Jahres.
    Berücksichtigt außerdem die Jahreszeiten nach Erdhälften
    
    station_weather_data: Dictionary mit Temperaturwerten einer Wetterstation aus der Funktion download_weather_data()
    first_year: Erstes Jahr, dessen Januar bis November ignoriert wird
    last_year: Letztes Jahr, wichtig um sicherzustellen dass der Dezember des letzten Jahres keinen neuen Winter-Eintrag erstellt
    latitude: Breitengrad um die Wetterstationen den Erdhälften zuzuordnen
    
    Rückgabe: JSON mit Durchschnittswerten für das Jahr und die Jahreszeiten
    """
    if latitude >= 0: # Nordhalbkugel (Jaherszeiten wie gewohnt)
        # Monate werden den Jahreszeiten zugewiesen:
        season_months = {
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11]
        }

        # Datenstruktur wird bereitgestellt / initiiert:
        seasonal_data = {
            "spring": {}, 
            "summer": {},
            "autumn": {},
            "winter": {},
            "entire_year": {}
        }

        # Es wird über jeden Eintrag in station_weather_data iteriert
        for date, values in sorted(station_weather_data["data"].items()):
            try:
                # Datum wird aufgeteilt in Jahr und Monat
                date_parts = date.split("-")
                year = int(date_parts[0])
                month = int(date_parts[1])
                if year == first_year and month < 12:
                    continue # Das erste Jahr wird bis auf den Dezember übersprungen

                tmax = values.get("TMAX")
                tmin = values.get("TMIN")
                # Jährliche Daten kumulieren
                if tmax is None:
                    tmax = np.nan
                if tmin is None:
                    tmin = np.nan
                    
                if year not in seasonal_data["entire_year"]:
                    seasonal_data["entire_year"][year] = {"TMAX": [], "TMIN": []}
                seasonal_data["entire_year"][year]["TMAX"].append(tmax)
                seasonal_data["entire_year"][year]["TMIN"].append(tmin)

                for season, months in season_months.items():
                    if month in months:
                        if year not in seasonal_data[season]:
                            seasonal_data[season][year] = {"TMAX": [], "TMIN": []}
                        seasonal_data[season][year]["TMAX"].append(tmax)
                        seasonal_data[season][year]["TMIN"].append(tmin)

                if month in [12, 1, 2]:
                    if year == last_year and month == 12:  
                        continue  # Der Dezember des letzten Jahres wird ignoriert
                    if month in [1, 2]:
                        winter_year = year
                    else:
                        winter_year = year + 1
                                
                    if winter_year not in seasonal_data["winter"]:
                        seasonal_data["winter"][winter_year] = {"TMAX": [], "TMIN": []}
                    seasonal_data["winter"][winter_year]["TMAX"].append(tmax)
                    seasonal_data["winter"][winter_year]["TMIN"].append(tmin)
            
            except Exception as e:
                print(f"Fehler beim Verarbeiten des Datums {date}: {e}")


        # Jetzt werden die Mittelwerte berechnet. Zuerst für das gesamte Jahr und dann für die Jahreszeiten
        # np.nanmean() berechnet den Mittelwert und ignoriert NaN-Werte -> keine Verfälschung durch fehlerhafte Werte.
        result = {"entire_year": {}}
        for year, values in seasonal_data["entire_year"].items():
            if year == first_year:
                continue
            result["entire_year"][year] = {
                "TMAX": np.nanmean(values["TMAX"]) if values["TMAX"] else None,
                "TMIN": np.nanmean(values["TMIN"]) if values["TMIN"] else None
            }

        # Jetzt werden die Mittelwerte für die Jahreszeiten basierend auf unserer Datenstruktur "seasonal_data" berechnet
        for season, data in seasonal_data.items():
            if season == "entire_year":
                continue
            result[season] = {}
            for year, values in data.items():
                result[season][year] = {
                    "TMAX": np.nanmean(values["TMAX"]) if values["TMAX"] else None,
                    "TMIN": np.nanmean(values["TMIN"]) if values["TMIN"] else None
                    }
                # Das dictionary wird sortiert, um einheitliche Darstellung nach Erdhälften zu versichern
        ordered_result = OrderedDict([
            ("entire_year", result.get("entire_year", {})),
            ("winter", result.get("winter", {})),
            ("spring", result.get("spring", {})),
            ("summer", result.get("summer", {})),
            ("autumn", result.get("autumn", {}))
        ]) 
        return json.dumps(ordered_result, indent=4)

    else: #Südhalbkugel
        # Monate werden den Jahreszeiten zugewiesen:
        season_months = {
            "spring": [9, 10, 11],
            "winter": [6, 7, 8],
            "autumn": [3, 4, 5]
        }

        # Datenstruktur wird bereitgestellt / initiiert:
        seasonal_data = {
            "spring": {}, 
            "summer": {},
            "autumn": {},
            "winter": {},
            "entire_year": {}
        }

        # Es wird über jeden Eintrag in station_weather_data iteriert
        for date, values in station_weather_data["data"].items():
            try:
                # Datum wird aufgeteilt in Jahr und Monat
                date_parts = date.split("-")
                year = int(date_parts[0])
                month = int(date_parts[1])
                if year == first_year and month < 12:
                    continue # Das erste Jahr wird bis auf den Dezember übersprungen

                tmax = values.get("TMAX")
                tmin = values.get("TMIN")
                # Jährliche Daten kumulieren
                if tmax is None:
                    tmax = np.nan
                if tmin is None:
                    tmin = np.nan
                    
                if year not in seasonal_data["entire_year"]:
                    seasonal_data["entire_year"][year] = {"TMAX": [], "TMIN": []}
                seasonal_data["entire_year"][year]["TMAX"].append(tmax)
                seasonal_data["entire_year"][year]["TMIN"].append(tmin)

                for season, months in season_months.items():
                    if month in months:
                        if year not in seasonal_data[season]:
                            seasonal_data[season][year] = {"TMAX": [], "TMIN": []}
                        seasonal_data[season][year]["TMAX"].append(tmax)
                        seasonal_data[season][year]["TMIN"].append(tmin)
                if month in [12, 1, 2]:
                    if year == last_year and month == 12:  
                        continue  # Der Dezember des letzten Jahres wird ignoriert
                    if month in [1, 2]:
                        summer_year = year
                    else:
                        summer_year = year + 1
                                
                    if summer_year not in seasonal_data["summer"]:
                        seasonal_data["summer"][summer_year] = {"TMAX": [], "TMIN": []}
                    seasonal_data["summer"][summer_year]["TMAX"].append(tmax)
                    seasonal_data["summer"][summer_year]["TMIN"].append(tmin)
            
            except Exception as e:
                print(f"Fehler beim Verarbeiten des Datums {date}: {e}")


        # Jetzt werden die Mittelwerte berechnet. Zuerst für das gesamte Jahr und dann für die Jahreszeiten
        # np.nanmean() berechnet den Mittelwert und ignoriert NaN-Werte -> keine Verfälschung durch fehlerhafte Werte.
        result = {"entire_year": {}}
        for year, values in seasonal_data["entire_year"].items():
            if year == first_year:
                continue
            result["entire_year"][year] = {
                "TMAX": np.nanmean(values["TMAX"]) if values["TMAX"] else None,
                "TMIN": np.nanmean(values["TMIN"]) if values["TMIN"] else None
            }

        # Jetzt werden die Mittelwerte für die Jahreszeiten basierend auf unserer Datenstruktur "seasonal_data" berechnet
        for season, data in seasonal_data.items():
            if season == "entire_year":
                continue
            result[season] = {}
            for year, values in data.items():
                result[season][year] = {
                    "TMAX": np.nanmean(values["TMAX"]) if values["TMAX"] else None,
                    "TMIN": np.nanmean(values["TMIN"]) if values["TMIN"] else None
                    }
        # Das dictionary wird sortiert, um einheitliche Darstellung nach Erdhälften zu versichern
        ordered_result = OrderedDict([
            ("entire_year", result.get("entire_year", {})),
            ("winter", result.get("winter", {})),
            ("spring", result.get("spring", {})),
            ("summer", result.get("summer", {})),
            ("autumn", result.get("autumn", {}))
        ])
        return json.dumps(ordered_result, indent=4)




if __name__ == "__main__":

    """
    print(load_stations_from_file())
    print(load_inventory_from_file())
    print(find_nearest_stations(48.0594, 8.4641, 100, 3, 2015, 2018))
    """

    """
    stations = load_stations_from_file()
    inv = load_inventory_from_file()
    print(f"Anzahl der Stationen mit TMAX und TMIN: {len(inv)}")
    print(list(inv.items())[:10])  # Zeigt die ersten 10 Einträge an
    print(find_nearest_stations(48.0594, 8.4641, 100, 3, 2016, 2017))
    """

    """
    try:
        stations = load_stations_data()
        if stations is not None:
            station_id = "GME00129634"
            test_latitude = -1
            weather_data = download_weather_data(station_id, 2015, 2016)
            if weather_data:
                result = calculate_means(weather_data, 2015, 2016, test_latitude)
                print("Ergebnisse der Mittelwerte pro Saison:")
                print(result)
    except Exception as e:
        print(f"Fehler: {e}")
        """
