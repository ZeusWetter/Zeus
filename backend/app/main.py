from fastapi import FastAPI, HTTPException
from typing import List
from utility_scripts import load_stations_from_file, load_inventory_from_file, find_nearest_stations, download_weather_data, calculate_means
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Erlaubt Anfragen vom Frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/nearest-stations", response_model=List[dict]) # API wurde in einem Beispiel getestet
async def get_nearest_stations(latitude: float,
                               longitude: float,
                               radius: int,
                               max_stations: int,
                               start_year: int,
                               end_year: int
                               ):
    # Stationsliste und Inventarsliste der Stationen werden aufgerufen und zugewiesen
    try:
        stations = load_stations_from_file()
        inventory = load_inventory_from_file()

        if not stations or not inventory:
            raise HTTPException(status_code=500, detail="Fehler beim Laden der Stations- oder Inventardaten")

        # Die nächsten Stationen werden basierend auf den Daten von stations und inventory, sowie der User-Eingabe berechnet.
        result = find_nearest_stations(latitude, longitude, radius, max_stations, start_year, end_year)

        # Die nächsten Stationen werden nun zurückgegeben
        if not result:
            raise HTTPException(status_code=404, detail="Keine passenden Stationen gefunden")
        return result
    except HTTPException as http_err:
        raise http_err  # Weiterreichen spezifischer HTTP-Fehler
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interner Serverfehler: {str(e)}")


@app.get("/weather-data/{station_id}", response_model=dict)
async def get_weather_data(station_id: str,
                           start_year: int,
                           end_year: int,
                           latitude: float):
    try:
        start_year -= 1
        # download_weather_data(station_id, start_year, end_year) wird ausgeführt um die Wetterdaten der Station zu speichern
        station_data = download_weather_data(station_id, start_year, end_year)
        # calculate_means(station_weather_data, first_year, last_year, latitude) wird ausgeführt
        processed_data = calculate_means(station_data, start_year, end_year, latitude)
        # die berechneten Mittelwerte werden zurückgegeben
        return processed_data
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interner Serverfehler: {str(e)}")
