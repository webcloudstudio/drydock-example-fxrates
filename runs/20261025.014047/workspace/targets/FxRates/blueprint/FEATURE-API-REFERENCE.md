# FEATURE: API Reference

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Exposes the generated API schema for programmatic discovery. |
| Depends On  | ARCHITECTURE.md |
| Provides    | GET /openapi.json |

## Purpose

Expose FastAPI's OpenAPI document at `GET /openapi.json` as the discovery entry point for the programmatic API. Keep the schema generated from the application's declared routes.

## Programmatic Acceptance

=== AC api-reference-discovery ===
Intent: The API discovery endpoint returns a schema that describes the provided API routes.

from app_server.testing import web_client

response = web_client().get("/openapi.json")
assert response.status_code == 200
schema = response.json()
assert isinstance(schema, dict)
paths = schema["paths"]
assert "/health" in paths
assert "/stats" in paths
assert "/currencies" in paths
assert "/rates/{date}" in paths
assert "/rates/latest" in paths
assert "/convert" in paths
assert "/history/{code}" in paths
=== END AC api-reference-discovery ===

## User Acceptance

- None.

## Guardrails

- Keep the discovery document generated from the API application so it reflects the routes the service actually exposes.
