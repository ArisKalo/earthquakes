from prepare import transform_earthquakes

raw_earthquakes = [
    {
        "id": "us6000o76c",
        "type": "Feature",
        "properties": {
            "mag": 4.4,
            "place": "10 km E of Ojai, California",
            "time": 1744987260000,
            "updated": 1744987360000,
            "tz": None,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000o76c",
            "status": "reviewed",
            "type": "earthquake"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-118.123456, 34.567890, 10.0]
        }
    },
    {
        "id": "us6000o76d",
        "type": "Feature",
        "properties": {
            "mag": 5.4,
            "place": "10 km E of Ojai, California",
            "time": 1744900860000,
            "updated": 1744987360000,
            "tz": None,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000o76c",
            "status": "reviewed",
            "type": "earthquake"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-118.123456, 34.567890, 10.0]
        }
    },
    {
        "id": "us6000o76d",
        "type": "Feature",
        "properties": {
            "mag": 2.4,
            "place": "10 km E of Ojai, California",
            "time": 1744900860000,
            "updated": 1744987360000,
            "tz": None,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000o76c",
            "status": "reviewed",
            "type": "earthquake"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-118.123456, 34.567890, 10.0]
        }
    },
    {
        "id": "us6000o76d",
        "type": "Feature",
        "properties": {
            "mag": 3.4,
            "place": "10 km E of Ojai, California",
            "time": 1744900860000,
            "updated": 1744987360000,
            "tz": None,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us6000o76c",
            "status": "reviewed",
            "type": "earthquake"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-118.123456, 34.567890, 10.0]
        }
    }
]

transformed_earthquakes, aggregation = transform_earthquakes(raw_earthquakes)

print(transformed_earthquakes)
print(aggregation)

