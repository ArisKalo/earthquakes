import requests

USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
PAGE_LIMIT = 20000 # The USGS API returns a maximum of 20000 features per request.

def fetch_all_earthquakes(start_date, end_date):
    """
    Fetches all earthquakes within a given date range from the USGS API.
    """
    
    all_earthquakes = []
    offset = 1
    
    # Specify eventtype as "earthquake" to exclude other types of events.
    # Offset is used to get the next page of results.
    # Limit is used to get the maximum number of features per request.
    # Starttime and endtime are used to get the earthquakes within the given date range.
    # Format is used to get the earthquakes in geojson format.
    
    while True:
        params = {
            "format": "geojson",
            "eventtype": "earthquake",
            "starttime": start_date,
            "endtime": end_date,
            "limit": PAGE_LIMIT,
            "offset": offset
        }
        
        response = requests.get(USGS_BASE_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"Error fetching earthquakes: {response.status_code}")
        
        data = response.json()
        earthquakes = data.get("features", [])
        if not earthquakes:
            break
        
        all_earthquakes.extend(earthquakes)
        offset += PAGE_LIMIT
   
    return all_earthquakes
