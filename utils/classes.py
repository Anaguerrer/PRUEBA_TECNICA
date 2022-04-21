import json
import statistics
import requests


class city:
    def __init__(self,name, lon, lat):
        self.lon = lon
        self.lat = lat
        self.name = name

    def weather_day(self, date, key):
        try:
            headers = {
                "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
                "X-RapidAPI-Key": key
                }
            queryparams = {"lat":self.lat,"lon":self.lon,"dt":date}
            response = requests.request("GET", "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine", headers=headers, params=queryparams)
            response_dict = json.loads(response.text)
            return response_dict
        except:
            print('Error at API request:', response)


class data_to_insert:
    def __init__(self, name, temps, humidity, windSpeed):
        self.name = name
        self.temp_Max = max(temps)
        self.temp_Min = min(temps)
        self.temp_Main = round(statistics.mean(temps), 2)
        self.hum_Main = round(statistics.mean(humidity), 2)
        self.wind_speed = windSpeed