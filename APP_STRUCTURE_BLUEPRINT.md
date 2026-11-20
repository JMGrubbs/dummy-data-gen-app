# Datadrop Application Structure Blueprint

Datadrop is a containerized dummy-data delivery prototype. This document maps
the repository, service boundaries, routes, and primary runtime flows for
contributors working across the React frontend, FastAPI services, Celery
worker, and local infrastructure.

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
├── postgres/
│   └── init/01-create-app-user.sh
├── frontend/
│   ├── BUILD_FRONTEND.md
│   ├── FEATURES.md
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── layouts/
│       ├── pages/
│       └── services/
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
├── receiver/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── api/v1/
│   ├── cache/
│   ├── core/
│   ├── httpxC/
│   ├── middleware/
│   ├── schemas/
│   └── services/
└── worker/
    ├── celery_app.py
    ├── tasks.py
    ├── repos.py
    ├── requirements.txt
    └── Dockerfile
```

## Runtime Architecture

```text
Browser or API client
  |
  +--> React/Vite frontend (:5173)
  |       |
  |       `--> FastAPI backend (host :8010, container :8000)
  |               |-- external authentication API
  |               |-- PostgreSQL (:5432)
  |               |-- Redis (:6379)
  |               `-- RabbitMQ (:5672)
  |                       |
  |                       v
  |                   Celery worker
  |                       |
  |                       `-- rate-limited HTTP POSTs
  |                                   |
  `-----------------------------------+--> receiver (host :8011, container :8000)
```

The client submits a payload, destination base URL, request count, and rate
limit. The backend persists the job and queues it through RabbitMQ. The worker
then posts the payload repeatedly to the destination's
`/api/v1/receiver/hook` path at the requested rate.

Docker Compose provides service DNS names including `backend`, `receiver`,
`postgres`, `db-cache`, and `rabbitmq`. Container-to-container traffic must use
those names instead of host-only `localhost` addresses.

## Root Files

| Path | Purpose |
| --- | --- |
| `README.md` | Project overview, configuration, runbook, API example, and known limitations. |
| `APP_STRUCTURE_BLUEPRINT.md` | This architecture and file-ownership reference. |
| `docker-compose.yaml` | Builds and connects the frontend, APIs, worker, PostgreSQL, Redis, and RabbitMQ. |
| `pyproject.toml` | Shared Ruff linting and formatting configuration for Python code. |
| `postgres/init/01-create-app-user.sh` | Creates the application database role and schema during initial database setup. |

## Frontend: `frontend/`

The frontend is a small React single-page application. It uses the browser
History API through `pageForPath` in `App.jsx`; React Router is not installed.
The backend base URL comes from `VITE_API_URL` and falls back to
`http://localhost:8010`.

### Current Frontend Layout

```text
frontend/
├── BUILD_FRONTEND.md
├── FEATURES.md
├── Dockerfile
├── index.html
├── package.json
├── vite.config.js
├── .env
├── .env.example
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    ├── layouts/
    │   └── Main.jsx
    ├── pages/
    │   ├── Home.jsx
    │   ├── About.jsx
    │   └── Login.jsx
    └── services/
        ├── api.js
        └── auth.js
```

### Frontend Root Files

| Path | Purpose |
| --- | --- |
| `BUILD_FRONTEND.md` | Frontend-only implementation rules, API-driven workflow, and verification checklist. |
| `FEATURES.md` | Ongoing frontend feature history, assumptions, and handoff notes. |
| `package.json` | React/Vite package metadata, scripts, and dependencies. |
| `Dockerfile` | Container definition for the frontend development service. |
| `index.html` | Vite document entry point. |
| `vite.config.js` | Vite, React, development host, and server configuration. |
| `.env` / `.env.example` | Browser environment values such as `VITE_API_URL`; never place secrets in `VITE_` values. |

### Frontend Source Layout

