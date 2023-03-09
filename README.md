# Spotify's artists CRUD API

A small API with CRUD operations on the table with the artists that were got using Spotify API


## Requirements
* [Python 3.11](https://docs.python.org/3/whatsnew/3.11.html)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Poetry](https://python-poetry.org/) for Python package and environment management

## Installation

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Activate python virtual environment 
```bash
poetry shell
```
* Install python packages
```bash
poetry install
```

* Run migrations
```bash
poetry run alembic upgrade head
```

* Run the API application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --lifespan=on --use-colors --loop uvloop --http httptools
```

The application is available by http://0.0.0.0:8000/

## API reference

The API reference is available by http://0.0.0.0:8000/docs




