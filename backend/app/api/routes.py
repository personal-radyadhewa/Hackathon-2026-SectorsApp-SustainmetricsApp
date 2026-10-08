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
from sustainmetric.data.tkbi_sectors_catalog import TKBI_8_SECTORS
from app.data.tkbi_sdt_catalog import (
    SDT_UMKM_CRITERIA,
    SDT_DNSH_QUESTIONS,
    SDT_SOCIAL_ASPECTS_QUESTIONS,
    evaluate_sdt_submission,
)

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


class TKBISimulatorRequest(BaseModel):
    scale_type: str = "KORPORASI"  # KORPORASI or UMKM
    sector_name: Optional[str] = "Energi"
    activity_name: Optional[str] = ""
    eo_primary: str = "EO1"
    tsc_status: str = "HIJAU"  # HIJAU, TRANSISI, TIDAK
    dnsh_harm: bool = False
    has_rmt: bool = False
    social_aspects_met: bool = True
    # SDT specific answers (for UMKM)
    eo_answers: Optional[dict[str, bool]] = {}
    dnsh_answers: Optional[dict[str, bool]] = {}
    social_answers: Optional[dict[str, bool]] = {}


class PortfolioItem(BaseModel):
    name: str
    amount: float
    classification: str  # HIJAU, TRANSISI, TRANSISI INTERIM, TIDAK MEMENUHI, OUT_OF_SCOPE


class TKBIPortfolioRequest(BaseModel):
    portfolio_type: str = "HOLDING_CONSOLIDATED"  # HOLDING_CONSOLIDATED, FINANCIAL_INSTITUTION
    financing_type: str = "GENERAL_PURPOSE"  # GENERAL_PURPOSE (Tier 2 debtor aggregation), USE_OF_PROCEEDS (Tier 1 activity direct)
    items: list[PortfolioItem]


# --- SectorsApp Live IDX Directory Endpoints ---

@router.get("/companies")
async def list_or_search_companies(
    query: Optional[str] = Query(None, description="Search by ticker symbol or company name"),
    limit: int = Query(50, ge=1, le=1000, description="Max results to return")
):
    """Retrieve real IDX listed companies from SectorsApp API (with local disk cache)."""
    from sustainmetric.sectors_client import SectorsClient
    client = SectorsClient()
    if query:
        return await client.search_companies(query, limit=limit)
    all_comps = await client.get_all_companies()
    return all_comps[:limit]


# --- Audit Endpoints ---

