"""REST and Streaming SSE routes for SustainMetric IDX Harness."""

import datetime
import io
import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models import AuditRun, TKBIAuditEntry, AuditTraceSpan, ScheduledJob
from app.services.audit_runner import execute_audit_for_ticker
from app.services.excel_exporter import generate_stamped_excel_buffer
from app.services.pdf_generator import generate_signed_audit_pdf
from app.services.llm_gateway import stream_chat_completion

router = APIRouter()


# --- Request / Response Schemas ---

class TriggerAuditRequest(BaseModel):
    tickers: list[str] = Field(..., min_length=1, description="List of IDX tickers, e.g. ['PGEO', 'ADRO']")


class UpdateHITLEntryRequest(BaseModel):
    auditor_feedback: Optional[str] = None
    auditor_override: Optional[str] = None  # HIJAU, TRANSISI, TIDAK


class CreateScheduleRequest(BaseModel):
    name: str
    cron_expression: str
    tickers: list[str]
    alert_threshold_score: float = 50.0


class ChatRequest(BaseModel):
    messages: list[dict[str, str]]
    provider: Optional[str] = "gemini"
    model: Optional[str] = "gemini-2.5-flash"
    api_key: Optional[str] = ""


# --- Audit Endpoints ---

@router.get("/audits", response_model=list[dict[str, Any]])
async def list_audit_runs(db: AsyncSession = Depends(get_db)):
    """List all completed and ongoing audit runs."""
    stmt = select(AuditRun).order_by(AuditRun.created_at.desc()).limit(50)
    res = await db.execute(stmt)
    runs = res.scalars().all()
    return [
        {
            "id": r.id,
            "ticker": r.ticker,
            "company_name": r.company_name,
            "subsector": r.subsector,
            "consistency_score": r.consistency_score,
            "viability_score": r.viability_score,
            "quadrant": r.quadrant,
            "quadrant_label": r.quadrant_label,
            "status": r.status,
            "trace_id": r.trace_id,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in runs
    ]


@router.post("/audits/trigger")
async def trigger_audit(req: TriggerAuditRequest, db: AsyncSession = Depends(get_db)):
    """Trigger green audit execution for one or more IDX tickers."""
    clean_tickers = [t.strip().upper() for t in req.tickers if t.strip()]
    if not clean_tickers:
        raise HTTPException(status_code=400, detail="At least one valid ticker is required.")

    created_runs = []
    for ticker in clean_tickers:
        audit_run = await execute_audit_for_ticker(ticker, db)
        created_runs.append({
            "id": audit_run.id,
            "ticker": audit_run.ticker,
            "status": audit_run.status,
            "consistency_score": audit_run.consistency_score,
            "viability_score": audit_run.viability_score,
            "quadrant": audit_run.quadrant,
            "trace_id": audit_run.trace_id,
        })

    return {"message": f"Successfully completed audit for {len(created_runs)} ticker(s).", "runs": created_runs}


@router.get("/audits/{audit_id}")
async def get_audit_detail(audit_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve full audit detail, scores, and company fundamentals."""
    stmt = select(AuditRun).where(AuditRun.id == audit_id)
    res = await db.execute(stmt)
    audit = res.scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found.")

    return {
        "id": audit.id,
        "ticker": audit.ticker,
        "company_name": audit.company_name,
        "subsector": audit.subsector,
        "consistency_score": audit.consistency_score,
        "viability_score": audit.viability_score,
        "quadrant": audit.quadrant,
        "quadrant_label": audit.quadrant_label,
        "status": audit.status,
        "executive_summary": audit.executive_summary,
        "financial_snapshot": audit.financial_snapshot,
        "audit_findings": audit.audit_findings,
        "trace_id": audit.trace_id,
        "created_at": audit.created_at.isoformat() if audit.created_at else None,
        "updated_at": audit.updated_at.isoformat() if audit.updated_at else None,
    }


@router.get("/audits/{audit_id}/tkbi")
async def get_audit_tkbi_entries(audit_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve all TKBI checklist rows conforming to Template_Audit_TKBI.xlsx."""
    stmt = select(TKBIAuditEntry).where(TKBIAuditEntry.audit_run_id == audit_id).order_by(TKBIAuditEntry.id.asc())
    res = await db.execute(stmt)
    entries = res.scalars().all()
    return [
        {
            "id": e.id,
            "kode_emiten": e.kode_emiten,
            "sektor": e.sektor,
            "bab": e.bab,
            "kbli": e.kbli,
            "tsc_id": e.tsc_id,
            "tsc": e.tsc,
            "bentuk_jawaban": e.bentuk_jawaban,
            "jawaban_ai": e.jawaban_ai,
            "keyakinan_ai": e.keyakinan_ai,
            "reasoning_ai": e.reasoning_ai,
            "bukti": e.bukti,
            "auditor_feedback": e.auditor_feedback,
            "auditor_override": e.auditor_override,
            "is_overridden": e.is_overridden,
            "updated_at": e.updated_at.isoformat() if e.updated_at else None,
        }
        for e in entries
    ]


@router.patch("/audits/{audit_id}/tkbi/{entry_id}")
async def update_hitl_entry(
    audit_id: str,
    entry_id: int,
    req: UpdateHITLEntryRequest,
    db: AsyncSession = Depends(get_db),
):
    """Human-in-the-loop: Auditor overrides or submits feedback on a TKBI criteria row."""
    stmt = select(TKBIAuditEntry).where(TKBIAuditEntry.id == entry_id, TKBIAuditEntry.audit_run_id == audit_id)
    res = await db.execute(stmt)
    entry = res.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="TKBI entry not found.")

    if req.auditor_feedback is not None:
        entry.auditor_feedback = req.auditor_feedback

    if req.auditor_override is not None:
        entry.auditor_override = req.auditor_override.upper()
        entry.is_overridden = True

    entry.updated_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    await db.commit()

    return {"status": "SUCCESS", "message": f"Updated criterion {entry.tsc_id}", "entry_id": entry.id}


@router.get("/audits/{audit_id}/traces")
async def get_audit_traces(audit_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve OpenTelemetry trace spans for the visual DAG / waterfall."""
    # Find audit trace_id
    audit_stmt = select(AuditRun).where(AuditRun.id == audit_id)
    audit_res = await db.execute(audit_stmt)
    audit = audit_res.scalar_one_or_none()
    if not audit or not audit.trace_id:
        return []

    spans_stmt = (
        select(AuditTraceSpan)
        .where(AuditTraceSpan.trace_id == audit.trace_id)
        .order_by(AuditTraceSpan.start_time.asc())
    )
    spans_res = await db.execute(spans_stmt)
    spans = spans_res.scalars().all()
    return [
        {
            "id": s.id,
            "trace_id": s.trace_id,
            "span_id": s.span_id,
            "parent_span_id": s.parent_span_id,
            "name": s.name,
            "service_name": s.service_name,
            "start_time": s.start_time.isoformat() if s.start_time else None,
            "end_time": s.end_time.isoformat() if s.end_time else None,
            "duration_ms": s.duration_ms,
            "status": s.status,
            "attributes": s.attributes,
        }
        for s in spans
    ]


# --- Export Endpoints ---

@router.get("/audits/{audit_id}/export/xlsx")
async def export_audit_xlsx(audit_id: str, db: AsyncSession = Depends(get_db)):
    """Download updated Template_Audit_TKBI.xlsx with live AI answers and auditor overrides."""
    audit_stmt = select(AuditRun).where(AuditRun.id == audit_id)
    audit = (await db.execute(audit_stmt)).scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found.")

    entries_stmt = select(TKBIAuditEntry).where(TKBIAuditEntry.audit_run_id == audit_id).order_by(TKBIAuditEntry.id.asc())
    entries = (await db.execute(entries_stmt)).scalars().all()

    buf = generate_stamped_excel_buffer(audit, entries)
    filename = f"{audit.ticker}_audit_TKBI_stamped.xlsx"
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/audits/{audit_id}/export/pdf")
async def export_audit_pdf(audit_id: str, db: AsyncSession = Depends(get_db)):
    """Download official signed PDF audit report with cryptographic SHA-256 stamp."""
    audit_stmt = select(AuditRun).where(AuditRun.id == audit_id)
    audit = (await db.execute(audit_stmt)).scalar_one_or_none()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit run not found.")

    entries_stmt = select(TKBIAuditEntry).where(TKBIAuditEntry.audit_run_id == audit_id).order_by(TKBIAuditEntry.id.asc())
    entries = (await db.execute(entries_stmt)).scalars().all()

    buf = generate_signed_audit_pdf(audit, entries)
    filename = f"{audit.ticker}_TKBI_signed_report.pdf"
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# --- Benchmarks & Divergence Heatmap ---

@router.get("/benchmarks")
async def get_benchmarks(db: AsyncSession = Depends(get_db)):
    """Retrieve 2x2 scatter matrix points and sector distribution across all audited tickers."""
    stmt = select(AuditRun).where(AuditRun.status == "COMPLETED").order_by(AuditRun.updated_at.desc())
    runs = (await db.execute(stmt)).scalars().all()

    # Deduplicate by ticker (take latest)
    seen = set()
    latest_runs = []
    for r in runs:
        if r.ticker not in seen:
            seen.add(r.ticker)
            latest_runs.append(r)

    matrix_points = [
        {
            "id": r.id,
            "ticker": r.ticker,
            "company_name": r.company_name,
            "subsector": r.subsector,
            "x_viability": r.viability_score,
            "y_consistency": r.consistency_score,
            "quadrant": r.quadrant,
            "quadrant_label": r.quadrant_label,
            "capex_coverage": (r.financial_snapshot or {}).get("capex_coverage_ratio", 0.0),
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in latest_runs
    ]

    return {"count": len(matrix_points), "tickers": matrix_points}


# --- Scheduled Jobs Endpoints ---

@router.get("/schedules")
async def list_schedules(db: AsyncSession = Depends(get_db)):
    """List all configured recurring audit cron schedules."""
    stmt = select(ScheduledJob).order_by(ScheduledJob.created_at.desc())
    jobs = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": j.id,
            "name": j.name,
            "cron_expression": j.cron_expression,
            "tickers": j.tickers,
            "is_active": j.is_active,
            "alert_threshold_score": j.alert_threshold_score,
            "last_run_at": j.last_run_at.isoformat() if j.last_run_at else None,
            "last_status": j.last_status,
            "next_run_at": j.next_run_at.isoformat() if j.next_run_at else None,
        }
        for j in jobs
    ]


@router.post("/schedules")
async def create_schedule(req: CreateScheduleRequest, db: AsyncSession = Depends(get_db)):
    """Register a new recurring audit schedule."""
    job_id = f"cron_{uuid.uuid4().hex[:8]}"
    job = ScheduledJob(
        id=job_id,
        name=req.name,
        cron_expression=req.cron_expression,
        tickers=req.tickers,
        is_active=True,
        alert_threshold_score=req.alert_threshold_score,
        created_at=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None),
    )
    db.add(job)
    await db.commit()
    return {"status": "SUCCESS", "schedule_id": job.id, "message": f"Created schedule '{req.name}'"}


@router.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a recurring audit schedule."""
    stmt = delete(ScheduledJob).where(ScheduledJob.id == schedule_id)
    await db.execute(stmt)
    await db.commit()
    return {"status": "SUCCESS", "message": f"Deleted schedule {schedule_id}"}


# --- Built-in AI Copilot Chat Endpoint ---

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """Streaming SSE endpoint for AI Copilot chat with FastMCP tool execution."""
    generator = stream_chat_completion(
        messages=req.messages,
        provider=req.provider or "gemini",
        model=req.model or "gemini-2.5-flash",
        api_key=req.api_key or "",
    )
    return StreamingResponse(generator, media_type="text/event-stream")
