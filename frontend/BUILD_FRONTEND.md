# Build Frontend Instructions

## Objective

Build and maintain the data-dummy frontend using the capabilities exposed by the data-dummy API.

API documentation:

- https://ddd-backend.johnmgrubbs.io/docs

Use the API's OpenAPI documentation as the source of truth for available endpoints, request bodies, response shapes, authentication behavior, and validation rules. Do not invent backend capabilities that are not documented or implemented.

## Scope boundary

- Only make changes inside the `frontend/` directory.
- Do not edit `backend/`, root infrastructure files, Docker Compose configuration, database migrations, or deployment files.
- If a requested frontend feature requires a backend change, document the dependency and stop short of editing backend files.

## Frontend implementation rules

1. Inspect the existing frontend before changing it.
2. Keep the existing React/Vite setup unless the task explicitly asks for a framework change.
3. Use `VITE_API_URL` for the API base URL, with the local development fallback documented by the project.
4. Put browser API calls in a service/helper layer as the frontend grows; keep network behavior out of presentational components when practical.
5. Include credentials on requests whenever the API uses cookie-based authentication.
6. Represent loading, empty, success, validation-error, unauthorized, network-error, and server-error states in the UI where applicable.
7. Keep the interface responsive, keyboard-accessible, and usable on narrow screens.
8. Match request and response fields exactly to the API documentation.
9. Avoid exposing secrets in source code, `.env` files, logs, or rendered UI.
10. Keep new code organized according to `APP_STRUCTURE_BLUEPRINT.md`.

## Feature tracking

All frontend work must be recorded in:

- `frontend/FEATURES.md`

Before implementation:

- Read the existing `FEATURES.md`.
- Add the requested work to an appropriate planned or in-progress section when useful.

After implementation:

- Add a concise entry describing the completed feature.
- Include the API endpoint(s) used, if any.
- Note important assumptions, limitations, or follow-up work.
- Do not remove prior feature history unless it is demonstrably incorrect.

The `FEATURES.md` file is the ongoing handoff record for future frontend work. New work should extend it rather than creating a separate feature log.

## API-driven workflow

For each requested feature:

1. Read the relevant endpoint in the API docs.
2. Identify the HTTP method, path, authentication requirement, request schema, response schema, and error behavior.
3. Add or update the frontend API helper.
4. Build the corresponding UI and state transitions.
5. Verify the feature against the documented API contract.
6. Run the frontend build or the narrowest relevant validation available.
7. Update `FEATURES.md` with the result.

## Current documented Watchtower capabilities

The current frontend can use these API areas when they are available in the docs:

- Authentication: registration, login, current-user/session lookup, and logout.
- Health monitoring: general health, readiness, and liveness probes.
- Projects: authenticated list, detail, create, update, and delete operations.
- Project environments: authenticated list, detail, create, update, and delete operations nested under a project.
- Environment monitors: authenticated list, detail, create, update, and delete operations nested under a project environment.
- Monitor uptime: current `status` and embedded `status_history` entries returned with monitor records.

Do not assume that an endpoint exists solely because a UI concept would be useful. Confirm it in the API documentation first.

## Verification checklist

- Confirm only files under `frontend/` changed.
- Confirm API URLs are configurable and no secrets are committed.
- Confirm authenticated requests send the required credentials.
- Confirm errors are understandable to the user.
- Confirm responsive behavior at desktop and mobile widths.
- Run the frontend build when dependencies are available.
- Update `FEATURES.md` before handing off the work.