@router.get("/audits", response_model=list[dict[str, Any]])
async def list_audit_runs(db: AsyncSession = Depends(get_db)):
    """List all completed and ongoing audit runs."""
    stmt = select(AuditRun).order_by(AuditRun.created_at.desc()).limit(200)
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
            "executive_summary": r.executive_summary,
            "financial_snapshot": r.financial_snapshot,
            "scale_type": getattr(r, "scale_type", "KORPORASI"),
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
        "scale_type": getattr(audit, "scale_type", "KORPORASI"),
        "entity_aggregation": getattr(audit, "entity_aggregation", None),
        "activities_breakdown": getattr(audit, "activities_breakdown", None),
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
            "eo_category": getattr(e, "eo_category", "EO1"),
            "dnsh_status": getattr(e, "dnsh_status", "PASS"),
            "rmt_status": getattr(e, "rmt_status", "N/A"),
            "social_status": getattr(e, "social_status", "PASS"),
            "is_interim": getattr(e, "is_interim", False),
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
async def get_benchmarks(
    tickers: Optional[str] = Query(None, description="Comma-separated ticker symbols to filter benchmarks"),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve 2x2 scatter matrix points and sector distribution across audited tickers."""
    stmt = select(AuditRun).where(AuditRun.status == "COMPLETED").order_by(AuditRun.updated_at.desc())
    runs = (await db.execute(stmt)).scalars().all()

    target_tickers = {t.strip().upper() for t in tickers.split(",") if t.strip()} if tickers else None

    # Deduplicate by ticker (take latest)
    seen = set()
    latest_runs = []
    for r in runs:
        if r.ticker not in seen:
            seen.add(r.ticker)
            if target_tickers is None or r.ticker in target_tickers:
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


# --- TKBI Flow & Regulatory Endpoints ---

@router.get("/tkbi/taxonomy/explorer")
async def get_tkbi_taxonomy_explorer():
    """Retrieve full 8-sector master taxonomy, NDC categories, and core OJK principles."""
    return {
        "framework": "Taksonomi Keuangan Berkelanjutan Indonesia (TKBI)",
        "version": "Rumah Tumbuh (Versi 1: Energi; Versi 2: 7 Sektor NDC; Versi 3: Interoperabilitas Global)",
        "sectors": TKBI_8_SECTORS,
        "principles": {
            "environmental_objectives": [
                {"code": "EO1", "name": "Mitigasi Perubahan Iklim", "desc": "Pencegahan emisi GRK menuju NZE 2060"},
                {"code": "EO2", "name": "Adaptasi Perubahan Iklim", "desc": "Peningkatan ketahanan terhadap bencana iklim & fisik"},
                {"code": "EO3", "name": "Perlindungan Ekosistem & Biodiversitas", "desc": "Konservasi habitat, air, tanah, dan keanekaragaman hayati"},
                {"code": "EO4", "name": "Pemanfaatan Sumber Daya & Ekonomi Sirkular", "desc": "Efisiensi material, daur ulang limbah, dan pemanfaatan siklus tertutup"},
            ],
            "essential_criteria": [
                {"code": "DNSH", "name": "Do No Significant Harm", "desc": "Aktivitas tidak boleh merusak satu pun dari 3 EO lainnya."},
                {"code": "RMT", "name": "Remedial Measures to Transition", "desc": "Rencana perbaikan terikat maksimal 3 tahun kalender bagi aktivitas dengan isu DNSH."},
                {"code": "MSS", "name": "Minimum Social Safeguards", "desc": "Kepatuhan hak asasi manusia, ketenagakerjaan, K3, dan perlindungan masyarakat adat."},
            ],
        },
        "ndc_targets": [
            {"sector": "Energi", "target": "358 Mt CO2e (CM1) / 446 Mt CO2e (CM2)"},
            {"sector": "Kehutanan (FOLU)", "target": "Net Sink 2030 (-140 Mt CO2e)"},
            {"sector": "Limbah (Waste)", "target": "40 Mt CO2e (CM1) / 43.5 Mt CO2e (CM2)"},
            {"sector": "Pertanian (Agriculture)", "target": "10 Mt CO2e"},
            {"sector": "Industri (IPPU)", "target": "7 Mt CO2e"},
        ],
    }


@router.get("/tkbi/sdt/catalog")
async def get_sdt_catalog():
    """Retrieve Sector-Agnostic Decision Tree (SDT) questions and guidance for UMKM (PP 7/2021)."""
    return {
        "framework": "OJK TKBI SDT for UMKM",
        "regulation": "PP No. 7 Tahun 2021 tentang Kemudahan, Pelindungan, dan Pemberdayaan Koperasi dan UMKM",
        "criteria": SDT_UMKM_CRITERIA,
        "dnsh_questions": SDT_DNSH_QUESTIONS,
        "social_questions": SDT_SOCIAL_ASPECTS_QUESTIONS,
    }


@router.post("/tkbi/simulator/evaluate")
async def evaluate_tkbi_simulator(req: TKBISimulatorRequest):
    """Interactive decision tree evaluator for Tingkat 1 (Aktivitas) conforming to Fact Sheet Page 23."""
    if req.scale_type == "UMKM":
        res = evaluate_sdt_submission(
            primary_eo=req.eo_primary,
            eo_answers=req.eo_answers or {},
            dnsh_answers=req.dnsh_answers or {},
            social_answers=req.social_answers or {},
            has_rmt_commitment=req.has_rmt,
        )
        return {
            "scale_type": "UMKM",
            "tier": "Tingkat 1 - Aktivitas (SDT Pathway)",
            "classification": res["classification"],
            "score_pct": res["eo_score_pct"],
            "dnsh_status": "PASS" if res["dnsh_passed"] else ("RMT_INTERIM" if req.has_rmt else "FAIL"),
            "social_status": "PASS" if res["social_passed"] else "FAIL",
            "rmt_clock_years": 3 if res["classification"] == "TRANSISI INTERIM" else 0,
            "decision_path": [
                "1. Penentuan Skala Usaha: UMKM (PP No. 7/2021)",
                f"2. Environmental Objective: {res['eo_name']}",
                f"3. Skor SDT EO: {res['eo_score_pct']}%",
                f"4. DNSH Compliance: {'Memenuhi' if res['dnsh_passed'] else ('Gagal (RMT 3 Tahun)' if req.has_rmt else 'Gagal')}",
                f"5. Aspek Sosial: {'Memenuhi' if res['social_passed'] else 'Tidak Memenuhi'}",
                f"6. Klasifikasi Akhir: {res['classification']}",
            ],
            "reasoning": res["notes"],
        }

    # KORPORASI / NON-UMKM (TSC Pathway)
    decision_path = [
        "1. Penentuan Skala: Korporasi Non-UMKM (Technical Screening Criteria / TSC)",
        f"2. EO Primer: {req.eo_primary}",
        f"3. Pemenuhan TSC: {req.tsc_status}",
    ]

    if not req.social_aspects_met:
        decision_path.append("4. Aspek Sosial: Gagal Minimum Social Safeguards")
        return {
            "scale_type": "KORPORASI",
            "tier": "Tingkat 1 - Aktivitas (TSC Pathway)",
            "classification": "TIDAK MEMENUHI KLASIFIKASI",
            "dnsh_status": "FAIL" if req.dnsh_harm else "PASS",
            "social_status": "FAIL",
            "rmt_clock_years": 0,
            "decision_path": decision_path,
            "reasoning": "Tidak memenuhi kriteria esensial perlindungan sosial dasar (K3, HAM, atau ketenagakerjaan).",
        }

    decision_path.append("4. Aspek Sosial: Lolos Minimum Social Safeguards")

    if req.tsc_status == "TIDAK":
        decision_path.append("5. Hasil TSC: Tidak Memenuhi ambang batas Hijau maupun Transisi")
        return {
            "scale_type": "KORPORASI",
            "tier": "Tingkat 1 - Aktivitas (TSC Pathway)",
            "classification": "TIDAK MEMENUHI KLASIFIKASI",
            "dnsh_status": "FAIL" if req.dnsh_harm else "PASS",
            "social_status": "PASS",
            "rmt_clock_years": 0,
            "decision_path": decision_path,
            "reasoning": "Aktivitas tidak memenuhi kriteria teknis TSC minimum OJK.",
        }

    if req.dnsh_harm:
        if req.has_rmt:
            decision_path.append("5. DNSH: Terjadi dampak signifikan, namun didukung Remedial Measures to Transition (RMT)")
            decision_path.append("6. Klasifikasi: Transisi Interim (Masa evaluasi 3 tahun kalender)")
            return {
                "scale_type": "KORPORASI",
                "tier": "Tingkat 1 - Aktivitas (TSC Pathway)",
                "classification": "TRANSISI INTERIM",
                "dnsh_status": "RMT_INTERIM",
                "social_status": "PASS",
                "rmt_clock_years": 3,
                "decision_path": decision_path,
                "reasoning": "Memenuhi kriteria TSC namun terdapat isu bahaya signifikan terhadap EO lain. Berdasarkan regulasi OJK TKBI 2024, entitas diklasifikasikan sebagai TRANSISI INTERIM dengan kewajiban menyelesaikan aksi korektif RMT dalam batas waktu maksimal 3 tahun kalender.",
            }
        else:
            decision_path.append("5. DNSH: Terjadi dampak signifikan tanpa komitmen rencana aksi perbaikan RMT")
            return {
                "scale_type": "KORPORASI",
                "tier": "Tingkat 1 - Aktivitas (TSC Pathway)",
                "classification": "TIDAK MEMENUHI KLASIFIKASI",
                "dnsh_status": "FAIL",
                "social_status": "PASS",
                "rmt_clock_years": 0,
                "decision_path": decision_path,
                "reasoning": "Melanggar prinsip Do No Significant Harm (DNSH) tanpa program Remedial Measures to Transition (RMT) terikat.",
            }

    # DNSH passed without harm
    decision_path.append("5. DNSH: Lolos, tidak menimbulkan kerugian signifikan pada EO lain")
    final_class = "HIJAU" if req.tsc_status == "HIJAU" else "TRANSISI"
    decision_path.append(f"6. Klasifikasi Akhir: {final_class}")
    return {
        "scale_type": "KORPORASI",
        "tier": "Tingkat 1 - Aktivitas (TSC Pathway)",
        "classification": final_class,
        "dnsh_status": "PASS",
        "social_status": "PASS",
        "rmt_clock_years": 0,
        "decision_path": decision_path,
        "reasoning": f"Memenuhi kriteria {final_class} secara penuh dengan kepatuhan terverifikasi pada TSC, DNSH, dan Safeguard Sosial.",
    }


@router.post("/tkbi/portfolio/evaluate")
async def evaluate_tkbi_portfolio(req: TKBIPortfolioRequest):
    """Aggregate Tingkat 2 (Entitas) & Tingkat 3 (Portofolio Holding/LJK) conforming to Fact Sheet Pages 4-5."""
    total_amount = sum(item.amount for item in req.items)
    if total_amount <= 0:
        return {
            "portfolio_type": req.portfolio_type,
            "financing_type": req.financing_type,
            "total_exposure": 0.0,
            "pct_hijau": 0.0,
            "pct_transisi": 0.0,
            "pct_transisi_interim": 0.0,
            "pct_tidak_memenuhi": 0.0,
            "pct_out_of_scope": 0.0,
            "weighted_green_transition_ratio": 0.0,
            "regulatory_summary": "Total eksposur portofolio bernilai 0.",
            "items_breakdown": [],
        }

    sum_hijau = sum(i.amount for i in req.items if i.classification.upper() == "HIJAU")
    sum_transisi = sum(i.amount for i in req.items if i.classification.upper() == "TRANSISI")
    sum_interim = sum(i.amount for i in req.items if "INTERIM" in i.classification.upper())
    sum_tidak = sum(i.amount for i in req.items if "TIDAK" in i.classification.upper())
    sum_oos = sum(i.amount for i in req.items if "SCOPE" in i.classification.upper())

    pct_hijau = round((sum_hijau / total_amount) * 100, 2)
    pct_transisi = round((sum_transisi / total_amount) * 100, 2)
    pct_interim = round((sum_interim / total_amount) * 100, 2)
    pct_tidak = round((sum_tidak / total_amount) * 100, 2)
    pct_oos = round((sum_oos / total_amount) * 100, 2)
    weighted_ratio = round(pct_hijau + pct_transisi + pct_interim, 2)

    if req.financing_type == "GENERAL_PURPOSE":
        reg_summary = (
            "Pembiayaan Korporasi Umum (General Purpose Financing): Menggunakan agregasi Tingkat 2 (Entitas). "
            "Evaluasi dilakukan terhadap keseluruhan portofolio anak usaha/debitur. "
            f"Kinerja portofolio tercatat {weighted_ratio}% tergolong Hijau & Transisi Terverifikasi OJK."
        )
    else:
        reg_summary = (
            "Pembiayaan Bertarget Spesifik (Use of Proceeds Financing): Menggunakan penelusuran langsung Tingkat 1 (Aktivitas). "
            "Alokasi dana dipersyaratkan menyasar aktivitas yang memenuhi ambang batas TSC/SDT."
        )

    return {
        "portfolio_type": req.portfolio_type,
        "financing_type": req.financing_type,
        "total_exposure": total_amount,
        "pct_hijau": pct_hijau,
        "pct_transisi": pct_transisi,
        "pct_transisi_interim": pct_interim,
        "pct_tidak_memenuhi": pct_tidak,
        "pct_out_of_scope": pct_oos,
        "weighted_green_transition_ratio": weighted_ratio,
        "regulatory_summary": reg_summary,
        "items_breakdown": [
            {
                "name": i.name,
                "amount": i.amount,
                "classification": i.classification,
                "share_pct": round((i.amount / total_amount) * 100, 2),
            }
            for i in req.items
        ],
    }


@router.get("/tkbi/grandfathering/scenarios")
async def get_grandfathering_scenarios():
    """Retrieve official OJK Sunsetting and Grandfathering criteria conforming to Fact Sheet Pages 6-8."""
    return {
        "framework": "OJK TKBI Grandfathering & Sunsetting Protocol",
        "clock_rules": {
            "unallocated_financing_protection_years": 7,
            "allocated_green_bonds": "Label dipertahankan hingga jatuh tempo (bond maturity tenor).",
            "sunsetting_cycles": "Evaluasi berkala ambang batas teknis (TSC) setiap pembaruan TKBI (Versi 1, Versi 2, Versi 3).",
        },
        "scenarios": [
            {
                "code": "Scenario A",
                "from_status": "HIJAU (Versi Lama)",
                "to_status": "HIJAU (Versi Baru)",
                "impact": "Status dipertahankan tanpa perubahan.",
                "action_required": "Pelaporan berkala kepatuhan.",
            },
            {
                "code": "Scenario B",
                "from_status": "TRANSISI (Versi Lama)",
                "to_status": "TRANSISI (Versi Baru)",
                "impact": "Status transisi dipertahankan.",
                "action_required": "Monitoring roadmap dekarbonisasi berkesinambungan.",
            },
            {
                "code": "Scenario C",
                "from_status": "HIJAU (Versi Lama)",
                "to_status": "TRANSISI (Versi Baru)",
                "impact": "Proteksi masa transisi (Grandfathering) berlaku hingga 7 tahun atau tenor jatuh tempo kredit.",
                "action_required": "Penyusunan penyesuaian roadmap menuju kriteria hijau baru.",
            },
            {
                "code": "Scenario D",
                "from_status": "TRANSISI (Versi Lama)",
                "to_status": "TIDAK MEMENUHI (Versi Baru)",
                "impact": "Pembiayaan berisiko kehilangan label berkelanjutan.",
                "action_required": "Wajib menyusun program Remedial Measures to Transition (RMT) maksimal 3 tahun atau reklasifikasi pembiayaan.",
            },
            {
                "code": "Scenario E",
                "from_status": "HIJAU (Versi Lama)",
                "to_status": "TIDAK MEMENUHI (Versi Baru)",
                "impact": "Masa proteksi grandfathering maksimal hingga jatuh tempo kontrak awal.",
                "action_required": "Audit ulang komprehensif saat perpanjangan fasilitas pembiayaan.",
            },
        ],
    }
