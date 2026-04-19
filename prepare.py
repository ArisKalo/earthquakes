import datetime as dt
from collections import defaultdict

MAG_BUCKETS = [(0,2), (2,4), (4,6), (6,10.1)]

def get_mag_bucket(mag):
    map_buckets = {0: '0-2', 1: '2-4', 2: '4-6', 3: '6-10'}
    if mag is None:
        return "None"
    for i, bucket in enumerate(MAG_BUCKETS):
        if mag >= bucket[0] and mag < bucket[1]:
            return map_buckets[i]
    return "None"

def transform_earthquakes(raw_earthquakes):
    transformed_earthquakes = []
    daily_earthquakes = defaultdict(lambda: defaultdict(int))
    for earthquake in raw_earthquakes:
        id, mag, place, longitude, latitude, depth, time, updated, tz, url, status = earthquake['id'], earthquake['properties']['mag'], earthquake['properties']['place'], earthquake['geometry']['coordinates'][0], earthquake['geometry']['coordinates'][1], earthquake['geometry']['coordinates'][2], earthquake['properties']['time'], earthquake['properties']['updated'], earthquake['properties']['tz'], earthquake['properties']['url'], earthquake['properties']['status']
        date = dt.datetime.fromtimestamp(time / 1000, tz=dt.timezone.utc).strftime("%Y-%m-%d")
        mag_bucket = get_mag_bucket(mag)
        
        daily_earthquakes[date][mag_bucket] += 1
        transformed_earthquakes.append({
            'id': id,
            'mag': mag,
            'mag_bucket': mag_bucket,
            'place': place,
            'longitude': longitude,
            'latitude': latitude,
            'depth': depth,
            'time': time,
            'date': date,
            'updated': updated,
            'tz': tz,
            'url': url,
            'status': status
        })

    aggregation = [
        {'date': date, 'mag_bucket': mag_bucket, 'num_earthquakes': count}
        for date, mag_bucket in daily_earthquakes.items() 
        for mag_bucket, count in mag_bucket.items()
    ]
    return transformed_earthquakes, aggregation

    

        

    