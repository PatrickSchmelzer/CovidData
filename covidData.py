import requests

def getInhabitants():
    inhabitants = {}
    inhabitants["Italy"] = 60260229
    inhabitants["Switzerland"] = 8603900
    inhabitants["Germany"] = 83166711
    inhabitants["Spain"] = 47100396
    inhabitants["France"] = 66993000
    inhabitants["UK"] = 66435550
    inhabitants["USA"] = 328000000

    return inhabitants

def getCovidData():
    summaryUrl = 'https://api.covid19api.com/summary'
    entries = requests.get(summaryUrl).json()
    data = {}
    dataWorld = entries["Global"]
    data["World"] = {"NewConfirmed": dataWorld["NewConfirmed"], "NewDeaths": dataWorld["NewDeaths"], "NewRecovered": dataWorld["NewRecovered"], 
                  "TotalConfirmed": dataWorld["TotalConfirmed"], "TotalDeaths": dataWorld["TotalDeaths"], "TotalRecovered": dataWorld["TotalRecovered"]}
    
    entryCountries = entries["Countries"]
    for entry in entryCountries:
        if entry['Country'] == "United Kingdom":
            data["UK"] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
        elif entry['Country'] == "United States of America":
            data["USA"] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
        else:
            data[entry["Country"]] = {"NewConfirmed": entry["NewConfirmed"], "NewDeaths": entry["NewDeaths"], "NewRecovered": entry["NewRecovered"], 
                  "TotalConfirmed": entry["TotalConfirmed"], "TotalDeaths": entry["TotalDeaths"], "TotalRecovered": entry["TotalRecovered"]}
    
    return data

def getDataPerCountry(country):
    country.replace(" ", "%20")
    url= f"https://api.covid19api.com/country/{country}/status/confirmed"
    days = requests.get(url).json()
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