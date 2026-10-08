# SustainMetric IDX — The Algorithmic Green Auditor Harness

An end-to-end audit harness and live dashboard built on top of **SustainMetric FastMCP** and **OJK TKBI 2024 (Versi 3)** sustainable finance criteria for Indonesia Stock Exchange (IDX) listed equities.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────┐
│                   FRONTEND (Svelte 5 + Vite + Tailwind)                │
│   • Theme: Modern ESG Dark Terminal (#090D16 + Emerald Accents)        │
│   • Live Emitent Dashboard & 2x2 Divergence Heatmap                    │
│   • Interactive TKBI Audit Spreadsheet (Template_Audit_TKBI.xlsx)      │
│   • OpenTelemetry Trace Waterfall DAG Viewer                           │
│   • Scheduled Background Cron Manager                                  │
│   • Global Slide-out AI Copilot Drawer (FastMCP Tool Integration)      │
└───────────────────────────────────▲────────────────────────────────────┘
                                    │ REST / SSE Streaming
┌───────────────────────────────────▼────────────────────────────────────┐
│                    BACKEND GATEWAY (Python FastAPI)                    │
│   • OpenTelemetry Tracer SDK & PostgreSQL Database Span Exporter       │
│   • Multi-Provider LLM Gateway (Gemini, OpenAI, Claude, Ollama)        │
│   • APScheduler Background Cron Runner                                 │
│   • 1-Click Stamped XLSX & Cryptographic SHA-256 Signed PDF Exporter   │
└──────────────▲──────────────────────────────────────────▲──────────────┘
               │ SQLAlchemy + asyncpg                     │ PyPI: sustainmetric-idx
┌──────────────▼─────────────┐             ┌──────────────▼──────────────┐
│  DATABASE (PostgreSQL)     │             │    SUSTAINMETRIC MCP CORE   │
│  • Container: Port 5432    │             │  • PyPI: sustainmetric-idx  │
│  • Alembic Migrations      │             │  • Sectors App API v2 Cache │
│  • audit_runs              │             │  • TKBI Vector Store Cosine │
│  • tkbi_audit_entries      │             │  • 4-Quadrant Scoring Math  │
│  • audit_traces (Otel)     │             │  • 8 TKBI Sectors Catalog   │
│  • scheduled_jobs          │             │  • Heuristic Greenwashing   │
│  • grandfathering & SDT    │             │    Risk Penalties           │
└────────────────────────────┘             └─────────────────────────────┘
```

---

## Core Capabilities

1. **Live Emitent Dashboard**:
   - Ticker selector (`PGEO`, `ADRO`, `BBRI`, `BREN`, `BUMI`, or custom IDX ticker).
   - Real-time **Consistency Score** (0–100) and **Viability Score** (0–100).
   - 4-Quadrant classification: `Q1: Transisi Tangguh`, `Q2: Dampak Spekulatif`, `Q3: Sumber Kas Konvensional`, `Q4: Tertinggal & Red Flag`.
   - Fundamental financial metrics (OCF, Capex, Capex Coverage Ratio, ROA, Net Debt).

2. **2×2 Divergence Heatmap (Greenwashing Radar)**:
   - Interactive scatter plot mapping Capex coverage against ESG claims.
   - Highlights Quadrant 2 divergence alerts ($\Delta\text{Claims} - \Delta\text{Capex}$).
   - Peer comparison dots with hover tooltips and 1-click ticker switching.

3. **TKBI Live Audit Sheet & Human-In-The-Loop (HITL)**:
   - Exactly matches the 12-column schema of [Template_Audit_TKBI.xlsx](file:///c:/Users/radyadhewa/Storage/code/personal/Hackathon-SectorsApp-SustainmetricsApp/Template_Audit_TKBI.xlsx).
   - Full search and sector filtering.
   - Inline feedback editing and override selection (`HIJAU`, `TRANSISI`, `TIDAK`).
   - **Export Stamped XLSX**: Generates updated Excel workbook reflecting auditor overrides.
   - **Signed Audit PDF**: Official audit document featuring an automated cryptographic SHA-256 audit stamp and verification watermark.

4. **Traceable Green Audit (OpenTelemetry Waterfall)**:
   - Complete trace visualization of the audit DAG:
     `audit.pipeline.{TICKER} → sectors.get_company_report → sectors.get_company_news → tkbi.vector_search → scoring_engine.evaluate → tkbi.populate_entries`.
   - Displays exact latency (ms), status, and attribute inspection (cache hit/miss, credit usage, matches).

5. **Built-in AI Copilot Chat Drawer**:
   - Slide-out streaming drawer accessible from anywhere in the application.
   - Multi-provider gateway: Gemini, OpenAI, or local Ollama.
   - Real-time function calling into FastMCP tools (`inspect_ticker_evidence`, `query_tkbi_knowledge_base`).
   - Intelligent offline fallback mode when no external API key is provided.

6. **Scheduled Background Cron Jobs**:
   - APScheduler engine orchestrating recurring portfolio audits.
   - Configurable alert score thresholds.

---

## Quickstart Guide

### 1. Start PostgreSQL (Docker)
```powershell
docker compose up -d
```

### 2. Run Database Migrations (Alembic)
```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

### 3. Run Backend Server (FastAPI + Embedded Frontend)
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open **`http://localhost:8000`** in your browser.

### 4. (Optional) Run Frontend in Vite Dev Mode
```powershell
cd frontend
npm run dev
```
Open **`http://localhost:5173`** (Vite proxies all `/api` requests to backend at port 8000).

---

## Automated Verification Tests
Run the test suite covering both end-to-end pipeline execution and REST endpoints:
```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\pytest.exe backend\tests\ -v
```
Result: **8 passed in ~2.9s**
- `test_audit_runner.py`: Verifies PGEO audit pipeline, 14 TKBI entries, and OpenTelemetry spans.
- `test_api_endpoints.py`: Verifies health check, trigger, HITL patch, Excel/PDF signed exports, schedules, and SSE chat.
- `test_tkbi_endpoints.py`: Verifies OJK TKBI taxonomy explorer, SDT UMKM decision trees, grandfathering scenarios, and portfolio aggregator.
