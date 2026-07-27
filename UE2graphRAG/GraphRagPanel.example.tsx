/**
 * Reference component for embedding the UE2 GraphRAG into the fiteagent FE.
 * Minimal, dependency-light: chat box → grounded answer → source list.
 * For the full graph visualisation, render the returned `subgraph` with
 * react-force-graph-2d (see the UE2 portal's client/src/pages/graphrag.tsx).
 *
 * Set GRAPHRAG_BASE to the deployed UE2 portal origin.
 */
import { useState } from "react";

const GRAPHRAG_BASE = import.meta.env.VITE_GRAPHRAG_BASE ?? "";

interface Article { id: number; title: string; authors: string | null; year: number | null; }
interface QueryResult {
  answer: string;
  subgraph: { articles: Article[] };
}

export function GraphRagPanel() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function ask() {
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${GRAPHRAG_BASE}/api/graphrag/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "query failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 640 }}>
      <textarea
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Ask about the literature-review articles…"
        rows={3}
        style={{ width: "100%" }}
      />
      <button onClick={ask} disabled={loading || !q.trim()}>
        {loading ? "Searching…" : "Ask the knowledge graph"}
      </button>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {result && (
        <div>
          <p style={{ whiteSpace: "pre-wrap" }}>{result.answer}</p>
          <h4>Sources</h4>
          <ul>
            {result.subgraph.articles.map((a) => (
              <li key={a.id}>
                {a.authors || "Unknown"}{a.year ? ` (${a.year})` : ""} — {a.title}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
