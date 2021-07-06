
import requests
import sys
import json
import datetime
from os.path import getmtime


class Weather:
    def __init__(self):
        self.response = []
        self.forecast_data = {}

    def get_response(self, key):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

        querystring = {"location":"Krakow,Poland","aggregateHours":"24","shortColumnNames":"0","unitGroup":"metric","contentType":"json"}

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }

        self.response = requests.request("GET", url, headers=headers, params=querystring).json()

    def load_response(self, key, file):
        sec = getmtime(file)
        current = datetime.datetime.now().timestamp()
        if current - sec < 60 * 60 * 24:
            with open(file, "r") as f:
                self.response = json.load(f)
        else:
            self.get_response(key)
            self.save_response(file)

    def save_response(self, file):
        with open(file, "w") as fp:
            file_content = json.dumps(self.response)
            fp.write(file_content)
        return True

    def forecast(self):
        for curr_val in self.response["locations"]["Krakow,Poland"]["values"]:
            date = datetime.datetime.utcfromtimestamp(curr_val["datetime"] / 1000).strftime("%Y-%m-%d")
            daily_forecast = curr_val["conditions"]
            self.forecast_data[date] = daily_forecast

    def __getitem__(self, item):
        if item not in self.forecast_data:
            return "NIE WIEM."
        if "Rain" in self.forecast_data[item]:
            return "BĘDZIE PADAC."
        else:
            return "NIE BEDZIE PADAC."


weather = Weather()
key = input()
outfile = sys.argv[1]
weather.get_response(key)
weather.load_response(key, outfile)
weather.forecast()

if sys.argv[2]:
    print(weather[sys.argv[2]])
if not sys.argv[2]:
    x = datetime.date.today() + datetime.timedelta(days=1)
    y = str(x)
    print(weather[y])
