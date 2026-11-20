<div align="center">
  <a href="https://www.chess.com/member/sahill17">
    <img src="assets/chess-hero.svg" alt="Sahil Pal — Chess Telemetry & Systems Engineering" width="100%" />
  </a>
</div>

<br/>

### ♟️ The Starting Four

Every system here is built with the same discipline as a classical chess game: calculate deep, eliminate wasted moves, verify invariants, and never pay for cloud bloat when a tight local data structure solves the problem faster.

---

#### ♔ King — [Synapse](https://github.com/saahilpal/synapse) *(My Favorite Build)*
> **Git-aware AST code-graph engine & Model Context Protocol (MCP) server for AI coding agents.**

* **Tree-sitter AST Parsing:** Indexes symbols, call graphs, and definitions, achieving **85.2% token context reduction** compared to raw file dumps into agent prompts.
* **SQLite WAL + FTS5:** Sub-token full-text code search operating at **2.1 ms P95 latency**.
* **Blast-Radius Centrality:** Recursive CTE graph traversal (**0.8 ms P95**) combined with Personalized PageRank to rank impacted files and functions before an agent writes a single diff.
* **Zero Cloud Footprint:** Runs 100% locally on device with zero API keys or third-party telemetry.

---

#### ♕ Queen — [PropEval](https://github.com/saahilpal/propeval) · [*Laya Training*](https://github.com/saahilpal/propeval-laya-training)
> **Production Hinglish voice AI eval & regression workbench for Indian real estate sales agents.**

* **Dual-Engine Cascade:** Sub-millisecond fine-tuned Laya System-1 classifier (**<0.4 ms CPU SLA**, 92.1% resolution rate, $\kappa = 0.9912$) resolving routine turns before escalating to an LLM System-2 judge.
* **PostgreSQL 17 Queue:** High-throughput `SKIP LOCKED` worker coordination with transactional turn commits and strict budget reservation fencing.
* **Paired Statistical Rigor:** Layered hypothesis testing with McNemar + Newcombe Method 10 ($K=1$), and Wilcoxon signed-rank + 10,000-sample Two-Stage Cluster Bias-Corrected & Accelerated Bootstrap ($K>1$).
* **158 Tests Passing:** Comprehensive test suite covering deterministic FSM buyer simulation, 8 kHz telephony ASR confusion matrices, and budget normalizers.

---

#### ♖ Rook — [Disha AI](https://github.com/saahilpal/disha-ai)
> **Chronic condition lifestyle health coach for hypertension & diabetes grounded in ICMR & NIN guidelines.**

* **Full-Duplex Audio:** WebSocket streaming audio with client-side Voice Activity Detection (VAD) for natural turn-taking.
* **RRF Hybrid Search:** Reciprocal Rank Fusion combining PostgreSQL `tsvector` full-text search and `pg_trgm` trigram fuzzy matching across clinical meal and biomarker databases.
* **Deterministic Emergency Breaker:** Sub-millisecond Aho-Corasick pattern matcher detecting clinical red flags (hypertensive crisis, severe angina) to bypass LLM generation and trigger immediate emergency escalation.
* **Production Deployment:** Containerized FastAPI backend with Alpine NGINX reverse proxy.

---

#### ♘ Knight — [RAG-DOCAnalyzer](https://github.com/saahilpal/RAG-DOCAnalyzer)
> **Full-stack technical document analysis platform with vector semantic retrieval.**

* **pgvector HNSW Search:** Cosine similarity retrieval (`vector_cosine_ops`) paired with an automatic fallback circuit to PostgreSQL full-text search when embedding models degrade.
* **Deduplicated Ingestion:** Asynchronous database-driven worker queue for PDF processing with SHA-256 hash deduplication and page-level chunking.
* **Streaming Architecture:** Real-time Server-Sent Events (SSE) streaming responses from Next.js 16 frontend through Express 5 API.

---

### ⚙️ Systems & Core Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Languages** | Python, TypeScript, SQL (PostgreSQL, SQLite), JavaScript |
| **Systems & Backends** | FastAPI, Express 5, Next.js 16, Node.js, Alpine NGINX, Docker Compose |
| **Databases & Search** | PostgreSQL 17 (`pgvector`, `tsvector`, `pg_trgm`), SQLite (WAL, FTS5), Redis |
| **AI & Eval Engines** | Model Context Protocol (MCP), Tree-sitter AST, Paired Hypothesis Testing (McNemar, Wilcoxon, Bootstrap) |
| **Telemetry & Protocols** | WebSocket full-duplex, Server-Sent Events (SSE), OpenTelemetry / Jaeger |

---

### ♟️ Connect & Play

* **Chess.com:** [sahill17](https://www.chess.com/member/sahill17) *(Send a 3+0 or 5+0 challenge)*
* **GitHub:** [saahilpal](https://github.com/saahilpal)
* **Portfolio:** [sahil-pal-portfolio-d147.vercel.app](https://sahil-pal-portfolio-d147.vercel.app/)
* **Hugging Face:** [saahilpal17](https://huggingface.co/saahilpal17)
* **LinkedIn:** [sahiilpal](https://linkedin.com/in/sahiilpal)
* **Email:** [sahil.sp.sp.2003@gmail.com](mailto:sahil.sp.sp.2003@gmail.com)
