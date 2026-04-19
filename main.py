import datetime as dt
import usgs_fetch
from prepare import transform_earthquakes
from db import init_db, insert_earthquakes, insert_daily_earthquakes, updated_earthquakes, new_earthquakes
import csv


if __name__ == "__main__":
    init_db()
    start_date = dt.date.today() - dt.timedelta(days=30)
    end_date = dt.date.today()

    print(f"Fetching earthquakes between {start_date} and {end_date}.")
    earthquakes = usgs_fetch.fetch_all_earthquakes(start_date, end_date)
    print(f"Fetched {len(earthquakes)} earthquakes.")

    print("Transforming earthquakes.")
    transformed_earthquakes, aggregation = transform_earthquakes(earthquakes)
    
    print("Inserting new earthquakes.")
    new_earthquakes = new_earthquakes(transformed_earthquakes)
    insert_earthquakes(new_earthquakes)
    print(f"Inserted {len(new_earthquakes)} new earthquakes.")
    
    print("Inserting updated earthquakes.")
    updated_earthquakes = updated_earthquakes(transformed_earthquakes)
    insert_earthquakes(updated_earthquakes)
    print(f"Inserted {len(updated_earthquakes)} updated earthquakes.")
    
    print("Inserting daily earthquakes.")
    insert_daily_earthquakes(aggregation)
    
