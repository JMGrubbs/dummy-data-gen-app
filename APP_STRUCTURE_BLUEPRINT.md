# Datadrop Application Structure Blueprint

This document describes the application structure, service boundaries, routes,
and primary runtime flows in this repository. It is intended as a map for
contributors working across the React frontend, FastAPI services, Celery
worker, and infrastructure.

## Technology Summary

| Area | Technology |
| --- | --- |
| Frontend | React 19, Vite 7, JavaScript with JSX, CSS |
| APIs | Python 3.12, FastAPI, Pydantic |
| Persistence | PostgreSQL 17, SQLAlchemy 2, Alembic, JSONB |
| Queue | RabbitMQ 4, Celery 5 |
| Cache | Redis |
| HTTP delivery | HTTPX |
| Local orchestration | Docker Compose |

## Repository Layout

```text
dummy-data-gen-app/
├── README.md
├── APP_STRUCTURE_BLUEPRINT.md
├── LICENSE
├── docker-compose.yaml
├── pyproject.toml
├── backend/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── api/v1/
│   │   ├── api.py
│   │   └── endpoints/
│   ├── auth/
│   ├── cache/
│   ├── core/
│   ├── db/
│   ├── httpxC/
│   ├── middleware/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── worker/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── layouts/
│       ├── pages/
│       └── services/
├── receiver/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── api/v1/
│   │   ├── api.py
│   │   └── endpoints/
│   ├── cache/
│   ├── core/
│   ├── httpxC/
│   ├── middleware/
│   ├── schemas/
│   └── services/
├── worker/
│   ├── celery_app.py
│   ├── tasks.py
│   ├── repos.py
│   ├── requirements.txt
│   └── Dockerfile
└── postgres/
    └── init/
        └── 01-create-app-user.sh
```

## Runtime Structure

```text
Browser or API client
  |
  +--> React/Vite frontend :5173
  |       |
  |       `--> FastAPI backend :8010
  |               |-- external authentication API
  |               |-- PostgreSQL
  |               |-- Redis
  |               `-- RabbitMQ
  |                       |
  |                       v
  |                   Celery worker
  |                       |
  |                       `-- HTTP POST --> destination webhook
  |
  `--------------------------------------> sample receiver :8011
                                                  |
                                                  `-- Redis readiness dependency
