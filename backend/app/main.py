from fastapi import FastAPI, File, Body
import requests
import json
from utility_scripts import find_nearest_stations
import logging

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/stations-in-range")
async def get_stations_in_range(latitude: float, longitude: float, range_km: int, max_stations: int):
    try:
        with open("data/stations.json", "r") as f:
            data = json.loads(f.read())
            nearest_stations = []
            nearest_stations = find_nearest_stations(user_lat=latitude,user_lon=longitude,radius=range_km,max_stations=max_stations,json_data=data)

    except FileNotFoundError as e:
        logging.error("Error: " + str(e))
        return {"error": "File not found."}, 404

    return {"data": nearest_stations}
