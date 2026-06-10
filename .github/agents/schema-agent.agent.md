# Implement schema.osm.dev interactive schema website, validation, docs, tests, Docker image, and Copilot custom agent configuration

## Objective

Implement, document, test, and containerise `schema.osm.dev`.

The repository must define and publish the machine-readable schema layer for Organisation Service Management (OSM), and must include an interactive website that allows users to navigate, search, inspect, validate, and understand the schema.

The implementation must reflect the repository `README.md`. The README is the first source of truth. If this task conflicts with the README, the README wins.

The website must use styling and language consistent with `osm.dev` branding:

- `osm.dev · Open Standards`
- Open Standards
- Open Source
- Schema-as-code
- Configuration-as-code
- Vendor independence
- Automation-first
- Standards-aligned
- Modular OSM suite
- Typed organisational entities and relationships
- Traceability, validation, auditability, and safer automation/AI use

The site must not hotlink external assets from `osm.dev`. If branding assets are not present in the repository, add a documented placeholder and note the missing asset in `docs/implementation-notes.md`.

---

## Mandatory first step

Before writing implementation code, inspect the repository and produce a short implementation plan in the PR body covering:

1. Current repository structure.
2. Contents and intent of `README.md`.
3. Existing schema files, examples, tests, build tooling, workflows, and docs.
4. Gaps between the current repository and this target state.
5. Assumptions made because the README is silent or ambiguous.
6. Any existing conventions that should be preserved.

Do not overwrite existing work unnecessarily. Prefer incremental changes.

---

## Source-of-truth priority

Use this priority order:

1. Existing `README.md`.
2. Existing schema files.
3. Existing examples, tests, docs, and workflows.
4. Existing package/build conventions.
5. Existing repository metadata such as license, package manager, and deployment conventions.
6. This task brief.
7. Minimal new conventions required to make the project coherent, buildable, testable, and maintainable.

If anything is ambiguous, document the assumption in:

```text
docs/implementation-notes.md
````

and summarise it in the PR body.

Do not invent schema semantics that are not supported by the README or existing repository direction.

---

## Required deliverables

The final PR must include:

1. Machine-readable OSM schema files.
2. Valid and invalid example documents.
3. Schema validation tests.
4. Interactive static website for navigating and understanding `schema.osm.dev`.
5. Docker image that builds and serves the website.
6. CI workflow covering schema validation, website checks, tests, and Docker image build/run smoke test.
7. Repository Copilot instructions.
8. GitHub custom agent profile under `.github/agents`.
9. Documentation for schema authors, website maintainers, Docker users, and test runners.
10. Clear PR evidence showing commands run and results.

---

# Part A — GitHub Copilot and custom-agent configuration

## Required Copilot/agent files

Create or update:

```text
.github/copilot-instructions.md
.github/agents/schema-osm-dev-implementer.agent.md
```

Optionally create these path-specific instruction files if useful:

```text
.github/instructions/schema.instructions.md
.github/instructions/frontend.instructions.md
.github/instructions/docker.instructions.md
.github/instructions/docs.instructions.md
.github/instructions/tests.instructions.md
.github/instructions/github-actions.instructions.md
AGENTS.md
```

Use `AGENTS.md` if the repository should also support non-Copilot coding agents.

---

## `.github/agents/schema-osm-dev-implementer.agent.md`

Create the following file.

````markdown
---
name: schema-osm-dev-implementer
description: Implements, documents, validates, tests, and containerises schema.osm.dev according to the repository README, OSM schema conventions, and repository quality gates.
target: github-copilot
tools: ["read", "search", "edit", "execute", "github/*", "playwright/*"]
user-invocable: true
disable-model-invocation: true
metadata:
  project: schema.osm.dev
  domain: Organisation Service Management schema-as-code
  owner: OrganisationServiceManagement
---

You are the implementation agent for `schema.osm.dev`.

Your task is to implement, document, validate, test, and containerise the schema.osm.dev repository.

## Operating principles

- The repository `README.md` is the primary source of truth.
- Do not invent schema semantics.
- Preserve existing schema IDs, naming conventions, and compatibility unless the README or existing tests require a change.
- Prefer small, reviewable changes.
- Keep the website static-export compatible.
- Keep runtime containers minimal.
- Do not commit secrets.
- Do not add telemetry or analytics.
- Do not use external APIs for normal website operation.
- Document every assumption.
- Run all relevant checks before finalising the PR.
- Update documentation whenever implementation behaviour changes.

## Source-of-truth priority

Use this priority order:

1. The repository `README.md`.
2. Existing schema files.
3. Existing examples, tests, and docs.
4. Existing package/build/deployment conventions.
5. Existing repository metadata and license.
6. The GitHub issue or task that invoked you.
7. Minimal new conventions required to make the project coherent, buildable, testable, and maintainable.

If anything conflicts with `README.md`, the README wins.

If the README is silent, prefer the least surprising implementation and document the assumption in:

```text
docs/implementation-notes.md
````

