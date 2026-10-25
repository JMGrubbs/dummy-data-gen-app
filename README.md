# Datadrop Dummy Data Generator

Datadrop is a containerized dummy-data delivery prototype. A client submits a
JSON payload, destination URL, request count, and rate limit to the FastAPI
backend. The backend persists the job in PostgreSQL and queues it in RabbitMQ;
a Celery worker then sends the payload to the destination at the requested
rate. The repository includes a small receiver API for exercising that flow
locally and a React/Vite marketing and login frontend.

> The generation form/workspace is not implemented in the frontend yet. Jobs
> can currently be created through the backend API or its Swagger UI.

For a file-by-file architecture reference, see
[`APP_STRUCTURE_BLUEPRINT.md`](APP_STRUCTURE_BLUEPRINT.md).

## Stack

- React 19 and Vite 7
- FastAPI and Pydantic
- PostgreSQL 17 with SQLAlchemy and Alembic
- RabbitMQ and Celery
- Redis
- Docker Compose

## Services

| Service | Default host port | Purpose |
| --- | ---: | --- |
| `frontend` | `5173` | React landing, about, and login pages. |
| `backend` | `8010` | Authentication proxy, health endpoints, and job creation API. |
| `receiver` | `8011` | Local webhook target used to inspect delivered payloads. |
| `postgres` | `5432` | Stores login events and data-generation jobs. |
| `db-cache` | `6379` | Redis connection used by API readiness checks and cache helpers. |
| `rabbitmq` | `5672` | Celery message broker. |
| `rabbitmq` management UI | `15672` | RabbitMQ administration interface. |
| `worker` | — | Consumes the `data-gen` queue and posts payloads to destinations. |

## Request Flow

```text
Client
  |
  | POST /api/v1/gen/create
  v
Backend API
  |-- persists app.data_gen_task --> PostgreSQL
  `-- enqueues task -------------> RabbitMQ
                                      |
                                      v
                                  Celery worker
                                      |
                                      | repeated, rate-limited POSTs
                                      v
                     <url_destination>/api/v1/receiver/hook
```

The worker currently sends the submitted `data` object unchanged. It waits
`60 / requests_per_min` seconds between requests and logs success or failure
for each delivery.

## Prerequisites

- Docker with Docker Compose v2
- Access to the configured external authentication API if you want to use the
  login and registration endpoints

Node.js and Python are only required when running services outside Docker.

## Configuration

Compose reads five local environment files. Existing `.env` files are ignored
by Git and should never be committed.

### Root `.env`

The root file configures PostgreSQL, RabbitMQ, and optional host-port
overrides:

```dotenv
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

APP_DB_USER=app
APP_DB_PASSWORD=change-me
APP_DB_SCHEMA=app

RABBITMQ_USER=celery
RABBITMQ_PASSWORD=change-me

# Optional host-port overrides
FRONTEND_PORT=5173
BACKEND_PORT=8010
POSTGRES_PORT=5432
REDIS_PORT=6379
RABBITMQ_PORT=5672
RABBITMQ_MANAGEMENT_PORT=15672
```

The PostgreSQL initialization script creates `APP_DB_USER` and
`APP_DB_SCHEMA` only when the database volume is initialized for the first
time.

### Service environment files

Start from the checked-in examples where available:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp receiver/.env.example receiver/.env
```

Ensure the following settings are present. Pydantic expects
`FRONTEND_ORIGIN_URL` to be a JSON list.

`backend/.env`:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/postgres
REDIS_URL=redis://db-cache:6379/0
COOKIE_KEY=access_token
COOKIE_SECURE=false
AUTH_API_URL=https://your-auth-service.example
FRONTEND_ORIGIN_URL=["http://localhost:5173"]
RECEIVER_URL=http://receiver:8000
CELERY_BROKER_URL=amqp://celery:change-me@rabbitmq:5672//
```

`frontend/.env`:

```dotenv
VITE_API_URL=http://localhost:8010
```

`receiver/.env`:

```dotenv
REDIS_URL=redis://db-cache:6379/0
```

`worker/.env`:

```dotenv
CELERY_BROKER_URL=amqp://celery:change-me@rabbitmq:5672//
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/postgres
```

Keep the PostgreSQL and RabbitMQ credentials consistent across the root and
service-specific files.

## Run Locally

Build and start the stack:

```bash
docker compose up --build
```

Apply database migrations in another terminal:

```bash
docker compose exec backend alembic upgrade head
```

Useful URLs:

- Frontend: <http://localhost:5173>
- Backend OpenAPI docs: <http://localhost:8010/docs>
- Backend health: <http://localhost:8010/api/v1/health>
- Receiver OpenAPI docs: <http://localhost:8011/docs>
- RabbitMQ management: <http://localhost:15672>

Check service state and follow logs with:

```bash
docker compose ps
docker compose logs -f backend worker receiver
```

Stop the services without removing database or Redis volumes:

```bash
docker compose down
```

## Create a Generation Job

The bundled receiver is the default destination. Submit a job through Swagger
UI or with `curl`:

```bash
curl -X POST http://localhost:8010/api/v1/gen/create \
  -H 'Content-Type: application/json' \
  -d '{
    "number_of_requests": 5,
    "requests_per_min": 60,
    "data": {
      "name": "Alex Morgan",
      "email": "alex@example.com",
      "status": "active"
    },
    "url_destination": "http://receiver:8000"
  }'
```

The backend appends `/api/v1/receiver/hook` to `url_destination`. When the
worker runs inside Compose, use a URL reachable from the worker container—not
`localhost`—for custom destinations.

## API Summary

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Basic backend health response. |
| `GET` | `/api/v1/health/ready` | Checks PostgreSQL and Redis. |
| `GET` | `/api/v1/health/live` | Liveness response with a timestamp. |
| `POST` | `/api/v1/auth/login` | Authenticates upstream and sets an HTTP-only cookie. |
| `GET` | `/api/v1/auth/me` | Resolves the cookie through the upstream auth API. |
| `POST` | `/api/v1/auth/logout` | Logs out upstream and clears the cookie. |
| `POST` | `/api/v1/auth/register` | Creates a user through the upstream auth API. |
| `POST` | `/api/v1/gen/create` | Persists and queues a data-delivery job. |
| `POST` | `/api/v1/receiver/hook` | Receiver-only endpoint that prints a delivered payload. |

## Development Notes

- Backend and receiver containers use Uvicorn reload mode and bind-mount their
  source directories.
- The frontend source is bind-mounted and served by Vite with hot reload.
- Alembic owns the PostgreSQL `app` schema and its migrations live under
  `backend/alembic/versions/`.
- Ruff settings are defined in `pyproject.toml`.
- Automated tests and a frontend lint script are not currently included.

Build the frontend directly with:

```bash
cd frontend
npm install
npm run build
```

## Current Limitations

- The frontend login form calls the backend, but no authenticated application
  area or data-generation form is implemented yet.
- The generation endpoint currently assigns every job a fixed placeholder user
  UUID and is not protected by the authentication dependency.
- Job status and remaining-request fields are persisted at creation time but
  are not updated by the worker.
- The receiver only prints payloads; it does not persist them.
- The receiver readiness implementation does not currently await its Redis
  ping or reduce the gathered result to a boolean, so it cannot reliably
  report a Redis outage after startup.
