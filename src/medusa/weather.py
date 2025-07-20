import requests, requests_cache
from datetime import datetime, timedelta
import logging
# Coordinates for Aachen, Germany

session = requests_cache.CachedSession('demo_cache', expire_after=3600)  # Cache for 1 hour
def get_Weather(session):
    latitude = 50.7753
    longitude = 6.0839


    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)  # Use Berlin time for better accuracy
    end_time = start_time + timedelta(hours=8)  # Current hour + next 8 hours = 9 hours total
    current_hour = start_time.hour
    
    # Format as ISO 8601
    start_str = start_time.isoformat() 
    end_str = end_time.isoformat() 

    # API Endpoint
    url = "https://api.open-meteo.com/v1/forecast"

    # Parameters
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,cloudcover",
        "start": start_str,
        "end": end_str,
        "timezone": "auto",
        "forecast_days"  : 2
    }

    response = session.get(url, params=params)  # Use session instead of requests

    new_data = {}

    if response.status_code == 200:
        data = response.json()
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])[current_hour:current_hour + 9]  # Get next 9 hours
        temperatures = hourly.get("temperature_2m", [])[current_hour:current_hour + 9]
        precipitation = hourly.get("precipitation", [])[current_hour:current_hour + 9]
        cloudcover = hourly.get("cloudcover", [])[current_hour:current_hour + 9]
        
        new_hourly = {
            "time": times,
            "temperature_2m": temperatures,
            "precipitation": precipitation,
            "cloudcover": cloudcover
        }
        new_data = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": new_hourly
        }

        # print(new_data)
        data = new_data  # Use the new data structure
        for i in range(len(times)):
            logging.info(f"{times[i]} | Temp: {temperatures[i]}°C | Precip: {precipitation[i]}mm | Cloud: {cloudcover[i]}%")
    else:
        logging.error(f"Error: {response.status_code} - {response.text}")
    return data

if __name__ == "__main__":
    get_Weather(session)