## Required outcome

Implement a production-ready repository that provides:

* Machine-readable OSM schema files.
* Valid and invalid examples.
* Schema validation tests.
* An interactive static website for navigating and understanding schema.osm.dev.
* A Docker image that serves the website.
* CI checks for schemas, website, tests, and Docker image.
* Repository-level Copilot instructions.
* Documentation for schema authors, website maintainers, test runners, and Docker users.

## Website requirements

The website must:

* Reflect the repository README.
* Be statically buildable.
* Let users navigate schema objects/entities.
* Provide search/filter.
* Show schema title, description, required fields, optional fields, properties, references, examples, and raw JSON.
* Provide a relationship or reference graph/browser.
* Provide example documents and validation status.
* Provide a local, client-side JSON validation playground if practical.
* Use OSM-style branding consistent with [https://osm.dev](https://osm.dev).
* Avoid hotlinking external assets.
* Avoid external APIs for normal operation.
* Work on desktop, tablet, and mobile.
* Support keyboard navigation and accessible contrast.

## Docker requirements

Add a Dockerfile and `.dockerignore`.

The Docker image must:

* Use a multi-stage build.
* Build the static website.
* Serve only built static assets at runtime.
* Listen on port `8080`.
* Include OCI labels.
* Exclude source files, package manager caches, and build tools from the runtime image.
* Be testable with curl against `/`.

## Testing requirements

Add or update automated tests so that:

* Every schema parses.
* Every schema validates as JSON Schema unless the README specifies a different schema language.
* Every `$id` is unique.
* Every `$ref` resolves.
* Every valid example validates against its declared schema.
* Invalid examples fail where provided.
* The website builds.
* Core website pages/components render.
* Search/filter works.
* Raw JSON view renders valid JSON.
* Internal links do not 404.
* Docker image builds and serves the site.

## Commands

Before finalising the PR, run the repository-equivalent of:

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run test:schema
npm run test:site
npm run build
docker build -t schema-osm-dev:local .
docker run --rm -d --name schema-osm-dev-test -p 8080:8080 schema-osm-dev:local
curl -fsS http://localhost:8080/
docker stop schema-osm-dev-test
```

If the repository uses a different package manager or tooling, adapt the commands and document the actual commands in the PR body.

## Pull request requirements

The PR body must include:

* README interpretation summary.
* Implementation summary.
* Schema changes.
* Website changes.
* Docker changes.
* CI/workflow changes.
* Tests run.
* Assumptions.
* Follow-up recommendations.

Do not claim standards coverage unless the repository data supports it.

Do not commit secrets.

Do not add analytics or telemetry.

Do not add a backend unless the README or existing architecture requires it.

````

---

## `.github/copilot-instructions.md`

Create or update this file.

```markdown
# Copilot instructions for schema.osm.dev

## Repository purpose

This repository defines and publishes `schema.osm.dev`, the machine-readable schema layer for Organisation Service Management.

The repository should support:

- schema-as-code
- configuration-as-code
- typed organisational entities and relationships
- validation
- traceability
- auditability
- interactive schema documentation
- Docker-based static website serving
- automated quality gates

## Source of truth

Use the following priority order:

1. `README.md`
2. Existing schema files
3. Existing examples/tests/docs
4. Existing package/build conventions
5. Issue/task instructions
6. Minimal new conventions required for maintainability

If anything conflicts with `README.md`, follow the README.

Do not invent domain semantics. Document assumptions in `docs/implementation-notes.md`.

## Schema rules

- Prefer JSON Schema unless the README specifies another format.
- Every schema should include stable metadata such as `$id`, `$schema`, `title`, and `description`.
- Preserve existing IDs and compatibility unless a deliberate migration is documented.
- Ensure examples validate against schemas.
- Ensure `$ref` values resolve.
- Keep naming consistent and predictable.
- Do not claim standards mappings unless backed by repository data.

## Website rules

- The website must be static-export compatible.
- No backend should be required for normal use.
- No external API should be required for schema browsing or validation.
- Client-side validation must not send user data externally.
- Styling should be consistent with `osm.dev`.
- Do not hotlink external brand assets.
- Keep the site accessible and keyboard navigable.

## Docker rules

- Use a multi-stage build.
- Runtime image should serve only static assets.
- Runtime image should not include source, package manager cache, or build tooling.
- Serve on port `8080` unless existing repo conventions say otherwise.
- Include `.dockerignore`.

## Quality gates

Before finalising any PR, run the repository-equivalent of:

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run test:schema
npm run test:site
npm run build
docker build -t schema-osm-dev:local .
docker run --rm -d --name schema-osm-dev-test -p 8080:8080 schema-osm-dev:local
curl -fsS http://localhost:8080/
docker stop schema-osm-dev-test
````

If commands differ, update README and document the actual commands in the PR body.

````

---

## Optional path-specific instruction files

### `.github/instructions/schema.instructions.md`

```markdown
---
applyTo: "schemas/**/*.json, schema/**/*.json, examples/**/*.json, src/schema/**/*"
---

# Schema authoring instructions

- Treat README.md as source of truth.
- Prefer JSON Schema unless README specifies another schema format.
- Do not invent OSM domain entities or relationships.
- Preserve existing `$id` values unless a migration is intentional and documented.
- Every schema must have:
  - `$id`
  - `$schema`
  - `title`
  - `description`
  - `type`
  - `properties`
  - `required` where applicable
  - `additionalProperties` decision
- Every `$ref` must resolve.
- Every schema must have at least one valid example if practical.
- Invalid examples should exist for important constraints.
- Standards coverage or mappings must be data-backed.
````

### `.github/instructions/frontend.instructions.md`

```markdown
---
applyTo: "src/site/**/*, src/frontend/**/*, public/**/*, index.html, vite.config.*, tsconfig*.json"
---

# Frontend instructions

- Build a static website.
- Do not add a backend unless README requires it.
- Do not require external APIs for schema navigation or validation.
- Use accessible semantic HTML.
- Support keyboard navigation.
- Use responsive layouts.
- Style consistently with osm.dev.
- Avoid hotlinked assets.
- Use generated schema indexes rather than manually duplicating schema data where practical.
- Keep dependencies minimal and justified.
```

### `.github/instructions/docker.instructions.md`

```markdown
---
applyTo: "Dockerfile, .dockerignore, compose.yaml, docker-compose.yml, nginx.conf, caddyfile, docs/docker.md"
---

# Docker instructions

- Use a multi-stage build.
- Build static website assets in the build stage.
- Serve only static output in the runtime stage.
- Runtime image should not contain source files, node_modules, package manager cache, tests, or build tooling.
- Serve on port 8080 unless repository conventions require otherwise.
- Include OCI labels.
- Include a `.dockerignore`.
- Add a Docker smoke test.
- Document build, run, and curl test commands.
```

### `.github/instructions/docs.instructions.md`

```markdown
---
applyTo: "README.md, docs/**/*.md, AGENTS.md, .github/**/*.md"
---

# Documentation instructions

- Do not destroy existing README structure unnecessarily.
- README must explain what schema.osm.dev is, how schemas are organised, how to validate, how to run the website, how to build Docker image, and how to run tests.
- Document assumptions in docs/implementation-notes.md.
- Keep docs accurate with implementation.
- Do not claim standard/framework coverage unless backed by repo data.
```

### `.github/instructions/github-actions.instructions.md`

```markdown
---
applyTo: ".github/workflows/**/*.yml, .github/workflows/**/*.yaml"
---

# GitHub Actions instructions

- CI must run on pull requests and pushes to the default branch.
- CI must cover install, lint, typecheck, tests, schema validation, site build, and Docker build/run smoke test.
- Avoid requiring secrets for normal CI.
- Use dependency caching where appropriate.
- Prefer pinned major versions for standard GitHub Actions.
- Keep workflows readable and maintainable.
```

---

# Part B — Repository implementation

## Preferred repository structure

Adapt to the existing repository conventions, but aim for a structure close to:

```text
.
├── README.md
├── AGENTS.md
├── package.json
├── package-lock.json
├── Dockerfile
├── .dockerignore
├── compose.yaml
├── docs/
│   ├── schema-authoring.md
│   ├── website.md
│   ├── docker.md
│   ├── testing.md
│   └── implementation-notes.md
├── schemas/
│   ├── index.json
│   └── *.schema.json
├── examples/
│   ├── valid/
│   └── invalid/
├── src/
│   ├── site/
│   ├── schema/
│   └── tests/
├── public/
│   ├── assets/
│   └── schema/
├── scripts/
│   ├── generate-schema-index.*
│   ├── validate-schemas.*
│   └── docker-smoke-test.*
├── .github/
│   ├── copilot-instructions.md
│   ├── agents/
│   │   └── schema-osm-dev-implementer.agent.md
│   ├── instructions/
│   │   ├── schema.instructions.md
│   │   ├── frontend.instructions.md
│   │   ├── docker.instructions.md
│   │   ├── docs.instructions.md
│   │   └── github-actions.instructions.md
│   └── workflows/
│       └── ci.yml
└── tests/
    ├── schema/
    ├── site/
    └── docker/
```

Do not force this structure if the repository already has a clearer established structure.

---

## Schema implementation requirements

Implement or normalise schema files so the repository has a clear, machine-readable schema model.

Requirements:

* Use the existing schema location if one exists.
* Otherwise use `schemas/`.
* Use JSON Schema unless README specifies another format.
* Each schema object must include, where applicable:

  * `$id`
  * `$schema`
  * `title`
  * `description`
  * `type`
  * `properties`
  * `required`
  * `additionalProperties`
  * `examples` or links to examples
* Use stable, dereferenceable IDs under the `schema.osm.dev` namespace, for example:

  * `https://schema.osm.dev/schemas/<name>.schema.json`
  * `https://schema.osm.dev/entities/<name>`
* Preserve README terminology exactly where it defines canonical names.
* Add validation for all schemas.
* Add sample instance documents for major schema types.
* Add tests proving examples validate against their schemas.
* Add tests proving important invalid examples fail validation.
* Keep schema descriptions readable and useful in the website.
* Add relationship metadata only where backed by schema references or README-supported relationships.

Do not invent domain entities that are not supported by README or existing schema direction.

If starter examples are needed, derive them from the README and mark them clearly as examples.

---

## Expected schema object quality

Where applicable, schema files should support automated documentation.

Recommended pattern:

```json
{
  "$id": "https://schema.osm.dev/schemas/example.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Example",
  "description": "Short human-readable description sourced from README or existing repo terminology.",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "type", "name"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Stable identifier for the object."
    },
    "type": {
      "const": "Example"
    },
    "name": {
      "type": "string"
    }
  }
}
```

Use the repository’s existing schema style if it already has one.

---

## Schema index generation

Implement a build-time schema index generator if needed.

The website should not manually duplicate schema metadata. Prefer generating a static index from schema files.

Suggested output:

```text
public/schema-index.json
public/schemas/*.json
```

Suggested schema index shape:

```json
{
  "generatedAt": "2026-06-10T00:00:00.000Z",
  "schemas": [
    {
      "id": "https://schema.osm.dev/schemas/example.schema.json",
      "name": "example",
      "title": "Example",
      "description": "Short description",
      "path": "/schemas/example.schema.json",
      "type": "object",
      "references": [],
      "examples": [
        {
          "name": "valid-example",
          "path": "/examples/valid/example.json",
          "valid": true
        }
      ]
    }
  ]
}
```

The exact shape may vary, but it must support:

* schema explorer
* search
* relationship/reference view
* examples page
* validation playground

---

# Part C — Interactive website

## Website technology

Use the existing frontend stack if present.

If no frontend exists, use one of:

1. Vite + React + TypeScript
2. Astro + TypeScript
3. Plain TypeScript static site if simpler

Preference: Vite + React + TypeScript for interactive schema exploration.

The output must be static assets that can be served by NGINX, Caddy, or any static file server.

No backend is required.

---

## Required website pages and features

### 1. Home page

The home page must:

* Explain what `schema.osm.dev` is.
* Use README wording for the canonical description.
* Use OSM-style positioning:

  * Open Standards
  * Open Source
  * Schema-as-code
  * Configuration-as-code
  * Vendor independence
  * Standards-aligned organisational management
  * Automation-first
  * Traceable
  * Auditable
  * Safe for automation/AI
* Include clear calls to action:

  * Explore schema
  * View examples
  * Validate JSON
  * Read docs
  * View GitHub repository

Suggested hero language, adapt to README:

```text
schema.osm.dev

Machine-readable organisational management schemas for Organisation Service Management.

Explore typed entities, relationships, examples, validation rules, and standards-aligned schema-as-code for governance, risk, compliance, IT operations, vendor management, and business continuity.
```

Do not claim capabilities not present in the repository.

---

### 2. Schema explorer

Build an interactive schema browser.

Required:

* Sidebar tree of schema objects/entities.
* Search/filter.
* Grouping by schema category/module if data supports it.
* Schema detail panel showing:

  * title
  * description
  * `$id`
  * schema draft/version
  * type
  * required fields
  * optional fields
  * properties
  * nested objects
  * enums/constants
  * references/relationships
  * examples
  * raw JSON view
* Deep links for each schema.
* Copy buttons for:

  * schema `$id`
  * field paths
  * example snippets
  * raw schema JSON
* Visual indication of required vs optional fields.
* Links between referenced schema objects.
* Graceful handling of schemas with missing optional metadata.

---

### 3. Relationship / graph view

Provide a navigable visual map of schema relationships.

Minimum viable version:

* Render nodes for schemas/entities.
* Render edges for `$ref` or explicit relationship fields.
* Clicking a node opens the schema detail page or panel.
* Include zoom/pan if practical.
* If a graph library is too heavy, implement a grouped relationship browser or SVG dependency map.

Acceptable implementation options:

* React Flow, if dependency weight is acceptable.
* D3, if already present.
* Custom SVG/HTML relationship browser.
* Mermaid-generated diagrams, if static output is enough.

Relationship semantics must be honest:

* `$ref` relationships may be labelled “schema reference”.
* Business/domain relationships may only be labelled that way if README or schema metadata supports it.

---

### 4. Examples page

Create an examples page that:

* Lists all example documents.
* Shows which schema each example validates against.
* Shows validation status.
* Provides copy JSON button.
* Provides raw JSON view.
* Links from examples to schema detail pages.
* Shows invalid examples separately if present.

Suggested grouping:

```text
Valid examples
Invalid examples
Examples by schema
Examples by module/category
```

---

### 5. Validate / playground page

Provide a client-side JSON validation page if feasible.

Minimum:

* Select a schema.
* Paste JSON.
* Validate with AJV or equivalent.
* Show validation success/failure.
* Show validation errors in readable form.
* Link errors to JSON paths where practical.
* Never send user data externally.
* Work offline once static assets are loaded.

If a validation playground is not feasible in the first PR, implement the page shell and document the missing capability as a follow-up. However, prefer implementing it.

---

### 6. Documentation pages

Provide website documentation pages generated from or aligned to repository docs:

* Overview
* Schema design principles
* Naming conventions
* Versioning
* How to add a schema
* How to add examples
* How to validate locally
* How to run the website locally
* How to build and run Docker image
* How to contribute

---

### 7. Standards / modules page

If the README supports these concepts, map schema concepts to OSM modules and standards.

Possible modules:

* GRCosm
* HRosm
* VLNosm
* CMosm
* BCMosm
* OSM Orchestrator

Possible standards:

* ISO/IEC 27001
* ISO/IEC 27002
* ISO 22301
* ACSC ISM
* ASD Essential Eight
* SOC 2
* NIST CSF

Important:

* Do not claim coverage unless repository data supports it.
* If README claims coverage, quote or paraphrase README accurately.
* If mappings are incomplete, label them as incomplete/in progress.
* If no mapping data exists, include a placeholder explaining that mappings can be added later.

---

## Branding and UI requirements

Style the website consistently with `osm.dev`.

Brand cues:

* Dark technical/product style.
* OSM logo if present in repo.
* “osm.dev · Open Standards” style header language.
* Clean navigation:

  * About
  * Schema
  * Examples
  * Validate
  * Standards
  * Open Source
  * GitHub
* Cards for schema entities/modules.
* Badges for:

  * Schema
  * Entity
  * Relationship
  * Reference
  * Example
  * Standard mapping
  * Required
  * Optional
  * Valid
  * Invalid
* Subtle gradients/borders if consistent with existing brand.
* Responsive desktop/tablet/mobile layouts.
* Accessible contrast.
* Keyboard navigation.
* Visible focus states.
* Semantic headings.
* No interaction requiring mouse only.

Do not hotlink OSM assets. Use repository-local assets only.

---

## Suggested frontend components

Implement components as appropriate:

```text
App
Layout
TopNav
Sidebar
SearchBox
SchemaTree
SchemaDetail
SchemaPropertyTable
SchemaRawJson
SchemaReferenceList
SchemaGraph
ExampleList
ExampleViewer
ValidationPlayground
CopyButton
Badge
MarkdownContent
NotFound
```

Keep components simple and testable.

---

# Part D — Docker image

## Docker requirements

Add:

```text
Dockerfile
.dockerignore
```

Optional:

```text
compose.yaml
nginx.conf
```

The Docker image must:

* Use a multi-stage build.
* Build the website in the build stage.
* Serve only built static assets at runtime.
* Listen on port `8080`.
* Include OCI labels.
* Avoid source files, tests, package manager caches, and build tooling in the runtime image.
* Support a simple HTTP smoke test against `/`.

Suggested runtime options:

* `nginxinc/nginx-unprivileged`
* `caddy`
* `busybox httpd`
* `node` only if a static server is already used and justified

Prefer a non-root runtime where practical.

---

## Suggested Dockerfile pattern

Adapt to package manager and build output.

```Dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM nginxinc/nginx-unprivileged:stable-alpine AS runtime

LABEL org.opencontainers.image.title="schema.osm.dev" \
      org.opencontainers.image.description="Interactive static website for Organisation Service Management schemas" \
      org.opencontainers.image.source="https://github.com/OrganisationServiceManagement/schema.osm.dev" \
      org.opencontainers.image.licenses="SEE LICENSE IN REPOSITORY"

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1
```

If using NGINX unprivileged, verify default listen port. Add `nginx.conf` if required to listen on `8080`.

---

## `.dockerignore`

Add at minimum:

```gitignore
.git
.github
node_modules
dist
build
coverage
.cache
.playwright
test-results
.env
.env.*
*.log
.DS_Store
Thumbs.db
.vscode
.idea
```

Do not exclude files required for build.

---

## Docker commands to document

```bash
docker build -t schema-osm-dev:local .
docker run --rm -p 8080:8080 schema-osm-dev:local
curl -fsS http://localhost:8080/
```

Optional compose:

```yaml
services:
  schema-osm-dev:
    build: .
    ports:
      - "8080:8080"
```

---

# Part E — Package scripts

If using Node/Vite, add or normalise scripts.

Use the repository’s existing package manager. If none exists, use `npm` and commit `package-lock.json`.

Suggested `package.json` scripts:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "npm run generate:schema-index && vite build",
    "preview": "vite preview --host 0.0.0.0 --port 8080",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:schema": "tsx scripts/validate-schemas.ts",
    "test:site": "playwright test",
    "test:docker": "bash scripts/docker-smoke-test.sh",
    "generate:schema-index": "tsx scripts/generate-schema-index.ts"
  }
}
```

Adjust for actual stack.

---

# Part F — Testing

## Schema tests

Add automated tests covering:

* Every schema JSON file parses.
* Every schema validates as a valid JSON Schema.
* Every `$id` is unique.
* Every `$id` uses expected namespace convention unless existing repo differs.
* Every `$ref` resolves.
* Every valid example validates against its declared schema.
* Every invalid example fails against its declared schema.
* Required fields are enforced.
* `additionalProperties` behaviour is intentional.
* Schema index generation succeeds.
* Schema index contains all schemas.

Use AJV or an equivalent JSON Schema validator if using JSON Schema.

Recommended test metadata for examples:

```json
{
  "$schema": "https://schema.osm.dev/schemas/example.schema.json",
  "schemaId": "https://schema.osm.dev/schemas/example.schema.json",
  "exampleName": "basic-valid-example"
}
```

If adding metadata inside examples is inappropriate, use sidecar files or filename conventions.

---

## Website tests

Add tests covering:

* Site builds successfully.
* Home page renders.
* Schema explorer renders.
* Search/filter works.
* At least one schema detail view renders.
* Required/optional fields render.
* Raw JSON view renders valid JSON.
* Example page renders validation status.
* Validation playground returns success for valid JSON.
* Validation playground returns readable errors for invalid JSON.
* Internal links do not 404.
* Basic accessibility checks pass.

Use Playwright for browser tests if practical.

If Playwright is too heavy for the first PR, use Vitest + Testing Library and a static link checker, but prefer Playwright because the custom agent profile enables `playwright/*`.

---

## Docker tests

Add a Docker smoke test that:

1. Builds the image.
2. Starts a container.
3. Waits for HTTP availability.
4. Requests `/`.
5. Optionally requests one static asset.
6. Stops the container.
7. Fails cleanly on errors.

Suggested script:

```bash
#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:-schema-osm-dev:local}"
CONTAINER="${CONTAINER:-schema-osm-dev-test}"
PORT="${PORT:-8080}"

docker build -t "$IMAGE" .

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker run -d --name "$CONTAINER" -p "$PORT:8080" "$IMAGE"

for i in $(seq 1 30); do
  if curl -fsS "http://127.0.0.1:$PORT/" >/dev/null; then
    echo "Docker smoke test passed"
    exit 0
  fi
  sleep 1
done

docker logs "$CONTAINER"
echo "Docker smoke test failed"
exit 1
```

---

# Part G — CI/CD

Add or update GitHub Actions workflows.

Required checks:

* install dependencies
* lint
* typecheck
* unit tests
* schema validation
* schema index generation
* site build
* website smoke test
* Docker build
* Docker runtime smoke test

Suggested workflow:

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main
      - master

permissions:
  contents: read

jobs:
  validate:
    name: Validate, test, and build
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Setup Node
        uses: actions/setup-node@v5
        with:
          node-version: "22"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Typecheck
        run: npm run typecheck

      - name: Test
        run: npm test

      - name: Validate schemas
        run: npm run test:schema

      - name: Build site
        run: npm run build

      - name: Install Playwright browsers
        if: hashFiles('playwright.config.*') != ''
        run: npx playwright install --with-deps

      - name: Site tests
        if: hashFiles('playwright.config.*') != ''
        run: npm run test:site

  docker:
    name: Docker build and smoke test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v5

      - name: Build Docker image
        run: docker build -t schema-osm-dev:ci .

      - name: Run Docker smoke test
        run: |
          docker run -d --name schema-osm-dev-test -p 8080:8080 schema-osm-dev:ci
          for i in $(seq 1 30); do
            if curl -fsS http://127.0.0.1:8080/ >/dev/null; then
              docker stop schema-osm-dev-test
              exit 0
            fi
            sleep 1
          done
          docker logs schema-osm-dev-test
          docker stop schema-osm-dev-test || true
          exit 1
```

Adjust versions and conditions to match repository conventions.

Optional publishing:

* GitHub Pages for static website.
* GitHub Container Registry for Docker image.

Do not add publishing unless repository policy supports it.

Do not require secrets for normal CI.

---

# Part H — Documentation

## README.md

Update README without destroying useful existing structure.

README must include:

1. What `schema.osm.dev` is.
2. Repository status.
3. Schema organisation.
4. Website overview.
5. Local development.
6. Install dependencies.
7. Validate schemas.
8. Run tests.
9. Run interactive website locally.
10. Build website.
11. Build Docker image.
12. Run Docker image.
13. Add a new schema.
14. Add examples.
15. Contribution rules.
16. License.
17. Relationship to OSM and `osm.dev`.

Suggested README sections:

```markdown
# schema.osm.dev

## Overview

## Repository structure

## Schema model

## Interactive website

## Development

## Validate schemas

## Run tests

## Docker

## Adding schemas

## Adding examples

## Standards and OSM modules

## Contributing

## License
```

Do not claim standards coverage unless repository data supports it.

---

## `docs/schema-authoring.md`

Include:

* Schema format.
* Naming conventions.
* File naming conventions.
* `$id` conventions.
* `$schema` conventions.
* Required metadata.
* `$ref` conventions.
* Example conventions.
* Validation requirements.
* Backward compatibility expectations.
* Versioning expectations.
* Deprecation guidance.
* How to add a new schema.
* How to add valid and invalid examples.

---

## `docs/website.md`

Include:

* Website architecture.
* Frontend stack.
* Static build model.
* Schema index generation.
* Schema explorer data flow.
* Relationship graph generation.
* Validation playground design.
* Styling/branding notes.
* How to add pages.
* How to run locally.
* How to troubleshoot common failures.

---

## `docs/docker.md`

Include:

* Docker image purpose.
* Build command.
* Run command.
* Port.
* Health check.
* Runtime server.
* Multi-stage build explanation.
* `.dockerignore` explanation.
* Smoke test.
* Troubleshooting.

---

## `docs/testing.md`

Include:

* Test types.
* Schema validation tests.
* Website unit/component tests.
* Playwright/e2e tests.
* Docker smoke tests.
* CI jobs.
* How to run tests locally.
* How to update snapshots if snapshots are used.

---

## `docs/implementation-notes.md`

Include:

* Assumptions made.
* README ambiguities.
* Deferred decisions.
* Known limitations.
* Follow-up recommendations.

---

# Part I — Website content guardrails

The website may use OSM-style language but must remain accurate to repository data.

Allowed broad positioning if aligned with README:

* OSM provides schema-as-code for organisational management.
* OSM supports typed entities and relationships.
* OSM supports validation and auditability.
* OSM is intended to align governance, risk, compliance, IT operations, vendor management, and business continuity.

Only claim specific standard/module coverage if backed by repository data or README:

* ISO/IEC 27001
* ISO/IEC 27002
* ISO 22301
* ACSC ISM
* ASD Essential Eight
* SOC 2
* NIST CSF
* auDA policy

If coverage is incomplete or unclear, label it:

```text
Mapping available where schema data exists.
```

or:

```text
Planned / in progress.
```

---

# Part J — Security and privacy requirements

* No secrets committed.
* No tokens in examples.
* No analytics.
* No telemetry.
* No external validation API.
* No external font or script dependency unless already used and justified.
* No dynamic backend required.
* Validation playground must run locally in browser.
* Docker image must not include `.git`, source files, tests, local env files, or package caches at runtime.
* Do not expose unnecessary ports.
* Avoid privileged containers.
* Prefer non-root static server image where practical.

---

# Part K — Accessibility requirements

Minimum:

* Semantic HTML landmarks.
* One `h1` per page.
* Logical heading order.
* Keyboard navigable menus, search, tabs, copy buttons, and graph/list controls.
* Visible focus styles.
* Sufficient colour contrast.
* Text alternatives for images/logos.
* Buttons must have accessible names.
* Copy buttons must announce success visually and/or via accessible text.
* Form fields must have labels.
* Error messages must be linked to validation inputs where practical.

---

# Part L — Performance requirements

* Website should load quickly as a static site.
* Avoid large dependencies unless justified.
* Lazy-load heavy graph components if used.
* Avoid bundling duplicate schema data.
* Prefer generated compact schema index plus on-demand loading of full schema JSON.
* Search should work client-side for expected schema size.
* Static assets should be cacheable.

---

# Part M — Acceptance criteria

## Functional

* [ ] `README.md` remains accurate and is reflected in implementation.
* [ ] Schema files are discoverable and validated.
* [ ] Examples validate against schemas.
* [ ] Invalid examples fail where provided.
* [ ] Generated schema index includes all schemas.
* [ ] Interactive website builds as static assets.
* [ ] Website lets users navigate schemas.
* [ ] Website lets users search/filter schema items.
* [ ] Website shows schema details, properties, required fields, optional fields, references, examples, and raw JSON.
* [ ] Website includes relationship/graph view or clear relationship browser.
* [ ] Website includes example browser.
* [ ] Website includes local validation playground if feasible.
* [ ] Website styling is consistent with `osm.dev` branding and language.
* [ ] Docker image builds.
* [ ] Docker image serves site on port `8080`.
* [ ] Docker container passes curl smoke test.

## Copilot / agent configuration

* [ ] `.github/copilot-instructions.md` exists.
* [ ] `.github/agents/schema-osm-dev-implementer.agent.md` exists.
* [ ] Agent profile has YAML frontmatter.
* [ ] Agent profile has required `description`.
* [ ] Agent profile has `target: github-copilot`.
* [ ] Agent profile has appropriate `tools`.
* [ ] Optional path-specific instructions are added if useful.
* [ ] Instructions tell agents not to invent schema semantics.
* [ ] Instructions tell agents to treat README as source of truth.

## Quality

* [ ] Tests cover schema validation.
* [ ] Tests cover website build and core UI behaviour.
* [ ] Tests cover Docker build/run smoke test.
* [ ] CI runs all relevant checks.
* [ ] No hardcoded claims of standards coverage unless backed by repo data.
* [ ] No external API dependency for schema navigation or validation.
* [ ] No hotlinked brand assets.
* [ ] Dependencies are minimal and justified.
* [ ] Generated files are either excluded or clearly documented.
* [ ] Code is typed where TypeScript is used.
* [ ] Linting passes.
* [ ] Typechecking passes.

## Documentation

* [ ] README includes install/build/test/Docker usage.
* [ ] Schema authoring guide exists.
* [ ] Website architecture guide exists.
* [ ] Docker guide exists.
* [ ] Testing guide exists.
* [ ] Implementation notes exist.
* [ ] PR explains assumptions.

## Security / maintainability

* [ ] Runtime container contains only static output and static server.
* [ ] `.dockerignore` excludes unnecessary files.
* [ ] No secrets are committed.
* [ ] No analytics or telemetry added.
* [ ] No unnecessary backend service added.
* [ ] PR body explains validation performed.
* [ ] CI can run without secrets.

---

# Part N — Commands to run before finalising PR

Run the repository-equivalent of:

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run test:schema
npm run test:site
npm run build
docker build -t schema-osm-dev:local .
docker run --rm -d --name schema-osm-dev-test -p 8080:8080 schema-osm-dev:local
curl -fsS http://localhost:8080/
docker stop schema-osm-dev-test
```

If commands differ because the repo uses a different stack, document the actual commands in the PR body and update README.

---

# Part O — PR body requirements

The pull request must include:

```markdown
## README interpretation

Summarise what README says schema.osm.dev is, what the schema model is, and any implementation constraints derived from it.

## What changed

Summarise implementation changes.

## Schema

Summarise schema files, examples, validation, and index generation.

## Website

Summarise interactive website features, pages, navigation, search, schema detail views, examples, graph/reference browser, and validation playground.

## Docker

Summarise Dockerfile, runtime image, port, health check, and smoke test.

## Copilot / custom agent configuration

Summarise `.github/copilot-instructions.md`, `.github/agents/schema-osm-dev-implementer.agent.md`, and any path-specific instructions.

## CI

Summarise workflow checks.

## Tests run

- [ ] npm ci
- [ ] npm run lint
- [ ] npm run typecheck
- [ ] npm test
- [ ] npm run test:schema
- [ ] npm run test:site
- [ ] npm run build
- [ ] docker build -t schema-osm-dev:local .
- [ ] docker run + curl smoke test

Include actual output summary or note if any command was unavailable.

## Assumptions

List assumptions and link to docs/implementation-notes.md.

## Follow-up

List sensible next steps that are not required for this PR.
```

---

# Part P — Non-goals

Do not:

* Replace the README’s domain model with a new one.
* Add unsupported OSM entities.
* Add a backend unless absolutely necessary.
* Add authentication.
* Add telemetry/analytics.
* Require external services for normal site use.
* Claim certification/compliance coverage not represented in repo data.
* Commit generated build output unless the repo already does this intentionally.
* Hotlink `osm.dev` assets.
* Store secrets or tokens.
* Introduce a large framework without clear benefit.
* Add AI-generated marketing claims that are not supported by README or schema data.
* Break existing schema IDs or examples without a documented migration.