| Path | Purpose |
| --- | --- |
| `src/main.jsx` | Mounts the React application and imports global styles. |
| `src/App.jsx` | Maps browser paths to pages and owns client-side navigation state. |
| `src/index.css` | Global design tokens, responsive rules, page layouts, and component styles. |
| `src/layouts/Main.jsx` | Shared header, primary navigation, content outlet, and footer. |
| `src/pages/Home.jsx` | Datadrop marketing page and static sample-data preview. |
| `src/pages/About.jsx` | Product story, values, and call to action. |
| `src/pages/Login.jsx` | Login form, submission state, password visibility, and API error display. |
| `src/services/api.js` | Credentialed JSON request wrapper and API methods. |
| `src/services/auth.js` | Reserved authentication service module; currently empty. |

### What Belongs In Each `src/` Folder

The frontend is intentionally small. Keep the current layout, and use these
boundaries as it grows. Some directories below are extension points and do not
exist until a feature needs them.

| Folder or file | Store here | Do not store here |
| --- | --- | --- |
| `src/main.jsx` | React bootstrap code, root providers, and the DOM mount call. | Feature UI, API requests, or page-specific logic. |
| `src/App.jsx` | Top-level application composition, path selection, session boundaries, and cross-feature orchestration. | Large reusable widgets, raw fetch logic, or global CSS. |
| `src/index.css` | CSS reset, design tokens, typography, global layout primitives, accessibility defaults, and shared utilities. | Component business logic or API response handling. |
| `src/assets/` | Images, icons, fonts, and other assets imported by JavaScript or CSS. | User-uploaded runtime files or secrets. |
| `src/components/` | Reusable presentational components and small interaction units shared by pages or features. | Route-level data loading or one-off screen composition. |
| `src/components/<feature>/` | Components for one substantial feature, such as `auth/` or `generation/`. | Unrelated components grouped only by visual type. |
| `src/pages/` | Path-level screens that compose layouts, load feature data, and define page-specific states. | Generic buttons, cards, inputs, or API clients. |
| `src/layouts/` | Shared page chrome such as public/authenticated shells, navigation, headers, sidebars, and footers. | Domain-specific data fetching or persistence models. |
| `src/services/` | Browser API clients, request helpers, auth calls, serializers, and external integrations. | JSX markup or visual styling. |
| `src/hooks/` | Reusable React behavior such as session state, polling, media queries, or request lifecycle state. | Static UI markup or backend-only code. |
| `src/context/` | React providers for genuinely app-wide state such as the current user, theme, or notifications. | State local to one component or page. |
| `src/lib/` | Framework-agnostic utilities, constants, formatters, and validation helpers. | Components, route definitions, or network side effects. |
| `src/types/` | Shared TypeScript types or schema declarations if the frontend moves to TypeScript. | Runtime API calls or rendered UI. |

For a new feature, prefer this separation when each layer is needed:

```text
src/
├── components/<feature>/    # Reusable feature UI
├── pages/<FeaturePage>.jsx  # Path-level composition
├── services/<feature>.js    # API calls and response mapping
└── hooks/use<Feature>.js    # Reusable feature behavior
```

Keep feature-specific code close together. Promote a component, hook, or
utility to a shared location only after multiple feature areas genuinely use
it. Record all frontend work in `frontend/FEATURES.md` as required by
`frontend/BUILD_FRONTEND.md`.

### Current Frontend Routes

| Route | Page | Behavior |
| --- | --- | --- |
| `/` | `Home.jsx` | Product landing page. |
| `/about` | `About.jsx` | Product background and values. |
| `/login` | `Login.jsx` | Sends credentials to the backend login endpoint. |
| Any other path | `Home.jsx` | Falls back to the home page. |

Navigation listens for browser back/forward events. Internal links retain real
`href` values while click handlers use `history.pushState` for in-app
navigation.

### Frontend API Surface

The shared API client includes these backend calls, although the current UI
only invokes login:

| Client capability | API endpoint |
| --- | --- |
| Sign in | `POST /api/v1/auth/login` |
| Create account | `POST /api/v1/auth/register` |
| Restore current session | `GET /api/v1/auth/me` |
| Sign out | `POST /api/v1/auth/logout` |
| Basic health | `GET /api/v1/health` |
| Readiness | `GET /api/v1/health/ready` |
| Liveness | `GET /api/v1/health/live` |

