# One-command runner for SustainMetric IDX Harness
Write-Host ">>> Starting PostgreSQL container..." -ForegroundColor Cyan
docker compose up -d

Write-Host ">>> Applying Alembic database migrations..." -ForegroundColor Cyan
$env:PYTHONPATH="backend"
.\.venv\Scripts\alembic.exe upgrade head

Write-Host ">>> Building latest frontend bundle..." -ForegroundColor Cyan
npm --prefix frontend run build

Write-Host ">>> Launching SustainMetric Unified Server on http://localhost:8000 ..." -ForegroundColor Green
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
