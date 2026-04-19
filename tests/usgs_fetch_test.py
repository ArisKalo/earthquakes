import usgs_fetch
import datetime as dt

start_date = dt.date.today() - dt.timedelta(days=30)
end_date = dt.date.today()

earthquakes = usgs_fetch.fetch_all_earthquakes(start_date, end_date)

print(f"Fetched {len(earthquakes)} earthquakes between {start_date} and {end_date}.")
for i in range(10):
    if earthquakes[i]['properties']['type'] != "earthquake":
        print(earthquakes[i]['properties']['type'])
    
