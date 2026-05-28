# Sahil Pal
![Sahil Pal DevOS Banner](banner.svg)

---

### [SYS_DIAGNOSTICS]
```
[DAEMON] Status: ACTIVE (Online since August 2024)
[ROLE] Software Engineer & Context Infrastructure Builder
[ACADEMIC] BCA Student @ Kristu Jayanti College, Bengaluru (2023 - 2026)
[FOCUS] Context Engineering & Systems Scaffolding
```

---

## ⚡ Flagship Engine: [Synapse](https://github.com/saahilpal/synapse)
**Git-aware persistent context injector for AI coding agents.**

Synapse is a local-first system daemon written in Python that mirrors Git state in real-time to inject exact, token-bounded codebase structural boundaries into LLM coding contexts.

[![PyPI version](https://img.shields.io/pypi/v/synap-git?color=3b82f6&style=flat-square)](https://pypi.org/project/synap-git/)
[![Python Version](https://img.shields.io/pypi/pyversions/synap-git?style=flat-square)](https://pypi.org/project/synap-git/)
[![CI Status](https://github.com/saahilpal/synapse/actions/workflows/ci.yml/badge.svg)](https://github.com/saahilpal/synapse/actions)

### Component Map
```
                          ┌────────────────────────┐
                          │     synap_git.cli      │
                          └───────────┬────────────┘
                                      │ (invokes)
                                      ▼
                          ┌────────────────────────┐
                          │  synap_git.indexer.    │
                          │        daemon          │
                          └─────┬────────────┬─────┘
          (starts watcher)      │            │      (hosts API server)
                 ┌──────────────┘            └──────────────┐
                 ▼                                          ▼
   ┌──────────────────────────┐               ┌──────────────────────────┐
   │   synap_git.git.state    │               │   synap_git.api.app      │
   └─────────────┬────────────┘               └─────────────┬────────────┘
                 │ (detects commits)                        │ (serves UI)
                 ▼                                          ▼
   ┌──────────────────────────┐               ┌──────────────────────────┐
   │   synap_git.indexer.     │               │   synap_git.api.static   │
   │         engine           │               └──────────────────────────┘
   └─────┬────────────┬───────┘
         │            │ (stores data)
         │            ▼
         │      ┌─────────────────────┐       ┌──────────────────────────┐
         │      │  synap_git.storage. │◀──────│    synap_git.mcp.server  │
         │      │       sqlite        │       └──────────────────────────┘
         │      └─────────────────────┘               (connects agent)
         │ (generates docs)
         ▼
   ┌──────────────────────────┐
   │    synap_git.indexer.    │
   │          wiki            │
   └──────────────────────────┘
```

### Core Architecture
* **L1 (Structural Graph):** Multi-threaded Tree-sitter parser that resolves imports and symbols into an SQLite dependency graph.
* **L2 (Semantic Wiki):** Asynchronous background worker that structures markdown summaries of files and modules.
* **L3 (Behavioral Memory):** Stored checkpoints, technical decisions, and failure lessons that persist through branch switches.
* **Tiktoken Context Packing:** High-performance tokenizer integration prioritizing local graph context within budget limits.
* **MCP Integration:** Serves code-graph context and memory states directly to coding agents via stdio.

---

## 🛠️ Production Systems

* **[RAG-DOCAnalyzer](https://github.com/saahilpal/RAG-DOCAnalyzer)**: Chat-first document Q&A workspace built with Next.js, Express, PostgreSQL (`pgvector`), and Google Gemini. Implements optimistic UI, SHA-256 PDF deduplication, Supabase Storage, and a database-backed worker queue (`FOR UPDATE SKIP LOCKED`) with fallback from vector search to lexical FTS.
* **[LeetSync](https://github.com/saahilpal/LeetSync)**: A Manifest V3 Chrome extension built with TypeScript and Vite. Captures LeetCode editor content and complexity analysis, organizing and syncing solutions directly into a GitHub directory structure via the Contents API.
* **[leetcode](https://github.com/saahilpal/leetcode)**: A dynamic C++ algorithmic library containing solutions to problem patterns.

---

## 📊 Developer Metrics
```
[STATISTICS]
-> Followers   : 2 (early stage)
-> Repositories : 20 Public
-> Achievements: Pull Shark (x2), YOLO
```

[![GitHub Stats](https://github-readme-stats.vercel.app/api?username=saahilpal&show_icons=true&theme=radical&hide_border=true)](https://github.com/saahilpal)

---

## 📡 Terminal Connect
* **Web Portfolio:** [sahil-pal-portfolio-d147.vercel.app](https://sahil-pal-portfolio-d147.vercel.app/)
* **LinkedIn:** [linkedin.com/in/sahiilpal](https://www.linkedin.com/in/sahiilpal)
* **PyPI Package:** [pypi.org/project/synap-git](https://pypi.org/project/synap-git/)
* **LeetCode:** [leetcode.com/u/saahilpal17](https://leetcode.com/u/saahilpal17/)
