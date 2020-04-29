import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
from newsapi.newsapi_client import NewsApiClient
from flask import Flask, render_template, send_from_directory
import json


def plot_data ():
  url = "https://api.covid19api.com/total/country/singapore"
  response = requests.get(url)
  data_ = response.json()
  # Country, CountryCode, Province, City, CityCode, Lat, Lon, Confirmed, Deaths, Recovered, Date
  dates = np.array([])
  confirmed_cases = np.array([])
  death_cases = np.array([])
  recovered_cases = np.array([])

  for data in data_:
    # print(data["Confirmed"], data["Deaths"], data["Recovered"], data["Date"])
    date_ = data["Date"].split("T")[0].split("-")
    date = datetime.datetime(int(date_[0]), int(date_[1]), int(date_[2]))
    dates = np.append(dates, date)
    confirmed_cases = np.append(confirmed_cases, int(data["Confirmed"]))
    death_cases = np.append(death_cases, int(data["Deaths"]))
    recovered_cases = np.append(recovered_cases, int(data["Recovered"]))

  fig, ax = plt.subplots()
  # print(dates)
  ax.plot(dates, confirmed_cases, label="Confirmed Cases")
  ax.plot(dates, death_cases, label="Death Cases")
  ax.plot(dates, recovered_cases, label="Recovered Cases")
  ax.set_xlabel("Date")
  ax.set_ylabel("Number of Cases")
  ax.set_title("Covid-19 in Singapore")
  ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
  ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
  ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
  ax.legend()
  fig.savefig("uploads/img/data.png")
  return "img/data.png"


def get_news ():
  API_KEY = "a621f645307c47129920cf7858d1dffe"
  newsapi = NewsApiClient(api_key=API_KEY)
  keywords = "covid19"
  all_articles = newsapi.get_everything(q=keywords, language="en")
  return all_articles["articles"]


app = Flask(__name__)

@app.route("/")
def index ():
  all_articles = get_news()
  with open ("static/text/news.json", "w") as news_file:
    news_file.write(json.dumps(all_articles))
  return render_template("index.html", all_articles=all_articles)

@app.route('/uploads')
def send_file():
  filename = plot_data()
  return send_from_directory("uploads", filename)

# main
if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")
  
# plot_data()
# get_news()