```

Docker Compose provides service DNS names such as `backend`, `receiver`,
`postgres`, `db-cache`, and `rabbitmq`. Container-to-container URLs must use
those names rather than host-only `localhost` addresses.

## Root Files

| Path | Purpose |
| --- | --- |
| `README.md` | Project overview, environment setup, runbook, API example, and current limitations. |
| `APP_STRUCTURE_BLUEPRINT.md` | This architecture and file ownership reference. |
| `docker-compose.yaml` | Builds and connects the frontend, APIs, worker, PostgreSQL, Redis, and RabbitMQ. |
| `pyproject.toml` | Shared Ruff linting and formatting configuration for Python code. |
| `postgres/init/01-create-app-user.sh` | Creates or updates the application database role and schema on first database initialization. |

## Frontend

The frontend is a small React single-page application. It uses the browser
History API through a local `pageForPath` function rather than React Router.

### Frontend files

| Path | Purpose |
| --- | --- |
| `frontend/index.html` | Vite document entry point. |
| `frontend/src/main.jsx` | Mounts the React application and imports global styles. |
| `frontend/src/App.jsx` | Maps browser paths to pages and owns client-side navigation state. |
| `frontend/src/index.css` | Global design tokens, responsive styles, page layouts, and component styles. |
| `frontend/src/layouts/Main.jsx` | Shared header, primary navigation, content outlet, and footer. |
| `frontend/src/pages/Home.jsx` | Datadrop marketing page and static sample-data preview. |
| `frontend/src/pages/About.jsx` | Product story, values, and call to action. |
| `frontend/src/pages/Login.jsx` | Login form, submission state, password visibility, and API error display. |
| `frontend/src/services/api.js` | Credentialed JSON request wrapper and API methods. |
| `frontend/src/services/auth.js` | Reserved authentication service module; currently empty. |
| `frontend/vite.config.js` | React plugin and development-host allowlist. |

### Frontend routes

| Route | Page | Behavior |
| --- | --- | --- |
| `/` | `Home.jsx` | Product landing page. |
| `/about` | `About.jsx` | Product background and values. |
| `/login` | `Login.jsx` | Sends credentials to the backend login endpoint. |
| Any other path | `Home.jsx` | Falls back to the home page. |

The login page uses `credentials: "include"`, allowing the browser to retain
the HTTP-only session cookie set by the backend. The Google, forgot-password,
terms, and privacy controls are currently presentation-only.

## Backend API

`backend/main.py` creates the primary FastAPI application, connects Redis and
the shared HTTP client during application lifespan, installs request-ID and
CORS middleware, and mounts the v1 router at `/api/v1`.

### Backend directories

| Path | Responsibility |
| --- | --- |
| `backend/api/v1/endpoints/` | HTTP route handlers for authentication, health, and job creation. |
| `backend/auth/` | Cookie-to-user dependency and admin API-key guard. |
| `backend/cache/` | Redis connection lifecycle, dependency injection, and JSON helpers. |
| `backend/core/` | Environment-backed settings and HTTP retry construction. |
| `backend/db/` | Declarative metadata, async engine, sessions, and FastAPI DB dependency. |
| `backend/httpxC/` | Shared asynchronous HTTPX client. |
| `backend/middleware/` | Request ID propagation. |
| `backend/models/` | SQLAlchemy models for generation tasks and login events. |
| `backend/schemas/` | Pydantic request/response models and auth-domain errors. |
| `backend/services/` | Authentication integration, job creation, and health checks. |
| `backend/worker/` | Celery producer used by the API to enqueue worker tasks. |
| `backend/alembic/` | Database migration environment and version history. |

### Backend routes

| Method | Route | Handler | Purpose |
| --- | --- | --- | --- |
| `GET` | `/api/v1/health` | `health_check` | Basic process health. |
| `GET` | `/api/v1/health/ready` | `readiness_check` | Verifies PostgreSQL and Redis connectivity. |
| `GET` | `/api/v1/health/live` | `liveness_check` | Returns an alive status and UTC timestamp. |
| `POST` | `/api/v1/auth/login` | `login_route` | Authenticates upstream, records a login, and sets the auth cookie. |
| `GET` | `/api/v1/auth/me` | `read_me_route` | Resolves the current cookie through the external auth service. |
| `POST` | `/api/v1/auth/logout` | `logout_route` | Requests upstream logout and removes the local cookie. |
| `POST` | `/api/v1/auth/register` | `register_route` | Creates a user through the external auth service. |
| `POST` | `/api/v1/gen/create` | `data_generator` | Persists and queues a generation task. |

### Authentication flow

```text
Login.jsx
  |
  | POST /api/v1/auth/login { username, password }
  v
Backend authentication service
  |
  | POST <AUTH_API_URL>/api/v1/auth/login
  | internal=true
  v
External auth API
  |
  +--> token and user identity
  |
Backend
  |-- inserts app.login_log
  `-- sets HTTP-only access_token cookie
```

`GET /auth/me` reads the configured cookie and sends its token upstream as a
Bearer token. Authentication identities remain owned by the external auth
service; this application only stores login events.

### Generation request contract

`PackageFormat` accepts:

| Field | Type | Meaning |
| --- | --- | --- |
| `number_of_requests` | integer | Number of webhook deliveries to attempt. |
| `requests_per_min` | integer | Requested delivery rate. The worker enforces a minimum divisor of one. |
| `data` | JSON object | Payload posted unchanged on every request. |
| `url_destination` | string | Base destination. Defaults to `http://receiver:8000`. |

The backend appends `/api/v1/receiver/hook` to the destination before enqueuing
the task.

## Persistence

All application-owned tables live in the PostgreSQL `app` schema.

### `app.data_gen_task`

