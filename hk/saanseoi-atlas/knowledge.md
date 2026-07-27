# Knowledge: the SaanSeoi Atlas module

Digest of the open-source repositories `saanseoi/saanseoi` and `tijptjik/hype` (studied 27 Jul 2026). Everything an agent needs to teach with this module truthfully.

## 1. The two projects

- **SaanSeoi (山水)** — "A Digital Commons for Hong Kong". A Bun/Turborepo monorepo of Cloudflare Workers apps. The core module is **atlas-api**: a public REST API (built with Hono + zod-openapi, data in Cloudflare D1/SQLite) serving Hong Kong **places** and **divisions** from versioned data snapshots (sources include Overture Maps, HK Gov ALS addresses, HK Post). Public site: saanseoi.hk.
- **HYPE** — "Journey through Hong Kong". A SvelteKit + Drizzle + Cloudflare app by the same community: hubs → projects → map layers → properties, with a capability/role system for community contribution. Think of HYPE as the *experience* layer and SaanSeoi as the *data commons* layer.
- Both are early-stage; the authors say contributor documentation is still thin. Contribution today = read the code, open issues, follow CONTRIBUTING.md conventions (commitizen commits, changesets, biome lint, tests required on PR).

## 2. The division taxonomy (the heart of the Atlas)

Seven levels; every division has exactly one level:

| Level | Name | Example |
|---|---|---|
| 0 | SAR | Hong Kong SAR |
| 1 | Area / City | Kowloon, Hong Kong Island, New Territories |
| 2 | District | Yau Tsim Mong |
| 3 | Town | Tuen Mun, Tai Po |
| 4 | Macrohood | Mong Kok, Shek Mun |
| 5 | Neighbourhood / Village | Prince Edward |
| 6 | Microhood / Hamlet | 30 Houses |

Rules that make the data computable:
- A division never contains another division of the same level.
- Every division at level 3 or below sits within **at least one district (level 2)**.
- Every district has exactly one Area; every Area has exactly one SAR.
- Levels 1 and below District are optional in a chain (a neighbourhood may hang directly under a district).
- Worked example: Prince Edward (5) → Mong Kok (4) → Yau Tsim Mong (2) → Kowloon (1) → Hong Kong SAR (0).

Data is mapped in from Overture Maps place types (e.g. Overture `neighborhood` → level 5, `macrohood` → level 4, `dependency` → level 0).

## 3. The API surface (v0)

Base pattern: `/v0/{region}/…` where region is `hk`. Real routes in the code:

- `GET /v0/{region}/places/{id}` — one place. 200 = place, 404 = not found, 503 = snapshot not ready, 422 = invalid input.
- `GET /v0/{region}/places/by-cell/{h3Level}/{h3Cell}` — places inside an H3 hexagonal map cell (H3 is Uber's hexagon grid system for indexing locations).
- `GET /v0/{region}/search?q=…` — full-text search over places. Can return 503 either because no snapshot is published or search indexing isn't ready.
- Divisions and meta routes expose the taxonomy and the currently active data snapshot.
- The whole API is described by an **OpenAPI specification** generated from zod schemas — the response shapes are the same contracts the server itself validates against.

Key concepts to teach accurately:
- **Snapshots:** the API serves from published, versioned data snapshots — a 503 "snapshot_not_ready" is a documented temporary state, not a crash.
- **Authentication:** the public deployment (api.saanseoi.hk) currently returns 401 `invalid_api_key` without a key — open *source and licence* does not automatically mean *unmetered public endpoint*. Anyone can, however, run the API themselves from the open repo.
- **Versioning:** `/v0` in the path means "contract may still change"; when it stabilises there will be a `/v1`.

## 4. The AI + open-module pattern (why this pack exists)

This pack is an experiment: take a module someone else built (the Atlas), and wrap it in a Learn → Act experience.

- **Part A (learn.json):** scenarios teach the concepts — commons, taxonomy, API, OpenAPI, grounding.
- **Part B (this agent):** practises the skills conversationally. The agent does not call the API live (no key is shipped); it teaches the learner to *read and write* the API's language, and to design agents that would call it.
- The generalisable pattern: **AI supplies language + reasoning; the open module supplies current, verifiable facts.** Answers grounded in a commons are checkable and improve automatically as the commons improves. This is the same pattern behind connecting any agent to any well-documented open API.

## 5. Honest limits

- The agent has no live Atlas connection: never fabricate place records, IDs, or counts. Show the URL the learner *would* call instead.
- Boundaries in the taxonomy follow the Atlas's editorial choices; real-world usage of names like "Prince Edward" is looser, and that tension is a teaching point, not an error.
