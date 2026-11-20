# Data-dummy frontend features

## Documentation

- Added `BUILD_FRONTEND.md` with API-driven implementation rules, frontend-only scope, verification guidance, and the required `FEATURES.md` handoff workflow.

## Implemented

- Added an authenticated workspace with responsive sidebar and mobile
  navigation, session restoration through `GET /api/v1/auth/me`, logout through
  `POST /api/v1/auth/logout`, and unauthorized-session redirects.
- Added `/dashboard`, with a real project count, latest-project summary, recent
  project list, loading/error states, and a first-project empty state. Data is
  loaded from `GET /api/v1/projects`.
- Added `/projects`, `/projects/new`, and `/projects/{project_id}/edit` screens
  for listing, creating, renaming, and deleting projects. These use
  `GET /api/v1/projects`, `GET /api/v1/projects/{project_id}`,
  `POST /api/v1/projects`, `PUT /api/v1/projects/{project_id}`, and
  `DELETE /api/v1/projects/{project_id}`.
- Improved API validation-error messages and connected successful login to the
  authenticated dashboard.

## API assumptions

- The live OpenAPI schema at `https://ddd-backend.johnmgrubbs.io/openapi.json`
  is the source of truth used for this implementation.
- Project list and detail responses use the documented `{ projects: [...] }`
  shape. Create and update requests send only the documented `name` field.
- The API does not currently expose environment, generation-history, or
  activity metrics, so the dashboard does not invent them.
- Project deletion uses a browser confirmation because the API documents no
  recovery or archive operation.

## Verification

- `npm run build` succeeds with Vite 7.3.8.

