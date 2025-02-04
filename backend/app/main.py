from fastapi import FastAPI, File, Body, Query, HTTPException
from utility_scripts import find_nearest_stations, download_weather_data, load_stations_data
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stations-in-range")
async def get_stations_in_range(
    latitude: float = Query(..., description="Breitengrad des Standorts"), 
    longitude: float = Query(..., description="Längengrad des Standorts"), 
    range_km: int = Query(..., description="Suchradius in Kilometern"), 
    max_stations: int = Query(..., description="Maximale Anzahl an Stationen die zurückgegeben werden")
):
    try:
        # Lade aktuelle Stationsdaten
        stations_df = load_stations_data()
        if stations_df is None:
            logging.error("Fehler: `load_stations_data()` hat None zurückgegeben.")
            raise HTTPException(status_code=500, detail="Fehler beim Laden der Stationsdaten.")

        # NaN-Werte werden durch `None` ersetzt, damit JSON sie verarbeiten kann
        stations_df = stations_df.replace({np.nan: None})

        # Konvertiere in JSON-kompatibles Format (Liste von Dictionaries)
        stations_list = stations_df.to_dict(orient="records")

        logging.debug(f"Geladene Stationen (erste 3 Einträge): {stations_list[:3]}")

        # Berechne die nächsten Stationen
        nearest_stations = find_nearest_stations(
            user_lat=latitude,
            user_lon=longitude,
            radius=range_km,
            max_stations=max_stations,
            json_data=stations_list
        )

        return {"data": nearest_stations}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.exception("Unerwarteter Fehler in `/stations-in-range`:")
        raise HTTPException(status_code=500, detail=f"Interner Fehler: {str(e)}")

@app.get("/weather/{station_id}")
async def get_weather_data(
    station_id: str,
    start_year: int = Query(..., description="Startjahr im Format XXXX"),
    end_year: int = Query(..., description="Endjahr im Format XXXX")
):
    try:
        # Wetterdaten abrufen:
        weather_data = download_weather_data(station_id, start_year, end_year)
        return weather_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interner Fehler: {str(e)}")