| Column | Purpose |
| --- | --- |
| `id` | Integer primary key passed to the Celery task. |
| `user_id` | Indexed UUID; currently populated with a fixed placeholder value. |
| `url_destination` | Submitted base destination URL. |
| `data_bp` | JSONB payload blueprint. |
| `remaining_requests` | Requested delivery count at creation. |
| `requests_per_min` | Requested rate. |
| `status` | Creation status, defaulting to `pending`. |

### `app.login_log`

| Column | Purpose |
| --- | --- |
| `id` | Integer primary key. |
| `user_id` | Indexed UUID returned by the auth service. |
| `login_datetime` | Indexed successful-login timestamp. |

Alembic uses `backend/db/base.py` metadata and stores its version table in the
`app` schema.

## Queue And Worker

### Producer

`backend/worker/worker.py` creates a lightweight Celery client. After the
database commit, `backend/services/dataGenTask.py` sends
`data_gen.process_data_gen_task` to the `data-gen` quorum queue.

### Consumer

| Path | Purpose |
| --- | --- |
| `worker/celery_app.py` | Configures RabbitMQ, quorum queue behavior, late acknowledgements, and worker prefetch. |
| `worker/tasks.py` | Defines the synchronous Celery entry point and starts the async delivery routine. |
| `worker/repos.py` | Validates task input and performs repeated HTTP POST requests with rate limiting. |

The worker is configured with late acknowledgements and a prefetch multiplier
of one. HTTP response errors are logged per request; they do not stop later
requests in the same task. Celery task results are not stored.

## Receiver API

The receiver is a minimal FastAPI service that provides a local webhook target.
It connects to Redis during its application lifespan and exposes:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Basic process health. |
| `GET` | `/api/v1/health/ready` | Receiver readiness route; its current Redis failure detection is incomplete. |
| `GET` | `/api/v1/health/live` | Returns an alive status and timestamp. |
| `POST` | `/api/v1/receiver/hook` | Prints the submitted JSON payload and returns `{"status": "ok"}`. |

The receiver is a development aid rather than a durable sink: received data is
not persisted.

## Configuration Boundaries

| File | Important settings |
| --- | --- |
| Root `.env` | PostgreSQL credentials, application DB role/schema, RabbitMQ credentials, host ports. |
| `backend/.env` | Database and Redis URLs, cookie settings, auth API URL, allowed frontend origins, receiver URL, Celery broker URL. |
| `frontend/.env` | Browser-visible backend base URL (`VITE_API_URL`). |
| `receiver/.env` | Redis URL. |
| `worker/.env` | Celery broker and database URLs. |

Environment files are ignored by Git. Values prefixed with `VITE_` are bundled
into browser code and must not contain secrets.

## Health And Startup

Compose startup dependencies are:

```text
postgres healthy --------> backend healthy --------> frontend
       |
       `------------------> receiver

rabbitmq healthy --------> worker
postgres healthy --------> worker
```

The backend application itself also connects to Redis on startup, although
Compose does not currently declare `db-cache` as a backend dependency. The
receiver follows the same Redis startup pattern. Its readiness helper does not
currently await the Redis ping and returns a gathered tuple rather than a
boolean, so post-startup Redis failures are not reported reliably.

## Development Commands

Run from the repository root unless noted otherwise:

```bash
# Build and start everything
docker compose up --build

# Apply schema migrations
docker compose exec backend alembic upgrade head

# Inspect containers and logs
docker compose ps
docker compose logs -f backend worker receiver

# Validate Python syntax
python -m compileall backend receiver worker

# Build the frontend
cd frontend
npm install
npm run build
```

## Current Extension Points

- Add a protected frontend workspace for configuring and submitting generation
  jobs.
- Replace the fixed job `user_id` with the authenticated user's ID.
- Add job retrieval, progress, cancellation, and terminal-status APIs.
- Update task status and remaining-request counts from the worker.
- Validate generation counts, rate limits, and destination URLs with explicit
  bounds.
- Decide whether the local receiver should persist request history.
- Add automated backend, worker, receiver, and frontend tests.