All requests use `credentials: "include"` so the browser can send and retain
the HTTP-only auth cookie. The Google sign-in, forgot-password, terms, and
privacy controls are presentation-only. The generation workspace is not yet
implemented in the frontend.

## Backend API: `backend/`

`backend/main.py` creates the primary FastAPI application, connects Redis and
the shared HTTP client during application lifespan, installs request-ID and
CORS middleware, and mounts the v1 router at `/api/v1`.

### Backend Directories

| Path | Responsibility |
| --- | --- |
| `api/v1/endpoints/` | HTTP route handlers for authentication, health, and job creation. |
| `auth/` | Cookie-to-user dependency and admin API-key guard. |
| `cache/` | Redis connection lifecycle, dependency injection, and JSON helpers. |
| `core/` | Environment-backed settings and HTTP retry construction. |
| `db/` | Declarative metadata, async engine, sessions, and FastAPI DB dependency. |
| `httpxC/` | Shared asynchronous HTTPX client. |
| `middleware/` | Request-ID propagation. |
| `models/` | SQLAlchemy models for generation tasks and login events. |
| `schemas/` | Pydantic request/response models and auth-domain errors. |
| `services/` | Authentication integration, job creation, receiver calls, and health checks. |
| `worker/` | Celery producer used by the API to enqueue worker tasks. |
| `alembic/` | Database migration environment and version history. |

### Backend Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Basic process health. |
| `GET` | `/api/v1/health/ready` | Verifies PostgreSQL and Redis connectivity. |
| `GET` | `/api/v1/health/live` | Returns an alive status and UTC timestamp. |
| `POST` | `/api/v1/auth/login` | Authenticates upstream, records a login, and sets the auth cookie. |
| `GET` | `/api/v1/auth/me` | Resolves the current cookie through the external auth service. |
| `POST` | `/api/v1/auth/logout` | Requests upstream logout and removes the local cookie. |
| `POST` | `/api/v1/auth/register` | Creates a user through the external auth service. |
| `POST` | `/api/v1/gen/create` | Persists and queues a data-delivery task. |

### Authentication Flow

```text
Login.jsx
  |
  | POST /api/v1/auth/login { username, password }
  v
Backend authentication service
  |
  | forwards credentials to <AUTH_API_URL>
  v
External authentication API
  |
  +--> token and user identity
  |
Backend
  |-- inserts app.login_log
  `-- sets configured HTTP-only auth cookie
```

`GET /auth/me` reads the configured cookie and forwards its token upstream as
a Bearer token. The external service owns authentication identities; Datadrop
only stores successful login events.

### Generation Request Contract

`POST /api/v1/gen/create` accepts the `PackageFormat` schema:

| Field | Type | Meaning |
| --- | --- | --- |
| `number_of_requests` | integer | Number of webhook deliveries to attempt. |
| `requests_per_min` | integer | Requested delivery rate; the worker guards against a divisor below one. |
| `data` | JSON object | Payload posted unchanged for every delivery. |
| `url_destination` | string | Base destination; defaults to `http://receiver:8000`. |

After committing the database row, the backend appends
`/api/v1/receiver/hook` to the base destination and enqueues the task. The
endpoint currently uses a fixed placeholder user UUID and is not protected by
the authentication dependency.

## Persistence

Application-owned tables live in the PostgreSQL `app` schema.

| Table | Purpose |
| --- | --- |
| `app.data_gen_task` | Stores destination, JSONB payload blueprint, initial request count, rate, status, and a user UUID for each generation job. |
| `app.login_log` | Stores the user UUID and timestamp for successful logins. |

The worker currently reads the task values passed through Celery; it does not
update `status` or `remaining_requests`. Alembic uses metadata from
`backend/db/base.py` and stores its version table in the `app` schema.

## Queue and Worker: `worker/`

`backend/worker/worker.py` is the producer. After the database commit,
`backend/services/dataGenTask.py` sends
`data_gen.process_data_gen_task` to the `data-gen` quorum queue.

