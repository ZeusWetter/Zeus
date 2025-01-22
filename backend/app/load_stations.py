#Libraries importieren:
import requests
import pandas as pd
from io import StringIO

#in folgender Funktion werden die Daten der 
#Wetterstationen in eine JSON Datei eingelesen
def load_stations_data():
    url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt"
    file_path = "backend/app/data/stations.json"
    response = requests.get(url)
    if response.status_code == 200:
        print("Datenzugriff war erfolgreich")
        #Die einzelnen Spalten benennen
        columns = ["ID", "Latitude", "Longitude", "Elevation", "State", "Name"]
        #Start- und Endpositionen der Spalten im Fixed-Width Format angeben
        colspecs = [(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71)]
        #Daten in einem Data Frame speichern
        stations = pd.read_fwf(StringIO(response.text), colspecs=colspecs, header=None, names=columns)
        # Die Daten in eine JSON-Datei speichern
        stations.to_json(file_path, orient="records", indent=4)
        print(f"Daten erfolgreich in {file_path} gespeichert")

        return stations
    else:
        print(f"Fehler beim Herunterladen der Datei: {response.status_code}")
        return None
    

if __name__ == "__main__":
    stations = load_stations_data()
    if stations is not None:
        print(stations.head())
    else:
        print("Keine Daten verfügbar.")
