# world-wire-be

# 1. Setup

It is assumed the GitHub repository is cloned.

## 1.1. Docker-compose
In case of using docker-compose

The setup is as easy as
```shell
docker-compose up
```

Or in case of running in the background
```bash
docker-compose up -d
# docker-compose logs -f # for viewing live logs
```

# 2. Usage (in local computer)
In order to start using the application, initial data ingestion must be triggered.

Open up the Swagger docs: http://0.0.0.0:8071/docs (or http://0.0.0.0:8071/docs#/default/ingest_countries_api_v1_countries_ingest_post to be precise)
and trigger it.

Track ingest task on celery flower on: http://0.0.0.0:45555


Once the countries are ingested successfully, you can list through countries, signup and (soon) will be able to bookmark countries.


# Improvements
- Finalize bookmark endpoints
- Increase test coverage
- Implement Redis cache
- Improve docstrings
- Add MKDocs