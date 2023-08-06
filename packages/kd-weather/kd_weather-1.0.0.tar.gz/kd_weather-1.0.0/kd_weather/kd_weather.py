import requests
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as dplt


class Weather:
    """
    Creates a Weather object that needs an API Key, city name or lat, long coordinates as input.
    Get your own API key from https://openweathermap.org, key activation will need up to a couple of hours.

    Example usage:

        # >>> weather = Weather(api_key="12345678910abcdefg...")

        # plot weather forecast for the next 16 hours, in your local time
        # >>> weather.forecast("Vienna")

        # print weather forecast for the next 16 hours, in your local time
        #  >>> weather.forecast(lat=40.71, long=-74.0, plot=False)

    """
    def __init__(self, api_key=None, city=None, lat=None, long=None):
        self.api_key = api_key
        self.city = city
        self.lat = lat
        self.long = long
        self.data = None

    def get_data(self):
        """
        Requests openweathermap.org API to retrieve weather data.

        :return: List of tuples (datetime, temperature, perceived temperature)
        """
        url = f"http://api.openweathermap.org/data/2.5/forecast?"
        # use city or lat/long for location
        url += f"q={self.city},," if self.city else f"lat={self.lat}&lon={self.long}"
        url += f"&appid={self.api_key}"
        url += f"&units=metric"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise ValueError(resp.json().get('message'))
        data_dict = resp.json()
        self.city = data_dict["city"]["name"]
        return self.parse_data(data_dict)

    def parse_data(self, raw_data):
        """
        Helper function that parses a dictionary response from openweathermap.org and transforms it
        into a list of tuples.

        :param raw_data: Data in dict format from openweathermap.org API.
        :return: List of tuples (datetime, temperature, perceived temperature, clouds, weather).
        """
        parsed_data = []
        former_weather = ""

        for row in raw_data["list"][:6]:

            # easy parsing
            time = datetime.fromtimestamp(row["dt"])
            temp = row["main"]["temp"]
            feels = row["main"]["feels_like"]
            clouds = row["clouds"]["all"]

            # convert weather to symbols
            weather = self.weather_to_symbol(row["weather"][0]["description"], former_weather)
            former_weather = row["weather"][0]["description"]

            # append data as tuples
            parsed_data.append((time, temp, feels, clouds, weather))

        return parsed_data

    @staticmethod
    def weather_to_symbol(weather, former_weather):
        """
        Converts weather text into ASCII symbols.
        :param weather: Text description of weather.
        :param former_weather: Text description of previous weather.
        :return: ASCII Symbol.
        """
        symbol = ""
        if weather == former_weather:
            pass
        elif "clear" in weather:
            symbol = "\u2600"
        elif "scattered clouds" in weather:
            symbol = "\u2601"
        elif "broken clouds" in weather or "overcast clouds" in weather:
            symbol = "\u2601\u2601"
        elif "light snow" in weather:
            symbol = "\u2744"
        elif "snow" in weather:
            symbol = "\u2042"
        elif "rain" in weather:
            symbol = "\u2614"
        elif "thunder" in weather:
            symbol = "\u2607\u2614"
        return symbol

    def plot(self):
        """
        Plot datetime, temperature, perceived temperature, clouds and additional weather conditions
        for the next 16 hours.
        """
        if not self.data:
            raise TypeError("No data to plot, call forecast() method.")

        clock, temp, feels, clouds, weather  = zip(*self.data)
        fig, host = plt.subplots(figsize=(8, 5))
        fig.suptitle(f"Weather temperature in {self.city}")

        # parallel plot
        par1 = host.twinx()

        host.set_ylim(-10, 45)
        par1.set_ylim(-5, 105)

        host.set_xlabel("local TIME")
        host.set_ylabel("TEMPERATURE in °C")
        par1.set_ylabel("CLOUDS %")

        # draw curves
        curve1, = host.plot(clock, temp, label="°C")
        curve2, = host.plot(clock, feels, label="°C perceived")
        curve3, = par1.plot(clock, clouds, color="gray", label="cloudiness %")

        # format appearance
        host.legend(handles=[curve1, curve2, curve3], loc='best')
        host.yaxis.label.set_color(curve1.get_color())
        par1.yaxis.label.set_color(curve3.get_color())

        # convert date
        plt.gcf().autofmt_xdate()
        myFmt = dplt.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)

        # annotate cloud curve with weather symbols
        ticks = len(weather)
        for i in range(ticks):
            annotation = weather[i] if i < ticks-1 else ""
            plt.annotate(annotation, (clock[i], clouds[i]-5))

        # plt.savefig("pyplot_multiple_y-axis.pdf")
        plt.show()

    def forecast(self, city=None, lat=None, long=None):
        """
        Make API calls and visualize temperature data for a given city or location.

        :param city: City name as string.
        :param lat: Latitude as float.
        :param long: Longtitude as float.
        :param plot: Boolean value. If True, plot, else print temperature data.
        """
        # see if user sets city / lat / long
        self.city = city or self.city
        self.lat = lat or self.lat
        self.long = long or self.long

        # get weather data
        self.data = self.get_data()

        # visualize data
        self.plot()
