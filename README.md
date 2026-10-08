# SustainMetric IDX — The Algorithmic Green Auditor Harness

[![PyPI - Version](https://img.shields.io/pypi/v/sustainmetric-idx?color=047857&logo=pypi&logoColor=white&label=PyPI%20Package)](https://pypi.org/project/sustainmetric-idx/)
[![MCP Server Repo](https://img.shields.io/badge/MCP%20Server%20Repo-GitHub-181717?logo=github&label=Ecosystem)](https://github.com/personal-radyadhewa/Hackathon-2026-SectorsApp-SustainmetricsMCP)
[![Protocol](https://img.shields.io/badge/Model%20Context%20Protocol-MCP%20v1.3-blue)](https://modelcontextprotocol.io/)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)

> **More than an application:** SustainMetric IDX is a full-stack algorithmic audit harness built upon a standalone, independently published **Model Context Protocol (MCP)** server: [`sustainmetric-idx`](https://pypi.org/project/sustainmetric-idx/). The MCP server provides plug-and-play green finance telemetry and OJK TKBI evaluation tools for any MCP-compliant AI client (Cursor, Claude Desktop, Antigravity, VS Code, or custom autonomous agents).

- **MCP Package Deployment (PyPI)**: [https://pypi.org/project/sustainmetric-idx/](https://pypi.org/project/sustainmetric-idx/)
- **MCP Server Core Repository**: [https://github.com/personal-radyadhewa/Hackathon-2026-SectorsApp-SustainmetricsMCP](https://github.com/personal-radyadhewa/Hackathon-2026-SectorsApp-SustainmetricsMCP)
- **Regulatory Framework**: OJK Taksonomi Keuangan Berkelanjutan Indonesia (TKBI 2024 Versi 3) & Indonesia Stock Exchange (IDX) Equities.

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

## Model Context Protocol (MCP) Server Integration

This platform is powered by **`sustainmetric-idx`**, an open Model Context Protocol server published on **[PyPI](https://pypi.org/project/sustainmetric-idx/)** and maintained in **[Hackathon-2026-SectorsApp-SustainmetricsMCP](https://github.com/personal-radyadhewa/Hackathon-2026-SectorsApp-SustainmetricsMCP)**.

### Why MCP?
This project is engineered beyond a conventional web application: it decouples **algorithmic audit logic** into an independent, reusable protocol layer. By adopting the open [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), any MCP-compliant AI assistant or autonomous agent (Cursor, Claude Desktop, Antigravity, or custom agent swarms) can consume IDX green finance data and OJK TKBI auditing primitives directly as native tool calls.

### Package & Repository Links
- **PyPI Package**: [`sustainmetric-idx`](https://pypi.org/project/sustainmetric-idx/) (`pip install sustainmetric-idx`)
- **MCP Server Repository**: [`Hackathon-2026-SectorsApp-SustainmetricsMCP`](https://github.com/personal-radyadhewa/Hackathon-2026-SectorsApp-SustainmetricsMCP)
- **Protocol**: FastMCP over `stdio` and `sse` transports

### Standalone MCP Quickstart
You can run the MCP server standalone in your own development environment or AI client:

```powershell
# Direct execution via uvx
uvx sustainmetric-idx

# Or install via pip
pip install sustainmetric-idx
python -m sustainmetric.server
```

#### Claude Desktop / Cursor Client Config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "sustainmetric-idx": {
      "command": "uvx",
      "args": ["sustainmetric-idx"],
      "env": {
        "SECTORS_API_KEY": "<YOUR_SECTORS_APP_API_KEY>"
      }
    }
  }
}
```

### Core MCP Tools Exposed
| MCP Tool | Description |
| :--- | :--- |
| `audit_emiten_tkbi` | Evaluates IDX emiten against OJK TKBI 2024 criteria (Technical Screening Criteria, DNSH, RMT). |
| `inspect_ticker_evidence` | Retrieves audited financial filings, operating cash flows, and capex metrics via SectorsApp API v2. |
| `query_tkbi_knowledge_base` | Semantic vector search across 8 master sectors, KBLI codes, and Indonesian NDC 2030 targets. |
| `evaluate_divergence_quadrant` | Mathematical 4-quadrant scoring detecting greenwashing divergence ($\Delta\text{Claims} - \Delta\text{Capex}$). |

---

## Prerequisites

Before running the application, make sure the following tools are installed.

### Required

| Requirement    | Version               |
| -------------- | --------------------- |
| Docker Desktop | Latest stable version |
| Python         | 3.11+                 |
| Node.js        | LTS                   |
| npm            | Included with Node.js |
| Git            | Latest stable version |

You can check whether the required tools are available by running:

```powershell
docker --version
docker compose version
python --version
node --version
npm --version
git --version
npm list marked
```

Python virtual environment support is also required:

```powershell
python -m venv --help
```

If `npm list marked` shows `(empty)` or returns an error, install the missing package inside the `frontend` directory:

PowerShell

```powershell
cd frontend
npm install marked
```

If all commands above work and the versions meet the requirements, you can continue directly to the [Quickstart Guide](#quickstart-guide).

### Optional: Installing the Prerequisites

If one of the required tools is missing, install it using the official sources below.

- **Docker Desktop**  
  [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

- **Python 3.11+**  
  [Download Python](https://www.python.org/downloads/)

- **Node.js LTS**  
  [Download Node.js](https://nodejs.org/en/download/)
  
  npm is included with Node.js.

- **Git**  
  [Download Git for Windows](https://git-scm.com/download/win)

> **Windows note:** Make sure Docker Desktop is running before starting the application. Also, use a modern Node.js LTS installation. Older Node.js versions bundled with other applications may not provide a compatible `npm` environment.

---

## Quickstart Guide

### 1. Configure Environment Variables

Copy:

```text
backend/.env.template
```

and rename the copy to:

```text
backend/.env
```

Open `backend/.env` and fill in the required API credentials:

```env
SECTORS_API_KEY=<YOUR SECTORS APP API KEY>

OPENROUTER_API_KEY=<YOUR OPENROUTER API KEY>
OPENROUTER_MODEL=<YOUR OPENROUTER MODEL>
```

- `SECTORS_API_KEY`: API key from Sectors App.
- `OPENROUTER_API_KEY`: OpenRouter API key.
- `OPENROUTER_MODEL`: OpenRouter model to use.

### 2. Prepare the Python Environment

If `.venv` does not exist yet, create it:

```powershell
python -m venv .venv
```

Install the backend dependencies:

```powershell
.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

> If `.venv` already exists and the dependencies have already been installed, you can skip this step.

### 3. Run the Application

From the project root, run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\run.ps1
```

The script will:

1. Start PostgreSQL using Docker.
2. Apply the database migrations.
3. Build the frontend.
4. Start the FastAPI backend.

Open:

[**http://localhost:8000**](http://localhost:8000)

You can also verify the backend by opening:

[**http://localhost:8000/docs**](http://localhost:8000/docs)

If the Swagger API documentation appears with the available API endpoints, the backend has started successfully.

> **Note:** The initial startup may take some time because the application also pre-populates demo audit data and creates the default recurring schedule. As long as no error messages appear, allow the process to finish.

---

## Manual Setup

If you prefer to run each component separately, or if `run.ps1` encounters an error, follow these steps.

### 1. Start PostgreSQL (Docker)

```powershell
docker compose up -d
```

### 2. Run Database Migrations (Alembic)

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

If an error occurs while running the command above, use:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

### 3. Run Backend Server

```powershell
$env:PYTHONPATH="backend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

[**http://localhost:8000**](http://localhost:8000)

Or verify the API through:

[**http://localhost:8000/docs**](http://localhost:8000/docs)

### 4. Run Frontend in Vite Dev Mode (Optional)

```powershell
cd frontend
npm run dev
```

Open:

[**http://localhost:5173**](http://localhost:5173)

Vite proxies `/api` requests to the backend running on port `8000`.

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
