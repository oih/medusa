import requests_cache
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

session = requests_cache.CachedSession('demo_cache', expire_after=1800)  # Cache
def get_Weather(session):
    latitude = 50.7753
    longitude = 6.0839


    start_time = datetime.now(ZoneInfo("Europe/Berlin")).replace(minute=0, second=0, microsecond=0)  
    end_time = start_time + timedelta(hours=8)  
    current_hour = start_time.hour
    
    # Format as ISO 8601
    start_str = start_time.isoformat() 
    end_str = end_time.isoformat() 

    # API Endpoint
    url = "https://api.brightsky.dev/weather"
    
    params = {
        "date":start_str,
        "last_date":end_str,
        "lat":str(latitude),
        "lon":str(longitude),
        }

    headers = {"Accept": "application/json"}


    response = session.get(url, params=params, headers=headers)  # Use session instead of requests

    if response.status_code == 200:
        data = response.json()
        new_data = dwd_to_webpage_format(data)
        if new_data:
            times = new_data["hourly"]["time"]
            temperatures = new_data["hourly"]["temperature_2m"]
            precipitation = new_data["hourly"]["precipitation"]
            cloudcover = new_data["hourly"]["cloudcover"]
            precipitation_probability = new_data["hourly"]["precipitation_probability"]

            for i in range(len(times)):
                print(f"{times[i]} | Temp: {temperatures[i]}°C | Precip: {precipitation[i]}mm | Cloud: {cloudcover[i]}% | Precip Prob: {precipitation_probability[i]}%")
            return new_data
        else:
            print("No data available or format is incorrect.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return None

# def dwd_to_webpage_format(weather_data):
    # new_hourly = {
    #         "time": times,
    #         "temperature_2m": temperatures,
    #         "precipitation": precipitation,
    #         "cloudcover": cloudcover
    #     }
    #     new_data = {
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "hourly": new_hourly
    #     }
#     weather_data = {
#   "weather": [
#     {
#       "timestamp": "2025-07-26T19:00:00+02:00",
#       "source_id": 3483,
#       "precipitation": 0,
#       "pressure_msl": 1014.6,
#       "sunshine": 22,
#       "temperature": 24.6,
#       "wind_direction": 293,
#       "wind_speed": 13,
#       "cloud_cover": 73,
#       "dew_point": 14.8,
#       "relative_humidity": null,
#       "visibility": 22100,
#       "wind_gust_direction": null,
#       "wind_gust_speed": 18.5,
#       "condition": "dry",
#       "precipitation_probability": 4,
#       "precipitation_probability_6h": null,
#       "solar": 0.272,
#       "icon": "partly-cloudy-day"
#     }],
# "sources": [
#     {
#       "id": 3483,
#       "dwd_station_id": "00003",
#       "observation_type": "forecast",
#       "lat": 50.78,
#       "lon": 6.1,
#       "height": 202,
#       "station_name": "AACHEN",
#       "wmo_station_id": "10501",
#       "first_record": "2025-07-26T16:00:00+02:00",
#       "last_record": "2025-08-06T00:00:00+02:00",
#       "distance": 513
#     }
#   ] 
# }
    # Convert the weather data to a format suitable for a webpage which is new_data

def dwd_to_webpage_format(weather_data):
    weather_entries = weather_data.get("weather", [])
    sources = weather_data.get("sources", [])

    if not weather_entries or not sources:
        return None  # or raise an exception, depending on use-case

    # Extract latitude and longitude from the first source
    latitude = sources[0].get("lat")
    longitude = sources[0].get("lon")

    # Initialize lists for each time series variable
    times = []
    temperatures = []
    precipitation = []
    cloudcover = []
    precipitation_probability = []

    # Populate the lists with relevant weather info
    for entry in weather_entries:
        times.append(entry.get("timestamp")[:-9])  # Remove timezone info and millisecs
        temperatures.append(entry.get("temperature"))
        precipitation.append(entry.get("precipitation"))
        cloudcover.append(entry.get("cloud_cover"))
        precipitation_probability.append(entry.get("precipitation_probability", 0) if entry.get("precipitation_probability") is not None else 0)

    # Build the format expected by the webpage
    hourly = {
        "time": times,
        "temperature_2m": temperatures,
        "precipitation": precipitation,
        "cloudcover": cloudcover,
        "precipitation_probability": precipitation_probability
    }

    data = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": hourly
    }

    return data


if __name__ == "__main__":
    get_Weather(session)