| Path | Purpose |
| --- | --- |
| `worker/celery_app.py` | Configures RabbitMQ, quorum queue behavior, late acknowledgements, and worker prefetch. |
| `worker/tasks.py` | Defines the synchronous Celery entry point and runs the async delivery routine. |
| `worker/repos.py` | Validates task values and performs repeated, rate-limited HTTP POST requests. |

The worker uses late acknowledgements and a prefetch multiplier of one. It
waits `60 / requests_per_min` seconds between deliveries. Individual HTTP
failures are logged and do not prevent later deliveries in the same task.
Celery results are not stored.

## Receiver API: `receiver/`

The receiver is a development-only webhook target. It connects to Redis
during startup and exposes:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Basic process health. |
| `GET` | `/api/v1/health/ready` | Receiver dependency readiness. |
| `GET` | `/api/v1/health/live` | Alive status and timestamp. |
| `POST` | `/api/v1/receiver/hook` | Prints the submitted JSON and returns `{"status": "ok"}`. |

Received payloads are not persisted. The readiness helper currently does not
await its Redis ping or reduce its gathered values to a boolean, so it cannot
reliably report a Redis outage after startup.

## Configuration Boundaries

| File | Important settings |
| --- | --- |
| Root `.env` | PostgreSQL credentials, application DB role/schema, RabbitMQ credentials, and host-port overrides. |
| `backend/.env` | Database and Redis URLs, cookie settings, auth API URL, allowed frontend origins, receiver URL, and Celery broker URL. |
| `frontend/.env` | Browser-visible backend base URL (`VITE_API_URL`). |
| `receiver/.env` | Redis URL. |
| `worker/.env` | Celery broker and database URLs. |

Environment files are ignored by Git. Keep credentials consistent between
Compose and service files. Values prefixed with `VITE_` are bundled into
browser code and must never contain secrets.

## Compose Services and Startup

| Service | Default host port | Role |
| --- | ---: | --- |
| `frontend` | `5173` | Vite development server. |
| `backend` | `8010` | Primary FastAPI API; listens on `8000` in the container. |
| `receiver` | `8011` | Local webhook target; listens on `8000` in the container. |
| `postgres` | `5432` | Application persistence. |
| `db-cache` | `6379` | Redis cache and readiness dependency. |
| `rabbitmq` | `5672` | Celery broker. |
| RabbitMQ management | `15672` | Broker administration UI. |
| `worker` | — | Celery consumer for the `data-gen` queue. |

```text
postgres healthy --------> backend healthy --------> frontend
       |
       +--------------------> receiver
       `--------------------> worker <-------- rabbitmq healthy
```

The backend and receiver also connect to Redis during application startup,
although Compose does not currently declare `db-cache` as their dependency.

## Development Commands

Run these from the repository root unless noted otherwise:

```bash
# Build and start the full stack
docker compose up --build

# Apply database migrations
docker compose exec backend alembic upgrade head

# Inspect services and logs
docker compose ps
docker compose logs -f backend worker receiver

# Validate Python syntax
python -m compileall backend receiver worker

# Build the frontend
cd frontend
npm install
npm run build
```

## Development Conventions

- Keep browser concerns inside `frontend/` and follow `BUILD_FRONTEND.md`.
- Keep API routing, validation, persistence, and infrastructure concerns in
  their owning backend, receiver, or worker layer.
- Add backend endpoints under `backend/api/v1/endpoints/` and include their
  router in `backend/api/v1/api.py`.
- Keep browser requests in `frontend/src/services/` and preserve
  `credentials: "include"` for authenticated calls.
- Represent loading, empty, success, validation, unauthorized, network, and
  server-error states where they apply.
- Update `frontend/FEATURES.md` for frontend work and update this blueprint
  when service boundaries, top-level directories, routes, or layout rules
  change.

## Current Extension Points

- Add a protected frontend workspace for configuring and submitting
  generation jobs.
- Replace the fixed job `user_id` with the authenticated user's ID.
- Add job retrieval, progress, cancellation, and terminal-status APIs.
- Update job status and remaining-request counts from the worker.
- Add explicit bounds for generation counts, rate limits, and destination URLs.
- Decide whether the local receiver should persist request history.
- Add automated backend, worker, receiver, and frontend tests.
