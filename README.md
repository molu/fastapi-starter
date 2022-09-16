# fastapi-starter

FastAPI, SQLModel, Alembic, asyncpg starter project.

---

## Project structure

- `/app/api/`: application routes (`/app/api/v1/endpoints/*` and
  `/app/api/v1/router.py` that should include all of the routes from the `endpoints` directory);
- `/app/core/`: core of the application (e.g. `config.py` configuration file);
- `/app/crud/`: CRUD models;
- `/app/db/`: database engine, session and Alembic migrations;
- `/app/models/`: database SQLModel models;
- `/app/schemas/`: SQLModel-based schemas;
- `/app/services/`: place for other business logic - celery, utils, exceptions etc.;
- `/app/tests/`: application tests.

## Running the project

1. Rename the `.env.example` file to `.env` and edit the configuration as needed.
2. (optional) Change the port forwarding in `docker-compose.yaml`.
3. Build and run the containers:

`docker compose up --build`

or run tests using `docker-compose.test.yaml`:

`docker compose -f docker-compose.test.yaml up --build`
