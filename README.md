# USGS Earthquake Data Pipeline

A Python pipeline that fetches earthquake data from the USGS API, transforms it into daily magnitude-bucketed aggregates, and stores both raw events and summaries in SQLite.

---

## Project Structure

```
earthquakes/
├── main.py          # Entry point — orchestrates fetch, transform, and store
├── usgs_fetch.py    # Fetches raw earthquake data from the USGS API with pagination
├── prepare.py       # Transforms raw GeoJSON features into structured records and daily aggregates
├── db.py            # SQLite schema, insert, and upsert logic
├── db_query.py      # Utility queries for inspecting the database
├── requirements.txt # Python dependencies
└── tests/
    ├── usgs_fetch_test.py            # Manual integration test for the fetcher
    ├── transform_earthquakes_test.py # Unit tests for the transformer using fixture data
    └── get_mag_bucket_test.py        # Unit tests for magnitude bucket assignment
```

---

## Setup

**Requirements:** Python 3.11+

1. Clone the repository and navigate into the project folder:
   ```bash
   git clone <your-repo-url>
   cd earthquakes
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Pipeline

```bash
python main.py
```

This will:
1. Fetch all earthquakes from the past 30 days via the USGS API
2. Transform them into structured records and daily magnitude-bucket aggregates
3. Insert new events and update changed events in `earthquakes.db`
4. Upsert the daily aggregate counts

The database file `earthquakes.db` will be created in the project root on first run.

---

## Running the Tests

The unit tests use hardcoded fixture data and do not require a live API connection.

**Run all tests from the project root:**
```bash
python -m pytest tests/
```

**Or run a specific test file:**
```bash
python -m pytest tests/transform_earthquakes_test.py
python -m pytest tests/get_mag_bucket_test.py
```

> Note: `tests/usgs_fetch_test.py` is a manual integration test that does hit the live API. Run it separately if you want to verify end-to-end connectivity:
> ```bash
> python -m tests.usgs_fetch_test
> ```

---

## Design Decisions

**Separation of concerns.** The pipeline is split into three distinct layers — fetching, transforming, and storing — so each can be tested and reasoned about independently. `usgs_fetch.py` is purely I/O; `prepare.py` is purely logic; `db.py` is purely persistence.

**API-level event type filtering.** The USGS API is queried with `eventtype=earthquake`, which filters out quarry blasts, explosions, and other non-earthquake seismic events at the source. This reduces data transfer and keeps the dataset focused.

**Offset-based pagination.** The USGS API does not use cursor tokens, so pagination is handled by incrementing an `offset` parameter. The loop exits when the API returns fewer results than the page limit, indicating the last page.

**Selective raw field storage.** Not every field from the raw GeoJSON response is stored. Fields retained are those useful for reprocessing or debugging — magnitude, location, timestamps, depth, and status. Fields that are mostly null (e.g. `felt`, `cdi`, `mmi`) or trivially reconstructable (e.g. `url` from the event ID) are omitted. This keeps the schema clean while preserving the ability to re-run the transformer against the raw table without re-fetching.

**Idempotent writes.** The pipeline distinguishes between new and updated events before inserting. The `daily_earthquakes` table uses `INSERT OR REPLACE`, making the aggregation step safely re-runnable — re-running the pipeline will always produce correct, non-duplicated counts.

**UTC timestamps throughout.** All datetime conversions use `tz=dt.timezone.utc` explicitly to ensure consistent date bucketing regardless of the machine's local timezone.

---

## Database Schema

**`earthquakes`** — one row per event
| Column | Type | Notes |
|---|---|---|
| `id` | TEXT (PK) | USGS canonical event ID |
| `mag` | REAL | Magnitude |
| `mag_bucket` | TEXT | One of: `0-2`, `2-4`, `4-6`, `6-10` |
| `place` | TEXT | Location description |
| `longitude` | REAL | |
| `latitude` | REAL | |
| `depth` | REAL | Depth in km |
| `date` | TEXT | UTC date (YYYY-MM-DD) |
| `time` | INTEGER | Unix timestamp in milliseconds |
| `updated` | INTEGER | Last updated timestamp (ms) |
| `tz` | TEXT | Timezone offset (deprecated by USGS, usually null) |
| `url` | TEXT | USGS event page URL |
| `status` | TEXT | e.g. `reviewed`, `automatic` |

**`daily_earthquakes`** — one row per (date, magnitude bucket)
| Column | Type | Notes |
|---|---|---|
| `date` | TEXT (PK component) | UTC date (YYYY-MM-DD) |
| `mag_bucket` | TEXT (PK component) | Magnitude bucket |
| `num_earthquakes` | INTEGER | Count of events |

---

## Known Limitations

- The USGS `properties.ids` field (which lists all network IDs for an event) is not used for deduplication. In rare cases where an event's canonical ID changes as networks reconcile, a re-fetch and re-run would be needed to catch it.
- The pipeline has no retry logic on failed API requests. Adding exponential backoff would improve resilience as a long-running scheduled job.
- Pagination assumes events are stable across pages during a single run. In practice, new events are added continuously by USGS; a very long-running fetch could theoretically miss or double-count events near a page boundary.
