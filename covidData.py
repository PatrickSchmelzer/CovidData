import requests
import datetime
import pandas as pd

class CovidData():
    def getInhabitants(self, country):
        inhabitants = {}
        inhabitants["Italy"] = 60260229
        inhabitants["Switzerland"] = 8603900
        inhabitants["Germany"] = 83166711
        inhabitants["Spain"] = 47100396
        inhabitants["France"] = 66993000
        inhabitants["United Kingdom"] = 66435550
        inhabitants["United States of America"] = 328000000
        return inhabitants[country]

    def getCovidDataWorldSummary(self):
        summaryUrl = 'https://api.covid19api.com/summary'
        try:
            entries = requests.get(summaryUrl).json()
        except Exception:
            #Exception getting the web content
            raise

        data = {}
        dataWorld = entries["Global"]
        data["World"] = {"NewConfirmed": dataWorld["NewConfirmed"], "NewDeaths": dataWorld["NewDeaths"], "NewRecovered": dataWorld["NewRecovered"], 
                      "TotalConfirmed": dataWorld["TotalConfirmed"], "TotalDeaths": dataWorld["TotalDeaths"], "TotalRecovered": dataWorld["TotalRecovered"]}
    
        entryCountries = entries["Countries"]
        for entry in entryCountries:
                data[entry["Country"]] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                      "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}  
        return data

    def getCountryHistory(self, country):
        country.replace(" ", "%20") # i.e "United Kingdom"
        url= f"https://api.covid19api.com/country/{country}/status/confirmed"
        try:
            days = requests.get(url).json()
        except Exception:
            #Exception getting the web content
            raise
        cases = []
        casesPerDay = []
        date = []
        for idx in range(0, len(days)):
            day = days[idx]
            cases.append(day['Cases'])
            date.append(day['Date'])
            if idx == 0:
                casesPerDay.append(day['Cases'])
            else:
                prevDay = days[idx-1]
                casesPerDay.append(day['Cases'] - prevDay['Cases'])
        return casesPerDay, date, url

    def getLastWeekSummary(self, country):
            today = datetime.datetime.now().date()
            week_ago = today - datetime.timedelta(days=7) # 8 days because we need to new cases of the last seven days (baseline)
            try:
                lastWeek = resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed", params={"from": week_ago, "to": today}).json()
                newCases = (lastWeek[-1]["Cases"] - lastWeek[-2]["Cases"])
                casesLastWeek = (lastWeek[-1]["Cases"] - lastWeek[0]["Cases"])
                inhabitants = self.getInhabitants(country)
                per100_000PerWeek = round((casesLastWeek / inhabitants) * 100000, 2)
                return newCases, casesLastWeek, per100_000PerWeek
            except Exception:
                raise

    def getZHRegionalData(self):
        url = "https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_bezirke/fallzahlen_kanton_ZH_bezirk.csv"
        csv = requests.get(url).content
        csv_file = open('downloaded.csv', 'wb')
        csv_file.write(csv)
        csv_file.close()

        data = {}
        with open ('downloaded.csv', 'r') as f:
            for line in f:
                districtId, district, population, week, year, newCases, newDeaths, totalCases, totalDeaths = line.split(",")

                if district not in data:
                    data[district] = []
                data[district].append({"Population": population, "Week": week, "Year": year, "NewCases": newCases, "NewDeaths": newDeaths, "TotalCases": totalCases, "TotalDeaths": totalDeaths})

        return data

    def getZHData(self):
        url = "https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_plz/fallzahlen_kanton_ZH_plz.csv"
        csv = requests.get(url).content
        csv_file = open('downloaded.csv', 'wb')
        csv_file.write(csv)
        csv_file.close()

        data = {}
        with open ('downloaded.csv', 'r') as f:
            for line in f:
                plz, date, population, newCases = line.split(",")

                if plz not in data:
                    data[plz] = []

                data.append({"Date": date, "Population": population, "NewCases": newCases})

        for entry in data["8802"]:
            print(entry)
        

if __name__ == '__main__':
    covid = CovidData()
    try:
        #newCases, casesPerWeek, stat = covid.getLastWeekSummary("Italy")
        #print(newCases, casesPerWeek, stat)
        data = covid.getZHRegionalData()
        for d in data["Bezirk Horgen"]:
            print(d)

    except Exception as e:
        print(e)
        print("Error retreiving data")
