# UE2 Literature-Review GraphRAG — integration package

A knowledge-graph RAG service built over the UCLC1009 (University English II)
literature-review article corpus. It lets students and teachers ask questions
that span **many** articles ("which theories explain X?", "which articles share
a methodology?", "what are the critiques of Y?") and get an answer grounded in a
typed knowledge graph, with source citations and a highlighted subgraph.

Built and hosted in the **UE2 Course Materials Portal** Repl (`tesolchina/uclc1009`).
This folder is the drop-in package to surface it inside the **fiteagent** front-end.

## What it is

- **Corpus (validation phase):** 37 articles — the Human Intelligence starter
  sets (subtopics 01–07) + the 4 professional model systematic reviews.
  Scales to all 143 corpus PDFs by re-running the ingest script.
- **Graph:** ~491 entities (concept / theory / method / finding / technology /
  field) and ~521 typed relations (supports / critiques / applies / extends /
  measures / causes / contrasts_with / part_of / related_to). Each relation is
  grounded in one article with an evidence quote.
- **Pipeline:** `pdftotext` → LLM entity/relation extraction → Postgres. Entities
  are deduplicated by normalised name, so a concept shared across articles becomes
  one node with many edges — the cross-article connections students need for an LR.

## HTTP API

Base URL: the deployed UE2 portal origin (set `GRAPHRAG_BASE` in the FE).

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/graphrag/graph` | — | `{ articles, entities, relations }` (full graph for visualisation) |
| GET | `/api/graphrag/articles` | — | article metadata + summaries (no full text — copyright) |
| POST | `/api/graphrag/query` | `{ "question": string }` | `{ answer, subgraph:{entities,relations,articles}, matchedEntityIds }` |

`POST /api/graphrag/query` runs a two-step retrieval: (1) match the question to
graph entities, (2) answer from the 1-hop subgraph + the summaries of the source
articles. The tutor prompt is guard-railed to *explain connections, not write the
student's assignment*.

### Example

```bash
curl -X POST "$GRAPHRAG_BASE/api/graphrag/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Which theories explain the evolution of human intelligence?"}'
```

## Embedding in the fiteagent FE

Two options:

1. **iframe** the `/graphrag` route of the deployed UE2 portal (fastest).
2. **Native tool** — call the JSON API from a fiteagent tool/agent and render the
   `subgraph` with any force-graph component (the portal uses
   `react-force-graph-2d`). `GraphRagPanel.example.tsx` in this folder is a
   minimal reference component (chat + answer + source list).

CORS: the portal currently serves same-origin. If the FE is on a different
origin, add its origin to an allow-list on the `/api/graphrag/*` routes.

## Regenerating / scaling the graph

In the UE2 portal Repl:

```bash
# 1. extract text from the corpus PDFs (already-downloaded) → /tmp/ue2/pdftxt
pdftotext each.pdf each.txt
# 2. ingest (idempotent — skips articles already in the DB)
npx tsx script/graphrag-ingest.ts /tmp/ue2/pdftxt
```

Add more topics by extracting their PDFs into the same folder and re-running;
the classifier derives subtopic/group from the OneDrive path.
