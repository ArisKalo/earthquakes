import datetime as dt
import usgs_fetch
from prepare import transform_earthquakes
from db import init_db, insert_earthquakes, insert_daily_earthquakes, updated_earthquakes, new_earthquakes
import csv
import logging
from db import curr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),          # logs to terminal
        logging.FileHandler("app.log")    # logs to file
    ]
)

def write_to_csv(cursor, table_name, filename, limit):
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    logging.info(f"Wrote {len(rows)} rows to {filename}")
    

if __name__ == "__main__":
    init_db()
    start_date = dt.date.today() - dt.timedelta(days=30)
    end_date = dt.date.today()

    logging.info(f"Fetching earthquakes between {start_date} and {end_date}.")
    earthquakes = usgs_fetch.fetch_all_earthquakes(start_date, end_date)
    logging.info(f"Fetched {len(earthquakes)} earthquakes.")

    logging.info("Transforming earthquakes.")
    transformed_earthquakes, aggregation = transform_earthquakes(earthquakes)
    
    logging.info("Inserting new earthquakes.")
    new_earthquakes = new_earthquakes(transformed_earthquakes)
    insert_earthquakes(new_earthquakes)
    
    logging.info("Inserting updated earthquakes.")
    updated_earthquakes = updated_earthquakes(transformed_earthquakes)
    insert_earthquakes(updated_earthquakes)
        
    logging.info("Inserting daily earthquakes.")
    insert_daily_earthquakes(aggregation)
    
    write_to_csv(curr, "daily_earthquakes", "tables/daily_earthquakes.csv", 150)
    write_to_csv(curr, "earthquakes", "tables/earthquakes.csv", 100)

    logging.info("Done.")
